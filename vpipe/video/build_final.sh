#!/usr/bin/env bash
# build_final.sh — 燒中文字幕 + 混入低音量環境底噪 -> final.mp4
set -euo pipefail
export PATH="$HOME/bin:$PATH"
cd "$(dirname "$0")"

FONT="Noto Sans CJK TC"
STYLE="FontName=${FONT},FontSize=26,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,\
BorderStyle=3,Outline=2,Shadow=0,BackColour=&HB0000000,MarginV=48,Alignment=2"

ffmpeg -y -v error -i concat_noSubs.mp4 \
  -f lavfi -t "$(ffprobe -v error -show_entries format=duration -of csv=p=0 concat_noSubs.mp4)" \
  -i "anoisesrc=c=pink:a=0.0025:r=48000" \
  -filter_complex "[0:v]subtitles=subtitles.srt:force_style='${STYLE}'[v];\
[0:a][1:a]amix=inputs=2:duration=first:weights=1 0.35,alimiter=limit=0.95[a]" \
  -map "[v]" -map "[a]" \
  -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -movflags +faststart \
  -c:a aac -b:a 192k final.mp4
echo "[final] final.mp4"
