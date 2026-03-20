FROM python:3.14.0-slim
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PYTHONDONTWRITEBUTECODE=1
ENV PYTHONUNBUFFERED=1
CMD [ "python", "main.py" ]