(function () {
    // Model for session object
    var ScipionSessionModel = Backbone.Model.extend({
        url: '/session',
        defaults: {
            session_id: 'session-id',
            microscope: '',
            dose_per_frame: null,
            numberOfIndividualFrames: null
        },
        validate: function (attrs, options) {
             if (isNaN(attrs.dose_per_frame)||isNaN(attrs.numberOfIndividualFrames)){
                return "Invalid entries!"
            }
        }
    });
    // Model for configuration items
    var ScipionConfigModel = Backbone.Model.extend({
        defaults: {
            'dose_per_frame': null,
            'numberOfIndividualFrames':null
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
            this.$('#scipion_dose').val(this.model.get('dose_per_frame'));
            this.$('#scipion_n_frames').val(this.model.get('numberOfIndividualFrames'));
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
            'click .scipion_config_btn': 'show_form',
            'click #scipion_save': 'on_spc_save',
            'click #scipion_cancel': 'on_spc_cancel',
            'keyup #scipion_dose': 'on_dose_change',
            'keyup #scipion_n_frames': 'on_n_frames_change'
        },

        initialize: function () {
            this.listenTo(this.model, 'sync change', this.render);
            this.model.fetch();
            this.render();
        },

        render: function () {
            let html = '<b>Your session id: </b>' + this.model.get('session_id');
            this.$('#scipion_session_id_label').html(html);
            this.$('#scipion_microscope').val(this.model.get('microscope'));
            this.$('#scipion_config_div').hide();
            // this.$('#scp_msg_label').hide();

            var mic = this.model.get('microscope');
            var dpf = this.model.get('dose_per_frame');
            var nif = this.model.get('numberOfIndividualFrames');
            var mic_url = '/get_config/' + mic;

            var cm = new ScipionConfigModel();
            if (dpf==null && nif==null){
                cm.fetch({url: mic_url});
            }
            else{
                cm.set({
                'dose_per_frame': dpf,
                'numberOfIndividualFrames': nif
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
                    'dose_per_frame': this.$('#scipion_dose').val(),
                    'numberOfIndividualFrames': this.$('#scipion_n_frames').val(),
                    'microscope': this.$('#scipion_microscope').val()
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

        on_dose_change: function () {
            if(isNaN(this.$('#scipion_dose').val())||isNaN(this.$('#scipion_n_frames').val())){
                this.$('#scipion_msg_label').html('<b><font color="red"> Invalid entries</font></b>');
            }
            else{
                this.$('#scipion_msg_label').html('');
            }

        },

        on_n_frames_change: function () {
            if(isNaN(this.$('#scipion_n_frames').val())||isNaN(this.$('#scipion_dose').val())){
                this.$('#scipion_msg_label').html('<b><font color="red"> Invalid entries</font></b>');
            }
            else{
                this.$('#scipion_msg_label').html('');
            }

        }
    });

    var sv = new ScipionConfigView({model: new ScipionSessionModel()});
 })();