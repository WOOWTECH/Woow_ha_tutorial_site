#!/usr/bin/env python3
"""capture.py — 用 Playwright 依 timeline.json 逐頁錄成 WebM。"""
import asyncio, json, pathlib, shutil, time
from playwright.async_api import async_playwright

ROOT   = pathlib.Path(__file__).resolve().parent
REPO   = ROOT.parent
CLIPS  = ROOT / "clips"
W, H   = 1920, 1080          # ROOT CAUSE 1: viewport 必須等於 record_video_size

async def main():
    tl = json.loads((ROOT / "timeline.json").read_text(encoding="utf-8"))
    leadins = []
    if CLIPS.exists(): shutil.rmtree(CLIPS)
    CLIPS.mkdir(parents=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(args=["--force-device-scale-factor=1"])
        for entry in tl:
            sid, total = entry["slide"], entry["duration"]
            ctx = await browser.new_context(
                viewport={"width": W, "height": H},
                record_video_dir=str(CLIPS),
                record_video_size={"width": W, "height": H},
                device_scale_factor=1,
            )
            page = await ctx.new_page()
            # Playwright 從「頁面建立」就開始錄，載入頁面那段死時間會被錄進去。
            # 必須量出來交給 build_segments.sh 從那個點才開始裁，否則所有動畫會晚 1~2 秒。
            t_rec = time.monotonic()
            await page.goto((REPO / "slides.html").as_uri())
            await page.wait_for_load_state("networkidle")
            try:
                await page.wait_for_function("document.fonts.status==='loaded'", timeout=8000)
            except Exception:
                pass
            await page.evaluate(f"showSlide({sid})")
            await page.wait_for_timeout(300)
            leadins.append(round(time.monotonic() - t_rec, 3))

            t = 0.0
            for r in entry["reveals"]:
                wait = max(0.0, r["at"] - t)
                if wait: await page.wait_for_timeout(int(wait * 1000))
                t = r["at"]
                await page.evaluate(f"revealStep({sid}, {r['index']})")
                await page.evaluate(f"setProgress({sid}, {min(1.0, r['at']/total):.4f})")
            await page.evaluate(f"setProgress({sid}, 1)")
            await page.wait_for_timeout(int(max(0.0, total - t) * 1000) + 700)  # 尾巴要留

            video = page.video
            await ctx.close()                                   # 關掉才會 flush 檔案
            src = pathlib.Path(await video.path())
            src.rename(CLIPS / f"clip_{sid:02d}.webm")
            print(f"[capture] clip_{sid:02d}.webm  ({total:.2f}s, lead-in {leadins[-1]:.2f}s)")
        await browser.close()
    (ROOT / "leadin.txt").write_text("\n".join(f"{x:.3f}" for x in leadins) + "\n")

asyncio.run(main())
