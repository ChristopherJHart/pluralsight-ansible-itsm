# Integrating IT Service Management into Ansible Network Workflows

This GitHub repository contains Ansible automation that can be used as a reference while learning from Pluralsight's Integrating IT Service Management into Ansible Network Workflows course.

## Setup

To set up this repository and follow along with the courseware, perform the following steps:

1. Use `git clone` to clone this repository to your local development machine.

```shell
$ git clone https://github.com/ChristopherJHart/pluralsight-ansible-itsm.git
```

2. Move into the newly-created directory.

```shell
$ cd pluralsight-ansible-itsm/
```

3. Create and activate a new Python virtual environment to house this project's dependencies.

```shell
$ python -m venv .venv; source .venv/bin/activate
```

4. Install this project's Python package dependencies using `pip`:

```shell
$ pip install -r requirements.txt
```

5. Install this project's Ansible collection dependencies using `ansible-galaxy`:

```shell
$ ansible-galaxy collection install -r collections/requirements.yaml
```

6. (Optional) If you are interested in using this project as a base to create your own Ansible automation, install this project's development-related Python package dependencies using `pip`:

```shell
$ pip install -r requirements-dev.txt
```

7. (Optional) If you are interested in using Ansible playbooks to deploy a network topology to a Cisco Modeling Labs instance that can be used to test automation, install this project's development-related Ansible collection dependencies using `ansible-galaxy`:

```shell
$ ansible-galaxy collection install -r collections/requirements-dev.yaml
```
