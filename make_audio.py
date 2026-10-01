"""Generate German audio for every word and example sentence with Piper.

Run:  python make_audio.py
Resumable: already-generated files are skipped, so it is safe to re-run.
Progress is appended to audio_progress.txt, one line per 25 clips.
"""
import json, os, subprocess, sys, time, wave, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "audio")
VOICES = os.path.join(HERE, "voices")
MANIFEST = os.path.join(HERE, "tts_manifest.json")
LOG = os.path.join(HERE, "audio_progress.txt")
VOICE = "de_DE-thorsten-high"

# a touch slower than default: clearer for someone learning the language
LENGTH_SCALE = 1.08
MP3_BITRATE = "40k"      # mono speech; small files, no audible loss at this rate

os.makedirs(OUT, exist_ok=True)
os.makedirs(VOICES, exist_ok=True)


def log(msg):
    line = time.strftime("%H:%M:%S ") + msg
    print(line, flush=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def ensure_voice():
    onnx = os.path.join(VOICES, VOICE + ".onnx")
    if os.path.exists(onnx) and os.path.getsize(onnx) > 1_000_000:
        log("voice already present")
        return onnx
    log("downloading voice " + VOICE + " ...")
    subprocess.run(
        [sys.executable, "-m", "piper.download_voices", VOICE, "--download-dir", VOICES],
        check=True,
    )
    if not os.path.exists(onnx):
        # some versions nest the files; find the onnx anywhere under voices/
        for root, _dirs, files in os.walk(VOICES):
            for fn in files:
                if fn.endswith(".onnx"):
                    return os.path.join(root, fn)
        raise SystemExit("voice model not found after download")
    return onnx


def main():
    texts = json.load(open(MANIFEST, encoding="utf-8"))
    todo = {h: t for h, t in texts.items()
            if not os.path.exists(os.path.join(OUT, h + ".mp3"))}
    log("clips total %d, still to make %d" % (len(texts), len(todo)))
    if not todo:
        log("nothing to do")
        return

    model = ensure_voice()
    from piper import PiperVoice
    try:
        from piper import SynthesisConfig
        syn = SynthesisConfig(length_scale=LENGTH_SCALE)
    except Exception:
        syn = None

    log("loading model ...")
    voice = PiperVoice.load(model)
    log("model loaded, starting")

    tmpdir = tempfile.mkdtemp(prefix="piperwav")
    started = time.time()
    done = 0
    failed = []

    for h, text in todo.items():
        wav = os.path.join(tmpdir, h + ".wav")
        mp3 = os.path.join(OUT, h + ".mp3")
        try:
            with wave.open(wav, "wb") as wf:
                if syn is not None:
                    voice.synthesize_wav(text, wf, syn_config=syn)
                else:
                    voice.synthesize_wav(text, wf)
            subprocess.run(
                ["ffmpeg", "-y", "-loglevel", "error", "-i", wav,
                 "-ac", "1", "-ar", "22050", "-b:a", MP3_BITRATE, mp3],
                check=True,
            )
            os.remove(wav)
        except Exception as e:
            failed.append((h, text, str(e)[:120]))
        done += 1
        if done % 25 == 0 or done == len(todo):
            rate = done / max(0.001, time.time() - started)
            left = (len(todo) - done) / max(0.001, rate)
            log("%d/%d  %.1f clips/s  ~%d min left  failed=%d"
                % (done, len(todo), rate, left / 60, len(failed)))

    total = sum(os.path.getsize(os.path.join(OUT, f)) for f in os.listdir(OUT))
    log("FINISHED. files=%d  size=%.1f MB  failed=%d"
        % (len(os.listdir(OUT)), total / 1024 / 1024, len(failed)))
    if failed:
        for h, t, e in failed[:20]:
            log("  FAILED %s %r %s" % (h, t[:40], e))


if __name__ == "__main__":
    main()
