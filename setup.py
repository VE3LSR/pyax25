import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyax25",
    version="0.0.2",
    author="VE3LSR / VE3YCA",
    author_email="projects@ve3lsr.ca",
    description="Python library to send AX25 UI packets over UDP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/VE3LSR/pyax25",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
