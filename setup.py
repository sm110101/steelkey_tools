from setuptools import setup, find_packages

setup(
    name="crypto_portfolio",
    version="0.1.0",
    description="A package for analyzing and managing cryptocurrency portfolios using APIs.",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "requests",
        "python-dotenv",
        "pandas",
        "numpy"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)