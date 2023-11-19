# Flask Gunicorn Dockerized

This project demonstrates how to containerize a Flask application using Gunicorn and Docker.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
  - [Build Docker Image](#build-docker-image)
  - [Run Docker Container](#run-docker-container)
- [Accessing the Application](#accessing-the-application)
- [Project Structure](#project-structure)
- [Customization](#customization)
- [License](#license)

## Prerequisites

Before you begin, ensure you have the following installed:

- [Docker](https://www.docker.com/)
- [Git](https://git-scm.com/)

## Getting Started

### Build Docker Image

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/proj-call.git
   cd proj-call

2. Run the Docker container:
    ```bash 
    docker-compose up --build

### Accessing the Application
Open your web browser and navigate to http://localhost:5000 to access the Flask application.

### Project Structure
- Dockerfile: Specifies the Docker container configuration.
- requirements.txt: Lists the Python dependencies for the Flask application.
- app.py: The main entry point for the Flask application.
- wsgi.py: WSGI handler for Gunicorn.
- handler: has the main controllers for the projects
- model: holds the db model for the project
- setup a .env file with in the project directory with required informations


### Customization
- Modify app.py, model and handler to customize your Flask application.
- Adjust the Dockerfile if additional dependencies or configuration are needed.
- Update the requirements.txt file with your specific Python package requirements.


### License
This project is licensed under the MIT License - see the LICENSE file for details.