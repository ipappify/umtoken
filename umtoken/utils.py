# Path: umtoken/utils.py

from typing import List, Optional, Union


def cumsum(items):
    total = 0
    yield total
    for x in items:
        total += x
        yield total
        
def index(find, text: str, start=0):
    try:
        return text.index(find, start)
    except ValueError:
        return -1
    
def tocase(text: str, cs: int) -> str:
    if not text:
        return text
    if cs == 1:
        text = text.capitalize()
    elif cs == 2:
        text = text.upper()
    return text
    
def format(ids, morpher, no_join: bool = False, apply_ws: bool = False, apply_case: bool = False):
    parts = []
    eow_before = True
    cs = 0
    ws = ""
    for rvid in ids:
        base = morpher.vocab[rvid[0]]
        rule = morpher.rules[rvid[1]]
        if len(rvid) == 4:
            ws = " " if apply_ws and rvid[3] else ""
            cs = rvid[2] if apply_case and eow_before else cs
        op = rule.op
        stem = op.apply(base) if op else base
        if stem != base:
            if hasattr(op, "apply_regex") and hasattr(op, "apply_sub"):
                # use actual regex op to format the base/stem (e.g., "ru[n->nn]")
                def sub(match):
                    repl = op.apply_sub
                    for i, grp in enumerate(match.groups()):
                        repl = repl.replace(f"\\{i+1}", grp)
                    return f"[{match.group(0)}->{repl}]"
                stem = op.apply_regex.sub(sub, base)
            else:
                # fall back to, format like common_part[end_base->end_stem]  (e.g., "run[->n]")
                common_len = ([a == b for a, b in zip(base, stem)] + [False]).index(False)
                common_part = base[:common_len]
                end_base = base[common_len:]
                end_stem = stem[common_len:]
                stem = common_part + "[" + end_base + "->" + end_stem + "]"
        stem = stem.replace("G", " ")
        parts.append(ws + tocase(stem + "+" + rule.suffix.replace("$",""), cs) or "/")
        eow_before = rule.suffix.endswith("X")
        if not eow_before:
            cs = 0 if cs < 2 else 2
    return parts if no_join else "|".join(parts)

def chunk_list(l: list, n: int):
    """
    Splits a list into n interleaved chunks.
    
    Args:
        l: The list to split.
        n: The number of chunks.
        
    Returns:
        A list of n chunks.
        
    Examples:
        chunk_list([1,2,3,4,5,6,7,8,9,10], 3) -> [[1,4,7,10], [2,5,8], [3,6,9]]    
    """
    if not isinstance(l, list):
        l = list(l)
    chunks = [l[i::n] for i in range(n)]
    assert sum(len(c) for c in chunks) == len(l)
    return chunks

def get_rules_bitmask(langs, rules):
    rules_langs = [0] * len(rules)
    for i, r in enumerate(rules):
        if not r.any_lang:
            rules_langs[i] = sum(1 << langs.index(l) for l in r.langs)
        else:
            rules_langs[i] = (1 << len(langs)) - 1 # all languages
    return rules_langs

def get_langs_bitmask(langs: List[str], ls: Optional[Union[int, str, List[str]]]) -> Optional[int]:
    if ls == 0:
        return 0
    elif isinstance(ls, int):
        return ls
    elif not ls:
        return None # all languages
    elif isinstance(ls, str):
        ls = [ls]
    mask = 0
    for l in ls:
        try:
            mask |= 1 << langs.index(l)
        except ValueError:
            pass
    return mask if mask else None

def expand_languages(languages):
    if "eu3" in languages:
        languages.remove("eu3")
        languages.extend(["de", "en", "fr"])
    if "eu5" in languages:
        languages.remove("eu5")
        languages.extend(["de", "en", "es", "fr", "it"])
    if "eu8" in languages:
        languages.remove("eu8")
        languages.extend(["de", "en", "es", "fr", "it", "nl", "pl", "ro"])
    if "eu12" in languages:
        languages.remove("eu12")
        languages.extend(["cs", "de", "el", "en", "es", "fr", "hu", "it", "nl", "pl", "pt", "ro"])
    if "eu24" in languages:
        languages.remove("eu24")
        languages.extend(["bg", "cs", "da", "de", "el", "en", "es", "et", 
                          "fi", "fr", "ga", "hr", "hu", "it", "lt", "lv", 
                          "mt", "nl", "pl", "pt", "ro", "sk", "sl", "sv"])
    languages = list(sorted(set(languages)))
    return languages