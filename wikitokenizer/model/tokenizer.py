# -*- coding: utf-8 -*-
from .spacy_base import SpacyBase


class Tokenizer(SpacyBase):

    def get_model(self, language):
        nlp = self.get_spacy_nlp(language)
        self.tokenizer = nlp.tokenizer

    def __call__(self, *args, **kwargs):
        try:
            return self.tokenizer(*args, **kwargs)
        except Exception as error:
            in_string = args[0]
            if self.language == 'ja' and self.size_in_bits(in_string) > 49149:
                tokens = in_string.split()
                n_tokens = int(len(tokens) / 2)

                first_half = list(self(' '.join(tokens[:n_tokens])))
                second_half = list(self(' '.join(tokens[n_tokens:])))

                # Reinitialise Japanese tokenizer to avoid memory leak issue
                self.get_model(self.language)
                return first_half + second_half

            raise error

    @staticmethod
    def size_in_bits(string):
        return len(string.encode('utf-8'))
