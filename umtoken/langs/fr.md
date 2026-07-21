# French (fr)

## adjectives
common:  petit-/ petit-s petit-e petit-es
adverbs: lent-ement absolu-ment

### adjectives ending with -al
m forms: principal-/ princip[al->/]-aux
``` python
op=RegexOp(r'al$', r'', r'$', r'al')
```

### adjectives ending with -sive -tive
m forms: act[iv->if]- act[iv->if]-s
``` python
op=RegexOp(r'([st])iv$', r'\1if', r'([st])if$', r'\1iv')
```

## nouns
m nouns: chat-/ chat-s
f nouns: maison-/ maison-s

### nouns and adjectives ending with -au -eu -ou
plural: chateau-x
``` python
constraint_regex='(au|eu|ou)$'
```

## verbs
### -er verbs
infinitive: parl-er
gerund:     parl-ant
verbal adj: parl-ant parl-ante parl-ants parl-antes
past part:  parl-é parl-és parl-ée parl-ées
indicative, present:   parl-e parl-es parl-e parl-ons parl-ez parl-ent
indicative, imperfect: parl-ais parl-ais parl-ait (parl-ions) parl-iez parl-aient
indicative, past hist: parl-ai parl-as parl-a (parl-âmes) (parl-âtes) parl-èrent
indicative, future:    parl-erai parl-eras parl-era parl-erons parl-erez parl-eront
conditional, present:  parl-erais parl-erais parl-erait parl-erions parl-eriez parl-eraient

### -ir verbs
infinitive: fin-ir
gerund:     fin-issant
verbal adj: fin-issant fin-issante fin-issants fin-issantes
past part:  fin-i fin-is fin-ie fin-ies
indicative, present:   fin-is fin-is fin-it fin-issons fin-issez fin-issent
indicative, imperfect: fin-issais fin-issais fin-issait fin-issions fin-issiez fin-issaient
indicative, past hist: fin-is fin-is fin-it (fin-îmes) (fin-îtes) fin-irent
indicative, future:    fin-irai fin-iras fin-ira fin-irons fin-irez fin-iront
conditional, present:  fin-irais fin-irais fin-irait fin-irions fin-iriez fin-iraient
subjunctive, present:  fin-isse fin-isses fin-isse fin-issions fin-issiez fin-issent

### -re verbs
* future/conditional omitted: suffixes (-rai -ras -ra -rais ...) are too short and collision-prone
infinitive: vend-re
gerund:     vend-ant
verbal adj: vend-ant vend-ante vend-ants vend-antes
past part:  vend-u vend-us vend-ue vend-ues
indicative, present:   vend-s vend-s vend-/ vend-ons vend-ez vend-ent
indicative, imperfect: vend-ais vend-ais vend-ait (vend-ions) vend-iez vend-aient
indicative, past hist: vend-is vend-is vend-it (vend-îmes) (vend-îtes) vend-irent

### -er verbs with base ending with -g
* future/conditional (mang-erai ...) are covered by the regular -er rules
infinitive: mang-er
gerund:     mang-eant
verbal adj: mang-eant mang-eante mang-eants mang-eantes
past part:  mang-é mang-és mang-ée mang-ées
indicative, present:   mang-e mang-es mang-e mang-eons mang-ez mang-ent
indicative, imperfect: mang-eais mang-eais mang-eait (mang-ions) mang-iez mang-eaient
indicative, past hist: mang-eai mang-eas mang-ea (mang-eâmes) (mang-eâtes) mang-èrent

### -er verbs with base ending with -c
* future/conditional (plac-erai ...) are covered by the regular -er rules
gerund:     pla[c->ç]-ant
verbal adj: pla[c->ç]-ant pla[c->ç]-ante pla[c->ç]-ants pla[c->ç]-antes
indicative, present:   pla[c->ç]-ons
indicative, imperfect: pla[c->ç]-ais pla[c->ç]-ais pla[c->ç]-ait pla[c->ç]-aient
indicative, past hist: pla[c->ç]-ai pla[c->ç]-as pla[c->ç]-a (pla[c->ç]-âmes) (pla[c->ç]-âtes)
``` python
op=RegexOp(r'c$', r'ç', r'ç$', r'c')
```

### -er verbs with base ending with -el -et (doubling)
indicative, present:  appe[l->ll]-e appe[l->ll]-es appe[l->ll]-ent
indicative, future:   appe[l->ll]-erai appe[l->ll]-eras appe[l->ll]-era appe[l->ll]-erons appe[l->ll]-erez appe[l->ll]-eront
conditional, present: appe[l->ll]-erais appe[l->ll]-erais appe[l->ll]-erait appe[l->ll]-erions appe[l->ll]-eriez appe[l->ll]-eraient
``` python
op=RegexOp(r'e([lt])$', r'e\1\1', r'e([lt])\1$', r'e\1')
```

### -er verbs with -e- in base (è alternation)
indicative, present:  ach[e->è]t-e ach[e->è]t-es ach[e->è]t-ent
indicative, future:   ach[e->è]t-erai ach[e->è]t-eras ach[e->è]t-era ach[e->è]t-erons ach[e->è]t-erez ach[e->è]t-eront
conditional, present: ach[e->è]t-erais ach[e->è]t-erais ach[e->è]t-erait ach[e->è]t-erions ach[e->è]t-eriez ach[e->è]t-eraient
``` python
op=RegexOp(r'e([lnrstv])$', r'è\1', r'è([lnrstv])$', r'e\1')
```

### -er verbs with -é- in base (è alternation)
indicative, present: préf[é->è]r-e préf[é->è]r-es préf[é->è]r-ent
``` python
op=RegexOp(r'é([bcdfglmnprstv]{1,2})$', r'è\1', r'è([bcdfglmnprstv]{1,2})$', r'é\1')
```

## derivation
V>N:   vend-eur vend-eurs vend-euse vend-euses
V>ADJ: aim-able aim-ables
ADJ>N: rapid-ité rapid-ités
