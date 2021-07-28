#!/usr/bin/env python
import setuptools

if __name__ == "__main__":
    setuptools.setup(
        author="Trevor Bača",
        author_email="trevor.baca@gmail.com",
        description="Trevor Bača's Abjad library.",
        install_requires=[
            "abjad",
            "mypy",
            "roman",
            "sphinx",
            "sphinx-rtd-theme",
            "uqbar>=0.2.13",
        ],
        keywords="abjad, lilypond, music composition, music notation",
        license="MIT",
        name="baca",
        packages=["baca"],
        platforms="Any",
        python_requires=">=3.9",
        url="https://github.com/trevorbaca/baca",
        version="3.2",
    )
