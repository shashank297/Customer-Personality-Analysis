# Use a base image with Python 3.8
FROM python:3.8-slim-buster

# Set the working directory
WORKDIR /home

# Copy the application files into the container
COPY . /home

# Update and install necessary packages
RUN apt-get update -y && apt-get install -y awscli

# Install Python dependencies
RUN pip install -r requirements.txt

# Expose the port that Streamlit will run on (default is 8501)
EXPOSE 8501

# Define the command to run the Streamlit app
CMD ["streamlit", "run", "home.py"]
