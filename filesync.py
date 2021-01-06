import os
import json
import requests
from init import driveinit

NEXUS_ROOT = "http://localhost:8005"

def listChildFilesInDriveFolder(service, folderID):
    results = service.files().list(
        q="'" + folderID + "' in parents and mimeType != 'application/vnd.google-apps.folder' ",
        fields="nextPageToken, files(id, name, mimeType)",
    ).execute()
    return results.get('files', [])

def listChildFilesInDB(course, filetype):
    return requests.get(f"{NEXUS_ROOT}/api/v1/files?course={course}&filetype={filetype}").json()


def fileSync(service):
    print('''


______ _ _        _____                    _____      _ _   _       _         _ 
|  ___(_) |      /  ___|                  |_   _|    (_) | (_)     | |       | |
| |_   _| | ___  \ `--. _   _ _ __   ___    | | _ __  _| |_ _  __ _| |_ ___  | |
|  _| | | |/ _ \  `--. \ | | | '_ \ / __|   | || '_ \| | __| |/ _` | __/ _ \ | |
| |   | | |  __/ /\__/ / |_| | | | | (__   _| || | | | | |_| | (_| | ||  __/ |_|
\_|   |_|_|\___| \____/ \__, |_| |_|\___|  \___/_| |_|_|\__|_|\__,_|\__\___| (_)
                         __/ |                                                  
                        |___/                                                   

    ''')
    print("Loading structure.json...", end = " ")
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
                        print("\nFileType: " + filetype )
                        drive_link = departments[department][course][filetype]
                        print("Drive_link: " + drive_link)

                        filesInDrive = listChildFilesInDriveFolder(service, drive_link)
                        filesInDB = listChildFilesInDB(course, filetype)
                        idsInDrive = list(
                            map(lambda file: file['id'], filesInDrive))
                        idsInDB = list(
                            map(lambda file: file['driveid'], filesInDB))
                        print(f"idsInDrive: {idsInDrive}")
                        print(f"idsInDB: {idsInDB}")
                        # Improve efficiency
                        extrasInDrive = [
                            item for item in idsInDrive if item not in idsInDB]
                        extrasInDB = [
                            item for item in idsInDB if item not in idsInDrive]
                        print("Extras in drive: ", extrasInDrive)
                            # for id in extrasInDrive:
                            #     print("Adding " + id + " to db")
                            #     print(course, type(course))
                            #     requests.post("http://localhost:8005/api/v1/files", data={
                            #         "title": "logo.jpg",  # TBD
                            #         "driveid": id,
                            #         "size": "99",  # To be fetched from drive
                            #         "filetype": filetype,
                            #         "finalized": True,
                            #         "code": course,
                            #     })
                        print("Extras in db: ", extrasInDB)
                            # for id in extrasInDB:
                            #     requests.delete("http://localhost:8005/api/v1/files", data={
                            #         "driveid": id,
                            #     })


fileSync(driveinit())
