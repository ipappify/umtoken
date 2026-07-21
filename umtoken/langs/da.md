# Danish (da)

## adjectives
common:      billig-/ billig-t billig-e
comparative: billig-ere
superlative: billig-st billig-ste ny-est ny-este

## nouns
class 1:   måned-/ måned-en måned-er måned-erne
           måned-s måned-ens måned-ers måned-ernes
class 2:   dag-/ dag-en  dag-e  dag-ene
           dag-s dag-ens dag-es dag-enes
class 3:   år-/ år-et  år-/ år-ene
           år-s år-ets år-s år-enes

### nouns ending with -er (definite plural -ne)
common: lærer-ne lærer-nes
``` python
constraint_regex='er$'
```

## verbs

### finite forms

*          prs act  past act  prs pas  past pas
class 1:   husk-er  husk-ede  husk-es  husk-edes
class 2:   dømm-er  døm-te    dømm-es  døm-tes

### vowel-final verbs (present -r)
common: bo-r tro-r se-r få-r
``` python
constraint_regex='[aeiouyæøå]$'
```

### non-finite forms

*          inf act  inf pas  pa         pp       (gerund)
class 1:   husk-e   husk-es  husk-ende  husk-et  (husk-en)
class 2:   dømm-e   dømm-es  dømm-ende  døm-t    (dømm-en)

### duplicate consonant before vowel in suffix
class 1:     dy[p->pp]-ede dy[p->pp]-edes
class 2:     dø[m->mm]-er dø[m->mm]-es dø[m->mm]-e dø[m->mm]-es dø[m->mm]-ende
comparative: sm[uk->ukk]-ere sm[uk->ukk]-est sm[uk->ukk]-este
nouns:       ko[p->pp]-en
``` python
op=RegexOp(r'([bdfgklmnprst])$', r'\1\1', r'([bdfgklmnprst])\1$', r'\1')
```

## derivation
V>N:   forsk-ning forsk-ningen forsk-ninger forsk-ningerne
       føl-else føl-elsen føl-elser føl-elserne
V>ADJ: brug-bar brug-bart brug-bare
ADJ>N: svag-hed svag-heden svag-heder svag-hederne
