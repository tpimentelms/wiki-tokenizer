from abc import ABC, abstractmethod
import spacy


class SpacyBase(ABC):
    spacy_dict = {
        'no': 'nb',  # Norwegian (Bokmål) has a different code in spacy
    }

    def __init__(self, language):
        self.language = language
        self.spacy_language = self.spacy_dict.get(language, language)
        self.get_model(self.spacy_language)

    @classmethod
    def get_spacy_nlp(cls, language):
        try:
            return spacy.blank(language)
        except ImportError:
            # If language unavailable, use multilingual one
            print('Warning: Using multilingual spaCy sentencizer')
            return spacy.blank('xx')

    @abstractmethod
    def get_model(self, language):
        pass

    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass
