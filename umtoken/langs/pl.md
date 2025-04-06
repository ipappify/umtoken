# Polish (pl)

## adjectives

### regular forms
nom: lw-i wielk-i drog-i duż-y
     lw-ia wielk-a drog-a duż-a
     lw-ie wielk-ie drog-ie duż-e 
     lw-i
     lw-ie wielk-ie drog-ie duż-e 
gen: lw-iego wielk-iego drog-iego duż-ego
     lw-iej wielk-iej drog-iej duż-ej
     lw-iego wielk-iego drog-iego duż-ego
     lw-ich wielk-ich drog-ich duż-ych
     lw-ich wielk-ich drog-ich duż-ych
dat: lw-iemu wielk-iemu drog-iemu duż-emu
     lw-iej wielk-iej drog-iej duż-ej
     lw-iemu wielk-iemu drog-iemu duż-emu
     lw-im wielk-im drog-im duż-ym
     lw-im wielk-im drog-im duż-ym
acc: lw-iego wielk-iego drog-iego duż-ego duż-y
     lw-ią wielk-ą drog-ą duż-ą
     lw-ie wielk-ie drog-ie duż-e
     lw-ich wielk-ich drog-ich duż-ych
     lw-ie wielk-ie drog-ie duż-e
ins: lw-im wielk-im drog-im duż-ym
     lw-ią wielk-ą drog-ą duż-ą
     lw-im wielk-im drog-im duż-ym
     lw-imi wielk-imi drog-imi duż-ymi
     lw-imi wielk-imi drog-imi duż-ymi
loc: lw-im wielk-im drog-im duż-ym
     lw-iej wielk-iej drog-iej duż-ej
     lw-im wielk-im drog-im duż-ym
     lw-ich wielk-ich drog-ich duż-ych
     lw-ich wielk-ich drog-ich duż-ych

### special cases of adjectives ending with ki
common: wiel[k->c]-y
``` python
op=RegexOp(r'k$', r'c', r'c$', r'k')
```

### special cases of adjectives ending with gi
common: dro[g->dz]-y
``` python
op=RegexOp(r'g$', r'dz', r'dz$', r'g')
```

### special cases of adjectives ending with ry
common: sta[r->rz]-y
``` python
op=RegexOp(r'r$', r'rz', r'rz$', r'r')
```

### special cases of adjectives ending with ży
common: du[ż->z]-i
``` python
op=RegexOp(r'ż$', r'z', r'z$', r'ż')
```

### special cases of adjectives ending with sny
common: żało[sn->śn]-i
``` python
op=RegexOp(r'sn$', r'śn', r'śn$', r'sn')
```

### special cases of adjectives ending with ty
common: popiela[t->c]-i
``` python
op=RegexOp(r't$', r'c', r'c$', r't')
```

### special cases of adjectives ending with ły
common: bia[ł->l]-i
``` python
op=RegexOp(r'ł$', r'l', r'l$', r'ł')
```

### adjective > adverb
common: szybk-o
        łagodn-ie

### adjective > adverb - special cases of adjectives ending with ry
common: dob[r->rz]-e
``` python
op=RegexOp(r'r$', r'rz', r'rz$', r'r')
```

## nouns
### f nouns: 
nom: skaz-a skaz-y
     skrob-ia skrob-ie
     chem-ia chem-ie
     długość-/ długośc-i
gen: skaz-y skaz-/
     skrob-ii skrob-ii
     chem-ii chem-ii
     wios-y wios-en
     długośc-i długośc-i
dat: skaz-ie skaz-om
     skrob-ii skrob-iom
     chem-ii chem-iom
     długośc-i długośc-iom
acc: skaz-ę skaz-y
     skrob-ię skrob-ie
     chem-ię chem-ie
     długość-/ długośc-i
ins: skaz-ą skaz-ami
     skrob-ią skrob-iami
     chem-ią chem-iami
     długośc-ią długośc-iami
loc: skaz-ie skaz-ach
     skrob-ii skrob-iach
     chem-ii chem-iach
     długośc-i długośc-iach
voc: skaz-o skaz-y
     skrob-io skrob-ie
     chem-io chem-ie
     długośc-i długośc-i

### m nouns:
nom: dom-/ dom-y
     gość-/ gośc-ie
gen: dom-u dom-ów
     gośc-ia gośc-i
dat: dom-owi dom-om
     gośc-iowi gośc-iom
acc: dom-/ dom-y
     gośc-ia gośc-i
ins: dom-em dom-ami
     gośc-iem gośc-mi
loc: dom-u dom-ie dom-ach
     gośc-iu gośc-iach
voc: dom-u dom-ie dom-y
     gośc-iu gośc-ie        

### n nouns:
nom: okn-o okn-a
     morz-e morz-a
gen: okn-a (ok-ien)
     morz-a (mórz-/)
dat: okn-u okn-om
     morz-u morz-om
acc: okn-o okn-a
     morz-e morz-a
ins: okn-em okn-ami
     morz-em morz-ami
loc: okn-ie okn-ach   
     morz-u morz-ach
voc: okn-o okn-a
     morz-e morz-a

## verbs

### -ać verbs
infinitive: koch-ać
ADV:        koch-ając
N:          koch-anie
PPA:        koch-ający koch-ająca koch-ające koch-ający koch-ające
PPP:        koch-any koch-ana koch-ane koch-ani koch-ane
indicative, present:   koch-am koch-asz koch-a koch-amy koch-acie koch-ają
indicative, imperfect: koch-ał koch-ała koch-ało koch-ali koch-ały
                       koch-ano
                       koch-ałem koch-ałam koch-ałom koch-aliśmy koch-ałyśmy
                       koch-ałeś koch-ałaś koch-ałoś koch-aliście koch-ałyście

### -ić verbs
infinitive: widz-ieć
            pal-ić
ADV:        widz-ąc
N:          widz-enie
PPA:        widz-ący widz-ąca widz-ące widz-ący widz-ące
PPP:        widz-iany widz-iana widz-iane widz-iani widz-iane
            pal-ony pal-ona pal-one pal-eni pal-one
indicative, present:   widz-ę widz-isz widz-i widz-imy widz-icie widz-ą
indicative, imperfect: widz-iał widz-iała widz-iało widz-ieli widz-iały
                       widz-iano
                       widz-iałem widz-iałam widz-iałom widz-ieliśmy widz-iałyśmy
                       widz-iałeś widz-iałaś widz-iałoś widz-ieliście widz-iałyście
                       pal-ił pal-iła pal-iło pal-ili pal-iły
                       pal-ono
                       pal-iłem pal-iłam pal-iłom pal-iliśmy pal-iłyśmy
                       pal-iłeś pal-iłaś pal-iłoś pal-iliście pal-iłyście

### -ować verbs
infinitive: mal-ować
ADV:        mal-ując
N:          mal-owanie
PPA:        mal-ujący mal-ująca mal-ujące mal-ujący mal-ujące
PPP:        mal-owany mal-owana mal-owane mal-owani mal-owane
indicative, present:   mal-uję mal-ujesz mal-uje mal-ujemy mal-ujecie mal-ują
indicative, imperfect: mal-ował mal-owała mal-owało mal-owali mal-owały
                       mal-owano
                       mal-owałem mal-owałam mal-owałom mal-owaliśmy mal-owałyśmy
                       mal-owałeś mal-owałaś mal-owałoś mal-owaliście mal-owałyście
