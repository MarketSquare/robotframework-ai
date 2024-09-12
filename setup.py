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

def get_requirements():
    with open("requirements.txt", "r") as file:
        return file.readlines()

setup(
    name="RobotFrameworkAI",
    version="0.0.2",
    classifiers=CLASSIFIERS,
    author="Stijn de Jong",
    author_email="stijndejong125@gmail.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    package_data={"": ["*.misc"]},
    python_requires=">=3.8",
    #install_requires=[get_requirements()],
)
