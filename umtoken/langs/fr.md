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
pres part:  parl-ant parl-ante parl-ants parl-antes
past part:  parl-é parl-és parl-ée parl-ées
indicative, present:   parl-e parl-es parl-e parl-ons parl-ez parl-ent
indicative, imperfect: parl-ais parl-ais parl-ait (parl-ions) parl-iez parl-aient
indicative, past hist: parl-ai parl-as parl-a parl-âmes parl-âtes parl-èrent

### -ir verbs
infinitive: fin-ir
gerund:     fin-issant
pres part:  fin-issant fin-issante fin-issants fin-issantes
past part:  fin-i fin-is fin-ie fin-ies
indicative, present:   fin-is fin-is fin-it fin-issons fin-issez fin-issent
indicative, imperfect: fin-issais fin-issais fin-issait fin-issions fin-issiez fin-issaient
indicative, past hist: fin-is fin-is fin-it fin-îmes fin-îtes fin-irent

### -re verbs
infinitive: vend-re
gerund:     vend-ant
pres part:  vend-ant vend-ante vend-ants vend-antes
past part:  vend-u vend-us vend-ue vend-ues
indicative, present:   vend-s vend-s vend-/ vend-ons vend-ez vend-ent
indicative, imperfect: vend-ais vend-ais vend-ait (vend-ions) vend-iez vend-aient
indicative, past hist: vend-is vend-is vend-it vend-îmes vend-îtes vend-irent

### -er verbs with base ending with -g
infinitive: mang-er
gerund:     mang-eant
pres part:  mang-eant mang-eante mang-eants mang-eantes
past part:  mang-é mang-és mang-ée mang-ées
indicative, present:   mang-e mang-es mang-e mang-eons mang-ez mang-ent
indicative, imperfect: mang-eais mang-eais mang-eait (mang-ions) mang-iez mang-eaient
indicative, past hist: mang-eai mang-eas mang-ea mang-eâmes mang-eâtes mang-èrent

### -er verbs with base ending with -c
gerund:     pla[c->ç]-ant
pres part:  pla[c->ç]-ant pla[c->ç]-ante pla[c->ç]-ants pla[c->ç]-antes
indicative, present:   pla[c->ç]-ons
indicative, imperfect: pla[c->ç]-ais pla[c->ç]-ais pla[c->ç]-ait pla[c->ç]-aient
indicative, past hist: pla[c->ç]-ai pla[c->ç]-as pla[c->ç]-a pla[c->ç]-âmes pla[c->ç]-âtes
``` python
op=RegexOp(r'c$', r'ç', r'ç$', r'c')
```
