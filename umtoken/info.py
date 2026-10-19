# Path: umtoken/info.py

import argparse
import json
from collections import Counter

from .alphabet import ASCII_RESERVED_EOW as EOW
from .pre import SPLIT_REGEXES
from .model import NO_EOW_REGEXES

def _name(pattern, named_patterns):
    """Returns the name of a known pattern, 'custom' for unknown patterns, or None."""
    if pattern is None:
        return None
    return next((name for name, p in named_patterns.items() if p == pattern), "custom")

def get_info(tokenizer_file: str) -> dict:
    """Returns summary information about a tokenizer file (without building the tokenizer)."""
    with open(tokenizer_file, 'r', encoding="utf8") as f:
        d = json.load(f)
    pre, model = d["pre"], d["model"]
    rules = model["rules"]

    rules_by_lang = Counter()
    for r in rules[2:]: # skip default rules (empty rule, end of word rule)
        for lang in r.get("langs") or ["*"]:
            rules_by_lang[lang] += 1

    return {
        "file": tokenizer_file,
        "thumbprint": d.get("thumbprint"),
        "vocab_size": len(model["vocab"]),
        "rule_count": len(rules),
        "rules_eow": sum(1 for r in rules if r["suffix"].endswith(EOW)),
        "rules_with_op": sum(1 for r in rules if r.get("op")),
        "rules_by_lang": dict(sorted(rules_by_lang.items())),
        "langs": model.get("langs"),
        "tied": bool(model.get("vocab_langs")),
        "alphabet_size": len(pre["alphabet"]) if pre.get("alphabet") else None,
        "reserved_tokens": len(pre.get("reserved_tokens") or []),
        "normalization": pre.get("normalization"),
        "split_regex": _name(pre.get("split_regex"), SPLIT_REGEXES),
        "no_eow": _name(model.get("no_eow_regex"), NO_EOW_REGEXES),
        "number_handling": model.get("number_handling"),
    }

def main(args):
    infos = [get_info(f) for f in args.tokenizer_file]
    if args.json:
        print(json.dumps(infos if len(infos) > 1 else infos[0], ensure_ascii=False, indent=2))
        return
    for info in infos:
        print(info["file"])
        print(f"  vocab size:      {info['vocab_size']}")
        print(f"  rules:           {info['rule_count']} (eow: {info['rules_eow']}, with op: {info['rules_with_op']})")
        if info["rules_by_lang"]:
            print(f"  rules by lang:   " + ", ".join(f"{l}: {c}" for l, c in info["rules_by_lang"].items()))
        print(f"  langs:           {', '.join(info['langs'] or [])}{' (tied)' if info['tied'] else ''}")
        print(f"  alphabet size:   {info['alphabet_size']}")
        print(f"  reserved tokens: {info['reserved_tokens']}")
        print(f"  normalization:   {info['normalization']}")
        print(f"  split regex:     {info['split_regex']}")
        print(f"  no eow:          {info['no_eow']}")
        print(f"  thumbprint:      {info['thumbprint']}")

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="Show vocab size, rule count and settings of tokenizer file(s).")

    parser.add_argument("tokenizer_file",
                        nargs="+",
                        help="tokenizer file(s) (json)")

    parser.add_argument("-j", "--json",
                        action="store_true",
                        help="output as json")

    args = parser.parse_args()
    main(args)
