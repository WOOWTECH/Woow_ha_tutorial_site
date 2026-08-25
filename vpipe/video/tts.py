#!/usr/bin/env python3
"""
tts.py — 補上 slide-video-pipeline 缺少的「第 0 階段」。

輸入 : video/script.yaml
輸出 : video/narration/slide_NN.mp3   (每頁一條旁白音軌)
        video/timeline.json           (每個 reveal 的觸發秒數，capture.py 用)
        video/durations.txt           (每頁總長，concat_xfade.py 用)
        video/subtitles.srt           (build_final.sh 燒字幕用)

引擎可切換（TTS_ENGINE=...）：
  azure    Azure AI Speech REST，zh-TW-HsiaoChenNeural／HsiaoYu／YunJhe ← 台灣口音，推薦
           需要 AZURE_SPEECH_KEY、AZURE_SPEECH_REGION
  gcloud   Google Cloud TTS REST，cmn-TW ← 需先用 --list-voices 確認該語系仍有語音
           需要 GOOGLE_TTS_KEY（API key）
  edge     edge-tts CLI，與 Azure 同一批神經語音，免金鑰但非官方、無 SSML 完整支援
  espeak   離線機器音，只拿來對時 dry-run
  file     旁白 mp3 已備妥（例如 higgsfield 生成後下載），本腳本只量長度排時間軸

自我檢查：
  python3 video/tts.py --list-voices     # 列出該引擎目前實際可用的中文語音
"""
import base64, json, os, subprocess, sys, pathlib, urllib.request, urllib.parse, yaml

ROOT   = pathlib.Path(__file__).resolve().parent
NARR   = ROOT / "narration"; NARR.mkdir(exist_ok=True)
ENGINE = os.environ.get("TTS_ENGINE", "espeak")
XFADE  = float(os.environ.get("XFADE", "0.35"))   # 必須與 concat_xfade.py 的 XDUR 一致
VOICE  = os.environ.get("TTS_VOICE", "zh-TW-HsiaoChenNeural")
RATE   = os.environ.get("TTS_RATE", "0%")         # Azure prosody rate，例：-8% 慢一點
PITCH  = os.environ.get("TTS_PITCH", "0%")

AZ_KEY, AZ_REGION = os.environ.get("AZURE_SPEECH_KEY"), os.environ.get("AZURE_SPEECH_REGION")
GC_KEY = os.environ.get("GOOGLE_TTS_KEY")

def _post(url, data, headers):
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()

def azure_ssml(text):
    """SSML 是 Azure 相對 edge-tts 的主要好處：可控語速、停頓、念法。"""
    esc = (text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
    return (f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" '
            f'xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="zh-TW">'
            f'<voice name="{VOICE}">'
            f'<prosody rate="{RATE}" pitch="{PITCH}">{esc}</prosody>'
            f'</voice></speak>').encode("utf-8")

def azure_tts(text, out_mp3):
    if not (AZ_KEY and AZ_REGION):
        sys.exit("請先設定 AZURE_SPEECH_KEY 與 AZURE_SPEECH_REGION")
    audio = _post(f"https://{AZ_REGION}.tts.speech.microsoft.com/cognitiveservices/v1",
                  azure_ssml(text),
                  {"Ocp-Apim-Subscription-Key": AZ_KEY,
                   "Content-Type": "application/ssml+xml",
                   # 48kHz 192kbps 直接對上 pipeline 的音訊規格，免再轉檔
                   "X-Microsoft-OutputFormat": "audio-48khz-192kbitrate-mono-mp3",
                   "User-Agent": "slide-video-pipeline"})
    out_mp3.write_bytes(audio)

def gcloud_tts(text, out_mp3):
    if not GC_KEY:
        sys.exit("請先設定 GOOGLE_TTS_KEY")
    body = json.dumps({
        "input": {"text": text},
        "voice": {"languageCode": VOICE.rsplit("-", 2)[0] if VOICE.count("-") > 2 else "cmn-TW",
                  "name": VOICE},
        "audioConfig": {"audioEncoding": "MP3", "sampleRateHertz": 48000,
                        "speakingRate": float(os.environ.get("GC_RATE", "1.0"))},
    }).encode()
    res = _post(f"https://texttospeech.googleapis.com/v1/text:synthesize?key={GC_KEY}",
                body, {"Content-Type": "application/json; charset=utf-8"})
    out_mp3.write_bytes(base64.b64decode(json.loads(res)["audioContent"]))

def list_voices():
    """跑之前先確認語音真的存在——Google 的 cmn-TW 供應狀況會變動。"""
    if ENGINE == "azure":
        req = urllib.request.Request(
            f"https://{AZ_REGION}.tts.speech.microsoft.com/cognitiveservices/voices/list",
            headers={"Ocp-Apim-Subscription-Key": AZ_KEY})
        vs = json.loads(urllib.request.urlopen(req, timeout=30).read())
        vs = [v for v in vs if v["Locale"].startswith("zh-TW")]
        for v in vs:
            print(f'{v["ShortName"]:<34}{v["Gender"]:<8}{v.get("VoiceType","")}')
    elif ENGINE == "gcloud":
        url = f"https://texttospeech.googleapis.com/v1/voices?key={GC_KEY}"
        vs = json.loads(urllib.request.urlopen(url, timeout=30).read()).get("voices", [])
        vs = [v for v in vs if any(c.startswith(("cmn-TW", "zh-TW")) for c in v["languageCodes"])]
        for v in vs:
            print(f'{v["name"]:<34}{v["ssmlGender"]:<8}{v["languageCodes"]}')
        if not vs:
            print("此專案 API 目前查無 cmn-TW / zh-TW 語音——請改用 Azure。")
    elif ENGINE == "edge":
        subprocess.run("edge-tts --list-voices | grep zh-TW", shell=True)
    else:
        print(f"引擎 {ENGINE} 不支援語音查詢")
    sys.exit(0)

def dur(p):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    return float(out.stdout.strip())

def synth(text, out_mp3, cfg):
    """產生單行旁白 mp3。換引擎只要改這個函式。"""
    if ENGINE == "espeak":
        wav = out_mp3.with_suffix(".wav")
        subprocess.run(["espeak-ng", "-v", cfg.get("voice", "cmn"),
                        "-s", str(cfg.get("speed", 150)), "-w", str(wav), text], check=True)
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(wav),
                        "-ar", "48000", "-ac", "2", "-b:a", "160k", str(out_mp3)], check=True)
        wav.unlink()
    elif ENGINE == "azure":
        azure_tts(text, out_mp3)
    elif ENGINE == "gcloud":
        gcloud_tts(text, out_mp3)
    elif ENGINE == "edge":
        subprocess.run(["edge-tts", "--voice", VOICE, "--text", text,
                        "--write-media", str(out_mp3)], check=True)
    elif ENGINE == "file":
        if not out_mp3.exists():
            sys.exit(f"TTS_ENGINE=file 但找不到 {out_mp3}")
    else:
        sys.exit(f"未知的 TTS_ENGINE: {ENGINE}")
    return dur(out_mp3)

