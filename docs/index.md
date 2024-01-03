# Welcome to PashehNet!

**PashehNet** is a tool for quickly and reproducibly creating simulated sensor 
networks (SSN) that can publish to a target system.  While there are a couple 
other options out there for building similar networks interactively via web 
UIs or proprietary systems you can license, we at [Zaggy AI](https://zaggy.ai/) 
felt that there needed to be a more flexible solution.  **PashehNet** was born 
from that need, and provides both a command line interface in addition to a 
programmable API.

## Application Programming Interface (API)

The API provides maximum flexibility in creating, executing, and managing an 
SSN directly from within Python.  It is also strongly OO in nature, which 
encourages customization via subclassing.  This makes it ideal for scenarios 
like local dev testing, unit testing, CI/CD pipelines, and endpoint testing.  

Written entirely in Python, it trades off raw performance for ease of use when 
compared to realtime systems,  but does leverage multiprocessing in order to 
scale on multicore systems.

## Command Line Interface (CLI)

**PashehNet** provides a command-line interface and declarative SSN 
configuration that provides a quick way to exchange simulated networks and 
integrate the network into containers, CI/CD pipelines, and general scripting. 
Custom sources, transforms, and formatters are made available via the SSN 
configuration, so you are neither constrained to the core modules shipped with 
the package nor required to build an entire application to add custom features.

## Why open source it?

[Zaggy AI](https://zaggy.ai/) believes in giving back to the FOSS community. 
This tool was built out of an internal need, but does not embody any proprietary 
software or systems that would prevent us from sharing it with the public.  There are plenty of FOSS tools we leverage in our internal development, and we 
strive to "pay it forward" whenever possible.

## Colophon

The name **PashehNet** comes from a play on words:

- "Pasheh" is the romanization of the Persian word for "mosquito."  One of the most common FOSS MQTT brokers out there is [Eclipse Mosquitto](https://mosquitto.org/), which was our initial target test broker internally.
- "Net" - well, network.  Or something that can catch the mosquitos. 🙂

## Table of Contents

```{toctree}
:maxdepth: 1

cli
docker
apidocs/index
```
