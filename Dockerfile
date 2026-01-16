FROM python:3.10-slim-trixie
RUN groupadd -r fastapi && useradd --no-log-init -r -g fastapi fastapi
WORKDIR /code
# Install dependencies
COPY ./requirements.txt ./
RUN pip3 install -r requirements.txt --no-cache-dir
# Copy backend files
COPY ./app ./app
# Switch user
USER fastapi
# Run server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]