def srt_ts(t):
    h, r = divmod(t, 3600); m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s%1)*1000)):03d}"

def main():
    cfg  = yaml.safe_load((ROOT / "script.yaml").read_text(encoding="utf-8"))
    dflt = cfg.get("defaults", {})
    tail = float(dflt.get("tail", 0.6))

    timeline, durations, srt, srt_i, slide_start = [], [], [], 1, 0.0

    for si, slide in enumerate(cfg["slides"]):
        sid, parts, reveals, t = slide["id"], [], [], 0.0
        # 關鍵：xfade 每個轉場會把時間軸壓縮 XFADE 秒，字幕時間必須跟著扣，
        # 否則第二頁之後旁白與字幕會愈差愈多（技能描述裡的 out-of-sync 症狀）。
        for li, text in enumerate(slide["lines"]):
            mp3 = NARR / f"line_{sid:02d}_{li:02d}.mp3"
            d = synth(text, mp3, dflt)
            parts.append(mp3)
            reveals.append({"index": li, "at": round(t, 3)})          # 行開始 = reveal 時間
            a = slide_start + t
            srt.append(f"{srt_i}\n{srt_ts(a)} --> {srt_ts(a + d)}\n{text}\n")
            srt_i += 1; t += d
        # 併成整頁旁白
        lst = NARR / f"list_{sid:02d}.txt"
        lst.write_text("".join(f"file '{p.name}'\n" for p in parts), encoding="utf-8")
        out = NARR / f"slide_{sid:02d}.mp3"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                        "-i", str(lst), "-c", "copy", str(out)], check=True)
        lst.unlink()
        total = round(t + tail, 3)
        durations.append(total)
        slide_start += total - XFADE          # 下一頁在成品時間軸上的起點
        timeline.append({"slide": sid, "audio": f"narration/slide_{sid:02d}.mp3",
                         "duration": total, "reveals": reveals})

    (ROOT / "timeline.json").write_text(json.dumps(timeline, ensure_ascii=False, indent=2), encoding="utf-8")
    (ROOT / "durations.txt").write_text("\n".join(f"{d:.3f}" for d in durations) + "\n", encoding="utf-8")
    (ROOT / "subtitles.srt").write_text("\n".join(srt), encoding="utf-8")
    print(f"[tts] engine={ENGINE} slides={len(durations)} total={sum(durations):.2f}s")

if __name__ == "__main__":
    if "--list-voices" in sys.argv:
        list_voices()
    main()
