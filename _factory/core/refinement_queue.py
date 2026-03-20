import sqlite3
import os
from datetime import datetime


class RefinementQueue:
    def __init__(self, db_path="_factory/queue.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                industry_slug TEXT NOT NULL,
                file_path TEXT NOT NULL,
                industry_name TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                created_at TEXT,
                completed_at TEXT,
                error TEXT
            )
        """)
        self.conn.commit()

    def enqueue(self, industry_slug, file_path, industry_name):
        existing = self.conn.execute(
            "SELECT id FROM jobs WHERE industry_slug=? AND file_path=? AND status IN ('pending','in_progress')",
            (industry_slug, file_path)
        ).fetchone()
        if existing:
            return
        self.conn.execute(
            "INSERT INTO jobs (industry_slug, file_path, industry_name, status, created_at) VALUES (?,?,?,'pending',?)",
            (industry_slug, file_path, industry_name, datetime.now().isoformat())
        )
        self.conn.commit()

    def next_job(self):
        row = self.conn.execute(
            "SELECT * FROM jobs WHERE status='pending' ORDER BY id ASC LIMIT 1"
        ).fetchone()
        return dict(row) if row else None

    def mark_in_progress(self, job_id):
        self.conn.execute("UPDATE jobs SET status='in_progress' WHERE id=?", (job_id,))
        self.conn.commit()

    def mark_done(self, job_id):
        self.conn.execute(
            "UPDATE jobs SET status='done', completed_at=? WHERE id=?",
            (datetime.now().isoformat(), job_id)
        )
        self.conn.commit()

    def mark_failed(self, job_id, error_message):
        self.conn.execute(
            "UPDATE jobs SET status='failed', error=? WHERE id=?",
            (error_message, job_id)
        )
        self.conn.commit()

    def reset_to_pending(self, job_id):
        self.conn.execute(
            "UPDATE jobs SET status='pending', error=NULL WHERE id=?", (job_id,)
        )
        self.conn.commit()

    def pending_count(self):
        return self.conn.execute(
            "SELECT COUNT(*) FROM jobs WHERE status='pending'"
        ).fetchone()[0]

    def stats(self):
        rows = self.conn.execute(
            "SELECT status, COUNT(*) as cnt FROM jobs GROUP BY status"
        ).fetchall()
        result = {"pending": 0, "done": 0, "failed": 0, "in_progress": 0, "total": 0}
        for row in rows:
            result[row["status"]] = row["cnt"]
            result["total"] += row["cnt"]
        return result

    def clear_done(self):
        self.conn.execute("DELETE FROM jobs WHERE status='done'")
        self.conn.commit()
