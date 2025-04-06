# English (en)

## adjectives
common:      nic-e
comparative: nic-er
superlative: nic-est

### adjective > adverb
common: nic-ely proud-ly

## nouns
common: cat-/ cat-s 
        tree-/ tree-s 
        hous-e hous-es

## verbs
infinitive: lov-e
gerund:     lov-ing
V>N:        lov-er lov-ers execut-able execut-ables feel-ing feel-ings
V>ADJ:      lov-able sens-ible
V>ADV:      lov-ably sens-ibly
PPP:        lov-ed (free-d|fre-ed)
indicative, present:   complet-e complet-es say-s
indicative, imperfect: complet-ed

### verbs ending with -y
PPP:        stud[y->i]-ed
V>N:        dr[y->i]-er dr[y->i]-ers
indicative, present:   stud[y->i]-es
indicative, imperfect: stud[y->i]-ed
``` python
op=RegexOp(r'y$', r'i', r'i$', r'y')
```

### verbs ending with b d f g k l m n p r s t
gerund:    ru[n->nn]-ing ru[n->nn]-ings
V>N:       ru[n->nn]-er ru[n->nn]-ers
V>ADJ:     control[l->ll]-able control[l->ll]-ables
V>ADV:     control[l->ll]-ably
``` python
op=RegexOp(r'([bdfgklmnprst])$', r'\1\1', r'([bdfgklmnprst])\1$', r'\1')
```

