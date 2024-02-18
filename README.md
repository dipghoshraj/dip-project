# Django Project with Docker Compose

This is a sample Django project configured to run with Docker Compose.

## Requirements

- Docker
- Docker Compose

## Setup

1. Clone the repository:

```bash
git clone git@github.com:dipghoshraj/dip-project.git
cd your_project
```



2. Create a .env file in the project directory and specify environment variables:

```bash
DB_NAME=socialnetwork
DB_USER=pandatoto
DB_PASSWORD=u4P0cqvXnLZqsmOZgR1s
DB_HOST=database-1.cjism6my0w9w.ap-south-1.rds.amazonaws.com
DB_PORT=3306
```


3. Build the Docker containers:
```bash
docker-compose build
```

4. Run the Docker containers:
```bash
docker-compose up
```