### General Information
This program was created using Python 3.5.2 and is structured as a console application.

### Compile and Run
In order to run the program, navigate to the /src folder from the terminal and run the following command:

-> python TagGrader.py

NOTE: If you have a different path variable for Python 3, substitute that for python.

### Database Information
This program connects to a MySQL database. The database host, admin, password and name can be changed at the top of the TagGrader.py file. By default it is the following:

host = "localhost"

admin = "root"

password = "root"

database_name = "testdb"

Since tables are created by the program itself as long as the database exists, no scripts were placed in the /schema folder.


### External Libraries
This program utilizes a few external libraries which are imported at the top of the TagGrader.py file. The following libraries are used:

import os

import pymysql

pymysql.install_as_MySQLdb()

import MySQLdb

import tkinter as tk

from tkinter import filedialog

from html.parser import HTMLParser

from datetime import datetime

import warnings

Since the import keyword was used, no local libraries were placed in the /vendors folder.


### Other Information
The query for average score was merged into the main menu of program instead of being in the /schema folder.

