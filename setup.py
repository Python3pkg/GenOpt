from distutils.core import setup
setup(
    name = 'GenOpt',
    py_modules = ['GenOpt'],
    version = '1.0.2',
    description = 'Contains a class for optimizing analytic functions utilizing a genetic algorithm.',
    author = 'Kevin Lioi',
    author_email = 'kevin.a.lioi@gmail.com',
    url = 'https://github.com/kevinlioi/GenOpt', 
    install_requires=[
        'numpy',
        'random',
        'heapq',
        'itertools'
    ],
    download_url = 'https://github.com/kevinlioi/GenOpt/archive/1.0.0.tar.gz',
    keywords = ['genetic', 'optimization', 'algorithm'],
    classifiers = [],
)