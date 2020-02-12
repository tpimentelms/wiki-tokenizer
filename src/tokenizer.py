import spacy
from spacy.lang.de import German
from spacy.lang.el import Greek
from spacy.lang.en import English
from spacy.lang.es import Spanish
from spacy.lang.fr import French
from spacy.lang.it import Italian
# from spacy.lang.lt import Lithuanian
from spacy.lang.nb import Norwegian
from spacy.lang.nl import Dutch
from spacy.lang.pt import Portuguese
from spacy.lang.xx import MultiLanguage
# from spacy.lang.af import Afrikaans
from spacy.lang.ar import Arabic
# from spacy.lang.bg import Bulgarian
from spacy.lang.bn import Bengali
# from spacy.lang.ca import Catalan
# from spacy.lang.cs import Czech
from spacy.lang.da import Danish
# from spacy.lang.et import Estonian
from spacy.lang.fa import Persian
from spacy.lang.fi import Finnish
from spacy.lang.ga import Irish
from spacy.lang.he import Hebrew
# from spacy.lang.hi import Hindi
from spacy.lang.hr import Croatian
from spacy.lang.hu import Hungarian
from spacy.lang.id import Indonesian
# from spacy.lang.is import Icelandic
from spacy.lang.ja import Japanese
# from spacy.lang.kn import Kannada
# from spacy.lang.ko import Korean
# from spacy.lang.lb import Luxembourgish
from spacy.lang.lv import Latvian
from spacy.lang.mr import Marathi
from spacy.lang.pl import Polish
from spacy.lang.ro import Romanian
from spacy.lang.ru import Russian
from spacy.lang.si import Sinhala
from spacy.lang.sk import Slovak
from spacy.lang.sl import Slovenian
from spacy.lang.sq import Albanian
from spacy.lang.sr import Serbian
from spacy.lang.sv import Swedish
from spacy.lang.ta import Tamil
from spacy.lang.te import Telugu
from spacy.lang.th import Thai
from spacy.lang.tl import Tagalog
from spacy.lang.tr import Turkish
from spacy.lang.tt import Tatar
from spacy.lang.uk import Ukrainian
from spacy.lang.ur import Urdu
from spacy.lang.vi import Vietnamese
from spacy.lang.zh import Chinese


class Tokenizer:
    # lang2model = {
    #     'de': German,
    #     'el': Greek,
    #     'en': English,
    #     'es': Spanish,
    #     'fr': French,
    #     'it': Italian,
    #     'lt': Lithuanian,
    #     'nb': Norwegian,
    #     'nl': Dutch,
    #     'pt': Portuguese,
    #     'xx': Multi,
    #     'af': Afrikaans,
    #     'ar': Arabic,
    #     'bg': Bulgarian,
    #     'bn': Bengali,
    #     'ca': Catalan,
    #     'cs': Czech,
    #     'da': Danish,
    #     'et': Estonian,
    #     'fa': Persian,
    #     'fi': Finnish,
    #     'ga': Irish,
    #     'he': Hebrew,
    #     'hi': Hindi,
    #     'hr': Croatian,
    #     'hu': Hungarian,
    #     'id': Indonesian,
    #     'is': Icelandic,
    #     'ja': Japanese,
    #     'kn': Kannada,
    #     'ko': Korean,
    #     'lb': Luxembourgish,
    #     'lv': Latvian,
    #     'mr': Marathi,
    #     'pl': Polish,
    #     'ro': Romanian,
    #     'ru': Russian,
    #     'si': Sinhala,
    #     'sk': Slovak,
    #     'sl': Slovenian,
    #     'sq': Albanian,
    #     'sr': Serbian,
    #     'sv': Swedish,
    #     'ta': Tamil,
    #     'te': Telugu,
    #     'th': Thai,
    #     'tl': Tagalog,
    #     'tr': Turkish,
    #     'tt': Tatar,
    #     'uk': Ukrainian,
    #     'ur': Urdu,
    #     'vi': Vietnamese,
    #     'zh': Chinese,
    # }

    def __init__(self, language):
        self.language = language
        self.tokenizer = self.get_tokenizer(language)

    @classmethod
    def get_tokenizer(cls, language):
        # model = cls.lang2model[language]
        # nlp = model()
        nlp = spacy.blank(language)
        spacy_tokenizer = nlp.Defaults.create_tokenizer(nlp)
        return spacy_tokenizer

    def __call__(self, *args, **kwargs):
        return self.tokenizer(*args, **kwargs)