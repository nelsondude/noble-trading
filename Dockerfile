# Use an official Python runtime as a parent image
FROM python:3

# Make port 8888 available to the world outside this container
EXPOSE 8888

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements/common.txt



# Run app.py when the container launches
CMD ["python", "app.py"]