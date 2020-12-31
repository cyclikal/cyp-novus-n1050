import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
shrt = "Cyckei Plugin Package, reads set and measured temps from Novus-1050 PID"

setuptools.setup(
    name="cyp-novus-n1050",
    version="1.0",
    author="Clark Ohnesorge",
    author_email="clark@cyclikal.com",
    description=shrt,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cyclikal/cyp-random",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
    ],
    python_requires='>=3.6',
    install_requires=[
        "pyserial",
        "minimalmodbus"
    ],
)