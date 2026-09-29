FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy deployment files
COPY . .

# Hugging Face Spaces expose port 7860
EXPOSE 7860

# Run Flask backend using Gunicorn on port 7860
CMD ["gunicorn", "-b", "0.0.0.0:7860", "backend_files.app:superkart_api"]