import asyncio
import os
import sys
import json
from datetime import datetime


class TokenBudget:
    def __init__(self, total_tokens, defer_after_tokens, tokens_per_minute):
        self.total_tokens = total_tokens
        self.defer_after_tokens = defer_after_tokens
        self.tokens_per_minute = tokens_per_minute
        self.used_tokens = 0
        self.minute_bucket = 0
        self.bucket_reset_time = datetime.now()

    @staticmethod
    def estimate_tokens(text):
        return len(text) // 4

    def can_proceed(self):
        now = datetime.now()
        if (now - self.bucket_reset_time).total_seconds() > 60:
            self.minute_bucket = 0
            self.bucket_reset_time = now
        if self.used_tokens >= self.defer_after_tokens:
            return False
        if self.minute_bucket >= self.tokens_per_minute:
            return False
        return True

    def record_usage(self, tokens):
        self.used_tokens += tokens
        self.minute_bucket += tokens

    def is_exhausted(self):
        return self.used_tokens >= self.total_tokens

    def stats(self):
        return {
            "used": self.used_tokens,
            "total": self.total_tokens,
            "remaining": max(0, self.total_tokens - self.used_tokens),
            "deferred": self.used_tokens >= self.defer_after_tokens,
        }


async def refine_file_async(job, industry_name, refiner_script, model, semaphore, budget, logger):
    async with semaphore:
        basename = os.path.basename(job["file_path"])

        if budget.is_exhausted():
            logger.log(f"Budget exhausted — deferring: {basename}", level="WARNING")
            return {"status": "deferred", "job_id": job["id"]}

        if not budget.can_proceed():
            await asyncio.sleep(2)

        try:
            with open(job["file_path"], "r") as f:
                content = f.read()
        except FileNotFoundError:
            return {"status": "failed", "job_id": job["id"], "error": "file not found"}

        estimated_tokens = TokenBudget.estimate_tokens(content) * 2

        env = os.environ.copy()
        env["REFINER_MODEL"] = model

        proc = await asyncio.create_subprocess_exec(
            sys.executable, refiner_script,
            job["file_path"], industry_name, job["industry_slug"],
            env=env,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        budget.record_usage(estimated_tokens)

        if proc.returncode == 0:
            return {"status": "done", "job_id": job["id"], "tokens": estimated_tokens}
        else:
            return {"status": "failed", "job_id": job["id"], "error": stderr.decode().strip()}


async def drain_queue(queue, industry_name, refiner_script, model, token_budget_config, logger, concurrency=3):
    budget = TokenBudget(
        total_tokens=token_budget_config["total_tokens"],
        defer_after_tokens=token_budget_config["defer_after_tokens"],
        tokens_per_minute=token_budget_config["tokens_per_minute"],
    )

    semaphore = asyncio.Semaphore(concurrency)
    tasks = []

    while True:
        job = queue.next_job()
        if job is None:
            break
        if budget.is_exhausted():
            logger.log("Token budget exhausted. Remaining jobs deferred to next run.", level="WARNING")
            break
        queue.mark_in_progress(job["id"])
        task = asyncio.create_task(
            refine_file_async(job, industry_name, refiner_script, model, semaphore, budget, logger)
        )
        tasks.append(task)

    results = await asyncio.gather(*tasks, return_exceptions=True)

    for result in results:
        if isinstance(result, Exception):
            continue
        if result["status"] == "done":
            queue.mark_done(result["job_id"])
        elif result["status"] == "failed":
            queue.mark_failed(result["job_id"], result.get("error", "unknown"))
        elif result["status"] == "deferred":
            queue.reset_to_pending(result["job_id"])

    queue.clear_done()
    logger.log(f"Pass 2 complete. Budget: {budget.stats()} | Queue: {queue.stats()}")
    return budget.stats()
