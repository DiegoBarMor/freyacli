from setuptools import setup, find_packages
from pathlib import Path

__version__: str
exec(Path("freyacli/_version.py").read_text())

setup(
    name="freyacli",
    version=__version__,
    description="Python CLI framework with well defined argument rules and automatic help string generation.",
    keywords="cli terminal user interface command line interface argument parsing help string",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="DiegoBarMor",
    author_email="diegobarmor42@gmail.com",
    url="https://github.com/diegobarmor/freya-cli",
    license="MIT",
    packages=find_packages(),
    package_data={
        "freyacli": [
            "_utils/utils_app.fyr", "_utils/utils_app.fyh",
        ],
    },
    install_requires=[],
    entry_points={
        "console_scripts": [
            "freyacli=freyacli.__main__:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
