# Spanish (es)
 
## adjectives

```
o adjectives: bonit-a bonit-as bonit-o bonit-os
e adjectives: grand-e grand-es
adverbs:      bonit-amente grand-emente real-mente
```

## nouns

```
f nouns: cas-a cas-as
m nouns: libr-o libr-os
m/f nouns: estudiant-e estudiant-es 
           flor-/ flor-es
```

### nouns ending with -z

```
common: acidez-/ acide[z->c]-es
```

``` python
op=RegexOp(r'z$', r'c', r'c$', r'z')
```

## verbs
### -ar verbs

```
infinitive: habl-ar
gerund:     habl-ando
V>N, V>ADJ: habl-ante habl-antes
past part:  habl-ado habl-ados habl-ada habl-adas
indicative, present:   habl-o habl-as habl-a habl-amos habl-áis habl-an
                       habl-ás
indicative, imperfect: habl-aba habl-abas habl-aba habl-ábamos habl-abais habl-aban
indicative, preterite: habl-é habl-aste habl-ó habl-amos habl-asteis habl-aron
indicative, future:    habl-aré habl-arás habl-ará habl-aremos habl-aréis habl-arán
conditional, present:  habl-aría habl-arías habl-aría habl-aríamos habl-aríais habl-arían
subjunctive, present:  habl-e habl-es habl-e habl-emos habl-éis habl-en
subjunctive, imperfect: habl-ara habl-aras habl-ara (habl-áramos) (habl-arais) habl-aran
```

### -ir verbs

```
infinitive: viv-ir
gerund:     viv-iendo
V>N, V>ADJ: viv-iente viv-ientes
past part:  viv-ido viv-idos viv-ida viv-idas
indicative, present:   viv-o viv-es viv-e viv-imos viv-ís viv-en
                       viv-ís
indicative, imperfect: viv-ía viv-ías viv-ía viv-íamos viv-íais viv-ían
indicative, preterite: viv-í viv-iste viv-ió viv-imos viv-isteis viv-ieron
indicative, future:    viv-iré viv-irás viv-irá viv-iremos viv-iréis viv-irán
conditional, present:  viv-iría viv-irías viv-iría viv-iríamos viv-iríais viv-irían
subjunctive, present:  viv-a viv-as viv-a viv-amos viv-áis viv-an
subjunctive, imperfect: viv-iera viv-ieras viv-iera (viv-iéramos) (viv-ierais) viv-ieran
```

### -er verbs

```
infinitive: com-er
gerund:     com-iendo
V>N, V>ADJ: corr-iente corr-ientes
past part:  com-ido com-idos com-ida com-idas
indicative, present:   com-o com-es com-e com-emos com-éis com-en
                       com-és
indicative, imperfect: com-ía com-ías com-ía com-íamos com-íais com-ían
indicative, preterite: com-í com-iste com-ió com-imos com-isteis com-ieron
indicative, future:    com-eré com-erás com-erá com-eremos com-eréis com-erán
conditional, present:  com-ería com-erías com-ería com-eríamos com-eríais com-erían
subjunctive, present:  com-a com-as com-a com-amos com-áis com-an
subjunctive, imperfect: com-iera com-ieras com-iera (com-iéramos) (com-ierais) com-ieran
```

### -car verbs (c -> qu before e)

```
indicative, preterite: bus[c->qu]-é
subjunctive, present:  bus[c->qu]-e bus[c->qu]-es bus[c->qu]-emos bus[c->qu]-éis bus[c->qu]-en
```

``` python
op=RegexOp(r'c$', r'qu', r'qu$', r'c')
```

### -gar verbs (g -> gu before e)

```
indicative, preterite: lle[g->gu]-é
subjunctive, present:  lle[g->gu]-e lle[g->gu]-es lle[g->gu]-emos lle[g->gu]-éis lle[g->gu]-en
```

``` python
op=RegexOp(r'g$', r'gu', r'gu$', r'g')
```

### -zar verbs (z -> c before e)

```
indicative, preterite: empe[z->c]-é
subjunctive, present:  empe[z->c]-e empe[z->c]-es empe[z->c]-emos empe[z->c]-éis empe[z->c]-en
```

``` python
op=RegexOp(r'z$', r'c', r'c$', r'z')
```

## derivation

```
V>N:   trabaj-ador trabaj-adora trabaj-adores trabaj-adoras
       vend-edor vend-edora vend-edores vend-edoras
       form-ación form-aciones equip-aje equip-ajes
V>ADJ: am-able am-ables pos-ible pos-ibles
ADJ>N: capac-idad capac-idades
```
