# Estonian (et)
* Estonian has no vowel harmony (unlike Finnish)
* cases attach to the genitive stem (raamat : raamatu : raamatus)
* clitics (-gi/-ki) attach after inflected forms and are not covered
* compounds concatenate directly (raamatukogu) and need no interfix rules

## adjectives
* adjectives decline like nouns and agree in case
* the superlative is usually analytic (kõige suurem) and needs no extra rules

### comparison

```
comparative: suure-m suure-ma suure-mad suure-mat
             ilusa-m
superlative: suur-im suur-ima suur-imad
adverbs:     kiire-lt aeglase-lt
```

### adverbs in -sti

```
common: ilusa-sti kiire-sti
```

``` python
constraint_regex='[^s]$'
```

## nouns

### declension (singular)

```
nominative:  raamat-/   keel-/
genitive:    raamatu-/  keele-/
partitive:   raamatu-t  keel-t
allative:    raamatu-le keele-le
adessive:    raamatu-l  keele-l
ablative:    raamatu-lt keele-lt
translative: raamatu-ks keele-ks
terminative: raamatu-ni keele-ni
essive:      raamatu-na keele-na
abessive:    raamatu-ta keele-ta
comitative:  raamatu-ga keele-ga
```

### inessive, elative, illative, plural partitive (s-initial endings)

```
inessive:     raamatu-s  keele-s
elative:      raamatu-st keele-st
illative:     raamatu-sse keele-sse
partitive pl: maja-sid auto-sid
```

``` python
constraint_regex='[^s]$'
```

### declension (plural)

```
nominative:  raamatu-d keele-d
genitive:    raamatu-te keel-te maja-de
partitive:   raamatu-id keel-i
inessive:    raamatu-tes maja-des
elative:     raamatu-test maja-dest
illative:    raamatu-tesse maja-desse
allative:    raamatu-tele maja-dele
adessive:    raamatu-tel maja-del
ablative:    raamatu-telt maja-delt
translative: raamatu-teks maja-deks
terminative: raamatu-teni
essive:      raamatu-tena
abessive:    raamatu-teta
comitative:  raamatu-tega maja-dega
```

### -ne words (inimene : inimese)

```
nominative: inime-ne inime-sed
genitive:   inime-se inime-ste
partitive:  inime-st inime-si
```

``` python
constraint_regex='[^s]$'
```

### weak grade (kk/pp/tt -> k/p/t)
* other gradation patterns (b -> v, g -> /, d -> /, ...) are not covered

```
genitive: sep[pp->p]-a kot[tt->t]-i luk[kk->k]-u
```

``` python
op=RegexOp(r'([aeiouõäöü])([kpt])\2$', r'\1\2', r'([aeiouõäöü])([kpt])$', r'\1\2\2')
```

## verbs
* the negative (ei ela) uses the particle "ei" and needs no rules
* strong/weak grade alternation in verb stems (lugema : loen) gives separate stems (loe-tud)

### infinitives, present, imperative, participles

```
ma-infinitive: ela-ma luge-ma
da-infinitive: ela-da luge-da
present:       ela-n ela-d ela-b ela-me ela-te ela-vad
               tule-n tule-b tule-vad
imperative:    ela-ge ela-gu luge-ge
supine forms:  ela-mas ela-mast ela-mata luge-mas
gerund:        ela-des luge-des
participles:   ela-v ela-nud ela-tud
               luge-v luge-nud loe-tud söö-dud
```

### past tense (s-initial endings)

```
past: ela-sin ela-sid ela-s ela-sime ela-site
      luge-sin luge-s
```

``` python
constraint_regex='[^s]$'
```

### conditional and passive

```
conditional: ela-ks ela-ksin ela-ksid ela-ksime ela-ksite
             luge-ks
passive:     ela-takse ela-ti ela-tav
```

## derivation

```
V>N:   luge-mine luge-mise luge-mist luge-mised luge-miste
       õpeta-ja õpeta-jad õpeta-jate õpeta-jaid
ADJ>N: kiir-us kiir-use kiir-ust kiir-used kiir-uste
       vaba-dus vaba-duse vaba-dust
N>ADJ: riik-lik riik-liku riik-likud
       aja-line aja-lise aja-list
       õnne-tu töö-tu
N>N:   eest-lane eest-lase eest-last eest-lased eest-laste eest-lasi
```
