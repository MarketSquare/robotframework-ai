from setuptools import setup, find_packages

CLASSIFIERS = """
Development Status :: 3 - Alpha
License :: OSI Approved :: Apache Software License
Operating System :: OS Independent
Framework :: Robot Framework
Programming Language :: Python :: 3.8
Programming Language :: Python :: 3.9
Programming Language :: Python :: 3.10
Programming Language :: Python :: 3.11
Programming Language :: Python :: 3.12
""".strip().splitlines()


def get_long_description():
    with open("README.md", "r") as file:
        return file.read()

def get_requirements():
    with open("requirements.txt", "r") as file:
        return file.readlines()

setup(
    name="robotframework-ai",
    version="0.0.3",
    classifiers=CLASSIFIERS,
    author="Stijn de Jong",
    author_email="stijndejong125@gmail.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    package_data={"": ["*.misc"]},
    python_requires=">=3.8",
    #install_requires=[get_requirements()],
)
