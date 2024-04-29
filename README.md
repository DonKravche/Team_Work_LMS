# Learning Management System (LMS) Django Project

Welcome to the Learning Management System (LMS) Django project! This system is designed to help educational institutions manage their faculties, subjects, lectures, and students efficiently.

## What is Django?

[Django](https://www.djangoproject.com/) is a high-level Python web framework that encourages rapid development and 
clean, pragmatic design. It provides a powerful set of tools for building web applications.

## Project Structure

### Models

In this project, we have the following models:

- **Faculty**: Represents a department or division within the educational institution.
- **Subject**: Describes a specific course offered within a faculty. Each subject has a title, description, syllabus file, and can be taught by multiple lecturers.
- **Lecture**: Represents an instructor who teaches subjects.
- **Student**: Describes a student enrolled in the institution, associated with a user account and a specific faculty.

### Views

Views are Python functions that take web requests and return web responses. In our project, we have the following views:

- **home**: Displays the homepage of the application.
- **login_user**: Renders the login page for users to log into the system.
- **register**: Handles the registration process for new users.
- **login_**: Authenticates users and logs them into the system.
- **students_page**: Manages the page where students can choose their subjects.

### Forms

Forms are used to collect and validate user input. We have the following forms:

- **UserRegistrationForm**: Allows users to register with the system, providing their username, password, name, surname, and faculty.
- **UserLoginForm**: Provides a login form for users to enter their credentials.

### URLs

URLs define the mapping between URL paths and views. Here are the main URLs(endpoints) in our project:

- **/home/**: Accesses the homepage of the application.
- **/register/**: Allows users to register for an account.
- **/login/**: Handles user authentication and login.
- **/students_page/**: Enables students to select their subjects.

## Getting Started

To run this project locally, follow these steps:

1. Clone this repository to your local machine.
    ```
    git clone https://github.com/DonKravche/Team_Work_LMS.git
    ```
2. Make sure you have Python and Django installed.
3. Install project dependencies by running:
    ```
    pip install -r requirements.txt
    ```
4. Apply migrations by running:
    ```
    python manage.py migrate
    ```
5. Start the Django development server:
    ```
    python manage.py runserver
    ```
6. Open your web browser and go to http://localhost:8000/home/ to access the application.


## Endpoints

- https://localhost:8000/home/ - Home page

- http://localhost:8000/student/register/ - Register page  

- http://localhost:8000/student/login/ - Login page 

- https://localhost:8000/students_page/ - Students page

- https://localhost:8000/admin/ - Default Admin page     


## Contributors
- [Don_Kravche](Giorgi Kravchenko)
- [iraklius9](Irakli Meparishvili)
- [Gvantsie](Gvantsa Euashvili)

