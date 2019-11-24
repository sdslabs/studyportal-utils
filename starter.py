import requests

URL_DEPARTMENTS = "https://channeli.in/lectut_api/departments/"
URL_COURSES = "https://channeli.in/lectut_api/departmentDetails/"
URL_POST_DEPARTMENTS = "http://nexus.sdslabs.local/api/v1/departments/"
URL_POST_COURSES = "http://nexus.sdslabs.local/api/v1/courses/"

r = requests.get(url = URL_DEPARTMENTS)
departmentList = r.json()
departments = departmentList["departments"]
for department in departments:
    print(department)
    data = {
        'title': department[1],
        'abbreviation': department[0],
        'imageurl': str(department[0]).lower()+".svg"
    }
    requests.post(url = URL_POST_DEPARTMENTS, data = data)
    url = URL_COURSES+str(department[0])+"/"
    r1 = requests.get(url = url)
    if not r1:
        continue
    courseList = r1.json()
    courses = courseList["courses"]
    for course in courses:
        coursedata = {
            'title': course["name"],
            'department': department[1],
            'code': course["code"]
        }
        requests.post(url = URL_POST_COURSES, data = coursedata)