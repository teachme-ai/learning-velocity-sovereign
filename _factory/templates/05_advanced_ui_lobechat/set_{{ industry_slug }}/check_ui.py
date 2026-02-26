import asyncio
import json
import os
from pathlib import Path
from playwright.async_api import async_playwright
try:
    from rich.console import Console
    from rich.terminal_theme import MONOKAI
except ImportError:
    pass

async def check_lobechat():
    print("=== LobeChat Sovereign Interface Validator ===")
    
    output_dir = Path(__file__).parent / "proof"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("\n1. Launching Headless Validator...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        print("2. Connecting to LobeChat (http://localhost:3200)...")
        try:
            # Go to the chat interface
            response = await page.goto("http://localhost:3200/chat", wait_until="networkidle")
            print(f"   [OK] HTTP Status: {response.status}")
            
            # Wait for main UI to load
            await page.wait_for_selector("div[data-testid='chat-header']", timeout=15000)
            print("   [OK] LobeChat UI Loaded successfully.")
            
            # Let's take a screenshot of the baseline UI
            screenshot_path = output_dir / "ui_loaded.png"
            await page.screenshot(path=str(screenshot_path))
            print(f"3. Captured UI Screenshot: {screenshot_path}")
            
        except Exception as e:
            print(f"\n[ERROR] Failed to validate LobeChat UI: {e}")
            await browser.close()
            return
            
        await browser.close()
        
    print("\n=== Validation Complete ===")

if __name__ == "__main__":
    asyncio.run(check_lobechat())
