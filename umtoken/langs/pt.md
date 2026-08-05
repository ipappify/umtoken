# Portuguese (pt)
 
## adjectives

```
o adjectives: rápid-a rápid-as rápid-o rápid-os
e adjectives: grand-e grand-es
adverbs:      lent-amente grand-emente feliz-mente
```

## nouns

```
f nouns: mes-a mes-as
m nouns: amig-o amig-os
m/f nouns: estudant-e estudant-es 
           flor-/ flor-es
```

### nouns ending with -m

```
common: homem-/ home[m->n]-s
```

``` python
op=RegexOp(r'm$', r'n', r'n$', r'm')
```

### nouns ending with -l

```
common: animal-/ anima[l->i]-s
```

``` python
op=RegexOp(r'l$', r'i', r'i$', r'l')
```

### nouns ending with -el

```
common: papel-/ pap[el->éi]-s
```

``` python
op=RegexOp(r'el$', r'éi', r'éi$', r'el')
```

### nouns ending with -ol

```
common: farol-/ far[ol->ói]-s
```

``` python
op=RegexOp(r'ol$', r'ói', r'ói$', r'ol')
```

### nouns ending with -ão and plural form -ões

```
common: informação-/ informaç[ão->õ]-es
```

``` python
op=RegexOp(r'ão$', r'õ', r'õ$', r'ão')
```

### nouns ending with -ão and plural form -ães

```
common: alemão-/ alem[ão->ã]-es
```

``` python
op=RegexOp(r'ão$', r'ã', r'ã$', r'ão')
```

## verbs
### -ar verbs
* future subjunctive forms are identical to the personal infinitive

```
infinitive: fal-ar fal-ares fal-ar fal-armos (fal-ardes) fal-arem
gerund:     fal-ando
past part:  fal-ado fal-ados fal-ada fal-adas
indicative, present:   fal-o fal-as fal-a fal-amos (fal-ais) fal-am
indicative, imperfect: fal-ava fal-avas fal-ava fal-ávamos (fal-áveis) fal-avam
indicative, preterite: fal-ei fal-aste fal-ou fal-ámos fal-amos (fal-astes) fal-aram
indicative, future:    fal-arei fal-arás fal-ará fal-aremos (fal-areis) fal-arão
conditional, present:  fal-aria fal-arias fal-aria fal-aríamos (fal-aríeis) fal-ariam
subjunctive, present:  fal-e fal-es fal-e fal-emos (fal-eis) fal-em
subjunctive, imperfect: fal-asse fal-asses fal-asse (fal-ássemos) (fal-ásseis) fal-assem
```

### -ir verbs

```
infinitive: part-ir part-ires part-ir part-irmos (part-irdes) part-irem
gerund:     part-indo
past part:  part-ido part-idos part-ida part-idas
indicative, present:   part-o part-es part-e part-imos (part-is) part-em
indicative, imperfect: part-ia part-ias part-ia part-íamos (part-íeis) part-iam
indicative, preterite: part-i part-iste part-iu part-imos (part-istes) part-iram
indicative, future:    part-irei part-irás part-irá part-iremos (part-ireis) part-irão
conditional, present:  part-iria part-irias part-iria part-iríamos (part-iríeis) part-iriam
subjunctive, present:  part-a part-as part-a part-amos (part-ais) part-am
subjunctive, imperfect: part-isse part-isses part-isse (part-íssemos) (part-ísseis) part-issem
```

### -er verbs

```
infinitive: com-er com-eres com-er com-ermos (com-erdes) com-erem
gerund:     com-endo
past part:  com-ido com-idos com-ida com-idas
indicative, present:   com-o com-es com-e com-emos (com-eis) com-em
indicative, imperfect: com-ia com-ias com-ia com-íamos (com-íeis) com-iam
indicative, preterite: com-i com-este com-eu com-emos (com-estes) com-eram
indicative, future:    com-erei com-erás com-erá com-eremos (com-ereis) com-erão
conditional, present:  com-eria com-erias com-eria com-eríamos (com-eríeis) com-eriam
subjunctive, present:  com-a com-as com-a com-amos (com-ais) com-am
subjunctive, imperfect: com-esse com-esses com-esse (com-êssemos) (com-êsseis) com-essem
```

### -car verbs (c -> qu before e)

```
indicative, preterite: fi[c->qu]-ei
subjunctive, present:  fi[c->qu]-e fi[c->qu]-es fi[c->qu]-emos fi[c->qu]-em
```

``` python
op=RegexOp(r'c$', r'qu', r'qu$', r'c')
```

### -gar verbs (g -> gu before e)

```
indicative, preterite: jo[g->gu]-ei
subjunctive, present:  jo[g->gu]-e jo[g->gu]-es jo[g->gu]-emos jo[g->gu]-em
```

``` python
op=RegexOp(r'g$', r'gu', r'gu$', r'g')
```

### -çar verbs (ç -> c before e)

```
indicative, preterite: come[ç->c]-ei
subjunctive, present:  come[ç->c]-e come[ç->c]-es come[ç->c]-emos come[ç->c]-em
```

``` python
op=RegexOp(r'ç$', r'c', r'c$', r'ç')
```

## derivation

```
V>N:   jog-ador jog-adora jog-adores jog-adoras
       vend-edor vend-edora vend-edores vend-edoras
       form-ação form-ações lav-agem lav-agens
V>ADJ: am-ável am-áveis poss-ível poss-íveis
ADJ>N: capac-idade capac-idades
```
