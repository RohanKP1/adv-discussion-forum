# Use an official Python image as the base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . /app/

# Expose ports for FastAPI (8000) and Streamlit (8501)
EXPOSE 8000 8501

# Command to run both the FastAPI server and Streamlit client
CMD ["sh", "-c", "uvicorn server.main:app --host 0.0.0.0 --port 8000 & streamlit run client/app.py --server.port 8501 --server.address 0.0.0.0"]