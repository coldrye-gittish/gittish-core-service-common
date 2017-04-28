# gittish-core-service-common

This project provides abstractions common to all gittish services.


## Setting up a Workspace

In order for this to work, you should create yourself a folder that acts as the
`WORKSPACE_ROOT` for maintaining and building the various gittish projects. 

Into that folder you will then clone the required gittish projects.


## Project Dependencies

The following gittish projects need to be available alongside this project.

* gittish-build-common
* gittish-build-python


## External Package Dependencies

In addition to the external package dependencies defined by the other gittish
projects, the following packages need to be installed.


### Runtime Dependencies

* python3
* gittish_core_protocol_common
* gittish_core_logging


### Development Dependencies

* pylint
* pycoverage

