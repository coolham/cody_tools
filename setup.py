from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="openclaw-tools",
    version="0.1.0",
    author="OpenClaw Community",
    description="A collection of utility tools for the OpenClaw AI automation framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/coolham/cody_tools",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    keywords="openclaw tools automation ai",
)
