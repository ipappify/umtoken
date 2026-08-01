# Path: umtoken/langs/fi.py

from umtoken.rules import RegexOp
from umtoken.langs.utils import DEFAULT_RULES, suffix_rules, interfix_rules

_lang = 'fi'

FI_RULES = (DEFAULT_RULES + 
            suffix_rules(_lang, ['een'], constraint_regex='[^e]$') +
            suffix_rules(_lang, ['seen','seksi','sella','selle','sen','sena','sessa','sesta','set','si','sia','silla','sille','sissa','ssa','ssä','sta','sti','stä'], constraint_regex='([^es]|ee)$') +
            suffix_rules(_lang, ['a','an','da','dä','han','hön','i','ien','ihin','iin','iksi','illa','ille','illä','ilta','iltä','immalla','imman','immassa','immat','imme','impia','in','ina','inen','inä','isen','isi','isimme','isin','isit','isitte','isivat','isivät','isiä','issa','issä','ista','istä','it','ita','itte','ivat','iä','ja','jan','jat','jen','jia','jien','jä','jän','kaa','ksi','kää','la','lainen','laisen','laiset','laisia','leet','lla','lle','llinen','llisen','llisia','llista','llä','lta','ltä','lut','läinen','läisen','läiset','läisiä','maan','massa','masta','matta','minen','misen','misessa','mista','mistä','mmalla','mman','mmassa','mmat','mme','mpaa','mpi','mpia','mässä','mään','n','na','neet','nen','ni','nne','nsa','nsä','nut','nyt','nä','o','on','t','ta','taan','ton','tta','tte','ttiin','ttu','tty','tä','tään','tön','u','uden','uksia','un','us','utta','va','vat','vä','vät','y','yyden','yyksiä','yys','yyttä','ä','än']) +
            suffix_rules(_lang, ['ksi','lla','lle','llä','lta','n','ssa','ssä','sta','t'], op=RegexOp(r'([aeiouäöy])([kpt])\2([aouäöy])$', r'\1\2\3', r'([aeiouäöy])([kpt])([aouäöy])$', r'\1\2\2\3')) +
            suffix_rules(_lang, ['llä','n','ssa','t'], op=RegexOp(r't([aouäöy])$', r'd\1', r'd([aouäöy])$', r't\1')) +
            [])
