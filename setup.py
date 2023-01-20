# pylint: disable=missing-module-docstring
import setuptools

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="luxtronik",
    version="0.0.0-dev",
    author="Bouni",
    author_email="bouni@owee.de",
    description="A luxtronik heatpump controller interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bouni/python-luxtronik",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
