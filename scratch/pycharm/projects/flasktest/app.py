from flask import Flask, jsonify, render_template, request
import json

import workflows
from workflows.transport.stomp_transport import StompTransport


app = Flask(__name__)

session = {

    #TODO:Get session/microscope amd possibly the path string to user data folder from ispyb

    
    'session_id': 'em12345-01',
    'microscope': 'M01',
    'dosePerFrame': None,
    'numberOfIndividualFrames': None,
    'samplingRate': None,
    'particleSize': None,
    'minDist': None
}

config_values = {
    'M01': {
        'dosePerFrame': 0.5,
        'numberOfIndividualFrames': 32,
        'samplingRate': 1.06
    },
    'M02': {
        'dosePerFrame': 0.5,
        'numberOfIndividualFrames': 40,
        'samplingRate': 1.06
    },
    'M03': {
        'dosePerFrame': 0.5,
        'numberOfIndividualFrames': 50,
        'samplingRate': 1.06
    },

    'M04': {
        'dosePerFrame': 0.5,
        'numberOfIndividualFrames': 50,
        'samplingRate': 1.06
    },
    'M05': {
        'dosePerFrame': 0.5,
        'numberOfIndividualFrames': 50,
        'samplingRate': 1.06
    },
    'M06': {
        'dosePerFrame': 0.5,
        'numberOfIndividualFrames': 50,
        'samplingRate': 1.06
    },
    'M07': {
        'dosePerFrame': 0.5,
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
        # print(data)
        # print(data['microscope'])
        try:
            config_file = json.load(open('./static/m03_workflow.json'))
        except:
            print ("Cannot find config file ")

        config_file[0]['dosePerFrame'] = float(data['dosePerFrame'])
        config_file[0]['numberOfIndividualFrames'] = int(data['numberOfIndividualFrames'])
        config_file[0]['samplingRate'] = float(data['samplingRate'])

        config_file[6]['particleSize'] = float(data['particleSize'])
        config_file[6]['minDist'] = float(data['minDist'])
        config_file[3]['findPhaseShift'] = bool(data['findPhaseShift'])

        # now these are passed onto the session object

        session['dosePerFrame'] = data['dosePerFrame']
        session['numberOfIndividualFrames'] = data['numberOfIndividualFrames']
        session['microscope'] = data['microscope']
        session['samplingRate'] = data['samplingRate']
        session['particleSize'] = data['particleSize']
        session['minDist'] = data['minDist']
        session['findPhaseShift'] = data['findPhaseShift']
        with open('config.json', 'w') as f:
            json.dump(config_file, f, indent=4, sort_keys=True)
        # print(json.dumps(config_file, indent=4, sort_keys=True))

        run_scipion()

        return jsonify(data)



    else:
        return jsonify(session)


@app.route('/get_mic_defaults')
def get_defaults():
    # config_file = json.load(open('./static/m03_workflow.json'))
    # print('Before Change:%s' % config_file[0]['dosePerFrame'])
    # # config_file[0]['dosePerFrame'] = config_values['dosePerFrame']
    # print('After Change:%s' % config_file[0]['dosePerFrame'])
    # print(config_file)
    # return jsonify(data=config_file)
    return jsonify(microscopes=config_values)


@app.route('/get_config/<microscope>', methods=['GET'])
def get_config(microscope):
    values = config_values[microscope]
    return jsonify(values)



def run_scipion():
    print ("Scipion run Pressed")
    print ("Information saved %s" % (json.loads(session)))
    # # use stomp to send this information to the zocalo queue

    # default_configuration = '/dls_sw/apps/zocalo/secrets/credentials-live.cfg'
    # if '--test' in sys.argv:
    #     default_configuration = '/dls_sw/apps/zocalo/secrets/credentials-testing.cfg'
    # # override default stomp host
    # try:
    #     StompTransport.load_configuration_file(default_configuration)
    # except workflows.Error as e:
    #     print("Error: %s\n" % str(e))
    #
    # StompTransport.add_command_line_options(parser)
    # (options, args) = parser.parse_args(sys.argv[1:])
    # stomp = StompTransport()
    #
    # message = {'recipes': [],
    #            'parameters': {}}
    #
    # # Build a custom recipe
    # recipe = {}
    # recipe['1'] = {}
    # recipe['1']['service'] = "scipion_runner"
    # recipe['1']['queue'] = "scipion_runner"
    # recipe['1']['parameters'] = session # {'microscope':'m01',
    #
    # recipe['1']['output'] = 2

    # message.recipe.append(recipe)

    # stomp.connect()
    # stomp.send(
    #     'processing_recipe',
    #     message
    # )

    print("\nReally Submitted.")

    # module load scipion and start scipion
    pass
    return None


if __name__ == '__main__':
    app.run()
