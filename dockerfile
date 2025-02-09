# Use an official Python image as a base
FROM python:3.12

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port the application will run on
EXPOSE 5000

# Run the command to start the application when the container launches
CMD ["flask", "run", "--host=0.0.0.0"]
