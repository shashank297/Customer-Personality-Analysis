# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN apt update -y && apt install -y libsndfile1
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port that Streamlit will run on (default is 8501)
EXPOSE 8501

# Define the command to run when the container starts
CMD ["streamlit", "run", "home.py"]
