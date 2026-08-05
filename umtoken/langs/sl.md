# Slovenian (sl)

## adjectives

### regular forms (incl. definite -i and dual -ima)

```
nom: nov-/ nov-i nov-a nov-o nov-e
gen: nov-ega nov-e nov-ih
dat: nov-emu nov-i nov-im nov-ima
acc: nov-ega nov-o nov-e nov-a
loc: nov-em nov-i nov-ih
ins: nov-im nov-o nov-imi nov-ima
```

### comparison

```
comparative: nov-ejši nov-ejša nov-ejše nov-ejšega nov-ejšemu nov-ejšem nov-ejšim nov-ejših nov-ejšimi nov-ejšo
             lep-ši lep-ša lep-še lep-šega lep-šemu lep-šem lep-šim lep-ših lep-šimi lep-šo
adverbs:     hitr-eje
```

### superlative (naj- prefix)

```
superlative: [->naj]nov-ejši [->naj]nov-ejša [->naj]nov-ejše
             [->naj]lep-ši [->naj]lep-ša [->naj]lep-še
adverbs:     [->naj]hitr-eje
```

``` python
op=RegexOp(r'^', r'naj', r'^naj', r'')
```

### possessive (-ov/-ev, -in)

```
common: brat-ov brat-ova brat-ovo brat-ovi brat-ove brat-ovega brat-ovemu brat-ovem brat-ovim brat-ovih brat-ovimi
        kralj-ev kralj-eva kralj-evo kralj-evi kralj-eve kralj-evega kralj-evemu kralj-evem kralj-evim kralj-evih kralj-evimi
        sestr-in sestr-ina sestr-ino sestr-ini sestr-ine sestr-inega sestr-inemu sestr-inem sestr-inim sestr-inih sestr-inimi
```

### adjective > adverb

```
common: hitr-o lep-o
```

## nouns

### masculine (hard and soft)

```
nom: korak-/ korak-i kralj-/ kralj-i
gen: korak-a korak-ov kralj-a kralj-ev
dat: korak-u korak-om kralj-u kralj-em
acc: korak-/ korak-e
loc: korak-u korak-ih
ins: korak-om korak-i kralj-em kralj-i
dual: korak-a korak-oma
```

### k -> c before masculine plural i

```
common: otro[k->c]-i
```

``` python
op=RegexOp(r'k$', r'c', r'c$', r'k')
```

### feminine (a-stems)

```
nom: lip-a lip-e
gen: lip-e lip-/
dat: lip-i lip-am
acc: lip-o lip-e
loc: lip-i lip-ah
ins: lip-o lip-ami
dual: lip-i lip-ama
```

### feminine (i-stems)

```
nom: stvar-/ stvar-i
gen: stvar-i stvar-i
dat: stvar-i stvar-em
loc: stvar-i stvar-eh
ins: stvar-jo stvar-mi
dual: stvar-i stvar-ema
```

### neuter

```
nom: mest-o mest-a
gen: mest-a mest-/
dat: mest-u mest-om
loc: mest-u mest-ih
ins: mest-om mest-i
dual: mest-i mest-oma
```

### neuter n-stems

```
nom: im-e im-ena
gen: im-ena im-en
dat: im-enu im-enom
loc: im-enih
ins: im-enom im-eni
```

## verbs
* Slovenian has dual forms (delava, delata) alongside singular and plural
* adverbial participles (delajoč, govoreč) are literary and excluded (parenthesized)

### -ati verbs

```
infinitive: del-ati
supine:     del-at
N:          del-anje
adv part:   (del-ajoč)
past part:  del-al del-ala del-alo del-ali del-ale
pass part:  del-an del-ana del-ano del-ani del-ane
indicative, present: del-am del-aš del-a del-amo del-ate del-ajo
dual:       del-ava del-ata
imperative: del-aj del-ajmo del-ajte del-ajva del-ajta
```

### -iti verbs

```
infinitive: govor-iti
supine:     govor-it
N:          govor-jenje
adv part:   (govor-eč)
past part:  govor-il govor-ila govor-ilo govor-ili govor-ile
pass part:  govor-jen govor-jena govor-jeno govor-jeni govor-jene
indicative, present: govor-im govor-iš govor-i govor-imo govor-ite govor-ijo
dual:       govor-iva govor-ita
imperative: govor-i govor-imo govor-ite
```

### -eti verbs

```
infinitive: vid-eti
past part:  vid-el vid-ela vid-elo vid-eli vid-ele
```

### -niti verbs

```
infinitive: dvig-niti
past part:  dvig-nil dvig-nila dvig-nilo dvig-nili dvig-nile
pass part:  dvig-njen dvig-njena dvig-njeno dvig-njeni dvig-njene
indicative, present: dvig-nem dvig-neš dvig-ne dvig-nemo dvig-nete dvig-nejo
dual:       dvig-neva dvig-neta
imperative: dvig-ni dvig-nimo dvig-nite
```

### -ovati verbs

```
infinitive: kup-ovati
N:          kup-ovanje
past part:  kup-oval kup-ovala kup-ovalo kup-ovali kup-ovale
pass part:  kup-ovan kup-ovana kup-ovano kup-ovani kup-ovane
indicative, present: kup-ujem kup-uješ kup-uje kup-ujemo kup-ujete kup-ujejo
dual:       kup-ujeva kup-ujeta
imperative: kup-uj kup-ujmo kup-ujte
```

## derivation

```
V>N:   uči-telj uči-telja uči-telju uči-teljem uči-telji uči-teljev
V>ADJ: razum-ljiv razum-ljiva razum-ljivo razum-ljivi razum-ljive
ADJ>N: hitr-ost hitr-osti hitr-ostjo hitr-ostih hitr-ostmi
N>ADJ: sloven-ski sloven-ska sloven-sko sloven-ske sloven-skega sloven-skemu sloven-skem sloven-skim sloven-skih sloven-skimi
N>N:   učitelj-ica učitelj-ice učitelj-ici učitelj-ico učitelj-icam učitelj-icah učitelj-icami
```

## interfixes (compounds): 

```
common: vod-o(-vod) zob-o(-zdravnik)
```
