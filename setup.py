import os
from setuptools import setup


def read(file_name):
    with open(
            os.path.join(os.path.dirname(__file__), file_name), "r"
        ) as f:
            return f.read()

install_requires = [
    "tornado",
    "selenium",
]

setup(
    name = "autobrowser",
    version = "0.1.0",
    author = "Sagar Nilesh Shah",
    author_email = "shah.sagar.nilesh@gmail.com",
    description = ("Toolset for automated browsing"),
    license = "MIT",
    keywords = "automation web browser",
    url = "http://packages.python.org/autobrowser",
    packages=["autobrowser"],
    long_description=read("README.rst"),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
    ],
    install_requires = install_requires,
)

