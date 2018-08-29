from flask import Flask, jsonify, render_template, request
import json

app = Flask(__name__)

session = {
    'session_id': 'em12345-01',
    'microscope': 'M01',
    'dose_per_frame': None,
    'numberOfIndividualFrames': None,
    'samplingRate': None,
    'particleSize': None,
    'minDist': None
}

config_values = {
    'M01': {
        'dose_per_frame': 100,
        'numberOfIndividualFrames': 32,
        'samplingRate': 1.06
    },
    'M02': {
        'dose_per_frame': 200,
        'numberOfIndividualFrames': 40,
        'samplingRate': 1.06
    },
    'M03': {
        'dose_per_frame': 300,
        'numberOfIndividualFrames': 50,
        'samplingRate': 1.06
    }
}


@app.route('/')
def index_page():
    return render_template('index.html')


@app.route('/session', methods=['GET', 'POST'])
def session_id():
    if request.method == 'POST':
        data = request.get_json()
        #print(data)
        #print(data['microscope'])
        try:
            config_file = json.load(open('./static/m03_workflow.json'))
        except:
            print ("Cannot find config file ")
        
        
        config_file[0]['dosePerFrame'] = float(data['dose_per_frame'])
        config_file[0]['numberOfIndividualFrames'] = int(data['numberOfIndividualFrames'])
        config_file[0]['samplingRate'] = float(data['samplingRate'])

        #print(config_file[6])
        # gautomatch params so 6 in config file
        # 
        config_file[6]['particleSize'] = float(data['particleSize'])
        config_file[6]['minDist'] = float(data['minDist'])

        #now these are passed onto the session object

        session['dose_per_frame'] = data['dose_per_frame']
        session['numberOfIndividualFrames'] = data['numberOfIndividualFrames']
        session['microscope'] = data['microscope']
        session['samplingRate'] = data['samplingRate']
        session['particleSize'] = data['particleSize']
        session['minDist'] = data['minDist']
        with open('config.json', 'w') as f:
            json.dump(config_file, f, indent=4, sort_keys=True)
        #print(json.dumps(config_file, indent=4, sort_keys=True))
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
    # # MAY BE LIES!!!

    print ("Information saved %s" %(json.loads(session)))
    # data = request.get_json()
    # # use stomp to send this information to the zocalo queue
    #
    # message = {'recipes': [],
    #            'parameters': {}}
    #
    # # Build a custom recipe
    # recipe = {}
    # recipe['1'] = {}
    # recipe['1']['service'] = "motioncor2_runner"
    # recipe['1']['queue'] = "motioncor2_runner"
    # recipe['1']['parameters'] = {'microscope':'m01',
    #
    # recipe['1']['output'] = 2

    #module load scipion and start scipion 
    pass
    return None

if __name__ == '__main__':
    app.run()
