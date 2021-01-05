import os
import json
import requests
from init import driveinit


def listChildFolders(service, folderID):
    results = service.files().list(
        q="'" + folderID + "' in parents and mimeType = 'application/vnd.google-apps.folder' ",
        fields="nextPageToken, files(id, name, mimeType)",
    ).execute()
    return results.get('files', [])


def listChildFiles(service, folderID):
    results = service.files().list(
        q="'" + folderID + "' in parents and mimeType != 'application/vnd.google-apps.folder' ",
        fields="nextPageToken, files(id, name, mimeType)",
    ).execute()
    return results.get('files', [])


def fileSync(service):
    print("fileSync!!")
    input_file = open('structure.json')
    departments = json.load(input_file)['study']
    for department in departments:
        if department == "WRDMD":  # to be removed
            #print("\n" + department)
            if department == 'id':
                #print("department id found, skipping!")
                continue
            for course in departments[department]:
                #print("\n\tcourse:" + course)
                if course == 'id':
                    #print("course id found, skipping!")
                    continue
                if course == 'WRN-551':
                    for filetype in departments[department][course]:
                        #print("\nmaterial: " + filetype )
                        if "_review" not in filetype:
                            drive_link = departments[department][course][filetype]
                            #print("drive_link: " + drive_link)
                            if(drive_link == "1vdKW_3eITxX9PL37mGJunEH3X1HigDrT"):  # to be removed
                                filesInDrive = listChildFiles(
                                    service, drive_link)
                                filesInDB = requests.get(
                                    "http://localhost:8005/api/v1/files?course=" + course + "&filetype=" + filetype).json()
                                idsInDrive = list(
                                    map(lambda file: file['id'], filesInDrive))
                                idsInDB = list(
                                    map(lambda file: file['driveid'], filesInDB))
                                print(idsInDrive)
                                print(idsInDB)
                                # Improve efficiency
                                extrasInDrive = [
                                    item for item in idsInDrive if item not in idsInDB]
                                extrasInDB = [
                                    item for item in idsInDB if item not in idsInDrive]
                                print("Extras in drive: ", extrasInDrive)
                                for id in extrasInDrive:
                                    print("Adding " + id + " to db")
                                    print(course, type(course))
                                    requests.post("http://localhost:8005/api/v1/files", data={
                                        "title": "logo.jpg",  # TBD
                                        "driveid": id,
                                        "size": "99",  # To be fetched from drive
                                        "filetype": filetype,
                                        "finalized": True,
                                        "code": course,
                                    })
                                print("Extras in db: ", extrasInDB)
                                for id in extrasInDB:
                                    requests.delete("http://localhost:8005/api/v1/files", data={
                                        "driveid": id,
                                    })


fileSync(driveinit())