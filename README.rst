

.. image:: https://img.shields.io/pypi/pyversions/colorama.svg
    :target: https://pypi.org/project/colorama/
    :alt: Supported Python versions

.. image:: https://travis-ci.org/tartley/colorama.svg?branch=master
    :target: https://travis-ci.org/tartley/colorama
    :alt: Build Status

Download and docs:
    https://pypi.org/project/colorama/
Source code & Development:
    https://github.com/tartley/colorama

Description
===========


# DOCUMENT SHARING SOFTWARE

This is an application layer protocol designed using deterministic finite automata. This document sharing software is similar to the Google document application that allows users authenticated users to edit, save selected document.

## Getting Started
download from the terminal using:
```
 git clone https://github.com/Francisobiagwu/DocumentSharing.git
```

### Prerequisites



```
Python3 
```

### Installing

From the terminal navigate to the folder where Document sharing software resides
To run server
```
python3 DSServer.py
```
To run client
```
python3 DSClient.py
```

From the client use the following commands to perform the required action

## LOGIN

````
LOGIN, USERNAME, PASSWORD, DOCUMENT_NAME 
````

## REQUEST DOCUMENT SECTION TO EDIT
```
SECTION, SECTION_ID
```

## COMMIT SECTION
```
COMMIT, SECTION_ID, DATA 
```

## LOGOFF
```
LOGOFF      
```
