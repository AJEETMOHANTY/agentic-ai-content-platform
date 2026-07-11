# Base Python Image
FROM python:3.11-slim

# Prevent Python from buffering logs
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy dependency file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Streamlit Port
EXPOSE 8501

# Run Streamlit
CMD ["streamlit", "run", "frontend.py", "--server.address=0.0.0.0"]