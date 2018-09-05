
from __future__ import print_function
from flask import Flask, jsonify, render_template, request
#flasks imports
#dials

from workflows.services.common_service import CommonService
import workflows
from workflows.transport.stomp_transport import StompTransport



#python3 path manipulations port
from pathlib2 import Path

import json


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
    'm03': {
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

        #Make changes to the template based on values  set by user

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

        #run_scipion()
        dict1={'test':1}
        send_recipe(dict1)

        return   jsonify(data)
    else:
        return jsonify(session)


#TODO: instead of writing out a file send file as recipie
def send_recipe(user_modified_json):
    #get posted data

    import workflows.recipe
    from workflows.transport.stomp_transport import StompTransport

    default_configuration = '/dls_sw/apps/zocalo/secrets/credentials-live.cfg'
    try:
        StompTransport.load_configuration_file(default_configuration)
    except workflows.Error as e:
        print("Error: %s\n" % str(e))

    stomp = StompTransport()

    #build Messge

    message = {'recipes': [],'parameters': {}}

    recipe = {}
    recipe['1'] = {}
    recipe['1']['service'] = "scipion_runner"
    recipe['1']['queue'] = "scipion_runner"

    recipe['1']['parameters'] = "diamond"


    recipe['start'] = [[1, []]]

    message['custom_recipe'] = recipe

    stomp.connect()
    test_valid_recipe = workflows.recipe.Recipe(recipe)

    test_valid_recipe.validate()


    #stomp.connect()
    stomp.transport.send(
        'processing_recipe',

        message

    )
    print("User app data submited ")

              #  def send_start_recipie(CommonService):

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

def create_project_paths_and_json():
    import shutil,os

    project_path,short_timestamp = find_visit_dir_from_session_info()
    gda2_workspace_dir = project_path/'processed'
    project_name = 'scipion_'+ project_path.name +'_' + str(short_timestamp)


    gda2_workspace_dir.mkdir(parents=True,exist_ok=True)


    #HACK:Copied the config.json to the folder path after creating it
    config_json  = '/home/jtq89441/workspace/zocalo_test/motioncor2_launcher/testing/share_local/webapp/scratch/pycharm/projects/flasktest/config.json'
    project_json = str(gda2_workspace_dir/project_name)+'.json'
    shutil.copyfile(config_json,project_json)
    return str(project_name),str(project_json),str(gda2_workspace_dir)






def _create_prefix_command(args):
    cmd = ('source /etc/profile.d/modules.sh;'
           'module unload python/ana;'
           'module unload scipion/release-1.2.1-zo;'
           'module load scipion/release-1.2.1-zo;'
           'export SCIPION_NOGUI=true;'
           'export SCIPIONBOX_ISPYB_ON=True;'
           )
    return cmd + ' '.join(args)


#     #TODO: get config.json from the session and run those commands
#
#     pass



def run_scipion():
    print ("Scipion run Pressed")
    from subprocess import Popen,PIPE
    import sys


    project_name,project_json,gda2_workspace_dir = create_project_paths_and_json()


    send_recipe()


    create_project_args = [ 'cd','$SCIPION_HOME;','scipion', 'python', 'scripts/create_project.py', project_name,project_json, gda2_workspace_dir]
    create_project_cmd = _create_prefix_command(create_project_args)

    print("prefix command is " + create_project_cmd)
    p1 = Popen(create_project_cmd, cwd=str(gda2_workspace_dir),stderr=PIPE,stdout=PIPE, shell=True)
    out_project_cmd,err_project_cmd = p1.communicate()

    if p1.returncode != 0:
         raise Exception("Could not create project ")
    else:
           schedule_project_args = [ 'cd','$SCIPION_HOME;','scipion', 'python', '$SCIPION_HOME/scripts/schedule_project.py', project_name]
           schedule_project_cmd  = _create_prefix_command(schedule_project_args)
           Popen(schedule_project_cmd, cwd=str(gda2_workspace_dir), shell=True)





    def on_message(self, headers, message):
        logging.warn("about to start processing{}".format(message))
        template = Path(message)

    # NOTE:This is session information from the webpage



def find_visit_dir_from_session_info():
    """ Returns a path  given a microscope and session-id """

    import datetime
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    #TODO:visit path cannot be constructed from user input but has to be constructed with ispyb
    #TODO:session_id not in Camel Case
    #  /dls/microscope/data/year/session['session_id]

    project_year = timestamp[:4]
    project_path = "/tmp/jtq89441/dls/{}/data/{}/{}/".format(str(session['microscope']).lower(),project_year,session['session_id'])
    print ("project path is %s" %project_path)

    short_timestamp=str(timestamp).split('_')[1]


    return Path(project_path),short_timestamp

    # send recipie
    #self.visit_dir = find_visit_dir_from_session_info()
    # scipion_module='scipion/release-1.2.1-zo'
    # scipion_home = "/dls_sw/apps/scipion/scipion_1_2_1_dials/scipion/"
    # scipion_path= os.path.join(scipion_home,'scipion')
    #
    #
    #
    # args = ['scipion','python',scipion_home,'scripts/create_project/py','']
    #
    # # # use stomp to send this information to the zocalo queue
    # p1 = "module load %s && env" % (scipion_module)
    # out1,err1 = subprocess.Popen(p1, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # p2 = "grep SCIPION_HOME"
    # out2,err2 = subprocess.Popen(p2,stdin=p1.stdout)
    # print (out2)
    #


    # STOMP send stuff

    # default_configuration = '/dls_sw/apps/zocalo/secrets/credentials-live.cfg'
    # if '--test' in sys.argv:
    # default_configuration = '/dls_sw/apps/zocalo/secrets/credentials-testing.cfg'
    # #override default stomp host
    # try:
    #     StompTransport.load_configuration_file(default_configuration)
    # except workflows.Error as e:
    #      print("Error: %s\n" % str(e))
    # #
    # # StompTransport.add_command_line_options(parser)
    # # (options, args) = parser.parse_args(sys.argv[1:])
    # stomp = StompTransport()
    # #
    # message = {'recipes': [],
    #             'parameters': {}}
    #
    # Build a custom recipe
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

    #print("\nReally Submitted.")

    # module load scipion and start scipion
if __name__ == '__main__':
    app.run()
