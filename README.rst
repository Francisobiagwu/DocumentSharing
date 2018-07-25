

.. image:: https://github.com/Francisobiagwu/DocumentSharing/blob/master/pythonVersion.svg
    :target: https://github.com/Francisobiagwu/DocumentSharing
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
.. code-block:: python

    git clone https://github.com/Francisobiagwu/DocumentSharing.git


Prerequisites
=============
Python3 

Start Server
=============
.. code-block:: python

    python3 DSServer.py

Start client
=============
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

