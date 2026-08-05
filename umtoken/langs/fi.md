# Finnish (fi)
* Finnish has vowel harmony: back suffixes (a/o/u) after back stems, front suffixes (ä/ö/y) after front stems
* clitics (-kin, -kaan, -ko, -han, ...) attach after inflected forms and are not covered
* compounds concatenate directly (kirjakauppa) and need no interfix rules

## adjectives
* adjectives decline like nouns (iso, isot, isossa, ...)

### comparison

```
comparative: iso-mpi iso-mman iso-mmat iso-mpaa iso-mpia iso-mmassa iso-mmalla
superlative: suur-in suur-imman suur-immat suur-impia suur-immassa suur-immalla
adverbs:     nopea-sti hitaa-sti
```

## nouns
* comitative (-ineen) and instructive (-in) are rare and excluded

### back harmony

```
nominative:  talo-/    talo-t
genitive:    talo-n    talo-jen
partitive:   talo-a    talo-ja
inessive:    talo-ssa  talo-issa
elative:     talo-sta  talo-ista
illative:    talo-on   talo-ihin
             kala-an   katu-un
             maa-han   työ-hön
adessive:    talo-lla  talo-illa
ablative:    talo-lta  talo-ilta
allative:    talo-lle  talo-ille
essive:      talo-na   talo-ina
translative: talo-ksi  talo-iksi
abessive:    talo-tta
plural stem of a-stems:
             kalo-ja   kalo-jen  kalo-issa
```

### front harmony

```
nominative:  kylä-/    kylä-t
genitive:    kylä-n    kyl-ien
partitive:   kylä-ä    kyl-iä
inessive:    kylä-ssä  kyl-issä
elative:     kylä-stä  kyl-istä
illative:    kylä-än   kyl-iin
adessive:    kylä-llä  kyl-illä
ablative:    kylä-ltä  kyl-iltä
allative:    kylä-lle  kyl-ille
essive:      kylä-nä   kyl-inä
translative: kylä-ksi  kyl-iksi
```

### e-stems and i-stems

```
nominative:  huone-/      kiv-i
genitive:    huonee-n     kive-n
partitive:   huone-tta    kive-ä
inessive:    huonee-ssa   kive-ssä
illative:    huonee-seen  kiv-een
partitive plural: huone-ita kiv-iä
inessive plural:  huone-issa kiv-issä
```

### -nen words (nainen, and all -inen/-lainen derivatives)

```
nominative:  nai-nen   nai-set
genitive:    nai-sen
partitive:   nai-sta   nai-sia
inessive:    nai-sessa nai-sissa
elative:     nai-sesta
illative:    nai-seen
adessive:    nai-sella nai-silla
allative:    nai-selle nai-sille
essive:      nai-sena
translative: nai-seksi
```

### possessive suffixes

```
common: talo-ni talo-si talo-nsa talo-mme talo-nne
        kylä-nsä
```

### weak grade (kk/pp/tt -> k/p/t)
* other gradation patterns (k -> /, p -> v, nt -> nn, nk -> ng) are not covered

```
genitive:      kau[pp->p]a-n  ka[tt->t]o-n  ty[tt->t]ö-n
nominative pl: kau[pp->p]a-t
inessive:      kau[pp->p]a-ssa  ty[tt->t]ö-ssä
elative:       ka[tt->t]o-sta
adessive:      kau[pp->p]a-lla  ty[tt->t]ö-llä
ablative:      ka[tt->t]o-lta
allative:      kau[pp->p]a-lle
translative:   ka[tt->t]o-ksi
```

``` python
op=RegexOp(r'([aeiouäöy])([kpt])\2([aouäöy])$', r'\1\2\3', r'([aeiouäöy])([kpt])([aouäöy])$', r'\1\2\2\3')
```

### weak grade (t -> d)

```
genitive:      ka[t->d]u-n  pöy[t->d]ä-n
nominative pl: ka[t->d]u-t
inessive:      ka[t->d]u-ssa
adessive:      pöy[t->d]ä-llä
```

``` python
op=RegexOp(r't([aouäöy])$', r'd\1', r'd([aouäöy])$', r't\1')
```

## verbs
* the negative (en puhu, ei puhu) uses the auxiliary "ei" and needs no rules
* strong/weak grade alternation in verb stems (luken -> luen) is not covered

### type 1 (-a/-ä)

```
infinitive:  puhu-a kysy-ä
present:     puhu-n puhu-t puhu-u puhu-mme puhu-tte puhu-vat
             kysy-y kysy-vät sano-o
past:        puhu-in puhu-it puhu-i puhu-imme puhu-itte puhu-ivat
conditional: puhu-isin puhu-isit puhu-isi puhu-isimme puhu-isitte puhu-isivat
             kysy-isi kysy-isivät
imperative:  puhu-kaa kysy-kää
passive:     puhu-taan puhu-ttiin kysy-tään kysy-ttiin
participles: puhu-va kysy-vä puhu-nut kysy-nyt puhu-neet puhu-ttu kysy-tty
inf forms:   puhu-maan puhu-massa puhu-masta puhu-matta
             kysy-mään kysy-mässä
```

### other infinitive types

```
infinitive:  syö-dä juo-da tul-la men-nä halu-ta pelä-tä
participles: tul-lut tul-leet men-nyt
```

## derivation

```
V>N:   puhu-minen puhu-misen puhu-mista puhu-misessa
       kysy-minen kysy-misen kysy-mistä
       opetta-ja opetta-jan opetta-jat opetta-jia opetta-jien
       teki-jä teki-jän
ADJ>N: vapa-us vapa-uden vapa-utta vapa-uksia
       syv-yys syv-yyden syv-yyttä syv-yyksiä
N>ADJ: kiv-inen kiv-isen kiv-istä kiv-isiä
       kansa-llinen kansa-llisen kansa-llista kansa-llisia
       raha-ton työ-tön
N>N:   suoma-lainen suoma-laisen suoma-laiset suoma-laisia
       helsinki-läinen helsinki-läisen helsinki-läiset helsinki-läisiä
```
