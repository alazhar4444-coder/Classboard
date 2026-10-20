import json, subprocess, traceback
lines = json.load(open('lines.json', encoding='utf-8'))
log = open('out/log.txt', 'w')
for i, t in enumerate(lines, 1):
    r = subprocess.run(['edge-tts', '--voice', 'ar-OM-AbdullahNeural', '--rate=-3%', '--text', t,
                        '--write-media', f'out/Abdu_{i:02d}.mp3'], capture_output=True, text=True)
    log.write(f'{i} rc={r.returncode} {r.stderr[-500:]}\n')
log.close()
