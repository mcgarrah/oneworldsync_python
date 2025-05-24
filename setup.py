from setuptools import setup, find_packages

setup(
    name="oneworldsync",
    version="0.2.2",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "python-dotenv>=0.15.0",
        "click>=8.0.0",  # Added for CLI support
    ],
    entry_points={
        'console_scripts': [
            'ows=oneworldsync.cli:cli',
        ],
    },
    author="Michael McGarrah",
    author_email="mcgarrah@gmail.com",
    description="A Python client for the 1WorldSync Content1 Search and Fetch REST API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mcgarrah/oneworldsync_python",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    python_requires=">=3.12",

)