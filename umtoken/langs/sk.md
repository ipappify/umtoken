# Slovak (sk)

## adjectives

### hard declension

```
nom: pekn-ý pekn-á pekn-é pekn-í pekn-é
gen: pekn-ého pekn-ej pekn-ých
dat: pekn-ému pekn-ej pekn-ým
acc: pekn-ého pekn-ý pekn-ú pekn-é
loc: pekn-om pekn-ej pekn-ých
ins: pekn-ým pekn-ou pekn-ými
```

### hard declension (short forms per the rhythmic law)

```
nom: krásn-y krásn-a krásn-e krásn-i krásn-e
gen: krásn-eho krásn-ej krásn-ych
dat: krásn-emu krásn-ej krásn-ym
acc: krásn-eho krásn-y krásn-u krásn-e
loc: krásn-om krásn-ej krásn-ych
ins: krásn-ym krásn-ou krásn-ymi
```

### soft declension

```
nom: cudz-í cudz-ia cudz-ie
gen: cudz-ieho cudz-ej cudz-ích
dat: cudz-iemu cudz-ej cudz-ím
acc: cudz-ieho cudz-í cudz-iu cudz-ie
loc: cudz-om cudz-ej cudz-ích
ins: cudz-ím cudz-ou cudz-ími
```

### comparison

```
comparative: star-ší star-šia star-šie star-šieho star-šiemu star-šej star-šiu star-šou star-šom star-ších star-ším star-šími
             rýchl-ejší rýchl-ejšia rýchl-ejšie
adverbs:     rýchl-ejšie
```

### superlative (naj- prefix)

```
superlative: [->naj]star-ší [->naj]star-šia [->naj]star-šie
             [->naj]rýchl-ejší [->naj]rýchl-ejšia [->naj]rýchl-ejšie
```

``` python
op=RegexOp(r'^', r'naj', r'^naj', r'')
```

### possessive (-ov, -in)

```
common: otc-ov otc-ova otc-ovo otc-ovi otc-ove otc-ovho otc-ovmu otc-ovom otc-ovým otc-ovej otc-ovu otc-ovou otc-ových otc-ovými
        matk-in matk-ina matk-ino matk-ini matk-ine matk-inho matk-inmu matk-inom matk-iným matk-inej matk-inu matk-inou matk-iných matk-inými
```

### adjective > adverb

```
common: pekn-e rýchl-o
```

## nouns

### masculine animate

```
nom: chlap-/ chlap-i hrdin-a hrdin-ovia
gen: chlap-a chlap-ov hrdin-u hrdin-ov
dat: chlap-ovi chlap-om hrdin-ovi hrdin-om
acc: chlap-a chlap-ov hrdin-u hrdin-ov
loc: chlap-ovi chlap-och hrdin-ovi hrdin-och
ins: chlap-om chlap-mi hrdin-om hrdin-ami
```

### masculine inanimate

```
nom: dub-/ dub-y stroj-/ stroj-e
gen: dub-a dub-ov stroj-a stroj-ov
dat: dub-u dub-om stroj-u stroj-om
acc: dub-/ dub-y stroj-/ stroj-e
loc: dub-e dub-och stroj-i stroj-och
ins: dub-om dub-mi stroj-om stroj-mi
```

### k -> c before masculine personal plural i

```
common: voja[k->c]-i
```

``` python
op=RegexOp(r'k$', r'c', r'c$', r'k')
```

### ch -> s before masculine personal plural i

```
common: mní[ch->s]-i
```

``` python
op=RegexOp(r'ch$', r's', r's$', r'ch')
```

### feminine

```
nom: žen-a žen-y ulic-a ulic-e dlaň-/ dlan-e kosť-/ kost-i
gen: žen-y žien-/ ulic-e ulíc-/ dlan-e dlan-í kost-i kost-í
dat: žen-e žen-ám ulic-i ulic-iam dlan-i dlan-iam kost-i kost-iam
acc: žen-u žen-y ulic-u ulic-e dlaň-/ dlan-e kosť-/ kost-i
loc: žen-e žen-ách ulic-i ulic-iach dlan-i dlan-iach kost-i kost-iach
ins: žen-ou žen-ami ulic-ou ulic-ami dlaň-ou dlaň-ami kosť-ou kosť-ami
```

