     1	# Use official Python runtime as base image
     2	FROM python:3.9-slim
     3	
     4	# Set working directory in container
     5	WORKDIR /app
     6	
     7	# Copy requirements file first to leverage Docker cache
     8	COPY req.txt .
     9	
    10	# Install Python dependencies
    11	RUN pip install --no-cache-dir -r req.txt
    12	
    13	# Copy the rest of the application code
    14	COPY . .
    15	
    16	# Create a non-root user for security
    17	RUN useradd --create-home --shell /bin/bash app && chown -R app:app /app
    18	USER app
    19	
    20	# Expose port if needed (for web applications)
    21	# EXPOSE 8000
    22	
    23	# Define entrypoint to allow flexible command execution
    24	ENTRYPOINT ["python"]
    25	CMD ["main.py"]
