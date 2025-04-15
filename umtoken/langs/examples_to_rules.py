import os
import argparse
import regex as re


def get_blocks(lines):
    # Each new block starts with a heading ('#+')
    blocks = []
    block = ""
    for line in lines:
        line = line.strip()
        if line.startswith("*"): # comments
            continue
        if re.match(r'^#+', line):
            if block:
                blocks.append(block)
            block = ""
        elif line:
            block += line + "\n"
    if block:
        blocks.append(block)
    return blocks

def get_groups(block):
    groups = []
    group = []
    for line in block.splitlines():
        if not line or line.startswith("`"):
            break
        if ":" in line:
            if group:
                groups.append(group)
            group = []
            line = line.split(":")[1]
        group += [w for w in line.split(" ") if w and not w.startswith("(")]
    if group:
        groups.append(group)
    return groups

def get_op(block):
    if "op=" in block:
        return re.search(r'(op=.+)', block).group(1)
    return None

def get_constraint_regex(block):
    if "constraint_regex=" in block:
        return re.search(r'(constraint_regex=.+)', block).group(1)
    return None

def main(args):
    lang_md_files = [f"umtoken/langs/{lang}.md" for lang in args.langs]
    output_dir = os.path.join("umtoken/langs/_staging")
    os.makedirs(output_dir, exist_ok=True)
    
    for lang_md_file in lang_md_files:
        lang = os.path.basename(lang_md_file).split(".")[0]
        output_file = os.path.join(output_dir, lang + ".py")
        
        lines = open(lang_md_file, encoding="utf8").readlines()
        blocks = get_blocks(lines)

        suffix_e_rules = []
        suffix_s_rules = []
        suffix_rules = []
        complex_suffix_rules = []
        interfix_e_rules = []
        interfix_s_rules = []
        interfix_rules = []
        complex_interfix_rules = []
        
        for block in blocks:
            # print(block)
            # print()
            
            groups = get_groups(block)
            op = get_op(block)
            constraint_regex = get_constraint_regex(block)
            
            for g in groups:
                for s in g:
                    assert "-" in s, f"Error in {lang_md_file}: {s}"

            try:
                suffixes = [s.split('-')[1:][-1] for g in groups for s in g if not "(-" in s]
                suffixes = [s for s in suffixes if s != '/']
                interfixes = [s.split('(')[0].split('-')[1:][-1] for g in groups for s in g if "(-" in s]
            except:
                raise ValueError(f"Error in {lang_md_file}: {groups}")
            
            #print(suffixes)
            #print(op)
            #print(constraint_regex)
            #print()
            
            if suffixes:
                if op is None and constraint_regex is None:
                    suffix_rules += [s for s in suffixes if not (s.startswith("s") or s.startswith("e"))]
                    suffix_e_rules += [s for s in suffixes if s.startswith("e")]
                    suffix_s_rules += [s for s in suffixes if s.startswith("s")]
                else:
                    complex_suffix_rules.append((list(sorted(set(suffixes))), op, constraint_regex))
                
            if interfixes:
                if op is None and constraint_regex is None:
                    interfix_rules += [i for i in interfixes if not (i.startswith("s") or i.startswith("e"))]
                    interfix_e_rules += [i for i in interfixes if i.startswith("e")]
                    interfix_s_rules += [i for i in interfixes if i.startswith("s")]
                else:
                    complex_interfix_rules.append((list(sorted(set(interfixes))), op, constraint_regex))
        
        suffix_rules = list(sorted(set(suffix_rules)))
        suffix_e_rules = list(sorted(set(suffix_e_rules)))
        suffix_s_rules = list(sorted(set(suffix_s_rules)))
        interfix_rules = list(sorted(set(interfix_rules)))
        interfix_e_rules = list(sorted(set(interfix_e_rules)))
        interfix_s_rules = list(sorted(set(interfix_s_rules)))        
        
        # print(f"# {lang_md_file}")
        # print("suffix_rules =")
        # print(suffix_rules)
        # print(suffix_e_rules)
        # print(suffix_s_rules)
        # print(complex_suffix_rules)
        # print("interfix_rules =")
        # print(interfix_rules)
        # print(interfix_e_rules)
        # print(interfix_s_rules)
        # print(complex_interfix_rules)
        # print()
        
        def compact(a):
            return f"{a}".replace(", ", ",")

        indent = " " * 12
        generated_rules = ""
        if suffix_e_rules:
            generated_rules += f"{indent}suffix_rules(_lang, {compact(suffix_e_rules)}, constraint_regex='[^e]$') +\n"
        if  suffix_s_rules:
            generated_rules += f"{indent}suffix_rules(_lang, {compact(suffix_s_rules)}, constraint_regex='([^es]|ee)$') +\n"
        if  suffix_rules:
            generated_rules += f"{indent}suffix_rules(_lang, {compact(suffix_rules)}) +\n"
        for s, op, constraint_regex in complex_suffix_rules:
            op = ", " + op if op else ""
            constraint_regex = ", " + constraint_regex if constraint_regex else ""
            generated_rules += f"{indent}suffix_rules(_lang, {compact(s)}{op}{constraint_regex}) +\n"
        if interfix_e_rules:
            generated_rules += f"{indent}interfix_rules(_lang, {compact(interfix_e_rules)}, constraint_regex='[^e]$') +\n"
        if interfix_s_rules:
            generated_rules += f"{indent}interfix_rules(_lang, {compact(interfix_s_rules)}, constraint_regex='([^es]|ee)$') +\n"
        if interfix_rules:
            generated_rules += f"{indent}interfix_rules(_lang, {compact(interfix_rules)}) +\n"
        for i, op, constraint_regex in complex_interfix_rules:
            op = ", " + op if op else ""
            constraint_regex = ", " + constraint_regex if constraint_regex else ""
            generated_rules += f"{indent}interfix_rules(_lang, {compact(i)}{op}{constraint_regex}) +\n"
        
        generated_rules = generated_rules.rstrip("\n")
        
        code = f"""# Path: umtoken/langs/{lang}.py

from umtoken.rules import RegexOp
from umtoken.langs.utils import DEFAULT_RULES, suffix_rules, interfix_rules

_lang = '{lang}'

{lang.upper()}_RULES = (DEFAULT_RULES + 
{generated_rules}
{indent}[])
"""
        with open(output_file, "w", encoding="utf8") as f:
            f.write(code)

        # print(code)
        # print()
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert examples to rules')
    parser.add_argument("-l", "--langs", nargs='+', help='Language codes')
    args = parser.parse_args()
    main(args)
