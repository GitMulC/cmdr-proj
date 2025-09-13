# lightweight Python Image
FROM python:3.10.5-slim

# Workdir
WORKDIR /app/backend

#Install Dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy App Code
COPY backend/ .

# Expose Port
EXPOSE 5000

# Run Flask
CMD ["python3", "app.py"]