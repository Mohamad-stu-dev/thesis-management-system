# فایل: modules/auth.py

from modules import models

def log_in(user_id, password):
    """
    Authenticates a user by checking both students and professors.
    Returns the user object and their role if successful, otherwise None.
    """
    
    student_user = models.student.find_by_id(user_id)
    if student_user:
        
        if student_user.password == password:
            return student_user, "student"
        else:
            return None, None

  
    professor_user = models.Professor.find_by_id(user_id)
    if professor_user:
      
        if professor_user.password == password:
          
            return professor_user, "professor"
        else:
        
            return None, None
    return None, None
