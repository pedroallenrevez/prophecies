from setuptools import setup, find_packages
import pathlib

setup(
    name="prophecies",
    version="0.0.1",
    description="Experimental HTML framework for TUI's, using a curses backend",
    url="https://github.com/pedroallenrevez/prophecies",
    author="Pedro Allen Revez",
    author_email="pedroallenrevez@gmail.com",
    python_requires=">=3.7, <4",
    install_requires=[
        "click",
        "pydantic",
        "parsy",
        "pyfiglet",
    ],
    entry_points={
        "console_scripts": [
            "prophecies=prophecies.cli:make_cli",
        ],
    },
)
