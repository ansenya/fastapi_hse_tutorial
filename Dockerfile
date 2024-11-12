FROM python:3.13.0-slim-bullseye

COPY . .
RUN pip install -r requirements.txt

CMD ["fastapi", "run", "main.py"]