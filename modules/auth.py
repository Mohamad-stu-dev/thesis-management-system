from . import models


def log_in(user_id, password):

    user = models.student.find_by_id(user_id)

    if user is not None and user.password == password:
        return user, "student"

    user = models.Professor.find_by_id(user_id)

    if user is not None and user.password == password:
        return user, "professor"

    return None, "user not found"
