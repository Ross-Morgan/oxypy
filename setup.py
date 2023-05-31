from distutils.core import setup

AUTHOR = "Ross Mogan"
AUTHOR_EMAIL = "rmorgan512@protonmail.ch"
DESC = "Fully-featured implementation of Rusts `Option` and `Result` in Python"
URL = "https://github.com/Ross-Morgan/oxypy/archive/refs/tags/v0.0.1.tar.gz"

setup(
    name="oxypy",
    packages=["oxypy"],
    version="0.0.1",
    license="MIT",
    description=DESC,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url="https://www.github.com/Ross-Morgan/oxypy",
    download_url=URL,
    keywords=["Rust", "Option", "Result"],
    install_requires=[],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
