# Path: umtoken/langs/hu.py

from umtoken.rules import RegexOp
from umtoken.langs.utils import DEFAULT_RULES, suffix_rules, interfix_rules

_lang = 'hu'

HU_RULES = (DEFAULT_RULES + 
            suffix_rules(_lang, ['e','ed','ei','eid','eik','eim','eink','eitek','ek','ekbe','ekben','ekből','eken','eket','ekhez','ekig','ekkel','ekké','ekként','eknek','eknél','ekre','ekről','ektől','eké','ekéi','ekért','el','em','en','endő','et','etek','ett'], constraint_regex='[^e]$') +
            suffix_rules(_lang, ['sz'], constraint_regex='([^es]|ee)$') +
            suffix_rules(_lang, ['a','ad','ai','aid','aik','aim','aink','aitok','ak','akat','akba','akban','akból','akhoz','akig','akkal','akká','akként','aknak','aknál','akon','akra','akról','aktól','aké','akéi','akért','alak','am','anak','andó','ani','ania','aniuk','anod','anom','anotok','anunk','at','atok','ba','ban','be','ben','ból','ből','hez','hoz','höz','i','ig','ik','itek','jük','ként','lek','nak','ned','nek','nem','netek','ni','nie','niük','nál','nél','nöd','nöm','nötök','nünk','od','ok','ol','om','on','otok','ott','otta','ottad','ottak','ottalak','ottam','ottatok','ottuk','ottunk','ották','ottál','ottátok','ra','re','ról','ről','te','ted','tek','telek','tem','tet','tetek','ték','tél','tétek','tól','tök','tük','tünk','től','uk','unk','va','val','ve','vel','vá','ván','vé','vén','ák','ás','átok','é','éi','ért','és','ó','ök','öm','ön','ött','ük','ünk','ő']) +
            suffix_rules(_lang, ['al','el','á','é'], op=RegexOp(r'([bdfgjklmnprstvz])(y?)$', r'\1\1\2', r'([bdfgjklmnprstvz])\1(y?)$', r'\1\2')) +
            [])
