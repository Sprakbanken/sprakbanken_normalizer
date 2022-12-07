import setuptools

if __name__ == "__main__":
    setuptools.setup(
        name="sprakbanken_normalizer",
        version="0.1.0",
        author="Per Erik Solberg",
        author_email="sprakbanken@nb.no",
        description="Norwegian ASR text normalization",
        license="Apache 2.0",
        url="https://github.com/Sprakbanken/sprakbanken_normalizer",
        requires=["pyparsing"],
        packages=setuptools.find_packages(),
    )
