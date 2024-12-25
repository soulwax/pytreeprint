from setuptools import setup, find_packages

# Read README with explicit UTF-8 encoding
with open("README.md", "r", encoding="utf-8") as readme_file:
    long_description = readme_file.read()

setup(
    name="pytree-print-soulwax",  # Changed to match directory name
    version="0.2.15",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "pytreeprint=pytreeprint.cli:main",
        ],
    },
    author="soulwax",
    author_email="soulwax@nandcore.com",
    description="Enhanced directory tree visualization tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/soulwax/pytreeprint",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: System :: Filesystems",
        "Topic :: Utilities",
    ],
    python_requires=">=3.6",
)
