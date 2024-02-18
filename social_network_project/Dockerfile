# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /code

# Install dependencies
COPY requirement.txt /code/
RUN pip install --no-cache-dir -r requirement.txt

# Copy the current directory contents into the container at /code/
COPY . /code/

# Collect static files
RUN python manage.py makemigrations
RUN python manage.py migrate

# Run Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "social_network_project.wsgi:application"]
