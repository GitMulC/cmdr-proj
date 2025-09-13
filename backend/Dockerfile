# lightweight Python Image
FROM python:3.10.5

# Workdir
WORKDIR /app

#Install Dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy App Code
COPY . .

# Expose Port
EXPOSE 5000

# Run Flask
CMD ["python3", "app.py"]