from setuptools import setup, find_packages
from pathlib import Path

__version__: str
exec(Path("freyacli/_version.py").read_text())

setup(
    name="freyacli",
    version=__version__,
    description="A CLI framework for Python",
    keywords="cli terminal user interface",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="DiegoBarMor",
    author_email="diegobarmor42@gmail.com",
    url="https://github.com/diegobarmor/freya-cli",
    license="MIT",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
