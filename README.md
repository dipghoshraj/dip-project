# Flask Gunicorn Dockerized

This project demonstrates how to containerize a Flask application using Gunicorn and Docker.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
  - [Build Docker Image](#build-docker-image)
  - [Run Docker Container](#run-docker-container)
- [Accessing the Application](#accessing-the-application)
- [Configuration](#configuration)
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
    docker build -t proj-call .
    docker run -p 3000:3000 proj-call
    

### Accessing the Application
Open your web browser and navigate to http://localhost:3000 to access the rails application.


### Configuration
Create a .env file in the project root with the following content, and update the values with your actual database details
```bash
DB_URL=xxxx
DB_USERNAME=xxxx
DB_PASSWORD=xxxx
REDIS_URL=xxxx
DB_NAME=xxx
```

### Customization
- Modify model and controller to customize your rails application.
- Adjust the Dockerfile if additional dependencies or configuration are needed.
- Update the gemfile with your specific gems requirements.


### License
This project is licensed under the MIT License - see the LICENSE file for details.