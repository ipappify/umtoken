# Irish (ga)
* initial mutations give separate stems: lenition (bord : bhord), eclipsis (bord : mbord), t-/h- prefixes (an t-uisce, na hoíche)
* only lenition of conditional/past verb forms is covered by an op (mol : mholfadh)
* the past tense with d' before vowels (ól : d'ól) is not covered
* slenderization in genitives and plurals (bord : boird, fear : fir) gives separate stems
* adverbs use the particle "go" (go maith) and need no rules

## adjectives
* the comparative follows "níos", the superlative "is" (níos airde, is airde)
* comparative forms use the slenderized stem (ard : aird-e, deas : deis-e)

### plural and comparison

```
plural:      mór-a deas-a maith-e
comparative: aird-e deis-e tábhacht-aí
```

## nouns

### plurals

```
-anna:   carr-anna bus-anna ceist-eanna áit-eanna
-acha:   cathr-acha oibr-eacha tábhacht-acha
-aí/-í:  rud-aí cúrs-aí cailín-í múinteoir-í
-ta/-te: síol-ta ceol-ta tin-te
```

### genitive singular (feminine)

```
common: scoil-e áit-e súil-e
```

## verbs
* after particles (an, ní, go, nach) stems are mutated and give separate stems

### present and imperative

```
present:    mol-ann bris-eann ceann-aíonn bail-íonn
            mol-aimid bris-imid ceann-aímid bail-ímid
imperative: mol-aigí bris-igí ceann-aígí bail-ígí
```

### future

```
future: mol-faidh bris-fidh ceann-óidh bail-eoidh éir-eoidh
        mol-faimid bris-fimid
```

### conditional and past (lenited stem)

```
conditional: [m->mh]ol-fadh [b->bh]ris-feadh [c->ch]eann-ódh [b->bh]ail-eodh
past:        [m->mh]ol-amar [b->bh]ris-eamar [c->ch]eann-aíomar
```

``` python
op=RegexOp(r'^([bcdfgmpst])([^h])', r'\1h\2', r'^([bcdfgmpst])h', r'\1')
```

### autonomous forms

```
present: mol-tar bris-tear ceann-aítear bail-ítear
future:  mol-far bris-fear ceann-ófar
```

### verbal nouns and adjectives

```
verbal noun: mol-adh bris-eadh ceann-ú bail-iú
             sábh-áil bain-t oscail-t
verbal adj:  mol-ta glan-ta bris-te ceann-aithe bail-ithe
```

## derivation

```
V>N:   múin-teoir múinteoir-eacht iascair-eacht
N>N:   siopa-dóir ceol-tóir teach-ín
ADJ>N: daonn-acht
N>ADJ: tábhacht-ach aist-each grian-mhar
       caird-iúil suim-iúil
```
