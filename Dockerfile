# Start with a Python 3.9 Alpine base image
FROM python:3.9-alpine

# Make container run predictably
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Install system dependencies
RUN apk add gcc musl-dev mysql-dev

# Set the working directory
WORKDIR /app

# Copy the project files to the working directory
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


# Set up the media directory as a volume
VOLUME /app/media

# Expose port 8000
EXPOSE 8000

# Run migrations and start the server
CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000
