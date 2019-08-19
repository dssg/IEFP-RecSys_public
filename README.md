# IEFP Recommender System

The IEFP, the institute of employment and vocational training in Portugal, run 80+ job centers around the country. At these job centers, job counsellors help job seekers to find good employment through recommending interventions (e.g. training courses) and assisting with job applications.

The project is to design an intervention recommender system for job counsellors. The system will recommend the most relevant and effective interventions for an individual job seeker based on their profile and what has been most effective for similar people.

## Table of Contents

1. [Introduction](https://github.com/dssg/repo_name#introduction)
2. [Installation and setup](https://github.com/dssg/repo_name#setup)
3. [Partners](https://github.com/dssg/repo_name#partners)
4. [Contributors]
5. [License]

## Introduction

### Data Science for Social Good at Imperial College London

The Data Science for Social Good Fellowship is a summer program to train aspiring data scientists to work on data mining, machine learning, big data, and data science projects with social impact. Working closely with governments and nonprofits, fellows take on real-world problems in education, health, energy, public safety, transportation, economic development, international development, and more.

For three months they learn, hone, and apply their data science, analytical, and coding skills, collaborate in a fast-paced atmosphere, and learn from mentors coming from industry and academia.

## Minimum infrastructure requirements

It is recommended to run the project with the infracstruture hosted on AWS. It has been tested with the
following system specifications:

```
- EC2 instance: c4.4xlarge
    - vCPU: 16
    - RAM: 30 GB
    - OS: ubuntu 18.04 LTS
    - Volumes: 1
    - Type: gp2
    - Size: 100 GB
- RDS: PostgreSQL
    - Engine: PostgreSQL
    - Engine version: 10.6
    - Instance: db.t2.xlarge
    - vCPU: 4
    - RAM: 16 GB
    - Storage: 150 GB
```

**Note:** The database system is required to be PostgreSQL, but does not have to be hosted on AWS.

**Caution:** Due to the size of the data it is recommended to have an EC2 instance with RAM size of 30GB or more.

## Installation and setup

### Clone the Repository

```bash
> git clone https://github.com/dssg/IEFP-RecSys
```

### Install required system packages
- [GNU make](https://gnu.org/software/make)
- [python3 >= 3.6](https://packages.ubuntu.com/bionic/python3)
- [python3-dev](https://packages.ubuntu.com/bionic/python3-dev) (Header files to
    compile python packages)
- [python3-venv](https://packages.ubuntu.com/bionic/python3-venv) (In case it is
    not installed with python3 by your package manager)
- [jq](https://github.com/stedolan/jq)
- [postgresql-client](https://www.postgresql.org/docs/9.3/app-psql.html)
- [gcc](https://packages.ubuntu.com/bionic/gcc)
- [libpg-dev](https://www.postgresql.org/docs/11/libpq.html)

For example:

```bash
> sudo apt update
> sudo apt install make gcc jq libpg-dev postgresql-client postgresql-client python3 python3-dev python3-venv
```


### Credentials Setup

1. Add PostgreSQL credentials to `IEFP-RecSys/conf/local/credentials.yml`.

For example:
``` yaml
db:
    pg_user: my_user
    pg_pass: my_password
    pg_host: name.id.region.rds.amazonaws.com
    pg_name: iefp
    pg_port: 5432
```
- **NOTE:** Make sure the PostgreSQL has a Database with the specified name
    (e.g. `iefp`) created and the specified user has read/write access to it.

2. Check that your aws s3 credentials are present in the local credentials file (`~/.aws/credentials`) under the `[default]` key.

```
[default]
  aws_access_key_id = ****
  aws_secret_access_key = ****
```

### S3 Bucket

Add the path to your s3 buckets in `IEFP-RecSys/conf/base/buckets.yml`

``` yaml
intermediate:
  filter: s3://**your-bucket**/intermediate/filter/
  clean: s3://**your-bucket**/intermediate/clean/
  transform: s3://**your-bucket**/intermediate/transform/
modelling: s3://**your-bucket**/modelling/mapping/
```

### Data Setup

Get a dump of SIGAE data to `IEFP-RecSys/data/`. Required files are:

- `EMP_PEDIDOS.csv`
- `MOV_INTERVENCOES.csv`

## Run the Project

### Install required python packages

Installs virtual environment and dependencies with `pip`:

```bash
> make requirements
```

### Create database tables

Trigger a script that creates the required database tables and copy the data.

```bash
> make database
```


### Run Luigi pipeline

We are using the Luigi pipeline framework in order to create a repeatable and reliable workflow from the raw data source to the model output (predictions, recommendations and evaluations).

Run the pipeline with:

```bash
> make luigi
```

### Use the command line:
```bash
> source env/bin/activate
> iefp-recsys --help
Usage: iefp-recsys [OPTIONS]

IEFP Intervention Recommender.

Options:
-r, --recommendations INTEGER  Number of recommendations
-s, --set-size INTEGER         Maximum number of interventions in a recommended set
--help                         Show this message and exit.
> iefp-recsys --recommendations 10 --set-size 3
```

### Run Jupyter Lab

We are using [Jupyter Lab](https://github.com/jupyterlab/jupyterlab) for
exploratory data analysis and fast prototyping. Run it with:

``` bash
> make lab
```

### Partners

- IEFP (Instituto de Emprego e Formação Profissional) | Key Partner
- Nova School of Business & Economics | Handover Partner

## Contributors

Rosa Lavelle-Hill, Nathan Coulson, Tobias Richter, Liliana Millán

## License

MIT License - Copyright 2019 Nova School of Business & Economics
