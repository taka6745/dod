# Doctor Rostering System

## Overview
The Doctor Rostering System is a web application that allows doctors to submit their rosters and administrators to manage them. It is built using FastAPI, SQLAlchemy, and Jinja2 for templating.

## Project Structure
- **app/**: Contains the main application code.
  - **main.py**: Entry point of the FastAPI application.
  - **services/**: Contains service modules for database interactions.
    - **database.py**: Database connection setup.
    - **doctor_service.py**: Functions for managing doctors.
    - **roster_service.py**: Functions for managing rosters.
    - **models.py**: SQLAlchemy models for the database.
  - **templates/**: HTML templates for rendering web pages.
  - **static/**: Static files like CSS.
- **requirements.txt**: List of Python dependencies.
- **Dockerfile**: Docker configuration for containerizing the application.
- **docker-compose.yml**: Docker Compose configuration for setting up the application and its dependencies.
- **init.sql**: SQL script for initializing the database.

## Prerequisites
- Docker and Docker Compose installed on your machine.
- A secure connection to the database. Follow the instructions on [serveradmin.takodamundy.tech](https://serveradmin.takodamundy.tech) to set up a secure connection.

## Setup Instructions
1. **Clone the repository:**
   ```sh
   git clone https://github.com/taka6745/dod.git
   cd doctor-rostering
   ```

2. **Create a `.env` file:**
   Create a `.env` file in the root directory with the following content:
   ```env
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=your_db_host
   DB_PORT=your_db_port
   DB_NAME=your_db_name
   ```

3. **Build and run the application using Docker Compose:**
   ```sh
   docker-compose up --build
   ```

4. **Access the application:**
   Open your web browser and go to `http://localhost:8000`.

## How It Works
- **Home Page:** Provides links to the doctor's side and the admin side.
- **Doctor's Side:** Doctors can submit their rosters.
- **Admin Side:** Administrators can manage rosters and export data.

## Database Initialization
To initialize the database, run the SQL script `init.sql` on your MySQL server. This script creates the necessary tables and a user with the required privileges.

## Important Files
- **app/main.py**: Contains the FastAPI routes and application setup.
- **app/services/database.py**: Manages the database connection.
- **app/services/models.py**: Defines the database models.
- **app/templates/**: Contains the HTML templates for the web pages.
- **app/static/style.css**: Contains the CSS for styling the web pages.

For more detailed information, refer to the code and comments within the project files.

## License
This project is licensed under the MIT License.
