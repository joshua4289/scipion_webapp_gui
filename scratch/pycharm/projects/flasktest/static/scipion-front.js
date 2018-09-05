(function () {
    // Model for session object
    var ScipionSessionModel = Backbone.Model.extend({
        url: '/session',
        defaults: {
            session_id: 'session-id',
            microscope: '',
            dosePerFrame: null,
            numberOfIndividualFrames: null,
            samplingRate:null,
            particleSize:null,
            minDist:null,
            findPhaseShift:null
        },
        validate: function (attrs, options) {
             if (isNaN(attrs.dosePerFrame)||isNaN(attrs.numberOfIndividualFrames)){
                return "Invalid entries!"
            }
        }
    });
    // Model for configuration items
    var ScipionConfigModel = Backbone.Model.extend({
        defaults: {
            'dosePerFrame': null,
            'numberOfIndividualFrames':null,
            'samplingRate':null,
            'particleSize':null,
            'minDist':null,
            'findPhaseShift':null
        }
    });

    // Main scipion view object
    var MainScipionView = Backbone.View.extend({
        el: '#scipion_cg',
        events: {
             'change #scipion_microscope': 'on_select_microscope',
        },

        initialize: function () {
            this.listenTo(this.model, 'sync change', this.render);
            // this.model.fetch();
            this.render();
        },

        render: function () {
            this.$('#scipion_dose').val(this.model.get('dosePerFrame'));
            this.$('#scipion_n_frames').val(this.model.get('numberOfIndividualFrames'));
            this.$('#scipion_sampling_rate').val(this.model.get('samplingRate'));
            this.$('#scipion_particle_size').val(this.model.get('particleSize'));
            this.$('#scipion_min_dist').val(this.model.get('minDist'));
            this.$('#scipion_phase_plate').val(this.model.get('findPhaseShift'));
            return this;
        },

        on_select_microscope: function (e) {
            var microscope = this.$('#scipion_microscope').val();
            var mic_url = '/get_config/' + microscope;
            this.model.fetch({url: mic_url});

            return this;
        },

    });
    //embedded view within the main view
    var ScipionConfigView = Backbone.View.extend({
        el: '#scipion_session_view',

        events: {
            'click #scipion_save': 'on_spc_save',
            'click #scipion_cancel': 'on_spc_cancel',

            },
          //  'keyup #scipion_dose': 'on_number_change',
           // 'keyup #scipion_n_frames': 'on_number_change',
           // 'keyup #scipion_sampling_rate': 'on_number_change',
           // 'keyup #scipion_particle_size': 'on_number_change',
           // 'keyup #scipion_min_dist': 'on_number_change'

            // 'keyup #scipion_phase_plate': 'scipion_phase_plate_used',

        initialize: function () {
            this.listenTo(this.model, 'sync change', this.render);
            this.model.fetch();
            this.render();
        },

        render: function () {
            let html = '<b>Your session id: </b>' + this.model.get('session_id');
            this.$('#scipion_session_id_label').html(html);
            this.$('#scipion_microscope').val(this.model.get('microscope'));
            this.$('#scipion_config_div');
            // this.$('#scp_msg_label').hide();

            var mic = this.model.get('microscope');
            var dpf = this.model.get('dosePerFrame');
            var nif = this.model.get('numberOfIndividualFrames');
            var sam = this.model.get('samplingRate');
            var psz = this.model.get('particleSize');
            var pha = this.model.get('findPhaseShift');
            var mdt = this.model.get('minDist');
            var mic_url = '/get_config/' + mic;

            var cm = new ScipionConfigModel();
            if (dpf==null && nif==null && sam==null && psz==null && mdt==null){
                cm.fetch({url: mic_url});
            }
            else{
                cm.set({
                'dosePerFrame': dpf,
                'numberOfIndividualFrames': nif,
                'samplingRate':sam,
                'particleSize':psz,
                'minDist':mdt,
                'findPhaseShift':pha,
                });

            }
            this.config = new MainScipionView({model: cm});
            return this;
        },

        show_form: function (e) {
            this.$('#scipion_config_div').toggle();
        },

        on_spc_save: function () {
            var valid = this.model.save(
                {
                    'dosePerFrame': this.$('#scipion_dose').val(),
                    'numberOfIndividualFrames': this.$('#scipion_n_frames').val(),
                    'samplingRate':this.$('#scipion_sampling_rate').val(),
                    'particleSize':this.$('#scipion_particle_size').val(),
                    'minDist':this.$('#scipion_min_dist').val(),
                    'microscope': this.$('#scipion_microscope').val(),
                    'findPhaseShift': this.$('input[name=scipion_phase_plate]:checked').val()
                });
            if (!valid){
                alert('Invalid entries. Values not saved!');
            }
        },

        on_spc_cancel: function () {
            this.$('#scipion_config_div').hide();
            this.$('#scipion_msg_label').html('');
            this.render();
        },

        on_scipion_run:function() {
        console.log('hello')
        },

        on_number_change: function () {
            if(isNaN(this.$('#scipion_dose').val())||
            isNaN(this.$('#scipion_n_frames').val())||
            isNaN(this.$('#scipion_sampling_rate').val())||
            isNaN(this.$('#scipion_particle_size').val())||
            isNaN(this.$('#scipion_min_dist').val())||
            isNaN(this.$('#scipion_phase_plate').val())){
                this.$('#scipion_msg_label').html('<b><font color="red"> Invalid entries</font></b>');
            }
            else{
                this.$('#scipion_msg_label').html('');
            }

        },
    });

    var sv = new ScipionConfigView({model: new ScipionSessionModel()});
 })();