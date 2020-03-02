import spacy


class Sentencizer:

    def __init__(self, language):
        self.language = language
        self.sentencizer = self.get_sentencizer(language)

    @classmethod
    def get_sentencizer(cls, language):
        nlp = spacy.blank(language)
        # spacy_tokenizer = nlp.Defaults.create_tokenizer(nlp)
        nlp.add_pipe(nlp.create_pipe('sentencizer'))
        return nlp

    def __call__(self, *args, **kwargs):
        return [x.text for x in self.sentencizer(*args, **kwargs).sents]
