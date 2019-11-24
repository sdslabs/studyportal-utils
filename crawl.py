from init import driveinit
from apiclient import errors
import requests
# ...

URL = "http://nexus.sdslabs.local/api/v1/files/"

def print_files_in_folder(service, folder_id):
  """Print files belonging to a folder.

  Args:
    service: Drive API service instance.
    folder_id: ID of the folder to print files from.
  """
  query="'" + folder_id + "' in parents"
  try:
    department_children = service.files().list(
        q=query,
        spaces='drive',
        fields='files(id)').execute()

    #   for child in children.get('items', []):
    #     print('File Id: %s' % child['id'])
    #   page_token = children.get('nextPageToken')
    #   if not page_token:
    #     break
    for ids in department_children['files']:
      query="'" + ids['id'] + "' in parents"

      try:
        course_children = service.files().list(
          q=query,
          spaces='drive',
          fields='files(id,name)').execute()

        for newids in course_children['files']:
          print('Folder %s: %s' % (newids['name'], newids['id']))
          query="'" + newids['id'] + "' in parents"

          try:
            filetype_children = service.files().list(
              q=query,
              spaces='drive',
              fields='files(id,name)').execute()
            
            for newerids in filetype_children['files']:
              print('Folder %s: %s \n' % (newerids['name'], newerids['id']))
              query="'" + newerids['id'] + "' in parents"

              try:
                file_children = service.files().list(
                  q=query,
                  spaces='drive',
                  fields='files(id,name,size,modifiedTime)').execute()
                if file_children['files'] == []:
                  continue
                for file in file_children['files']:
                  print('Found file: %s (%s, %s, %s)' % (file['name'], file['id'], file['size'], file['modifiedTime']))
                  data = {
                    'title': file['name'],
                    'driveid': file['id'],
                    'size': file['size'],
                    'code': newids['name'],
                    'filetype': newerids['name']
                  }
                  requests.post(url=URL, data=data)
                print('\n')

              except errors.HttpError as error:
                print('An error occurred: %s' % error)

          except errors.HttpError as error:
            print('An error occurred: %s' % error)

      except errors.HttpError as error:
        print('An error occurred: %s' % error)

  except errors.HttpError as error:
    print('An error occurred: %s' % error)
  # page_token = None
  # while True:
  #     response = service.files().list(q="mimeType='application/vnd.google-apps.folder'",
  #                                           spaces='drive',
  #                                           fields='nextPageToken, files(id, name)',
  #                                           pageToken=page_token).execute()
  #     for file in response.get('files', []):
  #       # Process change
  #         query="'" + file.get('id') + "' in parents"
  #         try:
  #             files = service.files().list(
  #               q=query,
  #               spaces='drive',
  #               fields='files(id,name,size,modifiedTime)').execute()
  #             if files['files'] == []:
  #                 continue
  #             for file in files['files']:
  #                 print('Found file: %s (%s)' % (file['name'], file['id']))

  #         except errors.HttpError as error:
  #             print('An error occurred: %s' % error)

  #     page_token = response.get('nextPageToken', None)
  #     if page_token is None:
  #         break
    

if __name__ == '__main__':
    print_files_in_folder(driveinit(),'1Zd-uN6muFv8jvjUSM7faanEL0Zv6BTwZ')