FROM python:3.11-slim

RUN apt-get update && apt-get install -y wget gnupg unzip curl \ 
    && rm -rf /var/lib/apt/lists/*

RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \ 
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \ 
    && apt-get update && apt-get install -y google-chrome-stable

RUN CHROMEDRIVER_VERSION=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE") && \ 
    wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip && \ 
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && rm /tmp/chromedriver.zip

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "-b", "0.0.0.0:5000", "main:app"]
