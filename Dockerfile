FROM python:3.8-slim-buster
WORKDIR /home
COPY . /home

RUN apt update -y && apt install awscli -y

RUN apt-get update && pip install -r requirements.txt

# Expose the port that Streamlit will run on (default is 8501)
EXPOSE 8501

# Define the command to run when the container starts
CMD ["streamlit", "run", "home.py"]