import time, json, os, re
from flask import Flask, request
from resnet import ResNet
# from resnet50 import predict

app = Flask(__name__)

model = ResNet(50)
file_dir = "/tmp"
inference_times = []
response_times = []
is_correctly_classified = []
count = 100
pointer = 0
throughput_per_x_second = 15
throughput_time = time.time()
throughput = 0
total_requests = 0

def set_inference_time(res_time: float) -> bool:
  global pointer

  inference_times.insert(pointer, res_time)

def get_inference_time() -> float:
  sum = 0.0
  for inference_time in inference_times:
    sum += inference_time

  if (len(inference_times) > 0):
    return sum / len(inference_times)
  else:
    return -1.0

def set_response_time(res_time: float) -> bool:
  global pointer

  response_times.insert(pointer, res_time)

def get_response_time() -> float:
  sum = 0.0
  for response_time in response_times:
    sum += response_time

  if (len(response_times) > 0):
    return sum / len(response_times)
  else:
    return -1.0

def get_accuracy() -> float:
  correct = 0

  for classification in is_correctly_classified:
    if (classification):
      correct+= 1

  if (len(is_correctly_classified) > 0):
    return correct / len(is_correctly_classified)
  else:
    return -1

@app.route("/", methods=["GET", "POST"])
def root():
  start_response_time = time.time()
  global pointer, count, throughput, total_requests

  if (request.method == "GET"):
    return '''
      <!doctype html>
      <title>Upload new File</title>
      <h1>Upload new File</h1>
      <form method=post enctype=multipart/form-data>
        <input type=file name=file>
        <input type=submit value=Upload>
      </form>
      '''
  elif (request.method == "POST"):
    file = request.files["file"]
    file_path = os.path.join(file_dir, file.filename)

    file.save(file_path)
    start_inference_time = time.time()
    prediction = ResNet(50).predict(file_path)
    # print(prediction)

    total_inference_time = time.time() - start_inference_time
    total_response_time = time.time() - start_response_time

    if (re.split("(_.*)", request.files["file"].filename)[0] == prediction[0][0]):
      is_correctly_classified.insert(pointer, True)
    else:
      is_correctly_classified.insert(pointer, False)

    set_inference_time(total_inference_time)
    set_response_time(total_response_time)

    pointer = (pointer + 1) % count
    throughput += 1
    total_requests += 1

    return str(prediction)
  else:
    return "Unknown"
  
@app.route("/metrics")
def metrics():
  global throughput_time, throughput, total_requests

  now = time.time()
  if (now >= throughput_time + throughput_per_x_second):
    throughput_time = now
    throughput = 0

  # TODO: Recall, Precision, F1-Score
  return json.dumps({
    "accuracy": get_accuracy(),
    "inferenceTime": get_inference_time(),
    "responseTime": get_response_time(),
    "throughput": throughput,
    "total_requests": total_requests
  })