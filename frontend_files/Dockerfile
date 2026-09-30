FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 7860

CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0", "--server.enableXsrfProtection=false"]