# Portuguese (pt)
 
## adjectives
o adjectives: rápid-a rápid-as rápid-o rápid-os
e adjectives: grand-e grand-es
adverbs:      rápid-amente grand-emente feliz-mente

## nouns
f nouns: mes-a mes-as
m nouns: amig-o amig-os
m/f nouns: estudant-e estudant-es 

### nouns ending with -m
common: homem-/ home[m->n]-s
``` python
op=RegexOp(r'm$', r'n', r'n$', r'm')
```

### nouns ending with -l
common: animal-/ anima[l->i]-s
``` python
op=RegexOp(r'l$', r'i', r'i$', r'l')
```

### nouns ending with -el
common: papel-/ pap[el->éi]-s
``` python
op=RegexOp(r'el$', r'éi', r'éi$', r'el')
```

### nouns ending with -ol
common: farol-/ far[ol->ói]-s
``` python
op=RegexOp(r'ol$', r'ói', r'ói$', r'ol')
```

### nouns ending with -ão and plural form -ões
common: informação-/ nformaç[ão->õ]-es
``` python
op=RegexOp(r'ol$', r'ói', r'ói$', r'ol')
```

## verbs
### -ar verbs
infinitive: jog-ar jog-ares jog-ar jog-armos jog-ardes jog-arem
gerund:     jog-ando
PPP:        jog-ado jog-ados jog-ada jog-adas
indicative, present:   jog-o jog-as jog-a jog-amos jog-ais jog-am
indicative, imperfect: jog-ava jog-avas jog-ava jog-ávamos jog-áveis jog-avam
indicative, preterite: jog-uei jog-aste jog-ou jog-ámos jog-amos jog-astes jog-aram

### -ir verbs
infinitive: sorr-ir
gerund:     sorr-indo
PPP:        sorr-ido sorr-idos sorr-ida sorr-idas
indicative, present:   sorr-io sorr-is sorr-i sorr-imos sorr-ides sorr-iem
indicative, imperfect: sorr-ia sorr-ias sorr-ia sorr-íamos sorr-íeis sorr-iam
indicative, preterite: sorr-i sorr-iste sorr-iu sorr-imos sorr-istes sorr-iram
 
### -er verbs
infinitive: com-er
gerund:     com-endo
PPP:        com-ido com-idos com-ida com-idas
indicative, present:   com-o com-es com-e com-emos com-eis com-em
indicative, imperfect: com-ia com-ias com-ia com-íamos com-íeis com-iam
indicative, preterite: com-i com-este com-eu com-emos com-estes com-eram