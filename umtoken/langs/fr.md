# French (fr)

## adjectives
common:  petit-/ petit-s petit-e petit-es
adverbs: lent-ement absolu-ment

### adjectives ending with -al
m forms: principal-/ princip[al->/]-aux
``` python
op=RegexOp(r'al$', r'', r'$', r'al')
```

### adjectives ending with -s -t plus ive
m forms: act[iv->if]- act[iv->if]-s
``` python
op=RegexOp(r'([st])iv$', r'\1if', r'([st])if$', r'\1iv')
```

## nouns
m nouns: chat-/ chat-s
f nouns: maison-/ maison-s

## verbs
### -er verbs
infinitive: parl-er
gerund:     parl-ant
PPA:        parl-ant parl-ante parl-ants parl-antes
PPP:        parl-é parl-és parl-ée parl-ées
indicative, present:   parl-e parl-es parl-e parl-ons parl-ez parl-ent
indicative, imperfect: parl-ais parl-ais parl-ait (parl-ions) parl-iez parl-aient

### -ir verbs
infinitive: fin-ir
gerund:     fin-issant
PPA:        fin-issant fin-issante fin-issants fin-issantes
PPP:        fin-i fin-is fin-ie fin-ies
indicative, present:   fin-is fin-is fin-it fin-issons fin-issez fin-issent
indicative, imperfect: fin-issais fin-issais fin-issait fin-issions fin-issiez fin-issaient

### -re verbs
infinitive: vend-re
gerund:     vend-ant
PPA:        vend-ant vend-ante vend-ants vend-antes
PPP:        vend-u vend-us vend-ue vend-ues
indicative, present:   vend-s vend-s vend-/ vend-ons vend-ez vend-ent
indicative, imperfect: vend-ais vend-ais vend-ait (vend-ions) vend-iez vend-aient

### -er verbs with base ending with -g
infinitive: mang-er
gerund:     mang-eant
PPA:        mang-eant mang-eante mang-eants mang-eantes
PPP:        mang-é mang-és mang-ée mang-ées
indicative, present:   mang-e mang-es mang-e mang-eons mang-ez mang-ent
indicative, imperfect: mang-eais mang-eais mang-eait (mang-ions) mang-iez mang-eaient

### -er verbs with base ending with -c
infinitive: plac-er
gerund:     pla[c->ç]-ant
PPA:        pla[c->ç]-ant pla[c->ç]-ante pla[c->ç]-ants pla[c->ç]-antes
PPP:        plac-é plac-és plac-ée plac-ées
indicative, present:   plac-e plac-es plac-e pla[c->ç]-ons plac-ez plac-ent
indicative, imperfect: pla[c->ç]-ais pla[c->ç]-ais pla[c->ç]-ait (plac-ions) plac-iez pla[c->ç]-aient
``` python
op=RegexOp(r'c$', r'ç', r'ç$', r'c')
```
