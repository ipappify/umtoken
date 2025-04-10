# German (de)

## adjectives
common: gut-e gut-em gut-en gut-er gut-es

## nouns
f nouns: Blum-e Blum-en
m nouns: Tag-/ Tag-s Tag-es Tag-e Tag-en
n nouns: Bild-/ Bild-s Bild-es Bild-er Bild-ern
         Leb-en Leb-ens

### nouns ending with -in
f nouns: Lehrerin-/ Lehrerin-nen
``` python
constraint_regex='in$'
```
 
## verbs
### verbs ending with b f g h k l m n p r s x z ß au eu ei
past part:  besag-t besag-te besag-tem besag-ten besag-ter besag-tes
indicative, present:   sag-e sag-st sag-t sag-en sag-t sag-en
indicative, imperfect: sag-te (sag-test) sag-tet sag-ten sag-tet sag-ten
``` python
constraint_regex='([bfghklmnprsxzß]|au|eu|ei)$'
```
 
### verbs ending with ending with d t or ending with b d f h k g followed by m n
past part:  bedeut-et bedeut-ete bedeut-etem bedeut-eten bedeut-eter bedeut-etes
indicative, present:   bedeut-e bedeut-est bedeut-et bedeut-en bedeut-et bedeut-en
indicative, imperfect: bedeut-ete (bedeut-etest) bedeut-ete bedeut-eten bedeut-etet bedeut-eten
``` python
constraint_regex='([dt]|[bdfhkg][mn])$'
```

### verbs ending with el er
infinitive: krizel-n
``` python
constraint_regex='e[lr]$'
```

### strong verbs
past part:  vergeb-en vergeb-ene vergeb-enem vergeb-enen vergeb-ener vergeb-enes

### ppp with ge- prefix
past part:  [->ge]sag-t [->ge]sag-te [->ge]sag-tem [->ge]sag-ten [->ge]sag-ter [->ge]sag-tes
            [->ge]deut-et [->ge]deut-ete [->ge]deut-etem [->ge]deut-eten [->ge]deut-eter [->ge]deut-etes
            [->ge]geb-en [->ge]geb-ene [->ge]geb-enem [->ge]geb-enen [->ge]geb-ener [->ge]geb-enes
``` python
op=RegexOp(r'^', r'ge', r'^ge', r'')
```

### verb > noun
common: bedeut-ung bedeut-ungen
``` python
constraint_regex='[^ea]$'
```

## interfixes (compounds): 
common: Bind-e(-glied) Bild-er(-buch) Blum-en(-strauß) 
        Leb-ens(-mittel) Tag-es(-geschäft) Aktivität-s(-diagramm)

### verb > noun
common: Tag-ungs(-hotel)
``` python
constraint_regex='[^ea]$'
```