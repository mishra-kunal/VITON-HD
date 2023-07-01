from flask import Flask, request, send_file, jsonify
from flask_ngrok import run_with_ngrok
from flask_cors import CORS
from PIL import Image
import base64
import io
import os
from queue import Queue

app = Flask(__name__)
run_with_ngrok(app)
CORS(app)

def make_dir(): 
  os.system("mkdir inputs && cd inputs && mkdir test && cd test && mkdir cloth cloth-mask image image-parse openpose-img openpose-json")

# Create a queue to handle task requests
task_queue = Queue()

@app.route("/")
def home():
    return jsonify("Hello there, trying to figure out our api :)!")

@app.route("/api/transform", methods=['POST'])
def begin():
    # Add the task to the queue
    task_queue.put(request)
    # Get the current task count
    task_count = task_queue.qsize()

    # Wait for the previous tasks to complete
    while task_count > 1:
        task_count = task_queue.qsize()

    # Process the current task
    return process_task()

def process_task():
    if not task_queue.empty():
        # Get the task from the queue
        task = task_queue.get()

        #create_directories()
        make_dir()
        print("data received")
        cloth = task.files['cloth']
        model = task.files['model']

        cloth = Image.open(cloth.stream)
        model = Image.open(model.stream)

        cloth.save("/content/VITON-HD/inputs/test/cloth/cloth.jpg")
        model.save("/content/VITON-HD/inputs/test/image/model.jpg")

        # running script to compute the predictions
        # Define the path for the log file
        log_file = "/content/VITON-HD/log_file.txt"

        # Execute the script and redirect the output to the log file
        os.system(f"python /content/VITON-HD/action.py > {log_file}")

        # Read the contents of the log file
        with open(log_file, "r") as file:
            log_contents = file.read()

        # Print the contents of the log file
        print(log_contents)

        # loading output
        op = os.listdir("/content/VITON-HD/results/test")[0]
        op = Image.open(f"/content/VITON-HD/results/test/{op}")
        buffer = io.BytesIO()
        op.save(buffer, 'png')
        buffer.seek(0)
        os.system("rm -rf /content/VITON-HD/results/test")
        return send_file(buffer, mimetype='image/gif')
    else:
        return jsonify("No task found")

if __name__ == "__main__":
    app.run()
