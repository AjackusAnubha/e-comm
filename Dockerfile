FROM python:latest
# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app/

# Install the required dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the port that Django will run on
EXPOSE 8000

# Command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
