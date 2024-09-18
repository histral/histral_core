from setuptools import setup, find_packages


# Read the requirements from the requirements.txt file
with open('requirements.txt') as f:
    required = f.read().splitlines()


setup(
    name='histral_core',  
    version='0.1',
    packages=find_packages(),
    install_requires=required,  
    description='Set of modules used in various Histral repositories.',
    author='Aditya Motale',
    url='https://github.com/histral/histral_core',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache-2.0 license',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)
