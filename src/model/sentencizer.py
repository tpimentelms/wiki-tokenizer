import spacy


class Sentencizer:
    spacy_dict = {
        'no': 'nb',  # Norwegian (Bokmål) has a different code in spacy
    }

    def __init__(self, language):
        self.language = language
        self.spacy_language = self.spacy_dict.get(language, language)
        self.sentencizer = self.get_sentencizer(self.spacy_language)

    @classmethod
    def get_spacy_nlp(cls, language):
        try:
            return spacy.blank(language)
        except ImportError:
            # If language unavailable, use multilingual one
            print('Warning: Using multilingual spaCy sentencizer')
            return spacy.blank('xx')

    @classmethod
    def get_sentencizer(cls, language):
        nlp = cls.get_spacy_nlp(language)
        nlp.add_pipe(nlp.create_pipe('sentencizer'))
        return nlp

    def __call__(self, *args, **kwargs):
        return [x.text for x in self.sentencizer(*args, **kwargs).sents]
