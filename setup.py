"""Installation script for dragonfly_grammars."""
from setuptools import setup, find_packages

setup(
    name='dragonfly_grammars',
    version='1.0',
    description='language aware dragonfly grammars',
    author='nihlaeth',
    author_email='info@nihlaeth.nl',
    python_requires='>=2.7,<3',
    packages=find_packages(),
    install_requires=[
        # 'dragonfly>=0.6.6',
        'dragonfly',
        'babel',
        'pathlib2',
        'simple-crypt'],
    entry_points={
        'console_scripts': [
            'speechpass = speechpass:encrypt_password']},
    package_data={'dragonfly_grammars': ['translations/*']},
    message_extractors={'dragonfly_grammars': [("**.py", 'python', None)]})
