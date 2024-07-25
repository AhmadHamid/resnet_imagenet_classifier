FROM golang AS metric-builder
WORKDIR /app

ADD prometheus-endpoint .

RUN ["go", "build", "-o", "rs-metric", "main.go"]

FROM tensorflow/tensorflow
WORKDIR /app

ADD setup.py .
RUN ["python", "setup.py"]
ADD . ./system
RUN ["pip", "install", "--ignore-installed", "Flask", "pillow"]

COPY --from=metric-builder /app/rs-metric ./metrics

CMD [ "python", "-m", "flask", "-A", "system/main", "run", "-h", "0.0.0.0" ]