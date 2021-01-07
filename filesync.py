import os
import json
import requests
from init import driveinit
import concurrent.futures
import time

NEXUS_ROOT = "http://localhost:8005"

# APIS
def listChildFilesInDriveFolder(service, folderID):
    results = service.files().list(
        q="'" + folderID + "' in parents and mimeType != 'application/vnd.google-apps.folder' ",
        fields="nextPageToken, files(id, name, mimeType)",
    ).execute()
    return results.get('files', [])


def listChildFilesInDB(course, filetype):
    results = requests.get(f"{NEXUS_ROOT}/api/v1/files?course={course}&filetype={filetype}")
    print(results.status_code)
    return results.json()


def deleteExtraInDB(driveid):
    print(f"deleting {driveid} from DB")
    return requests.delete("http://localhost:8005/api/v1/files",
                           data={"driveid": driveid})


def addExtraToDB(filedata):
    return requests.post("http://localhost:8005/api/v1/files", data=filedata)

# FileSync module
def fileSync(service):
    print('''
______ _ _          _____                          _             _      _   _   _ 
|  ___(_) |        /  ___|                        | |           | |    | | | | | |
| |_   _| | ___    \ `--. _   _ _ __   ___     ___| |_ __ _ _ __| |_   | | | | | |
|  _| | | |/ _ \    `--. \ | | | '_ \ / __|   / __| __/ _` | '__| __|  | | | | | |
| |   | | |  __/   /\__/ / |_| | | | | (__    \__ \ || (_| | |  | |_   |_| |_| |_|
\_|   |_|_|\___|   \____/ \__, |_| |_|\___|   |___/\__\__,_|_|   \__|  (_) (_) (_)
                           __/ |                                                  
                          |___/                                                   
    ''')

    print("Loading structure.json...", end=" ")
    input_file = open('structure.json')
    print("Loaded!")
    departments = json.load(input_file)['study']
    for department in departments:
        if department == "WRDMD":  # to be removed
            if department == 'id':
                continue
            print("\nDepartment: " + department)
            for course in departments[department]:
                if course == 'id':
                    continue
                print("Course: " + course)
                for filetype in departments[department][course]:
                    if filetype == 'id':
                        continue
                    if "_review" not in filetype:
                        print("\nFileType: " + filetype)
                        drive_link = departments[department][course][filetype]

                        filesInDrive = listChildFilesInDriveFolder(
                            service, drive_link)
                        
                        filesInDB = listChildFilesInDB(course, filetype)
                        
                        idsInDrive = list(
                            map(lambda file: file['id'], filesInDrive))
                        idsInDB = list(
                            map(lambda file: file['driveid'], filesInDB))

                        # Improve efficiency a lil here
                        extrasInDrive = [
                            item for item in idsInDrive if item not in idsInDB]
                        extrasInDB = [
                            item for item in idsInDB if item not in idsInDrive]
                        
                        print("Extras in drive: ", extrasInDrive)
                        for id in extrasInDrive:
                            print("Adding " + id + " to db")
                            filedata = {
                                "title": "logo.jpg",  # TBD
                                "driveid": id,
                                "size": "99",  # TBD
                                "filetype": filetype,
                                "finalized": True,
                                "code": course,
                            }
                            addExtraToDB(filedata)

                        print("Extras in db: ", extrasInDB)
                        with concurrent.futures.ThreadPoolExecutor() as executor:
                            executor.map(deleteExtraInDB, extrasInDB)
                            #results = [executor.submit(deleteExtraInDB, driveid) for driveid in extrasInDB]
                            # for f in concurrent.futures.as_completed(results):
                            #     print(f.result())
                        
                        # for driveid in extrasInDB:
                        #     print(deleteExtraInDB(driveid))


start = time.perf_counter()

fileSync(driveinit())

end = time.perf_counter()

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
print(f"Syncing time: {round(end - start, 3)} seconds")
