FROM golang AS metric-builder
WORKDIR /app

ADD prometheus-endpoint .

RUN ["go", "build", "-o", "rs-metric", "main.go"]

FROM tensorflow/tensorflow
WORKDIR /app

ADD setup.py wrapper.sh ./
RUN ["python", "setup.py"]
ADD main.py resnet50.py ./system/
RUN ["pip", "install", "--ignore-installed", "Flask", "pillow"]

COPY --from=metric-builder /app/rs-metric ./metrics

CMD [ "./wrapper.sh" ]