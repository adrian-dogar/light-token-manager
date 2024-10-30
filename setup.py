from setuptools import setup, find_packages

setup(
    name='light_token_manager',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'requests>=2.32.3,<3',
        'certifi>=2024.8.30',
        'charset-normalizer>=3.4.0,<4',
        'idna>=3.10,<4',
        'urllib3>=2.2.3,<3'
    ],
    entry_points={
        'console_scripts': [
            'light-token-manager=light_token_manager.main:main',
        ],
    },
    author='Adrian Ruben Dogar',
    author_email='adrian.dogar@gmail.com',
    description='A simple slick script to generate a token, save it in a local file and reuse it until expires',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/adrian-dogar/light-token-manager',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)