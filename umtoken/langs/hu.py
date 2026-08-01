# Path: umtoken/langs/hu.py

from umtoken.rules import RegexOp
from umtoken.langs.utils import DEFAULT_RULES, suffix_rules, interfix_rules

_lang = 'hu'

HU_RULES = (DEFAULT_RULES + 
            suffix_rules(_lang, ['e','ebb','ebbek','ebben','ebbet','ed','eget','ei','eid','eik','eim','eink','eitek','ek','ekbe','ekben','ekből','eken','eket','ekhez','ekig','ekkel','ekké','ekként','eknek','eknél','ekre','ekről','ektől','eké','ekéi','ekért','el','em','en','endő','es','et','etek','ett'], constraint_regex='[^e]$') +
            suffix_rules(_lang, ['sz','szer','szor','ször','ság','ságok','ságot','ség','ségek','séget'], constraint_regex='([^es]|ee)$') +
            suffix_rules(_lang, ['a','abb','abbak','abban','abbat','ad','ai','aid','aik','aim','aink','aitok','ak','akat','akba','akban','akból','akhoz','akig','akkal','akká','akként','aknak','aknál','akon','akra','akról','aktól','aké','akéi','akért','alak','am','an','ana','anak','andó','ani','ania','aniuk','anod','anom','anotok','anunk','aná','anád','anál','anám','anának','anánk','anátok','anék','as','at','atok','ba','ban','be','ben','ból','ből','gat','hat','hatja','hatnak','hatod','hatok','hatom','hatott','hattok','hatunk','het','heted','hetek','hetem','hetett','heti','hetnek','hettek','hetünk','hez','hoz','höz','i','ig','ik','itek','j','janak','jatok','jenek','jetek','jon','junk','jön','jük','jünk','k','kat','kban','kben','kból','kből','ket','khoz','khöz','kkal','kkel','knak','knek','kon','król','kről','któl','ktől','ként','kért','kön','lek','nak','ne','ned','nek','nem','netek','ni','nie','niük','nál','né','néd','nék','nél','ném','nének','nénk','nétek','nöd','nöm','nötök','nünk','obb','od','ok','okat','okba','okban','okból','okhoz','okig','okkal','okká','okként','oknak','oknál','okon','okra','okról','októl','oké','okéi','okért','ol','om','on','os','ot','otok','ott','otta','ottad','ottak','ottalak','ottam','ottatok','ottuk','ottunk','ották','ottál','ottátok','ra','re','ról','ről','t','te','ted','tek','telek','tem','tet','tetek','ték','tél','tétek','tól','tök','tük','tünk','től','uk','ul','unk','va','val','ve','vel','vá','ván','vé','vén','ák','ás','ások','ásokat','ást','átok','é','éi','ért','és','ések','éseket','ést','ó','ök','ökbe','ökben','ökből','öket','ökhöz','ökig','ökkel','ökké','ökként','öknek','öknél','ökre','ökről','öktől','öké','ökéi','ökért','ökön','öm','ön','ös','öt','ött','ük','ül','ünk','ő']) +
            suffix_rules(_lang, ['abb','abban','ebb','ebben','obb'], op=RegexOp(r'^', r'leg', r'^leg', r'')) +
            suffix_rules(_lang, ['al','el','á','é'], op=RegexOp(r'([bdfgjklmnprstvz])(y?)$', r'\1\1\2', r'([bdfgjklmnprstvz])\1(y?)$', r'\1\2')) +
            [])
