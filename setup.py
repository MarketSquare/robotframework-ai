from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='ai_interface',
    version='1.0.0',
    packages=find_packages(exclude=['atest', 'utest']),
    install_requires=requirements,
)
