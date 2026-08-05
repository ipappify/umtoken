# Latvian (lv)
* stems are segmented before the case/person endings (vīr-s, strādā-ju)
* palatalization before endings (brālis : brāļa, upe : upju) gives separate stems (brāļ-a, upj-u)
* the instrumental equals the accusative (sg) / dative (pl) and needs no extra rules
* 6th declension i-stems (sirds : sirdis) are not covered
* the negative prefix ne- (nestrādā) is not covered

## adjectives
* adjectives agree in gender, number and case (liels, liela, lieli, lielas)

### indefinite declension

```
masculine: liel-s liel-a liel-am liel-u liel-ā
           liel-i liel-iem liel-us liel-os
feminine:  liel-as liel-ai liel-ām liel-ās
```

### definite declension

```
masculine: liel-ais liel-ā liel-ajam liel-o liel-ajā
           liel-ie liel-ajiem liel-ajos
feminine:  liel-ajai liel-ajām liel-ajās
```

### comparison

```
comparative: liel-āks liel-āka liel-āki liel-ākas liel-āku liel-āko
adverbs:     ātr-i ātr-āk
```

### superlative (vis- prefix)

```
common: [->vis]liel-ākais [->vis]liel-ākā [->vis]liel-ākie [->vis]liel-ākās [->vis]liel-āko
        [->vis]ātr-āk
```

``` python
op=RegexOp(r'^', r'vis', r'^vis', r'')
```

## nouns

### masculine -s/-is (vīrs, brālis)

```
nominative: vīr-s  brāl-is   vīr-i brāļ-i
genitive:   vīr-a  brāļ-a    vīr-u brāļ-u
dative:     vīr-am brāl-im   vīr-iem brāļ-iem
accusative: vīr-u  brāl-i    vīr-us brāļ-us
locative:   vīr-ā  brāl-ī    vīr-os brāļ-os
```

### masculine -us (tirgus)

```
common: tirg-us tirg-um tirg-u tirg-ū tirg-i
```

### feminine -a (sieva)

```
nominative: siev-a  siev-as
genitive:   siev-as siev-u
dative:     siev-ai siev-ām
accusative: siev-u
locative:   siev-ā  siev-ās
```

### feminine -e (upe)

```
nominative: up-e  up-es
genitive:   up-es upj-u
dative:     up-ei up-ēm
accusative: up-i
locative:   up-ē  up-ēs
```

## verbs
* different tense stems (lasa : lasīja) give separate stems (las-a, lasī-ja)

### infinitive, present, past

```
infinitive: strādā-t lasī-t darī-t
present:    strādā-ju strādā-jam strādā-jat
            las-u las-i las-a las-ām las-āt dar-a
past:       strādā-ja strādā-jām strādā-jāt
            lasī-ju lasī-ji lasī-ja lasī-jām lasī-jāt
```

### future

```
future: strādā-šu strādā-si strādā-s strādā-sim strādā-siet
        lasī-s redzē-s
```

### conditional, imperative, reflexive

```
conditional: strādā-tu lasī-tu
imperative:  strādā-jiet las-iet
reflexive:   mazgā-ties mazgā-jas mazgā-jās
```

### participles

```
past active:     strādā-jis strādā-jusi strādā-juši lasī-jis
past passive:    strādā-ts strādā-ta strādā-ti strādā-tas
                 lasī-ts lasī-ta
present:         strādā-jošs strādā-jams
half-participle: dziedā-dams dziedā-dama
gerund:          strādā-jot las-ot
```

## derivation

```
V>N:   lasī-šana lasī-šanas lasī-šanu lasī-šanā strādā-šana
       skolo-tājs skolo-tāja skolo-tāji skolo-tāju lasī-tājs
ADJ>N: liel-ums liel-uma liel-umu jaun-ums
       brīv-ība brīv-ības brīv-ību vien-ība
N>ADJ: latv-isks latv-iska latv-iski
       laim-īgs laim-īga laim-īgi laim-īgu
N>N:   latv-ietis latv-ieša latv-ieši latv-iešu
```
