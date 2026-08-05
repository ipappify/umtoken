# Hungarian (hu)

## adjectives

### comparison

```
comparative: gyors-abb gyors-abbak gyors-abbat gyors-abban
             szép-ebb szép-ebbek szép-ebbet szép-ebben
             nagy-obb
adverbs:     gyors-an szép-en magyar-ul török-ül
```

### superlative (leg- prefix)

```
superlative: [->leg]gyors-abb [->leg]szép-ebb [->leg]nagy-obb
             [->leg]gyors-abban [->leg]szép-ebben
```

``` python
op=RegexOp(r'^', r'leg', r'^leg', r'')
```

## nouns
### front rounded harmony

```
nominative:      könyv-/         könyv-ek
accusative:      könyv-et        könyv-eket
dative:          könyv-nek       könyv-eknek
instrumental:    (könyv-vel)     könyv-ekkel
                 cső-vel
causal-final:    könyv-ért       könyv-ekért
translative:     (könyv-vé)      könyv-ekké
                 cső-vé
terminative:     könyv-ig        könyv-ekig
essive-formal:   könyv-ként      könyv-ekként
inessive:        könyv-ben       könyv-ekben
superessive:     könyv-ön        könyv-eken
adessive:        könyv-nél       könyv-eknél
illative:        könyv-be        könyv-ekbe
sublative:       könyv-re        könyv-ekre
allative:        könyv-höz       könyv-ekhez
elative:         könyv-ből       könyv-ekből
delative:        könyv-ről       könyv-ekről
ablative:        könyv-től       könyv-ektől
na poss sing:    könyv-é         könyv-eké
na poss plural:  könyv-éi        könyv-ekéi
poss 1st sing:   könyv-em        könyv-eim
poss 2nd sing:   könyv-ed        könyv-eid
poss 3rd sing:   könyv-e         könyv-ei
poss 1st plural: könyv-ünk       könyv-eink
poss 2nd plural: könyv-etek      könyv-eitek
poss 3rd plural: könyv-ük        könyv-eik
```

### front unrounded harmony

```
superessive:     dél-en
allative:        dél-hez
```

### back harmony

```
nominative:      ág-/       ág-ak
accusative:      ág-at      ág-akat
dative:          ág-nak     ág-aknak
instrumental:    (ág-gal)   ág-akkal
                 autó-val
causal-final:    ág-ért     ág-akért
translative:     (ág-gá)    ág-akká
                 autó-vá
terminative:     ág-ig      ág-akig
essive-formal:   ág-ként    ág-akként
inessive:        ág-ban     ág-akban
superessive:     ág-on      ág-akon
adessive:        ág-nál     ág-aknál
illative:        ág-ba      ág-akba
sublative:       ág-ra      ág-akra
allative:        ág-hoz     ág-akhoz
elative:         ág-ból     ág-akból
delative:        ág-ról     ág-akról
ablative:        ág-tól     ág-aktól
na poss sing:    ág-é       ág-aké
na poss plural:  ág-éi      ág-akéi
poss 1st sing:   ág-am      ág-aim
poss 2nd sing:   ág-ad      ág-aid
poss 3rd sing:   ág-a       ág-ai
poss 1st plural: ág-unk     ág-aink
poss 2nd plural: ág-atok    ág-aitok
poss 3rd plural: ág-uk      ág-aik
```

### back harmony (o linking)

```
nominative:      orvos-/     orvos-ok
accusative:      orvos-t     orvos-okat
                 bot-ot
dative:          orvos-nak   orvos-oknak
instrumental:    orvos-okkal
translative:     orvos-okká
causal-final:    orvos-okért
terminative:     orvos-okig
essive-formal:   orvos-okként
inessive:        orvos-okban
superessive:     orvos-okon
adessive:        orvos-oknál
illative:        orvos-okba
sublative:       orvos-okra
allative:        orvos-okhoz
elative:         orvos-okból
delative:        orvos-okról
ablative:        orvos-októl
na poss sing:    orvos-oké
na poss plural:  orvos-okéi
```

### front rounded harmony (ö linking)

```
nominative:      gyümölcs-/     gyümölcs-ök
accusative:      gyümölcs-öt    gyümölcs-öket
dative:          gyümölcs-öknek
instrumental:    gyümölcs-ökkel
translative:     gyümölcs-ökké
causal-final:    gyümölcs-ökért
terminative:     gyümölcs-ökig
essive-formal:   gyümölcs-ökként
inessive:        gyümölcs-ökben
superessive:     gyümölcs-ökön
adessive:        gyümölcs-öknél
illative:        gyümölcs-ökbe
sublative:       gyümölcs-ökre
allative:        gyümölcs-ökhöz
elative:         gyümölcs-ökből
delative:        gyümölcs-ökről
ablative:        gyümölcs-öktől
na poss sing:    gyümölcs-öké
na poss plural:  gyümölcs-ökéi
```

### vowel-final stems

