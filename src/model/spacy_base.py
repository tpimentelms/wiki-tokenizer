from abc import ABC, abstractmethod
import spacy


class SpacyBase(ABC):
    spacy_dict = {
        'no': 'nb',  # Norwegian (Bokmål) has a different code in spacy
    }

    def __init__(self, language, allow_multilingual=False):
        self.language = language
        self.allow_multilingual = allow_multilingual
        self.spacy_language = self.spacy_dict.get(language, language)
        self.get_model(self.spacy_language)

    def get_spacy_nlp(self, language):
        try:
            return spacy.blank(language)
        except ImportError:
            if self.allow_multilingual:
                return self.get_spacy_multilingual()
            else:
                error_msg = (
                    'Language code unavailable: %s. Use --allow-multilingual ' +
                    'argument to fallback to multilingual models.') % language
                raise ValueError(error_msg)

    @classmethod
    def get_spacy_multilingual(cls):
        # If language unavailable, use multilingual one
        print('Warning: Using multilingual spaCy sentencizer')
        return spacy.blank('xx')

    @abstractmethod
    def get_model(self, language):
        pass

    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass
