#!/usr/bin/env python3
"""concat_xfade.py — segments/*.mp4 -> concat_noSubs.mp4，用 fadeblack 硬切避免疊影。"""
import pathlib, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent
XDUR = 0.35                                   # ROOT CAUSE 3: fade 會疊影，用 fadeblack

durs = [float(x) for x in (ROOT / "durations.txt").read_text().split()]
segs = sorted((ROOT / "segments").glob("segment_*.mp4"))
if len(segs) != len(durs):
    sys.exit(f"segments={len(segs)} 與 durations={len(durs)} 不符")

cmd, fc = ["ffmpeg", "-y", "-v", "error"], []
for s in segs: cmd += ["-i", str(s)]

if len(segs) == 1:
    fc.append("[0:v]copy[v];[0:a]acopy[a]")
else:
    vprev, aprev, offset = "[0:v]", "[0:a]", 0.0
    for i in range(1, len(segs)):
        offset += durs[i-1] - XDUR
        vo, ao = f"[v{i}]", f"[a{i}]"
        fc.append(f"{vprev}[{i}:v]xfade=transition=fadeblack:duration={XDUR}:offset={offset:.3f}{vo}")
        fc.append(f"{aprev}[{i}:a]acrossfade=d={XDUR}:c1=tri:c2=tri{ao}")
        vprev, aprev = vo, ao
    fc.append(f"{vprev}copy[v]"); fc.append(f"{aprev}acopy[a]")

cmd += ["-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[a]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", str(ROOT / "concat_noSubs.mp4")]
subprocess.run(cmd, check=True)
print(f"[concat] concat_noSubs.mp4  ({sum(durs) - XDUR*(len(segs)-1):.2f}s)")
