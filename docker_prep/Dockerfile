FROM python:3.8-slim-buster
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["wget", "-q", "-O", "-https://dl-ssl.google.com/linux/linux_signing_key.pub", "|", "apt-key", "add", "-"]
CMD ["sh", "-c", "'echo", ""deb", "[arch=amd64]", "http://dl.google.com/linux/chrome/deb/", "stable", "main"", ">>", "/etc/apt/sources.list.d/google-chrome.list'"]
sudo apt install chromium-driver
CMD ["apt-get", "-y", "update"]
CMD ["apt-get", "install", "-y", "google-chrome-stable"]
#CMD ["wget", "-O", "/tmp/chromedriver.zip", "http://chromedriver.storage.googleapis.com/`curl", "-sS", "chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip"]
#CMD ["apt-get", "install", "-yqq", "unzip"]
#CMD ["unzip", "/tmp/chromedriver.zip", "chromedriver", "-d", "/usr/local/bin/"]
CMD ["python", "scraper/dcp_headless.py"]




