import psycopg2
import json
from init import driveinit
import concurrent.futures
import datetime


today = datetime.datetime.today()
date_today = today.strftime("%Y-%m-%d")
filesSynced = 0


try:

    connection = psycopg2.connect(database="studyportal", 
                            user = "studyportal", 
                            password = "studyportal", 
                            host = "localhost", 
                            port = "5432")
    cursor = connection.cursor()
    print("Database connected!")

except (Exception, psycopg2.Error) as error1:
        print("Failed to connect to database...", error1)



#returns files in present in a folder
def listFiles(service, folderID):
    results = service.files().list(
        q="'" + folderID + "' in parents and mimeType != 'application/vnd.google-apps.folder' ",
        fields="nextPageToken, files(id, name, size, mimeType)",
    ).execute()
    return results.get('files', [])


#get course ID from the table resources_course
def getCourseID(course):
    try:
        qry = '''
                SELECT * FROM resources_course WHERE code = %s 
                '''
        cursor.execute(qry,(course,))
        courseid = cursor.fetchone()
        if courseid is None:
            return(0)
        else: 
            return courseid[0]
    except (Exception, psycopg2.Error) as error:
        print("Failed to find course ID...", error)
                

#check whether file already exists in database
def checkIfFileInDB(driveid):
    try:
        qry = '''
            SELECT EXISTS (
                SELECT 1
                FROM resources_file
                WHERE driveid = %s
            )'''
        cursor.execute(qry, (driveid,))
        return cursor.fetchone()[0]
    except (Exception, psycopg2.Error) as error:
        print("error: ", error)
        return False


#add new file to the database
def addFileInDB(file):
    try:
        qry = '''
                INSERT INTO resources_file (title, driveid, downloads, size, date_modified, fileext, filetype, finalized, course_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            '''
        recordToInsert = (file['title'], file['driveid'], 0, file['size'], file['dateModified'], file['fileext'], file['filetype'], 't', file['courseid'] )
        cursor.execute(qry, recordToInsert)
        connection.commit()
        print(file['title'] + ' added in database...')
    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record", file['title'], file['courseid'], error)
    

def printContents():
    try:
        qry = '''
            SELECT * FROM resources_file 
            '''
        cursor.execute(qry)
        records = cursor.fetchall()

        for row in records:
            print (row[0],"\t",row[1],"\t",row[2],"\t",row[3],"\t",row[4],"\t",row[5],"\t",row[6],"\t",row[7],"\t",row[8],"\t",row[9])

    except (Exception, psycopg2.Error) as error:
        print("Failed to print", error)
    

def syncAction(file):
    global filesSynced
    fileExists = checkIfFileInDB(file['driveid'])
    if(fileExists):
        print(file['title'] + ' file already in database...')
            
    else:
        addFileInDB(file)
        filesSynced = filesSynced + 1
        
            
def courseScan(course, departments, depts):
    service = driveinit()
    for folder in departments[depts][course]:
        if course != 'id':
            if folder != 'id':
                pickFolder = departments[depts][course][folder]
                filesInDriveFolder = listFiles(service, pickFolder)
                if(len(filesInDriveFolder) != 0):
                    for item in filesInDriveFolder:
                        string = item['mimeType']
                        file_type, ext = string.split('/')
                        file_data = {
                            'title' : item['name'],
                            'driveid': item['id'],
                            'size': str(round((float(item['size'])/(10**6)), 2))+" MB",
                            'dateModified': date_today,
                            'fileext': ext,
                            'filetype': folder,
                            'courseid' : getCourseID(course)
                        }

                        if file_data['courseid'] == 0:
                            print(file_data['title'], "skipped, as course does not exist in database.")
                            continue
                        syncAction(file_data)

                        
def fileCheck():
    directoryStructure = open('structure.json')
    print('Scanning through all departments:\n')
    departments = json.load(directoryStructure)['study']
    for depts in departments:
        if(depts == 'id'):
            continue
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = [executor.submit(
                courseScan, course, departments, depts) for course in departments[depts]]
       


if __name__ == '__main__':
    fileCheck()
    # print('\nresources_file -> Table content: \n')
    # printContents()

    print('''
    ______ _ _          _____                      _____                       _      _          _   _   _ 
    |  ___(_) |        /  ___|                    /  __ \                     | |    | |        | | | | | |
    | |_   _| | ___    \ `--. _   _ _ __   ___    | /  \/ ___  _ __ ___  _ __ | | ___| |_ ___   | | | | | |
    |  _| | | |/ _ \    `--. \ | | | '_ \ / __|   | |    / _ \| '_ ` _ \| '_ \| |/ _ \ __/ _ \  | | | | | |
    | |   | | |  __/   /\__/ / |_| | | | | (__    | \__/\ (_) | | | | | | |_) | |  __/ ||  __/  |_| |_| |_|
    \_|   |_|_|\___|   \____/ \__, |_| |_|\___|    \____/\___/|_| |_| |_| .__/|_|\___|\__\___|  (_) (_) (_)
                               __/ |                                    | |                                
                              |___/                                     |_|                                
    ''')

    print('Number of new files added to database:', filesSynced)

