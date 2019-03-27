from __future__ import absolute_import, print_function
from flask import Flask, jsonify, render_template, request
from workflows.services.common_service import CommonService
from workflows.transport.stomp_transport import StompTransport

from pathlib2 import Path
import workflows, json
from optparse import OptionParser
import sys

app = Flask(__name__)

session = {

    # TODO:Get session/microscope amd possibly the path string to user data folder from ispyb

    'session_id': 'em12345-01',
    'microscope': 'M01',
    'dosePerFrame': None,
    'numberOfIndividualFrames': None,
    'patchX': 5,
    'patchY': 5,
    'samplingRate': None,
    'particleSize': None,
    'minDist': None,
    'windowSize': None,
}

config_values = {
    'M01': {
        'dosePerFrame': 0.5,
        'numberOfIndividualFrames': 32,
        'patchX': 5,
        'patchY': 5,
        'samplingRate': 1.06,
        'windowSize': 512
    },
    'M02': {
        'dosePerFrame': 0.5,
        'patchX': 5,
        'patchY': 5,
        'numberOfIndividualFrames': 40,
        'samplingRate': 1.06,
        'windowSize': 512
    },
    'M03': {
        'dosePerFrame': 0.5,
        'numberOfIndividualFrames': 50,
        'patchX': 5,
        'patchY': 5,
        'samplingRate': 1.06,
        'windowSize': 512
    },

    'M04': {
        'dosePerFrame': 0.5,
        'numberOfIndividualFrames': 50,
        'patchX': 5,
        'patchY': 5,
        'samplingRate': 1.06,
        'windowSize': 512,
    },
    'M05': {
        'dosePerFrame': 0.5,
        'numberOfIndividualFrames': 50,
        'patchX': 5,
        'patchY': 5,
        'samplingRate': 1.06,
        'windowSize': 512,
    },
    'M06': {
        'dosePerFrame': 0.5,
        'numberOfIndividualFrames': 50,
        'samplingRate': 1.06,
        'patchX': 5,
        'patchY': 5,
        'windowSize': 512,
    },
    'M07': {
        'dosePerFrame': 0.5,
        'numberOfIndividualFrames': 50,
        'samplingRate': 1.06,
        'patchX': 5,
        'patchY': 5,
        'windowSize': 512,
    }

}


@app.route('/')
def index_page():
    return render_template('index.html')


@app.route('/session', methods=['GET', 'POST'])
def session_id():
    if request.method == 'POST':
        data = request.get_json()

        session['session_id'] = data['session_id']
        session['dosePerFrame'] = data['dosePerFrame']
        session['numberOfIndividualFrames'] = data['numberOfIndividualFrames']
        session['patchX'] = data['patchX']
        session['patchY'] = data['patchY']
        session['microscope'] = data['microscope']
        session['samplingRate'] = data['samplingRate']
        session['particleSize'] = data['particleSize']
        session['minDist'] = data['minDist']
        session['findPhaseShift'] = data['findPhaseShift']
        session['windowSize'] = data['windowSize']

        print(jsonify(session))
        send_recipe(data)
        return jsonify(session, 202)
    else:
        return jsonify(session)


def send_recipe(session_dictionary):
    # get posted data

    import workflows.recipe
    from workflows.transport.stomp_transport import StompTransport

    default_configuration = '/dls_sw/apps/zocalo/secrets/credentials-live.cfg'
    try:
        StompTransport.load_configuration_file(default_configuration)
    except workflows.Error as e:
        print("Error: %s\n" % str(e))

    stomp = StompTransport()

    # build Messge

    message = {'recipes': [], 'parameters': {}}

    recipe = {1: {'service': 'Scipion_runner', 'queue': 'ScipionMain', 'parameters': ""}}
    recipe[1]['parameters'] = session_dictionary  # pass session information

    recipe['start'] = [[1, []]]

    message['custom_recipe'] = recipe

    stomp.connect()

    test_valid_recipe = workflows.recipe.Recipe(recipe)
    test_valid_recipe.validate()

    stomp.send(
        'processing_recipe',
        message
    )
    print(message)
    print("User app data submited ")


@app.route('/get_mic_defaults')
def get_defaults():
    return jsonify(microscopes=config_values)


@app.route('/get_config/<microscope>', methods=['GET'])
def get_config(microscope):
    values = config_values[microscope]
    return jsonify(values)


if __name__ == '__main__':

<<<<<<< HEAD
    # parser = OptionParser(usage="app_send_recipie.py [options] session-id",
    #                       description="Processing given collection_id ")
    #
    # parser.add_option("-s", "--session", dest="session_id", action="store", help=" ispyb session-id")
    #
    # (options, args) = parser.parse_args(sys.argv[1:])
    #
    # if "--session" or "-s" in sys.argv:
    #     session['session_id'] = options.session_id
=======
    parser = OptionParser(usage="app_send_recipie.py [options] session-id",
                          description="Processing given collection_id ")

    parser.add_option("-s", "--session", dest="session_id", action="store", help=" ispyb session-id")

    (options, args) = parser.parse_args(sys.argv[1:])

    if "--session" or "-s" in sys.argv:
        session['session_id'] = options.session_id
>>>>>>> 21b5ebe5a90248dce2f269152d38d3b7dc4e94a3


    def get_home_from_session(session_id):
        session_id = options.session_id

        group_name = str(session_id).replace('-', '_')
        scipion_user_data = '~/' + str(group_name) + 'ScipionUserData'
        scipion_user_datapath = Path(scipion_user_data)


    # get_home_from_session(session['session_id'])

    app.run(debug=False, port=8080)
