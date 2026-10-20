import json, subprocess
lines = json.load(open('lines.json', encoding='utf-8'))
log = open('out/log.txt', 'w')
VOICES = ['ar-SA-HamedNeural','ar-QA-MoazNeural','ar-KW-FahedNeural','ar-JO-TaimNeural']
for v in VOICES:
    tag = v.split('-')[1]
    for i, t in enumerate(lines, 1):
        r = subprocess.run(['edge-tts', '--voice', v, '--rate=-3%', '--text', t, '--write-media', f'out/{tag}_{i:02d}.mp3'], capture_output=True, text=True)
        log.write(f'{v} {i} rc={r.returncode} {r.stderr[-300:]}\n')
log.close()
