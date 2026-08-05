import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='umtoken',
    version='1.0.0',
    description='Unimorph Tokenizer (umtoken) is a tokenizer that decomposes words into vocabulary and property ids.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ipappify/umtoken',
    author='Thomas Eißfeller',
    author_email='t.eissfeller@ipappify.de',
    license='MIT',
    # umtoken.langs holds the morphological rules for all 24 languages -- listing
    # only 'umtoken' shipped a tokenizer without any rules. _staging is unfinished
    # rule work and is deliberately left out.
    packages=find_packages(include=['umtoken', 'umtoken.*'],
                           exclude=['umtoken.langs._staging', 'umtoken.langs._staging.*']),
    package_data={'umtoken.langs': ['*.md']},
    python_requires='>=3.9',
    install_requires=[
        'marisa-trie>=0.8.0',
        'numpy>=1.19.5',
        'regex>=2023.6.3',
        'tqdm>=4.66.1',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Text Processing :: Linguistic',
    ],
)
