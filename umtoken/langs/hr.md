# Croatian (hr)

## adjectives

### regular forms (definite and indefinite)
nom: nov-/ nov-i nov-a nov-o nov-e
gen: nov-og nov-oga nov-e nov-ih
dat: nov-om nov-omu nov-ome nov-oj nov-im nov-ima
acc: nov-og nov-u nov-o nov-e nov-a
ins: nov-im nov-om nov-ima
loc: nov-om nov-ome nov-oj nov-im nov-ima

### comparison
comparative: nov-iji nov-ija nov-ije nov-ijeg nov-ijem nov-ijih nov-ijim nov-ijima nov-iju nov-ijoj nov-ijom
             lak-ši lak-ša lak-še lak-šeg lak-šem lak-šu lak-šoj lak-šom lak-ših lak-šim lak-šima
adverbs:     nov-ije lak-še

### superlative (naj- prefix)
superlative: [->naj]nov-iji [->naj]nov-ija [->naj]nov-ije [->naj]nov-ijeg [->naj]nov-ijem [->naj]nov-ijih [->naj]nov-ijim [->naj]nov-ijima [->naj]nov-iju [->naj]nov-ijoj [->naj]nov-ijom
             [->naj]lak-ši [->naj]lak-ša [->naj]lak-še
``` python
op=RegexOp(r'^', r'naj', r'^naj', r'')
```

### possessive (-ov/-ev, -in)
common: brat-ov brat-ova brat-ovo brat-ovi brat-ove brat-ovu brat-ovog brat-ovom brat-ovim brat-ovih brat-ovima
        kralj-ev kralj-eva kralj-evo kralj-evi kralj-eve kralj-evu kralj-evog kralj-evom kralj-evim kralj-evih kralj-evima
        sestr-in sestr-ina sestr-ino sestr-ini sestr-ine sestr-inu sestr-inog sestr-inom sestr-inim sestr-inih sestr-inima

## nouns

### m nouns (hard, long plural -ovi)
nom: grad-/ grad-ovi
gen: grad-a grad-ova
dat: grad-u grad-ovima
acc: grad-/ grad-ove
voc: grad-e grad-ovi
loc: grad-u grad-ovima
ins: grad-om grad-ovima

### m nouns (soft, long plural -evi)
nom: kralj-/ kralj-evi
gen: kralj-a kralj-eva
dat: kralj-u kralj-evima
acc: kralj-a kralj-eve
voc: kralj-u kralj-evi
loc: kralj-u kralj-evima
ins: kralj-em kralj-evima

### m nouns (short plural)
nom: prozor-i
gen: prozor-a
dat: prozor-ima
acc: prozor-e

### f nouns (a-stems)
nom: žen-a žen-e
gen: žen-e žen-a
dat: žen-i žen-ama
acc: žen-u žen-e
voc: žen-o žen-e
loc: žen-i žen-ama
ins: žen-om žen-ama

### f nouns (i-stems)
nom: stvar-/ stvar-i
gen: stvar-i stvar-i
dat: stvar-i stvar-ima
acc: stvar-/ stvar-i
loc: stvar-i stvar-ima
ins: stvar-i stvar-ju stvar-ima

### n nouns
nom: sel-o sel-a mor-e mor-a
gen: sel-a mor-a
dat: sel-u mor-u
acc: sel-o mor-e
loc: sel-u mor-u
ins: sel-om mor-em
dat/loc/ins pl: sel-ima mor-ima

### n nouns (n-stems and t-stems)
nom: im-e tel-e
gen: im-ena tel-eta
dat: im-enu tel-etu
ins: im-enom tel-etom
pl:  im-ena im-enima

### k -> c before plural i (sibilarization)
common: vojni[k->c]-i vojni[k->c]-ima
``` python
op=RegexOp(r'k$', r'c', r'c$', r'k')
```

### g -> z before plural i (sibilarization)
common: bubre[g->z]-i bubre[g->z]-ima
``` python
op=RegexOp(r'g$', r'z', r'z$', r'g')
```

### h -> s before plural i (sibilarization)
common: ora[h->s]-i ora[h->s]-ima
``` python
op=RegexOp(r'h$', r's', r's$', r'h')
```

### k -> č in vocative (palatalization)
common: vojni[k->č]-e
``` python
op=RegexOp(r'k$', r'č', r'č$', r'k')
```

### g -> ž in vocative (palatalization)
common: dru[g->ž]-e
``` python
op=RegexOp(r'g$', r'ž', r'ž$', r'g')
```

### h -> š in vocative (palatalization)
common: du[h->š]-e
``` python
op=RegexOp(r'h$', r'š', r'š$', r'h')
```

## verbs
* aorist and imperfect forms are literary/archaic in modern Croatian and not covered
* irregular verbs in -ći (ići, reći) form their stems by suppletion/ablaut and are not covered

### -ati verbs
infinitive: gled-ati
ADV:        gled-ajući
N:          gled-anje
past part:  gled-ao gled-ala gled-alo gled-ali gled-ale gled-ala
pass part:  gled-an gled-ana gled-ano gled-ani gled-ane
indicative, present: gled-am gled-aš gled-a gled-amo gled-ate gled-aju
imperative: gled-aj gled-ajmo gled-ajte

### -iti verbs
infinitive: rad-iti
ADV:        rad-eći
N:          rađ-enje viđ-enje
past part:  rad-io rad-ila rad-ilo rad-ili rad-ile rad-ila
pass part:  rađ-en rađ-ena rađ-eno rađ-eni rađ-ene
            kup-ljen kup-ljena kup-ljeno kup-ljeni kup-ljene
indicative, present: rad-im rad-iš rad-i rad-imo rad-ite rad-e
imperative: rad-i rad-imo rad-ite

### -jeti verbs
infinitive: vid-jeti
past part:  vid-io vid-jela vid-jelo vid-jeli vid-jele

### -nuti verbs
infinitive: okre-nuti
past part:  okre-nuo okre-nula okre-nulo okre-nuli okre-nule
pass part:  okre-nut okre-nuta okre-nuto okre-nuti okre-nute
indicative, present: okre-nem okre-neš okre-ne okre-nemo okre-nete okre-nu
imperative: okre-ni okre-nimo okre-nite

### -ovati verbs
infinitive: kup-ovati
ADV:        kup-ujući
N:          kup-ovanje
past part:  kup-ovao kup-ovala kup-ovalo kup-ovali kup-ovale
pass part:  kup-ovan kup-ovana kup-ovano kup-ovani kup-ovane
indicative, present: kup-ujem kup-uješ kup-uje kup-ujemo kup-ujete kup-uju
imperative: kup-uj kup-ujmo kup-ujte

## derivation
V>N:   uči-telj uči-telja uči-telju uči-teljem uči-telji uči-telje uči-teljima
V>ADJ: čit-ljiv čit-ljiva čit-ljivo čit-ljivi čit-ljive
       izved-iv izved-iva izved-ivo
ADJ>N: brz-ost brz-osti brz-ostima
N>ADJ: grad-ski grad-ska grad-sko grad-ske grad-skog grad-skoj grad-skim grad-skih grad-skima grad-sku grad-skom
N>N:   učitelj-ica učitelj-ice učitelj-ici učitelj-icu učitelj-icom učitelj-icama

## interfixes (compounds): 
common: vod-o(-pad) par-o(-brod)
