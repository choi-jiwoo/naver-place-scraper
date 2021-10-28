from setuptools import setup, find_packages


DESCRIPTION = ('snstextscraper scrapes text data about the store/company from '
               'social network services.')

setup(
    name='snstextscraper',
    version='0.0.1',
    author='Choi Jiwoo',
    author_email='cho2wldn@gmail.com',
    description=DESCRIPTION,
    packages=find_packages(),
    keywords=['python', 'sns', 'scraper', 'crawler'],
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Education',
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)
