from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='RobotFrameworkAI',
    version='0.0.1',
    author="Stijn de Jong",
    author_email="stijndejong125@gmail.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    # install_requires=requirements,
)
