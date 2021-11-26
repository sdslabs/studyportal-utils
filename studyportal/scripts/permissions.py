import requests
from studyportal.init import driveinit
from apiclient import errors


FILE_URL = "https://nexus.sdslabs.co/api/v1/files?format=json"

def updatePermissions(service, fileId):
    try:
        new_permission = {"type": "anyone", "value": "anyone", "role": "reader"}
        service.permissions().create(fileId=fileId, body=new_permission).execute()
    except errors.HttpError as error:
        print("An error occurred:", error)

def update_file_perms(service):
    files = requests.get(FILE_URL).json()
    for file in files["files"]:
        updatePermissions(service, file["driveid"])

if __name__ == '__main__':
    service = driveinit()
    update_file_perms(service)

