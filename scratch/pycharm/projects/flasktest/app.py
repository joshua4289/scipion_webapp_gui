from flask import Flask, jsonify, render_template, request
import json

app = Flask(__name__)

session = {
    'session_id': 'em12345 - 01',
    'microscope': 'M01',
    'dose_per_frame': None,
    'numberOfIndividualFrames': None
}

config_values = {
    'M01': {
        'dose_per_frame': 100,
        'numberOfIndividualFrames': 32
    },
    'M02': {
        'dose_per_frame': 200,
        'numberOfIndividualFrames': 40
    },
    'M03': {
        'dose_per_frame': 300,
        'numberOfIndividualFrames': 50
    }
}


@app.route('/')
def index_page():
    return render_template('index.html')


@app.route('/session', methods=['GET', 'POST'])
def session_id():
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        print(data['microscope'])
        config_file = json.load(open('./static/m03_workflow.json'))
        print(config_file[0]['dosePerFrame'])
        config_file[0]['dosePerFrame'] = float(data['dose_per_frame'])
        config_file[0]['numberOfIndividualFrames'] = data['numberOfIndividualFrames']
        session['dose_per_frame'] = data['dose_per_frame']
        session['numberOfIndividualFrames'] = data['numberOfIndividualFrames']
        session['microscope'] = data['microscope']
        with open('config.json', 'w') as f:
            json.dump(config_file, f, indent=4, sort_keys=True)
        print(json.dumps(config_file, indent=4, sort_keys=True))
        return jsonify(data)

    else:
        return jsonify(session)


@app.route('/get_mic_defaults')
def get_defaults():
    # config_file = json.load(open('./static/m03_workflow.json'))
    # print('Before Change:%s' % config_file[0]['dosePerFrame'])
    # # config_file[0]['dosePerFrame'] = config_values['dose_per_frame']
    # print('After Change:%s' % config_file[0]['dosePerFrame'])
    # print(config_file)
    # return jsonify(data=config_file)
    return jsonify(microscopes=config_values)


@app.route('/get_config/<microscope>', methods=['GET'])
def get_config(microscope):
    values = config_values[microscope]
    return jsonify(values)


@app.route('/run_scipion', methods=['POST'])
def run_scipion():
    # MAY BE LIES!!!
    data = request.get_json()
    # use stomp to send this information to the zocalo queue

    message = {'recipes': [],
               'parameters': {}}

    # Build a custom recipe
    recipe = {}
    recipe['1'] = {}
    recipe['1']['service'] = "motioncor2_runner"
    recipe['1']['queue'] = "motioncor2_runner"
    recipe['1']['parameters'] = {'microscope':'m01',
                                 
    recipe['1']['output'] = 2

    return None

if __name__ == '__main__':
    app.run()
