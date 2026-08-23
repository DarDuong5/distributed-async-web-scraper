FROM python:3.14-slim
WORKDIR /asyncqueue 

# Install application dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy code
COPY . .

# Run code
CMD ["python3", "main.py"]


