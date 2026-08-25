#!/usr/bin/env bash
# run.sh <stage> [upload_url] — staged pipeline inside the Higgsfield sandbox
set -euo pipefail
cd "$(dirname "$0")"
S="$1"; LOG="stage${S}.log"
{
case "$S" in
1)
  mkdir -p "$HOME/.local/share/fonts"
  for f in NotoSansCJKtc-Regular.otf NotoSansCJKtc-Bold.otf; do
    [ -f "$HOME/.local/share/fonts/$f" ] || \
    curl -fsSL "https://raw.githubusercontent.com/notofonts/noto-cjk/main/Sans/OTF/TraditionalChinese/$f" \
      -o "$HOME/.local/share/fonts/$f" || \
    curl -fsSL "https://github.com/googlefonts/noto-cjk/raw/main/Sans/OTF/TraditionalChinese/$f" \
      -o "$HOME/.local/share/fonts/$f"
  done
  fc-cache -f >/dev/null 2>&1 || true
  fc-list | grep -i "Noto Sans CJK TC" | head -2
  pip install -q edge-tts pyyaml 2>/dev/null || pip install -q --break-system-packages edge-tts pyyaml
  TTS_ENGINE=edge TTS_VOICE=zh-TW-HsiaoChenNeural python3 video/tts.py
  ;;
2)
  python3 -c "import playwright" 2>/dev/null || pip install -q playwright 2>/dev/null || pip install -q --break-system-packages playwright
  python3 -m playwright install chromium >/dev/null 2>&1 || python3 -m playwright install chromium
  python3 video/capture.py
  ;;
3)
  bash video/build_segments.sh
  python3 video/concat_xfade.py
  bash video/build_final.sh
  ffprobe -v error -show_entries format=duration,size -of csv=p=0 video/final.mp4
  if [ -n "${2:-}" ]; then
    curl -sf -X PUT --upload-file video/final.mp4 "$2" -o /dev/null -w "PUT %{http_code}\n"
  fi
  ;;
esac
echo "STAGE${S}_OK"
} >"$LOG" 2>&1
