FROM python:3.9-slim as builder

 

WORKDIR /app

 

# Copy your Python source code and any necessary files

COPY delete.py requirements.txt ./

 

# Install dependencies

RUN pip install --no-cache-dir -r requirements.txt

 

# Build a standalone Python application (if needed)

 

# Switch to a non-root user

RUN useradd -m nonroot

USER nonroot

 

# Set environment variables, if necessary

# ENV VARIABLE_NAME=value

ENV PORT 8080

# Define the command to run your application

CMD ["python", "delete.py"]
