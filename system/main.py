import time, json, math
from flask import Flask, request
from resnet50 import predict

app = Flask(__name__)

response_times = []
count = 1000
pointer = 0

def set_response_time(res_time: float) -> bool:
  response_times.insert(pointer, res_time)
  pointer = (pointer + 1) % count

def get_response_time() -> float:
  sum = 0.0
  for res_time in response_times:
    sum += res_time

  if (len(response_times) > 0):
    return sum / len(response_times)
  else:
    return -1.0

@app.route("/", methods=["GET", "POST"])
def root():
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
    file.save("/{}".format(file.filename))
    start_time = time.time()
    print(predict(file.filename))
    total_time = time.time() - start_time

    set_response_time(total_time)

    return str(total_time)
  else:
    return "Unknown"
    
@app.route("/metrics")
def metrics():
  return json.dumps({
    "cpu": "100",
    "responseTime": get_response_time()
    })
# TODO: Response TIme, Accuracy, Recall, Precision, F1-Score