```
nominative:      autó-k      cipő-k
accusative:      autó-t      autó-kat    cipő-ket
dative:          autó-knak   cipő-knek
instrumental:    autó-kkal   cipő-kkel
causal-final:    autó-kért
inessive:        autó-kban   cipő-kben
superessive:     autó-kon    cipő-kön
allative:        autó-khoz   cipő-khöz
elative:         autó-kból   cipő-kből
delative:        autó-król   cipő-kről
ablative:        autó-któl   cipő-ktől
```

### instrumental / translative singular
**TODO: are there any nouns that end with f or fy?**

```
instrumental:   köny[v->vv]-el
                ször[n->nn]y-el
                á[g->gg]-al
                ara[n->nn]y-al
translative:    köny[v->vv]-é
                ször[n->nn]y-é
                á[g->gg]-á
                ara[n->nn]y-á
```

``` python
op=RegexOp(r'([bdfgjklmnprstvz])(y?)$', r'\1\1\2', r'([bdfgjklmnprstvz])\1(y?)$', r'\1\2')
```

## verbs
### -ik
**TODO: duplicate consonant in present def: ját[s->ss]z - is this a common rule or an exception**

```
present indef:    játsz-om játsz-ol játsz-ik játsz-unk játsz-otok játsz-anak
                  játsz-ok
                  törőd-öm törőd-sz törőd-ik törőd-ünk törőd-tök törőd-nek
                  törőd-ök
                  érkez-em érkez-el érkez-ik érkez-ünk érkez-tek érkez-nek
                  érkez-ek
present def:      játsz-om játsz-od játssz-a játssz-uk játssz-átok játssz-ák
present 2nd obj:  játsz-alak
past indef:       játsz-ottam játsz-ottál játsz-ott játsz-ottunk játsz-ottatok játsz-ottak
                  törőd-tem törőd-tél törőd-ött törőd-tünk törőd-tetek törőd-tek
                  érkez-tem érkez-tél érkez-ett érkez-tünk érkez-tetek érkez-tek
past def:         játsz-ottam játsz-ottad játsz-otta játsz-ottuk játsz-ottátok játsz-ották
past 2nd obj:     játsz-ottalak
infinitive:       játsz-ani játsz-anom játsz-anod játsz-ania játsz-anunk játsz-anotok játsz-aniuk
                  törőd-ni törőd-nöm törőd-nöd törőd-nie törőd-nünk törőd-nötök törőd-niük
                  érkez-ni érkez-nem érkez-ned érkez-nie érkez-nünk érkez-netek érkez-niük
other forms:      játsz-ás játsz-ó játsz-ott játsz-andó játsz-va játsz-ván játsz-at
                  törőd-és törőd-ő törőd-ött törőd-ve törőd-vén
                  érkez-és érkez-ő érkez-ett érkez-ve érkez-vén érkez-tet
potential:        játsz-hat játsz-hatok játsz-hatom játsz-hatod játsz-hatja játsz-hatunk játsz-hattok játsz-hatnak játsz-hatott
cond indef:       játsz-anék játsz-anál játsz-ana játsz-anánk játsz-anátok játsz-anának
cond def:         játsz-anám játsz-anád játsz-aná
```

### non -ik

```
present indef:    szeret-ek  szeret-sz  szeret-/   szeret-ünk  szeret-tek   szeret-nek
present def:      szeret-em  szeret-ed  szeret-i   szeret-jük  szeret-itek  szeret-ik
present 2nd obj:  szeret-lek
past indef:       szeret-tem szeret-tél szeret-ett szeret-tünk szeret-tetek szeret-tek
past def:         szeret-tem szeret-ted szeret-te  szeret-tük  szeret-tétek szeret-ték
past 2nd obj:     szeret-telek
infinitive:       szeret-ni szeret-nem szeret-ned szeret-nie szeret-nünk szeret-netek szeret-niük
other forms:      szeret-és szeret-ő szeret-ett szeret-endő szeret-ve szeret-vén
potential:        szeret-het szeret-hetek szeret-hetem szeret-heted szeret-heti szeret-hetünk szeret-hettek szeret-hetnek szeret-hetett
cond indef:       szeret-nék szeret-nél szeret-ne szeret-nénk szeret-nétek szeret-nének
cond def:         szeret-ném szeret-néd szeret-né
```

### imperative
* sibilant-final stems assimilate (szeret -> szeress, játszik -> játssz) and are not covered
* the future tense (fog + infinitive) is analytic and needs no rules

```
common: törőd-j törőd-jön törőd-jünk törőd-jetek törőd-jenek
        mond-j mond-jon mond-junk mond-jatok mond-janak
```

## derivation

```
V>N:   olvas-ás olvas-ást olvas-ások olvas-ásokat
       érkez-és érkez-ést érkez-ések érkez-éseket
ADJ>N: szabad-ság szabad-ságot szabad-ságok
       szép-ség szép-séget szép-ségek
N>ADJ: hat-os ház-as kert-es gyümölcs-ös
       város-i
V>V:   olvas-gat néz-eget
NUM>ADV: hat-szor egy-szer öt-ször
```
