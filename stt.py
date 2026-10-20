import glob, traceback, subprocess, json, re, difflib, numpy as np
lines = json.load(open('lines.json', encoding='utf-8'))
def norm(s):
    s = re.sub(r'[ً-ْـ]', '', s)
    s = re.sub('[إأآ]', 'ا', s).replace('ة', 'ه').replace('ى', 'ي')
    s = re.sub(r'[^ء-ي0-9 ]', ' ', s)
    return s.split()
out = open('out/transcripts.txt', 'w', encoding='utf-8')
try:
    from faster_whisper import WhisperModel
    m = WhisperModel('large-v3', device='cpu', compute_type='int8')
    scores = {}
    for f in sorted(glob.glob('out/*_*.mp3')):
        name = f.split('/')[-1]; tag, idx = name[:-4].split('_'); idx = int(idx)
        raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], capture_output=True).stdout
        audio = np.frombuffer(raw, np.int16).astype(np.float32) / 32768.0
        segs, _ = m.transcribe(audio, language='ar', beam_size=5)
        txt = ' '.join(s.text.strip() for s in segs)
        a, b = norm(lines[idx-1]), norm(txt)
        r = difflib.SequenceMatcher(None, a, b).ratio()
        scores.setdefault(tag, []).append(r)
        out.write(f'{name} | {r:.2f} | {txt}\n'); out.flush()
    out.write('\nSCORES\n')
    for k, v in sorted(scores.items(), key=lambda kv: -sum(kv[1])):
        out.write(f'{k} {sum(v)/len(v):.3f}\n')
except Exception:
    out.write(traceback.format_exc())
out.close()
