# Thesis Management System

## 1. Project Overview

This project is a command-line interface (CLI) application for managing the academic thesis process in a university setting. It provides a comprehensive and user-friendly system for students and professors to handle all stages of a thesis, from course selection to final grading and archiving. The system is built using Python and utilizes JSON files for data storage, simulating a lightweight database.

The primary goal of this project is to create a modular, object-oriented application that effectively models real-world academic workflows.

---

## 2. Core Features

The system is divided into two main user roles, each with a dedicated dashboard and set of functionalities:

### Student Features:
- **Secure Login:** Students can log in using their unique student ID and password.
- **Course Selection:** View a list of available thesis courses, including supervisor details and capacity.
- **Request Submission:** Submit a request to enroll in a thesis course.
- **Status Tracking:** Check the status of their requests (Pending, Approved, Rejected).
- **Defense Submission:** Once a thesis is approved and completed, students can submit it for defense by providing a title, abstract, keywords, and a file path.
- **Archive Search:** Search through a historical archive of all completed and graded theses.

### Professor Features:
- **Secure Login:** Professors can log in using their unique professor ID and password.
- **Request Management:** View and manage incoming thesis requests from students, with the ability to **Approve** or **Reject** them.
- **Defense Management:** Review submitted theses from their students.
- **Grading:** Assign a final grade (A, B, C, D, F) to a completed thesis, which marks the process as complete.
- **Archive Search:** Search the thesis archive.

---

## 3. Project Structure

The project is organized into a modular structure to ensure separation of concerns and maintainability.


- **`data/`**: Contains the JSON files that act as the database for the application.
- **`modules/`**: A Python package containing the core logic of the application.
  - **`database.py`**: Handles all read and write operations for the JSON files.
  - **`models.py`**: Defines the data structures of the application using classes (`Student`, `Professor`, `Course`, `Thesis`).
  - **`auth.py`**: Manages user authentication (login).
  - **`student_handler.py`**: Contains all logic related to the student's dashboard and actions.
  - **`professor_handler.py`**: Contains all logic related to the professor's dashboard and actions.
- **`main.py`**: The entry point of the application. It runs the main menu and directs users to the appropriate dashboards after successful login.
- **`README.md`**: This documentation file.

---

## 4. How to Run the Project

### Prerequisites:
- Python 3.x installed on your system.

### Steps:
1.  **Clone the repository** or download the project files to your local machine.
2.  **Navigate to the project's root directory** in your terminal.
    ```bash
    cd path/to/thesis-management-system
    ```
3.  **Run the application** using the following command:
    ```bash
    python main.py
    ```
4.  The main menu will appear. Follow the on-screen instructions to log in as a student or professor and interact with the system.

### Sample Login Credentials:
You can use the data provided in the `data/` directory to test the system.

- **Student Example:**
  - **ID:** `s1002`
  - **Password:** `pass2`

- **Professor Example:**
  - **ID:** `p202`
  - **Password:** `prof2`

---

## 5. Key Implementation Details

- **Object-Oriented Programming:** The system is heavily based on OOP principles. Data entities are modeled as classes, encapsulating both data (attributes) and behavior (methods).
- **Data Persistence:** All data is stored in JSON format, which is both human-readable and easy to parse in Python. The `database.py` module provides a clean interface for data handling.
- **Modularity:** The code is split into logical modules (`auth`, `models`, `handlers`), making it easy to understand, debug, and extend.
- **State Management:** The status of a thesis (e.g., `pending_approval`, `approved`, `defense_requested`, `completed`) is managed within the `Thesis` model, driving the application's workflow.
- **Error Handling:** The application includes `try-except` blocks to handle common errors, such as invalid user input (e.g., entering text instead of a number), ensuring a smoother user experience.
