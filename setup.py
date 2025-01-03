from setuptools import setup, find_packages

setup(
    name="crypto_portfolio",
    version="0.1.0",
    description="A package for analyzing and managing cryptocurrency portfolios using APIs.",
    author="Sean Morris",
    author_email="spm122@georgetown.edu",
    packages=find_packages(),
    install_requires=[
        "requests",
        "python-dotenv",
        "pandas",
        "numpy"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)