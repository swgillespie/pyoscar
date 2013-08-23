import requests
import time
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
del x # x has global scope due to the above list comprehension.
      # Delete it so it goes away, its value is undefined anyway.

class OscarException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

class OscarCourse:
    def __init__(self, department, number):
        self.department = department
        self.course_number = number
        info_dict = _get_course_info(department, number)
        self.credit_hours = info_dict['creditHours'][0] or 0
        self.description = info_dict['description']
        self.is_auditable = info_dict['grade_basis'].find('A') > 0
        self.is_letter_gradeable = info_dict['grade_basis'].find('L') > 0
        self.is_pass_failable = info_dict['grade_basis'].find('P') > 0
        self.lab_hours = info_dict['labHours'][0] or 0
        self.lecture_hours = info_dict['lectureHours'][0] or 0
        self.name = info_dict['name']

    def get_sections(self, year, semester):
        sections_dict = _get_course_sections(self.department, self.course_number,
                                             year, semester)
        sections = []
        for section in sections_dict:
            sections.append(OscarCourseSection(self.department, self.course_number,
                                               year, semester, section['crn'],
                                               section['where']))
        return sections

class OscarCourseSection:
    def __init__(self, department, course_number, year, semester, crn, location_list):
        self.department = department
        self.course_number = course_number
        self.year = year
        self.semester = semester
        self.crn = crn
        info_dict = _get_crn_info(department, course_number, year, semester, crn)
        self.name = info_dict['name']
        self.seats_total = info_dict['seats']['capacity']
        self.seats_filled = info_dict['seats']['actual']
        self.seats_remaining = info_dict['seats']['remaining']
        self.waitlist_total = info_dict['waitlist']['capacity']
        self.waitlist_filled = info_dict['waitlist']['actual']
        self.waitlist_remaining = info_dict['waitlist']['remaining']
        self.section = info_dict['section']
        self.schedule = OscarCourseSchedule(location_list)

    def refresh_seats_and_waitlist(self):
        info_dict = _get_crn_info(self.department, self.course_number,
                                  self.year, self.semester, self.crn)
        self.seats_total = info_dict['seats']['capacity']
        self.seats_filled = info_dict['seats']['actual']
        self.seats_remaining = info_dict['seats']['remaining']
        self.waitlist_total = info_dict['waitlist']['capacity']
        self.waitlist_filled = info_dict['waitlist']['actual']
        self.waitlist_remaining = info_dict['waitlist']['remaining']

class OscarCourseSchedule:
    def __init__(self, location_list):
        self.class_list = []
        for entry in location_list:
            out_dict = {}
            out_dict['start_time'] = time.strptime(entry['time'][0], '%H:%M')
            out_dict['end_time'] = time.strptime(entry['time'][1], '%H:%M')
            out_dict['professor'] = entry['prof']
            out_dict['type'] = entry['type']
            out_dict['location'] = entry['location']
            out_dict['days'] = entry['day']
            self.class_list.append(out_dict)

    def is_in_class_at_time(self, time_in):
        day_of_week = 'MTWRFSU'[time_in.tm_wday] # tm_wday is in [0, 6], 0 is monday 6 is sunday
        time_in.tm_wday = 0 # ensure that comparison operators don't consider the day of the week
        for session in self.class_list:
            # do we go to this class today?
            if session['days'].find(day_of_week) > 0:
                # if so, is this time within the time that we are in class?
                if time_in < session['end_time'] and time_in > session['start_time']:
                    return True
        return False
        

def get_courses_by_department(department):
    out_list = []
    course_list = _get_courses_by_department(department)
    for course in course_list:
        out_list.append(OscarCourse(department, course['number']))
    return out_list
        
# this is a "private" function and shouldn't be used outside this file. The above
# function wraps this functionality for outside use.
def _get_courses_by_department(department):
    if not department.lower() in DEPARTMENT_LIST:
        raise OscarException('Invalid department: {}'.format(department))
    response = requests.get(OSCAR_API_BASE_URL + department.lower())
    if response.status_code >= 300:
        raise OscarException('HTTP response had status code > 300: {}'.format(response.status_code))
    course_list = response.json()
    return course_list

def _get_course_info(department, course_number):
    if not department.lower() in DEPARTMENT_LIST:
        raise OscarException('Invalid department: {}'.format(department))
    response = requests.get(OSCAR_API_BASE_URL + department.lower() + "/" + course_number)
    if response.status_code >= 300:
        raise OscarException('HTTP response had status code > 300: {}'.format(response.status_code))
    class_info = response.json()
    return class_info

def _get_course_sections(department, course_number, year, semester):
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

def _get_crn_info(department, course_number, year, semester, crn_number):
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