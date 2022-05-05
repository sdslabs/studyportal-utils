import concurrent.futures
import time
import requests
import json
import random
from init import driveinit

NEXUS_ROOT = "http://localhost:8005"
NUM_OF_FILES = 100
filetypes = ['exampapers', 'notes', 'tutorials', 'books']


def listChildFilesInDriveFolder(service, folderID):
    results = service.files().list(
        q="'" + folderID + "' in parents and mimeType != 'application/vnd.google-apps.folder' ",
        fields="nextPageToken, files(id, name, mimeType)",
    ).execute()
    return results.get('files', [])


def addToDB():
    time.sleep(0.3)
    random.seed(time.time())
    filedata = {
        "title": "logo.jpg",  # TBD
        "driveid": str(random.randint(0, 100000)),
        "size": "99",  # TBD
        "filetype": filetypes[random.randint(0, 4) % 4],
        "finalized": True,
        "code": "WRN-551",
    }
    print(f'adding {filedata["driveid"]} to db')
    return requests.post(f"{NEXUS_ROOT}/api/v1/files", data=filedata)


def deleteFromDB(driveid):
    print(f"deleting {driveid} from DB")
    return requests.delete(f"{NEXUS_ROOT}/api/v1/files",
                           data={"driveid": driveid})


def deletor(service):
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
                        idsInDrive = list(
                            map(lambda file: file['id'], filesInDrive))

                        with concurrent.futures.ThreadPoolExecutor() as executor:
                            executor.map(deleteFromDB, idsInDrive)


def adder():

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = [executor.submit(addToDB) for _ in range(NUM_OF_FILES)]
        # for f in concurrent.futures.as_completed(results):
        #     pass
        #     print(f.result())


def warning():
    choice = input(
        "This deletes ALL the files present in DB that are in drive, and adds 1000 random files to the DB.\n Are you sure you want to continue? (y/n): ")
    if choice == "y":
        return 1
    else:
        exit()


if __name__ == '__main__':
    warning()
    start = time.perf_counter()
    adder()
    deletor(driveinit())
    end = time.perf_counter()
    print(f"Code executed in {round(end - start, 2)} seconds")
