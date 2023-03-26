import asyncio
from flask import Flask, jsonify

app = Flask(__name__)

async def load_data():
    # simulate a time-consuming data loading process
    await asyncio.sleep(5)
    return {"data": "Data loaded successfully"}

@app.route("/")
def home():
    # start an asynchronous data loading process
    task = asyncio.ensure_future(load_data())

    return jsonify({"status": "loading"})

@app.route("/data")
def get_data():
    if task.done():
        # return the loaded data if the task is done
        return jsonify(task.result())

    return jsonify({"status": "loading"})

if __name__ == "__main__":
    app.run(debug=True)
