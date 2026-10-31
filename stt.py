import json, subprocess, numpy as np
raw = subprocess.run(['ffmpeg','-v','error','-i','out/ahmed_full.mp3','-ac','1','-ar','16000','-f','s16le','-'],capture_output=True).stdout
audio = np.frombuffer(raw,np.int16).astype(np.float32)/32768.0
from faster_whisper import WhisperModel
m = WhisperModel('large-v3', device='cpu', compute_type='int8')
segs,_ = m.transcribe(audio, language='ar', beam_size=5, word_timestamps=True)
out=[]
for s in segs:
    out.append({'start':s.start,'end':s.end,'text':s.text,'words':[{'w':w.word,'s':w.start,'e':w.end} for w in (s.words or [])]})
json.dump(out, open('out/segments.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
