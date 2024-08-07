from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='wikitokenizer',
      version='0.1',
      description='Repository used to download wikipedia articles and tokenize them using spaCy.',
      long_description=readme(),
      keywords='wikipedia tokenizer nlp',
      url='https://github.com/tpimentelms/wiki-tokenizer',
      author='Tiago Pimentel',
      author_email='tpimentelms@gmail.com',
      license='MIT',
      packages=['wikitokenizer', 'wikitokenizer.model'],
      entry_points={
          'console_scripts': [
              'tokenize_wiki_40b=wikitokenizer.tokenize_wiki_40b:main',
              'tokenize_wiki_file=wikitokenizer.tokenize_wiki_file:main',
          ],
      },
      install_requires=[
          'pymorphy2-dicts',
          'pythainlp',
          'pyvi',
          'mecab-python3',
          'tensorflow',
          'tensorflow_datasets<4.9',
          'apache-beam[gcp]',
          'spacy',
          'tqdm',
          'jieba',
          'pymorphy2',
          'sudachipy',
          'sudachidict_core',
      ],
      zip_safe=False)
