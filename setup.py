from setuptools import find_packages, setup

setup(
    name="iefp",
    version="0.0.1",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "PyYAML>=5.1",
        "matplotlib>=3.1",
        "pandas>=0.23.4",
        "s3fs>=0.2.1",
    ],
)
