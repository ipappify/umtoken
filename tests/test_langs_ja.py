# Path: test/test_langs_ja.py

import regex as re

from umtoken.langs import get_rules
from umtoken.langs.ja import JA_RULES, _lang
from umtoken.alphabet import get_alphabet
from umtoken.morpher import Morpher
from umtoken.model import Model, NO_EOW_REGEXES
from umtoken.pre import PreTokenizer, SPLIT_REGEX, SPLIT_JA_REGEX
from umtoken.tokenizer import Tokenizer
from umtoken.trainer import DEFAULT_UTF8_SEED

from .utils import get_bases, decompose, format

def test_rules():
    # ja words are encoded without end of word marker
    examples = [
        ("東京には", "東京+には"),
        ("日本語の", "日本語+の"),
        ("学生です", "学生+です"),
        ("勉強します", "勉強+します"),
        ("田中さん", "田中+さん"),
        ("書きました", "書[く->き]+ました"),
        ("書かない", "書[く->か]+ない"),
        ("書けば", "書[く->け]+ば"),
        ("書こう", "書[く->こ]+う"),
        ("書いて", "書[く->い]+て"),
        ("泳いでいる", "泳[ぐ->い]+でいる"),
        ("話した", "話[す->し]+た"),
        ("待って", "待[つ->っ]+て"),
        ("読んだ", "読[む->ん]+だ"),
        ("帰ります", "帰[る->り]+ます"),
        ("行って", "行[く->っ]+て"),
        ("食べました", "食べ[る->]+ました"),
        ("食べられる", "食べ[る->]+られる"),
        ("高くない", "高[い->]+くない"),
        ("高かった", "高[い->]+かった"),
        # verb forms + particle
        ("参照すると", "参照+すると"),
        ("参照しては", "参照+しては"),
        ("含まれるが", "含[む->ま]+れるが"),
        ("書いたが", "書[く->い]+たが"),
        ("泳いでいるか", "泳[ぐ->い]+でいるか"),
        ("食べないと", "食べ[る->]+ないと"),
        ("食べてから", "食べ[る->]+てから"),
        ("形態において", "形態+において"),
        # kana-only grammatical verbs and adjectives
        ("であった", "であ[る->っ]+た"),
        ("されている", "され[る->]+ている"),
        ("よく", "よ[い->]+く"),
    ]

    morpher = Morpher([_lang], get_bases(examples), rules=JA_RULES)

    for word, expected in examples:
        ids = decompose(word, morpher)
        actual = format(ids, morpher)
        assert expected in actual

def test_no_made_up_verbs():
    # function words must not be analyzed as inflected kana-only "verbs" (まる, はまる, よう)
    morpher = Morpher([_lang], ["まる", "はまる", "よう", "また", "は"], rules=JA_RULES)
    for word in ["また", "または", "まず", "はまた", "よって"]:
        actual = format(decompose(word, morpher), morpher)
        assert "[" not in actual, f"{word}: {actual}"

def test_split_regex():
    examples = [
        ("東京タワーに行きました", ["東京", "タワーに", "行きました"]),
        ("ラーメン屋でカレーを食べる", ["ラーメン", "屋で", "カレーを", "食べる"]),
        ("ﾗｰﾒﾝ屋", ["ﾗｰﾒﾝ", "屋"]),
        ("すごーい", ["すごーい"]),
        ("一ヶ月", ["一ヶ月"]),
        ("東京tokyo", ["東京", "tokyo"]),
        ("Tokyoタワー", ["Tokyo", "タワー"]),
        ("これはPythonです", ["これは", "Pythonです"]),
        ("αβγ東京", ["αβγ", "東京"]),
        ("ＵＳＢメモリ", ["ＵＳＢ", "メモリ"]),
    ]
    split_regex = re.compile(SPLIT_JA_REGEX)
    for text, expected in examples:
        assert [m.group(1) for m in split_regex.finditer(text)] == expected

    # no change for scripts other than ja
    text = "Hello World, ABCdef CamelCase  123 Grüße aus Köln. Москва αβγ"
    assert ([m.group(1) for m in split_regex.finditer(text)] ==
            [m.group(1) for m in re.compile(SPLIT_REGEX).finditer(text)])

def _get_tokenizer():
    alphabet = get_alphabet(["en", _lang])
    pre = PreTokenizer(alphabet=alphabet, split_regex=SPLIT_JA_REGEX, normalization="ipt-cjk")
    bases = ["東京", "行く", "日本語", "テキスト", "tokyo", "tower"]
    vocab = ["[UNK]"] + [pre.encoding.escape(b) for b in bases] + list(alphabet) + DEFAULT_UTF8_SEED
    vocab = list(dict.fromkeys(vocab))
    rules = get_rules([_lang])
    vocab_logits = [0.0 if len(v) > 1 else -5.0 for v in vocab]
    model = Model(vocab, rules, vocab_logits, [0.0] * len(rules), 1.0, 0.02,
                  no_eow_regex=NO_EOW_REGEXES["ja"])
    return Tokenizer(pre, model)

def test_no_eow():
    tokenizer = _get_tokenizer()
    model = tokenizer.model

    # ja words: no eow, words of other scripts: eow
    assert not model.is_eow_rule[model.encode(tokenizer.pre.encoding.escape("東京には"))[-1][1]]
    assert model.is_eow_rule[model.encode("tokyo")[-1][1]]
    # ja suffixes end words on detokenization, other suffixes don't
    assert all(model.is_word_end_rule[i] for i, r in enumerate(model.rules) if r.suffix in ("の", "には", "ました"))
    assert not model.is_word_end_rule[0]

    for text in ["東京には行きました。", "日本語のテキスト", "東京 Tokyo tower", "東京Tokyo", "Tokyo東京には"]:
        tokens = tokenizer.tokenize(text)
        assert tokenizer.detokenize(tokens) == text

    # words end after ja suffixes
    text, ranges, _ = tokenizer.detokenize(tokenizer.tokenize("東京には行きました"), return_ranges=True)
    words = [text[o:o+l] for o, l in ranges]
    assert words[0] == "東京には"
    assert words[-1].endswith("ました")

def test_save_load():
    tokenizer = _get_tokenizer()
    loaded = Tokenizer.load_dict(tokenizer.save_dict())
    assert loaded.model.no_eow_regex.pattern == NO_EOW_REGEXES["ja"]
    assert loaded.model.is_word_end_rule == tokenizer.model.is_word_end_rule
    text = "東京には行きました。"
    assert loaded.tokenize(text) == tokenizer.tokenize(text)
