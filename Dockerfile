FROM python:3.11-slim

WORKDIR /workspace

# Optional system packages if needed in future
RUN apt-get update && apt-get install -y build-essential

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "init_launchpad.py"]

