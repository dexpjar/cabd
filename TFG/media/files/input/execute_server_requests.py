import time 
import MySQLdb
import pyslurm
import os
import subprocess
from os.path import join
from os import listdir, rmdir
from shutil import move

# Data Base connection info
host = 'localhost'
username = 'ftpsUser'
password = 'd86aewXiGUfxFy4'
dbName = 'ftps_slurm'

# Global Variables
partitionQueue = 'month'
numberCores = "10"
inputPath = '/home/ftpsUser/input/'
pendingPath = inputPath+'pending/'
inQueuePath = inputPath+'inQueue/'

# Function to start a database connection
def DBConnection(host, username, password, dbName):
	db = MySQLdb.connect(host=host,        # your host, usually localhost
                     	     user=username,    # your username
                             passwd=password,  # your password
                             db=dbName)        # name of the data base
	return db

# Function to close a database connection
def DBDeconnection(db):
	db.close()

# Function to move files from one folder to another one
def moveFolders(folderToMove, srcFolder, dstFolder):
	for filename in listdir(join(srcFolder, folderToMove)):
		#First we check if the directory doesn't exist, in that case we create it
		if not os.path.exists(join(dstFolder, folderToMove)):
				os.makedirs(join(dstFolder, folderToMove))
		move(join(srcFolder, folderToMove, filename), join(dstFolder, folderToMove, filename))
	rmdir(join(srcFolder, folderToMove))


# This functions will take from the DB those jobs uncompleted and will check
# if they are in the SLURM queue or if for some reason they aren't there and
# need to be included in the queue again. 
def pendingJobs(db):
	global partitionQueue

	# Cursor object let you execute all the queries you need
	cur = db.cursor(MySQLdb.cursors.DictCursor)

	# Take those jobs that haven't finish yet.
	cur.execute("SELECT * FROM files_jobs WHERE completed = 0")

	# We load the SLURM queue jobs in the partition we are working
	# jobs = pyslurm.job().get()
	partitionJobs = pyslurm.job().find('partition',partitionQueue) 

	# For every job unfinished we check if it is in SLURM queue
	jobs = cur.fetchall()
	for job in jobs:
		jobId = job['jobId']
		# Check if the jobId is in SLURM queue, if it isn't we have to put it again in the queue
		if jobId not in partitionJobs:
			#TODO: re run the job
			print 're run job'





# Function to read from the input folder new tasks, include them in the DB and trigger SLURM
# Having in midn that the input folder has the following structure:
# input
#   |-> pending
#   |       |---> taskX
#   |		   |---> cmd.txt
#   |		   |---> file.fasta / other files
#   | 	    |---> taskY
#   |	           |---> cmd.txt
#   |       	   |---> file.fasta / other files
#   |-> inQueue
def newJobs(db):
	global inputPath, pendingPath, inQueuePath

	# Cursor object let you execute all the queries you need
	cur = db.cursor(MySQLdb.cursors.DictCursor)

	# we parse the folder 'pending' to see the new tasks
	folderNames = []
	for taskFolder in next(os.walk(pendingPath))[1]:
		# we have to check every folder "taskx" in pending folder 
		folderNames.append(taskFolder)

	# Now we check if those tasks are already in the database to prevent duplicate tasks
	folderNamesStr = "', '".join(folderNames)
	cur.execute("SELECT * FROM files_jobs WHERE taskCode IN ('"+folderNamesStr+"')")
	tasksExisting = cur.fetchall()	
	
	# we have to move those tasks that are already in the DB to the inQueue folder and remove from the folderNames array
	for taskExisting in tasksExisting:
		moveFolders(taskExisting['taskCode'], pendingPath, inQueuePath)
		folderNames.remove(taskExisting['taskCode'])
	
	# At this point we have those tasks that need to be included in the SLURM queue and in the DB
	# We have to check the cmd.txt file to see what app we need to run
	for folder in folderNames:
		#We read the cmd file to know which app we want to run
		file  = open(pendingPath+folder+"/cmd.txt", "r")
		content = file.read()
		#We need the first parameter because it contains the app to execute
		#contentAux = content.split(';')
		#app = contentAux[0]
		response = executeApp(content)
		#Now we store it in the DB and run the app in slurm 
		cur.execute("INSERT INTO files_jobs (taskCode, jobId, completed, command) values (%s, %s, %s, %s)", (folder, response['jobId'], 0, response['cmd']))
		#TODO uncomment it to store the data in DB, it is comment for testing
		db.commit()
		print response
		# Once the task has been included in SLURM queue we move the file to inQueue folder
		#TODO uncomment it, it is commented to don't have to create a folder in every test
		moveFolders(folder, pendingPath, inQueuePath)
	
# Function to execute different apps
def executeApp(parameters):
	global partitionQueue, numberCores

	cmd = parameters
	#TODO: Configure the apps to be executed with the specified commandas (parameters array)
	#if app == 'prodigal':
	#	cmd = '/apps/prodigal/prodigal -v'
	#elif app == 'sma3':
	#	cmd = 'sma3 -v'
		#TODO: right now it isn't taking correctly the jobID, maybe we have to change it to pyslurm?
	command = "srun -n "+numberCores+" -p "+partitionQueue+" "+cmd+" --constraint=\"WEB\""
	output = subprocess.check_output(command, shell=True)
	
	#TODO it has to be modified to store the result of the srun (or maybe a sbatch) into the output folder
	response = {}
	response['cmd'] = cmd
	response['jobId'] = output
	return response

while True:
	# Initialize the connection with the DB
	db = DBConnection(host,username, password, dbName)
	
	# Check if there are pending jobs in the DB and check their status
	pendingJobs(db)

	# Check if there are new tasks to be included in SLURM queue
	newJobs(db)

	# Close the connection with the DB
	DBDeconnection(db)

	# Sleep before start again the proccess
	time.sleep(10)




