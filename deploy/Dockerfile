FROM python:3.9.6

COPY requirements.txt /requirements.txt
WORKDIR /bot
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "bot.py"]