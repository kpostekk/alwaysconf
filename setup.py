from setuptools import setup
from alwaysconf import __version__

setup(
    name="alwaysconf",
    version=__version__,
    packages=["alwaysconf"],
    install_requires=["pyyaml"],
    author="Krystian Postek"
)
