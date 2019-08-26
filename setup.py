from setuptools import find_packages, setup

setup(
    name="iefp",
    version="0.0.1",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "PyYAML==5.1",
        "boto3==1.9.180",
        "click==7.0",
        "luigi==2.8.7",
        "pandas==0.24.2",
        "psutil==5.6.3",
        "psycopg2==2.8.3",
        "pyarrow==0.14.0",
        "s3fs==0.2.2",
        "scikit-learn==0.21.2",
        "sqlalchemy==1.2.19",
    ],
    entry_points="""
            [console_scripts]
            iefp-recsys=iefp.cli:cli
        """,
)
