from modules import auth
from modules import student_handler
from modules import professor_handler

def main():
    print("=" * 50)
    print(" Welcome to the University Thesis Management System")
    print("=" * 50)

    while True:
        print("\n--- Main Menu ---")
        print("1. Login")
        print("2. Exit")
        
        choice = input("Please select an option: ")

        if choice == '1':
            user_id = input("Enter your ID: ")
            password = input("Enter your password: ")

            logged_in_user, user_role = auth.log_in(user_id, password)

            if logged_in_user:
                if user_role == "student":
                    student_handler.student_dashboard_menu(logged_in_user)
                elif user_role == "professor":
                    professor_handler.show_professor_dashboard(logged_in_user)
                
                print("\nYou have been successfully logged out.")

            else:
                print("\nLogin failed. Invalid ID or password. Please try again.")
        
        elif choice == '2':
            print("Thank you for using the system. Goodbye!")
            break
        
        else:
            print("Invalid option. Please choose 1 or 2.")


if __name__ == "__main__":
    main()
