from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="RobotFrameworkAI",
    version="0.0.2",
    author="Stijn de Jong",
    author_email="stijndejong125@gmail.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    package_data={"": ["*.misc"]},
    python_requires=">=3.7",
    install_requires=requirements,
)
