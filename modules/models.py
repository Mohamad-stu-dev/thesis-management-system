from . import database
import datetime

class student:
    def __init__(self, student_id, password,first_name, last_name , courses=None):
        self.student_id=student_id
        self.password=password
        self.first_name=first_name
        self.last_name=last_name
        self.courses=courses if courses is not None else []

    def to_dict(self):

        return {
            "student_id" : self.student_id,
            "password" : self.password,
            "first_name" : self.first_name,
            "last_name" : self.last_name,
            "courses" : self.courses
        }

    @classmethod
    def get_all_students (cls):
        all_students_data = database.load_data("students.json")
        return [cls(**data) for data in all_students_data]

    @classmethod
    def save_all(cls , students_list):
        data_to_save = [student.to_dict() for student in students_list]
        database.save_data("students.json" , data_to_save)


    @classmethod
    def find_by_id(cls, student_id):
        all_student_data=cls.get_all_students()
        for student in all_student_data:
            if student.student_id == student_id:
                return student
        return None


    def save(self):

        all_students = self.__class__.get_all_students()
        
        found = False
        for i, student in enumerate(all_students):
            if student.student_id == self.student_id:
                all_students[i] = self  
                found = True
                break
        
        if not found:
            all_students.append(self)
            
        self.__class__.save_all(all_students)


class Professor:
    
    def __init__(self, professor_id, password, first_name, last_name, expertise=None, supervision_capacity=5, judgement_capacity=10):
        self.professor_id = professor_id
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.expertise = expertise if expertise is not None else []
        self.supervision_capacity = supervision_capacity
        self.judgement_capacity = judgement_capacity


    def to_dict(self):

        return {
            "professor_id": self.professor_id,
            "password": self.password,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "expertise": self.expertise,
            "supervision_capacity": self.supervision_capacity,
            "judgement_capacity": self.judgement_capacity
        }

    def save(self):
        
        all_professors = self.__class__.get_all_professors()
        
        found = False
        for i, prof in enumerate(all_professors):
            if prof.professor_id == self.professor_id:
                all_professors[i] = self
                found = True
                break
        
        if not found:
            all_professors.append(self)
            
        self.__class__.save_all(all_professors)

    @classmethod
    def find_by_id(cls, professor_id):
        
        all_professors_data = database.load_data('professors.json')
        for prof_data in all_professors_data:
            if prof_data['professor_id'] == professor_id:
                return cls(**prof_data)
        return None

    @classmethod
    def get_all_professors(cls):
        
        all_professors_data = database.load_data('professors.json')
        return [cls(**data) for data in all_professors_data]

    @classmethod
    def save_all(cls, professors_list):
        
        data_to_save = [prof.to_dict() for prof in professors_list]
        database.save_data('professors.json', data_to_save)



class Course:
   
   
    def __init__(self, course_id, title, professor_id, year, semester, capacity, unit):
        self.course_id = course_id
        self.title = title
        self.professor_id = professor_id
        self.year = year
        self.semester = semester
        self.capacity = capacity
        self.unit = unit

    
    def to_dict(self):
        
        return {
            "course_id": self.course_id,
            "title": self.title,
            "professor_id": self.professor_id,
            "year": self.year,
            "semester": self.semester,
            "capacity": self.capacity,
            "unit": self.unit
        }

    def save(self):
        all_courses = self.__class__.get_all_courses()
        
        found = False
        for i, course in enumerate(all_courses):
            if course.course_id == self.course_id:
                all_courses[i] = self
                found = True
                break
        
        if not found:
            all_courses.append(self)
            
        self.__class__.save_all(all_courses)

    @classmethod
    def find_by_id(cls, course_id):
        all_courses_data = database.load_data('courses.json')
        for course_data in all_courses_data:
            if course_data['course_id'] == course_id:
                return cls(**course_data)
        return None

    @classmethod
    def get_all_courses(cls):
        all_courses_data = database.load_data('courses.json')
        return [cls(**data) for data in all_courses_data]

    @classmethod
    def save_all(cls, courses_list):
        data_to_save = [course.to_dict() for course in courses_list]
        database.save_data('courses.json', data_to_save)


class thesis:
    def __init__(self, student_id, course_id, supervisor_id, thesis_id = None, 
                 status = "pending_approval", request_date=None , title=None ,
                 abstract=None, key_word=None, thesis_path =None ,
                  defense_date=None, judges=None, grade=None
                ):
   
        self.thesis_id = thesis_id if thesis_id is not None else int(datetime.datetime.now().timestamp())
        self.student_id = student_id
        self.course_id = course_id
        self.supervisor_id = supervisor_id
        self.status = status
        self.request_date = request_date if request_date is not None else datetime.datetime.now()
        self.title = title
        self.abstract = abstract
        self.key_word = key_word if key_word is not None else []
        self.thesis_path = thesis_path
        self.defense_date = defense_date
        self.judges = judges if judges is not None else []
        self.grade = grade
    
    def to_dict(self):
        return {
            "thesis_id" : self.thesis_id,
            "student_id" : self.student_id,
            "course_id" : self.course_id,
            "supervisor_id" : self.supervisor_id,
            "status" : self.status,
            "request_date" : self.request_date,
            "title" : self.title,
            "abstract" : self.abstract,
            "key_word" : self.key_word,
            "thesis_path" : self.thesis_path,
            "defense_date" : self.defense_date,
            "judges" : self.judges,
            "grade" : self.grade
        }

    @classmethod
    def get_all_theses(cls):
        all_theses_data=database.load_data("theses.json")
        return [cls(**data) for data in all_theses_data]


    def save(self):
        all_theses = self.__class__.get_all_theses()
        
        found = False
        for i, thesis in enumerate(all_theses):
            if thesis.thesis_id == self.thesis_id:
                all_theses[i] = self
                found = True
                break
        
        if not found:
            all_theses.append(self)
            
        self.__class__.save_all(all_theses)

    @classmethod
    def find_by_id(cls, thesis_id):
        all_theses=cls.get_all_theses()
        for thesis in all_theses:
            if thesis.thesis_id == thesis_id:
                return thesis
        return None
    
    @classmethod
    def save_all(cls,theses_list):
        data_to_save = [thesis.to_dict() for thesis in theses_list]
        database.save_data("theses.json" , data_to_save)

    def approve(self):
        self.status = "approved"
        self.save()

    def reject(self):
        self.status = "rejected"
        self.save()

    def get_student(self):
        student_id_to_find = self.student_id
        student_object = student.find_by_id(student_id_to_find)
        return student_object
    
    def get_supervisor(self):
        return Professor.find_by_id(self.supervisor_id)
    
    def request_defense(self, title, abstract, keywords, thesis_file_path):
        if self.status != "approved":
            print("you can not request defense when status is not approved")
            return False
        thesis = Thesis(title, abstract, keywords, thesis_file_path, self)
        self.title = title
        self.abstract = abstract
        self.keywords = keywords
        self.thesis_file_path = thesis_file_path
        self.status = "defense_requested"
        self.save()

        print("defense requested")
        return True
            