### neuter

```
nom: mest-o mest-á srdc-e srdc-ia vysvedčen-ie vysvedčen-ia
gen: mest-a miest-/ srdc-a sŕdc-/ vysvedčen-ia vysvedčen-í
dat: mest-u mest-ám srdc-u srdc-iam vysvedčen-iu vysvedčen-iam
loc: mest-e mest-ách srdc-i srdc-iach vysvedčen-í vysvedčen-iach
ins: mest-om mest-ami srdc-om srdc-ami vysvedčen-ím vysvedčen-iami
```

### neuter t-stems

```
nom: dievč-a dievč-atá
gen: dievč-aťa dievč-at
dat: dievč-aťu dievč-atám
loc: dievč-ati dievč-atách
ins: dievč-aťom dievč-atami
```

## verbs
* transgressives are literary in modern Slovak and excluded (parenthesized)
* strong verbs (niesť - niesol) form past stems by ablaut and are not covered

### -ať verbs (á-type)

```
infinitive: chyt-ať
N:          chyt-anie
act part:   chyt-ajúci
transgressive: (chyt-ajúc)
past part:  chyt-al chyt-ala chyt-alo chyt-ali
pass part:  chyt-aný chyt-aná chyt-ané chyt-aní
indicative, present: chyt-ám chyt-áš chyt-á chyt-áme chyt-áte chyt-ajú
                     čít-am čít-aš čít-a čít-ame čít-ate čít-ajú
imperative: chyt-aj chyt-ajme chyt-ajte
```

### -ieť verbs (ie-type)

```
infinitive: rozum-ieť vid-ieť
past part:  rozum-el rozum-ela rozum-elo rozum-eli
            vid-el vid-ela vid-elo vid-eli
indicative, present: rozum-iem rozum-ieš rozum-ie rozum-ieme rozum-iete rozum-ejú
```

### -iť verbs (í-type)

```
infinitive: rob-iť
N:          rob-enie
act part:   rob-iaci
transgressive: (rob-iac)
past part:  rob-il rob-ila rob-ilo rob-ili
pass part:  rob-ený rob-ená rob-ené rob-ení
indicative, present: rob-ím rob-íš rob-í rob-íme rob-íte rob-ia
                     chvál-im chvál-iš chvál-i chvál-ime chvál-ite chvál-ia
```

### -núť verbs

```
infinitive: pad-núť min-úť
N:          min-utie
past part:  pad-ol pad-la pad-lo pad-li
            min-ul min-ula min-ulo min-uli
pass part:  min-utý min-utá min-uté
indicative, present: pad-nem pad-neš pad-ne pad-neme pad-nete pad-nú
imperative: pad-ni pad-nime pad-nite
```

### -ovať verbs

```
infinitive: prac-ovať
N:          prac-ovanie
act part:   prac-ujúci
transgressive: (prac-ujúc)
past part:  prac-oval prac-ovala prac-ovalo prac-ovali
pass part:  prac-ovaný prac-ovaná prac-ované prac-ovaní
indicative, present: prac-ujem prac-uješ prac-uje prac-ujeme prac-ujete prac-ujú
imperative: prac-uj prac-ujme prac-ujte
```

## derivation

```
V>N:   uči-teľ uči-teľa uči-teľovi uči-teľom uči-telia uči-teľov
V>ADJ: použi-teľný použi-teľná použi-teľné
ADJ>N: rýchl-osť rýchl-osti rýchl-osťou rýchl-ostí rýchl-ostiam rýchl-ostiach rýchl-osťami
N>ADJ: motor-ový motor-ová motor-ové motor-ového motor-ovému motor-ovom
       mest-ský mest-ská mest-ské mest-ského mest-skému mest-skom mest-skou mest-skú mest-skí mest-ských mest-ským mest-skými
N>N:   učiteľ-ka učiteľ-ky učiteľ-ke učiteľ-ku učiteľ-kou učiteľ-kám učiteľ-kách učiteľ-kami
```

## interfixes (compounds): 

```
common: vod-o(-pád) zem-e(-guľa)
```
