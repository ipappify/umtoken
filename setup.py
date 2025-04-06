from setuptools import setup

setup(
    name='umtoken',
    version='1.0.0',    
    description='Unimorph Tokenizer (umtoken) is a tokenizer that decomposes words into vocabulary and property ids.',
    url='https://github.com/ipappify/umtoken',
    author='Thomas Eißfeller',
    author_email='t.eissfeller@ipappify.de',
    license='MIT',
    packages=['umtoken'],
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
    ],
)