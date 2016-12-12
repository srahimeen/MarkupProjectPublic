import os
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
import tkinter as tk
from tkinter import filedialog
from html.parser import HTMLParser
from datetime import datetime

#database information, change values here. 
host = "localhost"
admin = "root"
password = "root"
database_name = "testdb"

#map of tags and corresponding values
scoringRules = {
        "div": 3,
        "p": 1,
        "h1": 3,
        "h2": 2,
        "html": 5,
        "body": 5,
        "header": 10,
        "footer": 10,
        "font": -1,
        "center": -2,
        "big": -2,
        "strike": -1,
        "tt": -2,
        "frameset": -5,
        "frame": -5
    }


menu = True #loop condition

#menu for options
while(menu):
	print("Select the appropiate number to perform desired action:")
	print("1 : Calculate the score of a HTML file and save it to the database.")
	print("2 : Retrieve the score of a saved HTML file by name.")
	print("3 : Find the scores within a data range.")
	print("4 : Find the lowest score.")
	print("5 : Find the highest score.")
	print("6 : Exit the menu.")

	try:
		value = int(input("Select an input: "))
		break
	except ValueError:
		print("Invalid input. Please try again!")


	#calulate and save
	if(value == 1):
		root = tk.Tk()
		root.withdraw()
		filename = filedialog.askopenfilename()
		print(filename)

		startTags = [] #list of start tags found in file
		score = 0; #total score of tags

		#method to update list with start tags founds
		class parseStartTags(HTMLParser):
				def handle_starttag(self, tag, attrs):
					print("Encountered a start tag:", tag)
					startTags.append(tag)

					#get file
		f=open(filename,"r")
		s=f.read()
		#initialize parser and feed file
		parser = parseStartTags()
		parser.feed(s)
		#increment score
		for i in startTags:
			score += scoringRules[i]

		print(score)

		#get filename with extension to store
		filename = os.path.basename(filename)
		print(filename)

		#create datetime from filename to store
		filevalue = os.path.splitext(filename)[0] #remove extension
		person_name = filevalue.split("_")[0] #extract name from filename
		date = '/'.join(filevalue.split("_")[1::]) #create date string
		parsed_date = datetime.strptime(date, "%Y/%m/%d") #create datetime from strong
		sql_date = parsed_date.strftime('%Y-%m-%d %H:%M:%S') #make datemine sql friendly
		print(sql_date)

		#get current time
		sql_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S") #create datetime 
		
		print(sql_now)


		#open database connection
		db = MySQLdb.connect(host,admin,password,database_name)
		#prepare a cursor object using cursor() method
		cursor = db.cursor()

		#drop table for testing
		cursor.execute("DROP TABLE IF EXISTS HTMLSCORES")

		#query to create table if it does not exist	
		create_query = """CREATE TABLE IF NOT EXISTS HTMLSCORES (
		         FILE_NAME  CHAR(50) NOT NULL,
		         PERSON_NAME  CHAR(50),
		         SCORE INT,
		         DATE_CREATED DATETIME,
		         DATE_RUN DATETIME,
		         PRIMARY KEY (FILE_NAME))"""

		cursor.execute(create_query)

		#query with placeholder for data
		store_query = ("""INSERT INTO HTMLSCORES (FILE_NAME, PERSON_NAME, SCORE, DATE_CREATED, DATE_RUN)
				VALUES (%s, %s, %s, %s, %s)""")
		#current data to store
		data = (filename, person_name, score, sql_date, sql_now)
		#update database
		cursor.execute(store_query, data)
		db.commit()
		db.close()

	#retrieve score by filename
	elif(value==2):
		print("Please enter file name to search.")
		filename = input("Filename: ")

		#open database connection
		db = MySQLdb.connect(host,admin,password,database_name)
		#prepare a cursor object using cursor() method
		cursor = db.cursor()

		retrieve_query = "SELECT SCORE FROM HTMLSCORES WHERE FILE_NAME='%s'" % (filename)

		cursor.execute(retrieve_query)

		#fetch result integer
		result = cursor.fetchone()
		result = result[0]

		print(result)

		db.close()







