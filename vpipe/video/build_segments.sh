#!/usr/bin/env bash
# build_segments.sh — clips/clip_NN.webm + narration/slide_NN.mp3 -> segments/segment_NN.mp4
set -euo pipefail
export PATH="$HOME/bin:$PATH"
cd "$(dirname "$0")"
mkdir -p segments

mapfile -t LEAD < leadin.txt 2>/dev/null || LEAD=()
i=0
while IFS= read -r total; do
  i=$((i+1)); NN=$(printf "%02d" "$i")
  clip="clips/clip_${NN}.webm"; audio="narration/slide_${NN}.mp3"
  lead="${LEAD[$((i-1))]:-0}"      # 裁掉 Playwright 錄進來的載入死時間
  [ -f "$clip" ] || { echo "missing $clip"; exit 1; }

  # ROOT CAUSE 5 修法：fps -> tpad(clone 尾幀) -> trim，順序不能換
  # -nostdin 必要：否則 ffmpeg 會吃掉 while-read 的 stdin，只跑出第一段
  ffmpeg -nostdin -y -v error -i "$clip" -i "$audio" -filter_complex \
"[0:v]fps=30,tpad=stop_mode=clone:stop_duration=2,trim=start=${lead}:duration=${total},setpts=PTS-STARTPTS,\
scale=1920:1080:force_original_aspect_ratio=decrease:flags=lanczos,\
pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=black,format=yuv420p[v];\
[1:a]apad=whole_dur=${total}[a]" \
    -map "[v]" -map "[a]" -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p \
    -c:a aac -b:a 192k -ar 48000 -ac 2 -shortest "segments/segment_${NN}.mp4"
  echo "[segments] segment_${NN}.mp4  (${total}s, 起點 ${lead}s)"
done < durations.txt
