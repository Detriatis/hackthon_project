from flask import Flask, render_template, url_for
import json

app = Flask(__name__)

@app.route('/')
def index():
    # Sample data
    data = {
        "nodes": [
            {"id": "Wind Farm", "type": "source", "image": url_for("static", filename="wind.webp")},
            {"id": "Nuclear Plant", "type": "source", "image": url_for("static", filename="powerstation.webp")},
            {"id": "Coal Plant", "type": "source", "image": url_for("static", filename="wind.webp")},
            {"id": "City A", "type": "sink", "image": url_for("static", filename="wind.webp")},
            {"id": "City B", "type": "sink", "image": url_for("static", filename="wind.webp")},
        ],
        "links": [
            {"source": "Wind Farm", "target": "City A", "power": 50},
            {"source": "Nuclear Plant", "target": "City A", "power": 200},
            {"source": "Coal Plant", "target": "City B", "power": 150},
        ]
    }
    return render_template('index.html', graph_data=json.dumps(data))

if __name__ == '__main__':
    app.run(debug=True)
