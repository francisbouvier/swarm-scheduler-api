# Swarm scheduler API

A basic web server providing an API compliant with [Docker Swarm](https://github.com/docker/swarm) scheduler API backend.  
Based on [Tornado](http://www.tornadoweb.org/).

**Note:** Not intended to be used in production.

## Installation

```sh
pip install swarm-scheduler-api
```

## Usage

```sh
swarm-scheduler-api --host=<ip>:<port>
# See swarm-scheduler-api --help

# Then launch Docker Swarm
swarm manage --scheduler=api --scheduler-option=url:<ip>:<port>
```
