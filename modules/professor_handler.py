from modules import models


def show_professor_dashboard(professor_object):

    print(f"Welcome, Professor {professor_object.first_name} {professor_object.last_name}!")


    while True:
        print("\n--- Professor Menu ---")
        print("1. View and Manage Thesis Requests")
        print("2. View and Manage Defense Requests")
        print("3. Search in Thesis Archive")
        print("4. Logout")

        choice = input("Please select an option: ")

        if choice == "1":
            manage_thesis_requests(professor_object)
        elif choice == "2":
            manage_defense_requests(professor_object)
        elif choice == "3":
            search_theses()
        elif choice == "4":
            print("Logging out...")
            break
        else:
            print("Error: Invalid option. Please enter a number between 1 and 4.")


def manage_thesis_requests(professor_object):
    all_theses = models.thesis.get_all_theses()
    pending_requests = []
  
    for thesis in all_theses:
        if thesis.supervisor_id == professor_object.professor_id and thesis.status == "pending_approval":
            pending_requests.append(thesis)

    if not pending_requests:
        print("You have no new thesis requests at the moment.")
        return

    print("your pending thesis requests are:")
    for i, thesis in enumerate(pending_requests, start=1):
        student = models.student.find_by_id(thesis.student_id)
        student_name = (
            f"{student.first_name} {student.last_name}" if student else "unknown"
        )

        print(f"\n{i}. Request from: {student_name} (Student ID: {thesis.student_id})")
        print(f"   Course ID: {thesis.course_id}")
        print(f"   Request Date: {thesis.request_date}")

    try:
        choice_index = int(
            input(
                "\nEnter the number of the request you want to manage (or 0 to cancel): "
            )
        )
        if not (0 <= choice_index <= len(pending_requests)):
            print("Error: Invalid number. Returning to menu.")
            return
    except ValueError:
        print("Error: Please enter a valid number. Returning to menu.")
        return

    if choice_index == 0:
        print("Operation cancelled.")
        return

    selected_thesis = pending_requests[choice_index - 1]
    action = input(
        f"Do you want to (A)pprove or (R)eject this request? [A/R]: "
    ).upper()

    if action == "A":
        selected_thesis.approve()
        print("Success: The request has been approved.")
    elif action == 'R':
        selected_thesis.reject()
        course = models.Course.find_by_id(selected_thesis.course_id)
        if course:
            course.capacity += 1
            course.save()
            print("Success: The request has been rejected and the course capacity has been restored.")
        else:
            print("Success: The request has been rejected.")


def manage_defense_requests(professor_object):
    all_theses = models.thesis.get_all_theses()
    defense_requests = []
    for thesis in all_theses:
        if (
            thesis.supervisor_id == professor_object.professor_id
            and thesis.status == "defense_requested"
        ):
            defense_requests.append(thesis)

    if not defense_requests:
        print("You have no pending defense requests to manage.")
        return

    print("Here is a list of submitted theses awaiting defense management:")
    for i, thesis in enumerate(defense_requests, 1):
        student = models.Student.find_by_id(thesis.student_id)
        student_name = (
            f"{student.first_name} {student.last_name}" if student else "Unknown"
        )

        print(f"\n{i}. Student: {student_name}")
        print(f"   Thesis Title: {thesis.title}")
        print(f"   Abstract: {thesis.abstract}")
        print(f"   Keywords: {', '.join(thesis.keywords)}")
        print(f"   Submitted File Path: {thesis.thesis_file_path}")

    try:
        choice_index = int(
            input(
                "\nEnter the number of the thesis you want to grade (or 0 to cancel): "
            )
        )
        if not (0 <= choice_index <= len(defense_requests)):
            print("Error: Invalid number.")
            return
    except ValueError:
        print("Error: Please enter a valid number.")
        return
    
    if choice_index == 0:
        print("Operation cancelled.")
        return
    selected_thesis = defense_requests[choice_index - 1]

    grade = input("Enter the final grade for this thesis (e.g., A, B, C, D): ").upper()
    if grade not in ["A", "B", "C", "D", "F"]:
        print("Error: Invalid grade. Please use A, B, C, D, or F.")
        return

    selected_thesis.grade = grade
    selected_thesis.status = "completed"
    selected_thesis.save()

    print(
        f"\nSuccess! The grade '{grade}' has been registered for the thesis '{selected_thesis.title}'."
    )
    print("The thesis process is now complete.")


def search_theses():
    print("\n--- Search in Thesis Archive ---")

    query = input(
        "Enter a keyword to search by title, author, or keyword (or leave blank to see all): "
    ).lower()

    all_theses = models.thesis.get_all_theses()
    completed_theses = [t for t in all_theses if t.status == "completed"]

    if not completed_theses:
        print("The thesis archive is currently empty.")
        return

    results = []
    for thesis in completed_theses:
        student = models.student.find_by_id(thesis.student_id)
        supervisor = models.Professor.find_by_id(thesis.supervisor_id)

        search_content = f"{thesis.title} {' '.join(thesis.keywords)}".lower()
        if student:
            search_content += f" {student.first_name} {student.last_name}".lower()
        if supervisor:
            search_content += f" {supervisor.first_name} {supervisor.last_name}".lower()

        if query in search_content:
            results.append((thesis, student, supervisor))

    if not results:
        print(f"No results found for '{query}'.")
        return

    print(f"\nFound {len(results)} result(s):")
    for thesis, student, supervisor in results:
        student_name = f"{student.first_name} {student.last_name}" if student else "N/A"
        supervisor_name = (
            f"{supervisor.first_name} {supervisor.last_name}" if supervisor else "N/A"
        )

        print("\n" + "-" * 20)
        print(f"Title: {thesis.title}")
        print(f"Author: {student_name}")
        print(f"Supervisor: {supervisor_name}")
        print(f"Keywords: {', '.join(thesis.keywords)}")
        print(f"Grade: {thesis.grade}")
        print(f"File Path: {thesis.thesis_file_path}")
