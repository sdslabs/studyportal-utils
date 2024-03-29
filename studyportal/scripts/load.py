import os
import json
from studyportal.scripts.setup import DEPARTMENTS
import requests

ROOT = os.getcwd()
DEPARTMENTS = os.path.join(ROOT, 'resources/departments.json')
COURSES = os.path.join(ROOT, 'resources/courses.json')

URL_POST_DEPARTMENTS = "https://nexus.sdslabs.co/api/v1/departments/"
URL_POST_COURSES = "https://nexus.sdslabs.co/api/v1/courses/"

SECRET_KEY = "s-0n5h@4*e((tj3ll%8v=)9t$*24t*mdx6tyt&4+5k-l3x)pl="


def load_resources():
    with open(DEPARTMENTS) as h:
        departments = json.load(h)
        for department in departments["department"]:
            data = {
                'title': department["title"],
                'abbreviation': department["abbreviation"]
            }
            requests.post(
                url=URL_POST_DEPARTMENTS,
                data=data,
                headers={"Authorization": "Bearer " + SECRET_KEY},
            )

    with open(COURSES) as h:
        courses = json.load(h)
        for course in courses:
            print(course)
            data = {
                'title': course["title"],
                'code': course["code"],
                'department': course["department"]["title"]
            }
            requests.post(
                url=URL_POST_COURSES,
                data=data,
                headers={"Authorization": "Bearer " + SECRET_KEY},
            )


if __name__ == '__main__':
    load_resources()
