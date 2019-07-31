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

## Installation and setup

### Minimum system requirements

Operating system: Developed on Ubuntu 18.04 (other recent linux distros should work but are untested)
RAM: 30GB+ (due to the memory intensive data extraction process)

### Clone the Repository

```bash
> git clone https://github.com/dssg/IEFP-RecSys
```

### Install required Packages

Installs virtual environment and dependencies with `pip`:

```bash
> make requirements
```

### Run Jupyter Lab

``` bash
> make lab
```

### Add infrastructure parameters

#### s3

Add the path to your s3 buckets in /conf/base/buckets.yml

``` yaml
intermediate:
  filter: s3://**your-bucket**/intermediate/filter/
  clean: s3://**your-bucket**/intermediate/clean/
  transform: s3://**your-bucket**/intermediate/transform/
modelling: s3://**your-bucket**/modelling/mapping/
```

Check that your s3 credentials are present in your local aws credentials config file (_~/.aws/credentials.yml_) under the [default] key.

#### Postgres

Postgres is used as an intermediate step in our data extraction pipeline. For more details see our Wiki [page](https://github.com/dssg/IEFP-RecSys/wiki/Pipeline-Overview).

Add Postgres credentials to /conf/local/credentials.yml

``` yaml
db:
    pg_user: ******
    pg_pass: ******
    pg_host: ******
```

### Run Luigi pipeline

``` bash
> make luigi
```

### Partners

#### IEFP (Instituto de Emprego e Formação Profissional) | Key Partner
#### NOVA School of Business and Economics | Handover Partner

## Contributors

Rosa Lavelle-Hill, Nathan Coulson, Tobias Richter

## License

A short snippet describing the license
