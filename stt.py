import glob, traceback, subprocess, numpy as np
out = open('out/transcripts.txt', 'w', encoding='utf-8')
try:
    from faster_whisper import WhisperModel
    m = WhisperModel('large-v3', device='cpu', compute_type='int8')
    for f in sorted(glob.glob('out/Abdu_*.mp3')):
        raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], capture_output=True).stdout
        audio = np.frombuffer(raw, np.int16).astype(np.float32) / 32768.0
        segs, _ = m.transcribe(audio, language='ar', beam_size=5)
        out.write(f.split('/')[-1] + ' | ' + ' '.join(s.text.strip() for s in segs) + '\n')
        out.flush()
except Exception:
    out.write(traceback.format_exc())
out.close()
