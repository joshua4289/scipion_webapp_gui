from __future__ import absolute_import, print_function
from flask import Flask, jsonify, render_template, request
from workflows.services.common_service import CommonService
from workflows.transport.stomp_transport import StompTransport

from pathlib2 import Path
import workflows, json
from  optparse import OptionParser
import sys
#import webbrowser
#import threading

app = Flask(__name__)

session = {

    # TODO:Get session/microscope amd possibly the path string to user data folder from ispyb

    'session_id': 'em12345-01',
    'microscope': 'M01',
    'dosePerFrame': None,
    'numberOfIndividualFrames': None,
    'samplingRate': None,
    'particleSize': None,
    'minDist': None,
    'windowSize':None,
}

config_values = {
    'M01': {
        'dosePerFrame': 0.5,
        'numberOfIndividualFrames': 32,
        'samplingRate': 1.06,
        'windowSize':512
    },
    'M02': {
        'dosePerFrame': 0.5,
        'numberOfIndividualFrames': 40,
        'samplingRate': 1.06,
        'windowSize':512
    },
    'M03': {
        'dosePerFrame': 0.5,
        'numberOfIndividualFrames': 50,
        'samplingRate': 1.06,
        'windowSize':512
    },

    'M04': {
        'dosePerFrame': 0.5,
        'numberOfIndividualFrames': 50,
        'samplingRate': 1.06,
        'windowSize':512,
    },
    'M05': {
        'dosePerFrame': 0.5,
        'numberOfIndividualFrames': 50,
        'samplingRate': 1.06,
        'windowSize':512,
    },
    'M06': {
        'dosePerFrame': 0.5,
        'numberOfIndividualFrames': 50,
        'samplingRate': 1.06,
        'windowSize':512,
    },
    'M07': {
        'dosePerFrame': 0.5,
        'numberOfIndividualFrames': 50,
        'samplingRate': 1.06,
        'windowSize':512,
    }

}


@app.route('/')
def index_page():
    return render_template('index.html')


@app.route('/session', methods=['GET', 'POST'])
def session_id():
    if request.method == 'POST':
        data = request.get_json()

        # try:
        #     config_file = json.load(open('./static/m03_workflow.json'))
        #     print("config_file  load sucess")
        # except:
        #     print("Cannot find config file ")
        #
        # # Make changes to the template based on values  set by user
        #
        # config_file[0]['dosePerFrame'] = float(data['dosePerFrame'])
        # config_file[0]['numberOfIndividualFrames'] = int(data['numberOfIndividualFrames'])
        # config_file[0]['samplingRate'] = float(data['samplingRate'])
        #
        # config_file[6]['particleSize'] = float(data['particleSize'])
        # config_file[6]['minDist'] = float(data['minDist'])
        # config_file[3]['findPhaseShift'] = bool(data['findPhaseShift'])

        # now these are passed onto the session object

        session['dosePerFrame'] = data['dosePerFrame']
        session['numberOfIndividualFrames'] = data['numberOfIndividualFrames']
        session['microscope'] = data['microscope']
        session['samplingRate'] = data['samplingRate']
        session['particleSize'] = data['particleSize']
        session['minDist'] = data['minDist']
        session['findPhaseShift'] = data['findPhaseShift']
        session['windowSize']= data['windowSize']


        # with open('config.json', 'w') as f:
        #     json.dump(config_file, f, indent=4, sort_keys=True)

        # create json from template
        # save json to path determined by session
        # add to queue (send recipe)
        # run scipion
        # 200 OK or 500 Server error
        # 202 Accepted
        # The request has been accepted for processing, but the processing has not been completed.
        send_recipe(data)
        return jsonify(session, 202)  # jsonify(send_recipe(config_file)) #jsonify(data)
    else:
        return jsonify(session)


# TODO: instead of writing out a file send file as recipie


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

    recipe = {1: {'service': 'Scipion_runner', 'queue': 'Scipion_runner', 'parameters': ""}}
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


if __name__ == '__main__':
    # print ("opening browser")
    # threading.Timer(1,lambda:webbrowser.open('http://127.0.0.1:5000'))
    parser = OptionParser(usage="app_send_recipie.py [options] session-id",description="Processing given collection_id ")

    parser.add_option("-s","--session",dest="session_id",action="store", help=" ispyb session-id" )

    (options, args) = parser.parse_args(sys.argv[1:])

    if "--session" in sys.argv:
        session['session_id'] = options.session_id


    def get_home_from_session(session_id):
        session_id = options.session_id

        group_name = str(session_id).replace('-','_')
        scipion_user_data = '~/' + str(group_name) + 'ScipionUserData'
        scipion_user_datapath = Path(scipion_user_data)

    # get_home_from_session(session['session_id'])

    # webbrowser.open('127.0.0.1:5000')
    app.run(debug=False,port=8080)
