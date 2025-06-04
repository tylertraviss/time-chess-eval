from setuptools import setup, find_packages

setup(
    name="time-considering-chess-evaluator",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "python-chess>=1.0.0",
        "stockfish>=3.28.0",  # Adding stockfish for position evaluation
    ],
    author="Tyler Travis",
    author_email="tylertraviss@gmail.com",
    description="A chess evaluation bar that combines engine evaluation with time pressure",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/tylertraviss/time-chess-eval",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
) 