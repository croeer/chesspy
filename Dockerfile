FROM python:2.7

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY color.py detect.py functions.py fserver.py ./
COPY templates ./templates/
COPY packages ./packages/

EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "fserver:app"]
