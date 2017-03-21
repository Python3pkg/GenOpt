from distutils.core import setup
setup(
    name = 'GenOpt',
    packages = ['GenOpt'], # this must be the same as the name above
    version = '1.0.0',
    description = 'Contains a class for optimizing analytic functions utilizing a genetic algorithm.',
    author = 'Kevin Lioi',
    author_email = 'kevin.a.lioi@gmail.com',
    url = 'https://github.com/kevinlioi/GenOpt', # use the URL to the github repo
    download_url = 'https://github.com/kevinlioi/GenOpt/archive/1.0.0.tar.gz', # I'll explain this in a second
    install_requires=[
        'numpy',
        'random',
        'heapq',
        'itertools'
    ],
    keywords = ['genetic', 'optimization', 'algorithm'], # arbitrary keywords
    classifiers = [],
)