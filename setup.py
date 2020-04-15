import json
import requests
from init import driveinit

URL_DEPARTMENTS = "https://channeli.in/lectut_api/departments/"
URL_COURSES = "https://channeli.in/lectut_api/departmentDetails/"
 
 
class dictionary(dict):   
    # __init__ function 
    def __init__(self): 
        self = dict() 
          
    # Function to add key:value 
    def add(self, key, value): 
        self[key] = value 


def create_root(service=driveinit()):
    """
    Create root folder to hold files
    """
    file_metadata = {
        'name': 'study',
        'mimeType': 'application/vnd.google-apps.folder'
    }
    file = service.files().create(body=file_metadata, fields='id').execute()
    return file.get('id')


def create_folder(folder_name, folder_id, service=driveinit()):
    """
    Create appropriate folder within a parent folder
    """
    file_metadata = {
        'name': folder_name,
        'parents': [folder_id],
        'mimeType': 'application/vnd.google-apps.folder'
    }
    file = service.files().create(body=file_metadata, fields='id').execute()
    return file.get('id')


def create_folder_for_files(dictionary, folder_id, service=driveinit()):
    """
    Create folder corresponding to files
    """
    folders = ['tutorials', 'books', 'notes', 'exampapers', 'tutorials_review', 'books_review', 'notes_review', 'exampapers_review']
    for folder in folders:
        file_folder_id = create_folder(folder, folder_id)
        dictionary.add(folder, file_folder_id)


if __name__ == '__main__':
    main_dict = dictionary()
    root_dict = dictionary()
    FOLDER_ID = create_root()
    root_dict.add('id', FOLDER_ID)
    r = requests.get(url=URL_DEPARTMENTS)
    departments_list = r.json()['departments']

    for department in departments_list:
        department_dict = dictionary()
        department_folder_id = create_folder(department[0], FOLDER_ID)
        department_dict.add('id', department_folder_id)
        url_course = URL_COURSES+str(department[0])+"/"
        r1 = requests.get(url=url_course)
        
        if r1:
            courses_list = r1.json()['courses']
            for course in courses_list:
                course_dict = dictionary()
                course_folder_id = create_folder(course['code'], department_folder_id)
                course_dict.add('id', course_folder_id)
                create_folder_for_files(course_dict, course_folder_id)
                department_dict.add(course['code'], course_dict)
        root_dict.add(department[0], department_dict)
    main_dict.add('study', root_dict)
    f = open("structure.json", "w+")
    f.write(json.dumps(main_dict))
    f.close
