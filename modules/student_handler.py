from modules import models


def student_dashboard_menu(student_object):
    print(f"/n welcome {student_object.first_name} {student_object.last_name}")

    while True:
        print("----student menu----")
        print("1. View and Request Thesis Courses")
        print("2. View My Requests Status")
        print("3. Submit Defense Request")
        print("4. Search in Thesis Archive")
        print("5. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            # Call the function to handle course requests
            handle_thesis_request(student_object)
        elif choice == "2":
            # Call the function to view request status
            view_request_status(student_object)
        elif choice == "3":
            # Call the function to handle defense requests
            handle_defense_request(student_object)
        elif choice == "4":
            # Call the search function
            search_theses()
        elif choice == "5":
            print("Logging out...")
            break  # Exit the while loop and return to main.py
        else:
            print("Error: Invalid option. Please enter a number between 1 and 5.")

def view_request_status(student_object):
            print("\n--- Status of Your Requests ---")
            student_theses = []
            all_theses = models.thesis.get_all_theses()
            for thesis in all_theses:
                if thesis.student_id == student_object.student_id:
                    student_theses.append(thesis)

                if not student_theses:
                    print("you have no requests")
                    return

                for i, thesis in enumerate(student_theses, 1):
                    course = models.Course.find_by_id(thesis.course_id)
                    supervisor = models.Professor.find_by_id(thesis.supervisor_id)

                    print(f"\n{i} for course : {course.title if course else 'UNKNOWN'}")
                    print(
                        f"supervisor : {supervisor.first_name if supervisor else ' '} {supervisor.last_name if supervisor else ' '}"
                    )
                    print(f"status : {thesis.status.replace('_', ' ').title() }")
                    if thesis.title:
                        print(f"   Thesis Title: {thesis.title}")

def handle_thesis_request(student_object):
    print("\n--- Request a Thesis Course ---")

    all_courses = models.Course.get_all_courses()
    available_courses = [course for course in all_courses if course.capacity > 0]

    if not available_courses:
        print("No available courses with capacity. Please try again later.")
        return

    print("Here are the available thesis courses:")
    for i, course in enumerate(available_courses, 1):
        professor = models.Professor.find_by_id(course.professor_id)
        professor_name = f"{professor.first_name} {professor.last_name}" if professor else "N/A"
        
        print(f"\n{i}. Course Title: {course.title}")
        print(f"   Course ID: {course.course_id}")
        print(f"   Supervisor: {professor_name}")
        print(f"   Capacity: {course.capacity}")

    try:
        choice = int(input("\nEnter the number of the course you want to request (or 0 to cancel): "))
        if not (0 <= choice <= len(available_courses)):
            print("Error: Invalid number. Returning to menu.")
            return
    except ValueError:
        print("Error: Please enter a valid number. Returning to menu.")
        return

    if choice == 0:
        print("Operation cancelled.")
        return

    selected_course = available_courses[choice - 1]
    selected_course.capacity -= 1
    selected_course.save()

    new_thesis_request = models.thesis(
        student_id=student_object.student_id,
        course_id=selected_course.course_id,
        supervisor_id=selected_course.professor_id
    )
    new_thesis_request.save()

    print(f"\nSuccess: Your request for the course '{selected_course.title}' has been submitted.")
    print("Please wait for the supervisor's approval.")


def handle_defense_request(student_object):
            """
            Allows a student to submit a defense request for an approved thesis.
            """
            print("\n--- Submit a Defense Request ---")

            all_theses = models.thesis.get_all_theses()

            approved_thesis = None
            for thesis in all_theses:
                if (
                    thesis.student_id == student_object.student_id
                    and thesis.status == "approved"
                ):
                    approved_thesis = thesis
                    break
            if not approved_thesis:
                print("Error: You don't have an approved thesis.")
                return

            print(
                f"\nYou are submitting a defense request for the thesis related to Course ID: {approved_thesis.course_id}"
            )
            print("Please provide the final details for your thesis.")

            try:
                title = input("Enter the final title of your thesis: ")
                abstract = input("Enter the abstract of your thesis: ")
                keywords_str = input(
                    "Enter keywords, separated by commas (e.g., AI, Python, NLP): "
                )
                keywords = [keyword.strip() for keyword in keywords_str.split(",")]
                print(
                    "\nNote: For file uploads, please provide the full path to the file on your computer."
                )
                pdf_path = input("Enter the path to your final thesis PDF file: ")

                if not title or not abstract or not keywords or not pdf_path:
                    print("\nError: All fields are required. Please try again.")
                    return

            except Exception as e:
                print(f"\nAn error occurred while gathering input: {e}")
                return

            success = approved_thesis.request_defense(
                title=title,
                abstract=abstract,
                keywords=keywords,
                thesis_file_path=pdf_path,
            )

            if success:
                print("\nSuccess! Your defense request has been submitted.")
                print(
                    "Your supervisor will now review it and schedule the defense session."
                )
            else:
              
                print(
                    "\nAn error occurred while submitting your request. Please check the status and try again.")



def search_theses():
    print("\n--- Search in Thesis Archive ---")

    query = input("Enter a keyword to search by title, author, or keyword (or leave blank to see all): ").lower()

    all_theses = models.thesis.get_all_theses()
    completed_theses = [t for t in all_theses if t.status == "completed"]

    if not completed_theses:
        print("The thesis archive is currently empty.")
        return

    results = []
    for thesis in completed_theses:
        student = models.Student.find_by_id(thesis.student_id)
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
        supervisor_name = f"{supervisor.first_name} {supervisor.last_name}" if supervisor else "N/A"

        print("\n" + "-" * 20)
        print(f"Title: {thesis.title}")
        print(f"Author: {student_name}")
        print(f"Supervisor: {supervisor_name}")
        print(f"Keywords: {', '.join(thesis.keywords)}")
        print(f"Grade: {thesis.grade}")
        print(f"File Path: {thesis.thesis_file_path}")
    print("-" * 20)


