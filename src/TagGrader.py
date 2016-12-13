# Author: Soufin Rahimeen
# Sequential console program solution.
import os
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
import tkinter as tk
from tkinter import filedialog
from html.parser import HTMLParser
from datetime import datetime
import warnings

#don't display warnings in console for IF NOT EXISTS for table creation
warnings.filterwarnings('ignore', category=MySQLdb.Warning) 

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
	print("6 : Find the average score.")
	print("7 : Exit the menu.")

	try:
		value = int(input("Select an input: "))
	except ValueError:
		print("Invalid input. Try again! \n")
		continue


	#calulate and save
	if(value == 1):
		root = tk.Tk()
		root.withdraw()
		filename = filedialog.askopenfilename()
		print("Selected file: " + filename)

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

		print("Calulated score: " + str(score))

		#get filename with extension 
		filename = os.path.basename(filename)
		#create datetime from filename to store
		filevalue = os.path.splitext(filename)[0] #remove extension
		person_name = filevalue.split("_")[0] #extract name from filename
		date = '/'.join(filevalue.split("_")[1::]) #create date string
		parsed_date = datetime.strptime(date, "%Y/%m/%d") #create datetime from strong
		sql_date = parsed_date.strftime('%Y-%m-%d %H:%M:%S') #make datemine sql friendly
		#print(sql_date)

		#get current time
		sql_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S") #create datetime 
		
		#print(sql_now)


		#open database connection
		db = MySQLdb.connect(host,admin,password,database_name)
		#prepare a cursor object using cursor() method
		cursor = db.cursor()

		#UTILITY:drop table for testing
		#cursor.execute("DROP TABLE IF EXISTS HTMLSCORES")

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
		data = (filevalue, person_name, score, sql_date, sql_now)
		#perform query update database and handle exceptions
		try:
			cursor.execute(store_query, data)
			db.commit()
		except Exception as e:
			print("File already exists. Try a different file. \n" )
			continue

		print("File saved! \n")

		db.close()

	#retrieve score by filename
	elif(value==2):
		print("Please enter file name without the extension (eg. bob_2013_02_15) to search.")
		filename = input("Filename: ")

		#open database connection
		db = MySQLdb.connect(host,admin,password,database_name)
		#prepare a cursor object using cursor() method
		cursor = db.cursor()

		#query to get value by filename
		retrieve_query = "SELECT SCORE FROM HTMLSCORES WHERE FILE_NAME='%s'" % (filename)

		try:
			cursor.execute(retrieve_query)
		except Exception as e:
			print("Invalid file name. Try again. \n" )
			continue

		if(cursor.rowcount == 0):
			print("Invalid file name. Try again. \n" )
			continue
		

		#fetch result integer
		result = cursor.fetchone()
		result = result[0]

		print("Score for the file is: " + str(result) + "\n")

		db.close()
	#retrieve scores between date range
	elif(value == 3):
		print("Enter starting date in format yyyy/mm/dd.")
		start_date = input("Start date: ")
		print("Enter end date in format yyyy/mm/dd.")
		end_date = input("End date: ")

		#open database connection
		db = MySQLdb.connect(host,admin,password,database_name)
		#prepare a cursor object using cursor() method
		cursor = db.cursor()

		#query to get value by filename
		date_query = "SELECT PERSON_NAME, SCORE FROM HTMLSCORES WHERE DATE_CREATED>='%s' AND DATE_CREATED<='%s'" % (start_date, end_date)

		try:
			cursor.execute(date_query)
		except Exception as e:
			print("Invalid date format. Try again. \n" )
			continue

		if(cursor.rowcount == 0):
			print("No results found within date range. Try again. \n" )
			continue

		result = cursor.fetchall()

		print("Name|Score")
		for row in result:
			print(str(row[0]) + " | " + str(row[1]))
		print("\n")


		db.close()

	#retrieve min
	elif(value == 4):
		#open database connection
		db = MySQLdb.connect(host,admin,password,database_name)
		#prepare a cursor object using cursor() method
		cursor = db.cursor()

		min_query = "SELECT PERSON_NAME, SCORE FROM HTMLSCORES WHERE SCORE=(SELECT MIN(SCORE) FROM HTMLSCORES)"

		#handle exceptions
		try:
			cursor.execute(min_query)
		except Exception as e:
			print("Invalid query. Try again. \n" )
			continue

		if(cursor.rowcount == 0):
			print("No value found. Try again. \n" )
			continue

		#fetch result integer
		result = cursor.fetchone()
		name = result[0]
		min_score = result[1]

		print("The lowest score is : " + name + " | " + str(min_score) + "\n")

		db.close()
	#retieve max
	elif(value == 5):
		#open database connection
		db = MySQLdb.connect(host,admin,password,database_name)
		#prepare a cursor object using cursor() method
		cursor = db.cursor()

		max_query = "SELECT PERSON_NAME, SCORE FROM HTMLSCORES WHERE SCORE=(SELECT MAX(SCORE) FROM HTMLSCORES)"

		try:
			cursor.execute(max_query)
		except Exception as e:
			print("Invalid query. Try again. \n" )
			continue

		if(cursor.rowcount == 0):
			print("No value found. Try again. \n" )
			continue

		#fetch result integer
		result = cursor.fetchone()
		name = result[0]
		max_score = result[1]

		print("The highest score is : " + name + " | " + str(max_score) + "\n")

		db.close()
	#exit
	elif(value == 6):
		#open database connection
		db = MySQLdb.connect(host,admin,password,database_name)
		#prepare a cursor object using cursor() method
		cursor = db.cursor()

		min_query = "SELECT AVG(SCORE) FROM HTMLSCORES"

		#handle exceptions
		try:
			cursor.execute(min_query)
		except Exception as e:
			print("Invalid query. Try again. \n" )
			continue

		if(cursor.rowcount == 0):
			print("No value found. Try again. \n" )
			continue

		#fetch result integer
		result = cursor.fetchone()
		avg_score = result[0]
	

		print("The average score is " + str(avg_score) + "\n")

		db.close()
	elif(value == 7):
		print("Exiting program.")
		menu = False
		break
	else:
		print("Invalid input. Try again. \n")
		continue

