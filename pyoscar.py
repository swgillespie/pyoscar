import requests

OSCAR_API_BASE_URL = 'http://burdellanswers.com:3000/api/oscar/'
DEPARTMENTS = { 'ACCT' : 'Accounting',
                'AE'   : 'Aerospace Engineering',
                'AS'   : 'Air Force Aerospace Studies',
                'APPH' : 'Applied Physiology',
                'ASE'  : 'Applied Systems Engineering',
                'ARBC' : 'Arabic',
                'ARCH' : 'Architecture',
                'BIOL'  : 'Biology',
                'BMEJ' : 'Biomedical Engineering Joint Emory PKU',
                'BME'  : 'Biomedical Engineering',
                'BMEM' : 'Biomedical Engineering Joint Emory',
                'BC'   : 'Building Construction',
                'CETL' : 'Center Enhancement Teach/Learn',
                'CHBE' : 'Chemical % Biomolecular Engineering',
                'CHEM' : 'Chemistry',
                'CHIN' : 'Chinese',
                'CP'   : 'City Planning',
                'CEE'  : 'Civil and Environmental Engineering',
                'COA'  : 'College of Architecture',
                'COE'  : 'College of Engineering',
                'CX'   : 'Computational Mod, Sim, & Data',
                'CSE'  : 'Computational Science and Engineering',
                'CS'   : 'Computer Science',
                'COOP' : 'Co-op',
                'UCGA' : 'Cross-enrollment',
                'EAS'  : 'Earth and Atmospheric Sciences',
                'ECON' : 'Economics',
                'ECE'  : 'Electrical and Computer Engineering',
                'ENGL' : 'English',
                'FS'   : 'Foreign Studies',
                'FREN' : 'French',
                'GT'   : 'Georgia Tech',
                'GTL'  : 'Georgia Tech Lorraine',
                'GRMN' : 'German',
                'HPS'  : 'Health Performance Science',
                'HS'   : 'Health Systems',
                'HIST' : 'History',
                'HTS'  : 'History, Technology, and Society',
                'ISYE' : 'Industrial and Systems Engineering',
                'ID'   : 'Industrial Design',
                'INTA' : 'International Affairs',
                'IL'   : 'International Logistics',
                'INTN' : 'Internship',
                'JAPN' : 'Japanese',
                'KOR'  : 'Korean',
                'LS'   : 'Learning Support',
                'LING' : 'Linguistics',
                'LCC'  : 'Literature, Communication, and Culture',
                'MGT'  : 'Management',
                'MOT'  : 'Management of Technology',
                'MSE'  : 'Materials Science and Engineering',
                'MATH' : 'Mathematics',
                'ME'   : 'Mechanical Engineering',
                'MP'   : 'Medical Physics',
                'MSL'  : 'Military Science and Leadership',
                'ML'   : 'Modern Languages',
                'MUSI' : 'Music',
                'NS'   : 'Naval Science',
                'NRE'  : 'Nuclear and Radiological Engineering',
                'PERS' : 'Persian',
                'PHIL' : 'Philosophy',
                'PHYS' : 'Physics',
                'POL'  : 'Political Science',
                'PTFE' : 'Polymer, Texture, and Fiber Engineering',
                'DOPP' : 'Professional Practice',
                'PSYC' : 'Psychology',
                'PUBP' : 'Public Policy',
                'RGTR' : 'Regent\'s Reading Skills',
                'RGTE' : 'Regent\'s Writing Skills',
                'RUSS' : 'Russian',
                'SOC'  : 'Sociology',
                'SPAN' : 'Spanish' }

DEPARTMENT_LIST = [x.lower() for x in DEPARTMENTS.iterkeys()]
del x

class OscarException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

def get_courses_by_department(department):
    if not department.lower() in DEPARTMENT_LIST:
        raise OscarException('Invalid department: {}'.format(department))
    response = requests.get(OSCAR_API_BASE_URL + department.lower())
    if response.status_code >= 300:
        raise OscarException('HTTP response had status code > 300: {}'.format(response.status_code))
    course_list = response.json()
    return course_list

def get_course_info(department, course_number):
    if not department.lower() in DEPARTMENT_LIST:
        raise OscarException('Invalid department: {}'.format(department))
    response = requests.get(OSCAR_API_BASE_URL + department.lower() + "/" + course_number)
    if response.status_code >= 300:
        raise OscarException('HTTP response had status code > 300: {}'.format(response.status_code))
    class_info = response.json()
    return class_info

def get_course_sections(department, course_number, year, semester):
    if not semester in ['fall', 'spring', 'summer']:
        raise OscarException('Invalid semester, must be fall, spring, or summer: {}'.format(semester))
    if not department.lower() in DEPARTMENT_LIST:
        raise OscarException('Invalid department: {}'.format(department))
    response = requests.get(OSCAR_API_BASE_URL + '{}/{}/{}/{}'.format(department, course_number,
                                                                      year, semester))
    if response.status_code >= 300:
        raise OscarException('HTTP response had status code > 300: {}'.format(response.status_code))
    course_sections = response.json()
    return course_sections

def get_crn_info(department, course_number, year, semester, crn_number):
    if not semester in ['fall', 'spring', 'summer']:
        raise OscarException('Invalid semester, must be fall, spring, or summer: {}'.format(semester))
    if not department.lower() in DEPARTMENT_LIST:
        raise OscarException('Invalid department: {}'.format(department))
    response = requests.get(OSCAR_API_BASE_URL + '{}/{}/{}/{}/{}'.format(department, course_number,
                                                                         year, semester, crn_number))
    if response.status_code >= 300:
        raise OscarException('HTTP response had status code > 300: {}'.format(response.status_code))
    crn_info = response.json()
    return crn_info