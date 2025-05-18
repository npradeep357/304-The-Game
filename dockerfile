FROM node:20-slim AS builder
RUN apt-get update && apt-get install -y nodejs npm && rm -rf /var/lib/apt/lists/*

# Build the client UI
COPY ./client /app/client
COPY ./client/package.json /app/client/package.json
COPY ./client/. /app/client
WORKDIR /app/client
RUN npm install && npm run build

FROM python:3.13-slim-bullseye AS python_builder

WORKDIR /app
COPY ./server/requirements.txt /app/requirements.txt
RUN python3.13 -m pip install -r /app/requirements.txt

FROM python:3.13-slim-bullseye
RUN python3.13 -m pip install --upgrade pip

ENV PYTHONPATH="/app"
WORKDIR /app

# copy files
COPY ./server/304/ /app/304/
# Copy the main entry point for the server
COPY ./server/304/__main__.py /app/__main__.py

# Copy installed Python packages from the python_builder stage
COPY --from=python_builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
# Copy the built client UI from the builder stage
COPY --from=builder /app/client/dist /app/client/dist
EXPOSE 80

CMD ["python3.13", "/app/__main__.py", "--version", "1.0.0"]
