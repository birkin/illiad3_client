from setuptools import setup, find_packages

setup(name='illiad3',
    version='0.11',
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
    ],
)
