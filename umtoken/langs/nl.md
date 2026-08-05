# Dutch (nl)

## adjectives

```
common: klein-/ klein-e klein-s
comparative: klein-er klein-ere
superlative: klein-st klein-ste
```

## nouns

```
common: deur-en
        tant-e tant-es
        bod-e bod-en
        akker-s
        ree-ën
        blad-eren
```

### diminutives

```
common: huis-je huis-jes
        tafel-tje tafel-tjes
        mann-etje mann-etjes
        boom-pje boom-pjes
```

## verbs
* strong-verb imperfect forms (verdween, verdwenen) are formed by ablaut and not covered

```
infinitive: verdel-en
            verwerk-en
            verdwijn-en
past part:  verdeel-d verdeel-de (verdeel-ds)
            verwerk-t verwerk-te (verwerk-ts)
            verdwen-en verdwen-ene verdwen-ens
indicative, present:   verdeel-t
                       verwerk-t verwerk-en
                       verdwijn-t verdwijn-en
indicative, imperfect: verdeel-de verdeel-den
                       verwerk-te verwerk-ten
```

### long-vowel stems (vowel doubling before consonant-initial suffixes)

```
indicative, present:   verd[el->eel]-t
indicative, imperfect: verd[el->eel]-de verd[el->eel]-den
past part:             verd[el->eel]-d verd[el->eel]-de
```

``` python
op=RegexOp(r'([aeou])([bcdfgklmnprst])$', r'\1\1\2', r'([aeou])\1([bcdfgklmnprst])$', r'\1\2')
```

### ppp with ge- prefix

```
past part:  [->ge]deel-d [->ge]deel-de ([->ge]deel-ds)
            [->ge]werk-t [->ge]werk-te ([->ge]werk-ts)
            [->ge]zi-en [->ge]zi-ene [->ge]zi-ens
```

``` python
op=RegexOp(r'^', r'ge', r'^ge', r'')
```

## derivation

```
V>N:   verwerk-ing verwerk-ingen
       werk-er werk-ers
V>ADJ: werk-baar werk-bare
ADJ>N: snel-heid snel-heden
```

## interfixes (compounds): 

```
common: deur-en(-knop)
        akker-s(-bouw)
        ree-ën(-poot)
        blad-eren(-dak)
        ei-er(-schaal)
        bod-e(-dienst)
        gemeent-e(-huis)
```
