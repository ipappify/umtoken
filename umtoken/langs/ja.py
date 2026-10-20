# Path: umtoken/langs/ja.py

# Japanese words are encoded without end-of-word marker (train.py --no-eow ja), because a pre-token
# (content word + hiragana tail) may continue with further hiragana words. Hence, all rules are
# interfix rules (without EOW); the detokenizer ends a word after each of their suffixes.
# Rules require kana in the alphabet (languages: ja). Verbs and i-adjectives use the dictionary
# form as base (書く, 食べる, 高い), the final kana is replaced by a regex op.

from umtoken.rules import RegexOp
from umtoken.alphabet import ASCII_RESERVED_UTF8
from umtoken.langs.utils import DEFAULT_RULES, interfix_rules

_lang = 'ja'

# Verb and adjective bases must contain kanji or katakana (or escaped characters), or end with one of
# the (closed set of) kana-only grammatical verbs/adjectives. Otherwise, function words are analyzed
# as made-up verbs: また = まる[る->]+た, または = まる[る->]+たは, まず = まる[る->]+ず.
VERB_BASE_REGEX = (r'[\p{Han}\p{Katakana}' + ASCII_RESERVED_UTF8 + r']|(ある|いる|なる|できる|おく|よる|わたる|したがう|'
                   r'しまう|みる|いく|くる|いう|される|させる|られる|せる|れる)$')
ADJ_BASE_REGEX = r'[\p{Han}\p{Katakana}' + ASCII_RESERVED_UTF8 + r']|(ない|よい|いい)$'

def _rules(suffixes, op=None, constraint_regex=None):
    # single-kanji bases (人の) must be allowed if kanji are in the alphabet; verbs and adjectives
    # have at least two characters (行く, 見る) - otherwise a bare kana could be morphed to an empty stem
    if op is not None and constraint_regex is None:
        constraint_regex = VERB_BASE_REGEX
    return interfix_rules(_lang, suffixes, op=op, constraint_regex=constraint_regex, penalty=0.0,
                          min_base_length=1 if op is None else 2)

def _op(src, dst):
    """replace the final kana src of the base by dst"""
    return RegexOp(src + '$', dst, dst + '$', src)

# particles and compound particles
PARTICLES = ['の','は','が','を','に','で','と','へ','も','や','か',
             'から','まで','より','など','だけ','しか','ばかり','ほど','くらい',
             'には','では','とは','にも','でも','とも','からは','までは','よりも',
             'への','での','との','からの','までの',
             'として','について','によって','による','における','において','においては']
# sentence-final particles
FINAL_PARTICLES = ['ね','よ','よね','かな']
# copula (after nouns and na-adjectives)
COPULA = ['だ','だった','だろう','です','でした','でしょう','である','であり',
          'ではない','じゃない','ではありません','な']
# suru-verbs (after sino-japanese nouns: 勉強する)
SURU = ['する','します','しました','しません','しない','した','して','している','しています',
        'される','された','させる','できる','できます','できない']
HONORIFICS = ['さん','さま','くん','ちゃん','たち']

# verb forms by stem
MASU = ['ます','ました','ません','ませんでした','ましょう','たい','たかった','たくない','ながら','そう','すぎる']
NAI = ['ない','なかった','なくて','なければ','ず','れる','れた','れない','せる','せた']
E_ROW = ['る','ます','ない','ば'] # potential, conditional
O_ROW = ['う'] # volitional
TE = ['て','た','ている','ています','ていた','ていました','ていない','てください',
      'たら','たり','ても','ては','てしまう','てしまった']
def _voiced(xs):
    """te/ta forms of godan verbs with voiced onbin (泳いで, 読んだ)"""
    return ['で' + s[1:] if s.startswith('て') else 'だ' + s[1:] for s in xs]
TE_VOICED = _voiced(TE)

# verb forms followed by a particle (参照すると, 含まれるが): rules do not chain, so without combined
# rules the inflected form would have to be a vocab entry to serve as base of the particle rule
VERB_PARTICLES = ['と','が','か','は','も','まで','の','より']
TE_PARTICLES = ['は','も','の','より','から'] # しては, しても, しての, してより, してから
def _with_particles(forms, te_forms=(), extra=(), particles=VERB_PARTICLES):
    return [f + p for f in forms for p in particles] + [f + p for f in te_forms for p in TE_PARTICLES] + list(extra)
SURU_P = _with_particles(['する','される','させる','できる','した','している','しない'], ['して'],
                         ['せずに','するまでの','されるまでの','するには'])
# godan rules are generated for all 9 rows: only the most frequent particles
GODAN_PARTICLES = ['と','が','か','は','も','まで']
GODAN_A_P = _with_particles(['ない','れる','せる'], extra=['ずに'], particles=GODAN_PARTICLES) # a-row
GODAN_TE_P = _with_particles(['た','ている'], ['て'], particles=GODAN_PARTICLES) # onbin
ICHIDAN_P = _with_particles(['ない','た','ている','ていない','られる','させる'], ['て'], ['ずに'])

# godan verbs: dictionary ending -> i-row (masu), a-row (nai), e-row, o-row, te/ta onbin, voiced te
GODAN = [('う','い','わ','え','お','っ',False), ('く','き','か','け','こ','い',False),
         ('ぐ','ぎ','が','げ','ご','い',True),  ('す','し','さ','せ','そ','し',False),
         ('つ','ち','た','て','と','っ',False), ('ぬ','に','な','ね','の','ん',True),
         ('ぶ','び','ば','べ','ぼ','ん',True),  ('む','み','ま','め','も','ん',True),
         ('る','り','ら','れ','ろ','っ',False)]

# ichidan verbs: drop る (食べる -> 食べます)
ICHIDAN = MASU + ['ない','なかった','なくて','なければ','ず','られる','られた','させる','させた',
                  'よう','れば','ろ'] + TE

# i-adjectives: drop い (高い -> 高くない)
I_ADJ = ['く','くて','くない','くなかった','かった','ければ','さ','そう','すぎる','くなる','くなった']

GODAN_RULES = sum((_rules(MASU, _op(d, i)) + _rules(NAI, _op(d, a)) + _rules(E_ROW, _op(d, e)) +
                   _rules(O_ROW, _op(d, o)) + _rules(TE_VOICED if voiced else TE, _op(d, te))
                   for d, i, a, e, o, te, voiced in GODAN), [])
GODAN_P_RULES = sum((_rules(GODAN_A_P, _op(d, a)) + _rules(_voiced(GODAN_TE_P) if voiced else GODAN_TE_P, _op(d, te))
                     for d, i, a, e, o, te, voiced in GODAN), [])

JA_RULES = (DEFAULT_RULES +
            _rules(PARTICLES) +
            _rules(FINAL_PARTICLES) +
            _rules(COPULA) +
            _rules(SURU) +
            _rules(HONORIFICS) +
            GODAN_RULES +
            _rules(TE, _op('く','っ')) + # 行く -> 行って
            _rules(ICHIDAN, _op('る','')) +
            _rules(I_ADJ, _op('い',''), ADJ_BASE_REGEX) +
            # verb forms + particle
            _rules(SURU_P) +
            GODAN_P_RULES +
            _rules(ICHIDAN_P, _op('る','')) +
            [])
