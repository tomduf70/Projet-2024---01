from flask import Flask, request, jsonify, render_template
import RPi.GPIO as GPIO

app = Flask(__name__)

# Configuration de la broche GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)  # Remplacez 17 par le numéro de broche que vous utilisez

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/load_labels', methods=['POST'])
def load_labels():
    global labels_dict
    data = request.json
    labels = data.get('labels', [])
    labels_dict = {label: i for i, label in enumerate(labels)}
    return jsonify({'status': 'labels loaded', 'labels': labels_dict})

@app.route('/toggle', methods=['POST'])
def toggle_gpio():
    data = request.json
    label = data.get('label')
    print(label, labels_dict[label])

    if label == "clavier noir":  
        GPIO.output(17, GPIO.HIGH)  # Activer la broche
        return jsonify({'status': 'GPIO HIGH'})
    else:
        GPIO.output(17, GPIO.LOW)  # Désactiver la broche
        return jsonify({'status': 'GPIO LOW'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
