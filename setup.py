from setuptools import find_packages, setup

setup(
    name="iefp",
    version="0.0.1",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "PyYAML>=5.1",
        "luigi>=2.8.7",
        "pandas>=0.24.2",
        "psycopg2>=2.8.3",
        "pyarrow>=0.14.0",
        "sqlalchemy==1.2.19",
    ],
)
