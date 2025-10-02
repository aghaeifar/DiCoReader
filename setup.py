from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="dicoreader",
    version="0.1.0",
    author="Ali Aghaeifar",
    description="Tool for extracting Directional Coupler (DiCo) sample data from Siemens Twix file format",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aghaeifar/DiCoReader",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "twixtools",
        "tqdm",
        "numpy",
    ],
)
