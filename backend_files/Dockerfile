FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all deployment files into /app
COPY . .

# Default port exposed
EXPOSE 7860

# Run Flask backend using Gunicorn pointing directly to app:app
CMD ["gunicorn", "-b", "0.0.0.0:7860", "app:app"]