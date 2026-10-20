import json, subprocess, sys, traceback, os
lines = json.load(open('lines.json', encoding='utf-8'))
log = open('out/log.txt', 'w')
ok = 0
try:
    log.write(subprocess.run(['edge-tts', '--list-voices'], capture_output=True, text=True).stdout[-3000:])
except Exception:
    log.write(traceback.format_exc())
for i, t in enumerate(lines, 1):
    for v in ['ar-OM-AbdullahNeural', 'ar-OM-AyshaNeural']:
        tag = v.split('-')[2][:4]
        r = subprocess.run(['edge-tts', '--voice', v, '--rate=+4%', '--text', t,
                            '--write-media', f'out/{tag}_{i:02d}.mp3'], capture_output=True, text=True)
        log.write(f'{v} {i} rc={r.returncode} {r.stderr[-800:]}\n')
        ok += r.returncode == 0
if ok == 0:
    log.write('edge failed, trying gTTS\n')
    try:
        from gtts import gTTS
        for i, t in enumerate(lines, 1):
            gTTS(t, lang='ar').save(f'out/gtts_{i:02d}.mp3')
    except Exception:
        log.write(traceback.format_exc())
log.close()
