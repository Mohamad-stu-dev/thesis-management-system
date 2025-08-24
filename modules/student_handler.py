from . import models


def show_student_dashboard(student_object):
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
            """
            available thesis courses(capacity)and handles the student's request to take one.
            """
            print("\n--- Request a Thesis Course ---")
            all_courses = models.Course.get_all_courses()
            available_courses = [
                course for course in all_courses if course.capacity > 0
            ]
            if not available_courses:
                print("No available courses. Please try again later.")
                return

            for i, course in enumerate(available_courses, 1):
                professor = models.Professor.find_by_id(course.supervisor_id)

                print(f"{i}.course title : {course.title}")
                print(f"course id : {course.course_id}")
                print(f"supervisor : {professor.first_name} {professor.last_name}")
                print(f"capacity : {course.capacity}")

                choice = int(
                    input(
                        "Enter the number of the course you want to request: (0 for cancel request) "
                    )
                )
                try:
                    if not 0 <= choice <= len(available_courses):
                        print("Error: invalid input")
                        return
                except ValueError:
                    print("Error: invalid input")
                    return
                if choice == 0:
                    print("Request canceled.")
                    return
                selected_course = available_courses[choice - 1]
                selected_course.capacity -= 1

                new_thesis_req = models.thesis(
                    student_id=student_object.student_id,
                    course_id=selected_course.course_id,
                    supervisor_id=selected_course.professor_id,
                )
                new_thesis_request.save()
                print(
                    "\nSuccess! Your request has been submitted and is waiting for supervisor approval."
                )

        def handle_defense_request(student_object):
            """
            Allows a student to submit a defense request for an approved thesis.
            """
            print("\n--- Submit a Defense Request ---")

            all_theses = models.get_all_theses()

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
                    "\nAn error occurred while submitting your request. Please check the status and try again."
                )
