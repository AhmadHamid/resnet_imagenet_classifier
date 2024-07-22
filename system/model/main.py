import time, json, os
from flask import Flask, request
from resnet50 import predict

app = Flask(__name__)

file_dir = "/tmp"
inference_times = []
is_correctly_classified = []
count = 100
pointer = 0


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


def get_accuracy() -> float:
    correct = 0

    for classification in is_correctly_classified:
        if (classification):
            correct += 1

    if (len(is_correctly_classified) > 0):
        return correct / len(is_correctly_classified)
    else:
        return -1


@app.route("/", methods=["GET", "POST"])
def root():
    start_response_time = time.time()
    global pointer, count

    if (request.method == "GET"):
        return '''
      <!doctype html>
      <title>Upload new File</title>
      <h1>Upload new File</h1>
      <form method=post enctype=multipart/form-data>
        <input type=file name=file>
        <input type=text name=label>
        <input type=submit value=Upload>
      </form>
      '''
    elif (request.method == "POST"):
        file = request.files["file"]
        file_path = os.path.join(file_dir, file.filename)

        file.save(file_path)
        start_inference_time = time.time()
        print(predict(file_path))
        total_inference_time = time.time() - start_inference_time
        total_response_time = time.time() - start_response_time

        # TODO: Match Label with prediction
        if (request.form.get("label") == "123"):
            is_correctly_classified.insert(pointer, True)
        else:
            is_correctly_classified.insert(pointer, False)

        set_inference_time(total_inference_time)
        pointer = (pointer + 1) % count
        return str(total_inference_time)
    else:
        return "Unknown"


@app.route("/metrics")
def metrics():
    # TODO: Recall, Precision, F1-Score
    return json.dumps({
        "cpu": "100",
        "inferenceTime": get_inference_time(),
        # TODO: Implement response time calculation
        "responseTime": get_inference_time(),
        "accuracy": get_accuracy()
    })
