import wave, numpy as np, json, re, sys, os
from pocketsphinx import Decoder

OUT = r"C:\Users\blazy\OneDrive\Pictures\AI Content\Dark Lantern\DL17 - The Wallace Line\voice_grady"
LINES = os.path.join(OUT, "lines_list.json")
lines = json.load(open(LINES))
segs = json.load(open(f'{OUT}/clips.json'))

w = wave.open(f'{OUT}/voiceover.wav')
sr = w.getframerate()
mono = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).reshape(-1, 2).mean(1)

NUMS = {
    '40': 'forty percent', '80': 'eighty percent', '2016': 'twenty sixteen',
    '2013': 'twenty thirteen', '2021': 'twenty twenty one', '2006': 'two thousand six',
    '2019': 'twenty nineteen', '2023': 'twenty twenty three', '17': 'seventeen',
    '47': 'forty seven', '53': 'fifty three', '300': 'three hundred',
    '206': 'two hundred and six', '20': 'twenty', '30': 'thirty',
    '180': 'one hundred and eighty', '2009': 'two thousand nine', '1st': 'first',
    '1859': 'eighteen fifty nine', '2012': 'twenty twelve', '1966': 'nineteen sixty six',
    '1971': 'nineteen seventy one'
}

def spoken(tok):
    core = re.sub(r'[^0-9a-z]', '', tok.lower())
    if core in NUMS:
        return NUMS[core].split()
    if core.isdigit():
        from num2words import num2words
        n = int(core)
        w = num2words(n, to='year') if 1100 <= n <= 2099 else num2words(n)
        return w.replace('-', ' ').replace(',', '').split()
    t = tok.lower().replace('-', ' ').replace('…', ' ')
    t = t.replace('100,000', 'one hundred thousand').replace('20', 'twenty').replace('50', 'fifty')
    return re.sub(r"[^a-z' ]", " ", t).split()

dec = Decoder(samprate=16000, bestpath=False, loglevel='FATAL')
custom_words = [
    ('lombok', 'L AA M B AA K'),
    ('cockatoos', 'K AA K AH T UW Z'),
    ('cockatoo', 'K AA K AH T UW'),
    ('snorkel', 'S N AO R K AH L'),
    ('seafloor', 'S IY F L AO R'),
    ('trench', 'T R EH N CH'),
    ('kangaroos', 'K AE NG G AH R UW Z'),
    ('bali', 'B AA L IY')
]
for wd, ph in custom_words:
    if not dec.lookup_word(wd):
        dec.add_word(wd, ph, True)

caps = []
fails = 0
words = []

for line, (s, e) in zip(lines, segs):
    x = mono[int(s * sr):int(e * sr)]
    x16 = np.interp(np.arange(0, len(x), 1.5), np.arange(len(x)), x).astype(np.int16)
    toks = line.split()
    sp = [spoken(t) for t in toks]
    flat = [q for z in sp for q in z]
    known = all(dec.lookup_word(wd) for wd in flat)
    
    times = []
    if known:
        dec.set_align_text(' '.join(flat))
        dec.start_utt()
        dec.process_raw(x16.tobytes(), full_utt=True)
        dec.end_utt()
        for seg in dec.seg():
            if seg.word and not seg.word.startswith('<'):
                times.append((round(s + seg.start_frame * 0.01, 3), round(s + seg.end_frame * 0.01, 3)))
    
    if len(times) != len(flat):
        fails += 1
        dur = e - s
        dt = dur / max(1, len(flat))
        times = [(round(s + i * dt, 3), round(s + (i + 1) * dt, 3)) for i in range(len(flat))]
    
    idx = 0
    cur = []
    cs = None
    for tok, z in zip(toks, sp):
        if not z:
            continue
        st = times[idx][0]
        en = times[idx + len(z) - 1][1]
        idx += len(z)
        if cs is None:
            cs = st
        cur.append(tok)
        ce = en
        words.append([tok, st, en, len(caps)])
        if len(cur) >= 4 or re.search(r'[.,?!…:]$', tok):
            caps.append([' '.join(cur), cs, ce])
            cur = []
            cs = None
    if cur:
        caps.append([' '.join(cur), cs, ce])

for i in range(len(caps) - 1):
    caps[i][2] = min(caps[i + 1][1], caps[i][2] + 0.35)
caps[-1][2] = segs[-1][1]

json.dump(caps, open(f'{OUT}/captions_fa.json', 'w'), indent=2)
json.dump(words, open(f'{OUT}/words_fa.json', 'w'), indent=2)
print(f'Done! Generated {len(words)} aligned words and {len(caps)} captions (fallback lines: {fails}/{len(lines)})')
