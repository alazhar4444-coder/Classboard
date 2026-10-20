import glob, traceback
out = open('out/transcripts.txt', 'w', encoding='utf-8')
try:
    from faster_whisper import WhisperModel
    m = WhisperModel('large-v3', device='cpu', compute_type='int8')
    for f in sorted(glob.glob('out/Abdu_*.mp3')):
        segs, _ = m.transcribe(f, language='ar', beam_size=5)
        out.write(f.split('/')[-1] + ' | ' + ' '.join(s.text.strip() for s in segs) + '\n')
except Exception:
    out.write(traceback.format_exc())
out.close()
