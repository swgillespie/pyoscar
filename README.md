PyOscar
============

PyOscar provides a Python interface to get data from the Georgia Tech class catalog. 

```python
>>> import pyoscar
>>> print pyoscar.get_courses_by_department('math')

(lots of output)

>>> print pyoscar.get_course_info('math', '2406')

{u'creditHours': [3],
 u'description': u'A proof-based development of linear algebra and vector spaces, with additional topics such as multilinear algebra and group theory.',
 u'grade_basis': u'ALP',
 u'labHours': [None],
 u'lectureHours': [3],
 u'name': u'Abstract Vector Spaces'}
 
>>> print pyoscar.get_course_sections('math', '2406', '2013', 'fall')

[{u'crn': u'85426',
  u'section': u'F1',
  u'where': [{u'day': u'TR',
    u'location': u'Skiles 257',
    u'prof': u'Guillermo H. Goldsztein (P)',
    u'time': [u'12:05', u'13:25'],
    u'type': u'Lecture'}]},
 {u'crn': u'90860',
  u'section': u'F2',
  u'where': [{u'day': u'TR',
    u'location': u'Skiles 311',
    u'prof': u'Kirsten G Wickelgren (P)',
    u'time': [u'12:05', u'13:25'],
    u'type': u'Lecture'}]}]
    
>>> print pyoscar.get_crn_info('math', '2406', '2013', 'fall', '90860')

{u'name': u'Abstract Vector Spaces',
 u'seats': {u'actual': u'31', u'capacity': u'35', u'remaining': u'4'},
 u'section': u'F2',
 u'waitlist': {u'actual': u'4', u'capacity': u'12', u'remaining': u'8'}}

```

Many thanks to:
* cobookman - https://github.com/cobookman/schedule/ - Without his API this would not be possible.
* requests - http://docs.python-requests.org/
