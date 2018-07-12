

.. image:: https://img.shields.io/pypi/pyversions/colorama.svg
    :target: https://pypi.org/project/colorama/
    :alt: Supported Python versions


Download and docs:
    https://github.com/Francisobiagwu/DocumentSharing
    
Source code & Development:
   https://github.com/Francisobiagwu/DocumentSharing

Description
===========

This is an application layer protocol designed using deterministic finite automata. This document sharing software is similar to the Google document application that allows users authenticated users to edit, save selected document.


Getting Started
==============
download from the terminal using:

.. code-block:: python

    git clone https://github.com/Francisobiagwu/DocumentSharing.git


Prerequisites
=============
Python3 

Installing
===========

From the terminal navigate to the folder where Document sharing software resides
To run server
.. code-block:: python

    python3 DSServer.py

To run client
.. code-block:: python

    python3 DSClient.py


From the client use the following commands to perform the required action

LOGIN
==========

.. code-block:: python
    LOGIN, USERNAME, PASSWORD, DOCUMENT_NAME 

REQUEST DOCUMENT SECTION TO EDIT
=============================
.. code-block:: python

    SECTION, SECTION_ID


COMMIT SECTION
=======================
.. code-block:: python

    COMMIT, SECTION_ID, DATA 


LOGOFF
======================
.. code-block:: python

    LOGOFF      

