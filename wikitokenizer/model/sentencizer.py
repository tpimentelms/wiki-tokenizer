# -*- coding: utf-8 -*-
from .spacy_base import SpacyBase


class Sentencizer(SpacyBase):
    MAX_LEN = 1000000

    def get_model(self, language):
        nlp = self.get_spacy_nlp(language)
        nlp.add_pipe('sentencizer')
        self.sentencizer = nlp

    def __call__(self, *args, **kwargs):
        return [x.text for x in self.sentencizer(*args, **kwargs).sents]
