from flask import render_template, url_for, session, redirect, request
from app.forms.sign_in_form import SignInForm
from app.forms.sign_up_form import SignUpForm
from app.forms.input_info_form import InputInfoForm
from app.model.auth import Auth
from app.model.sign_up import SignUp
from app.model.collect_info import CollectInfo


def init(application):
    @application.route('/')
    def root(message=None, message_type=None):
        if 'id' in session:
            return render_template('base.html', name=session['username'],
                                   message=message,
                                   message_type=message_type)
        else:
            return render_template('base.html', message=message,
                                   message_type=message_type)

    @application.route('/sign_in', methods=['GET'])
    def sign_in_get():
        form = SignInForm()
        json = dict(request.args)
        if 'type' in json and json['type'] == 'confirmed':
            return render_template('sign_in.html', form=form,
                                   message='Account confirmed!',
                                   message_type='alert-success')
        else:
            return render_template('sign_in.html', form=form)

    @application.route('/sign_in', methods=['POST'])
    def sign_in_post():
        form = SignInForm()
        if form.validate():
            Auth().sign_in(form.username.data, form.password.data)
            if session['full_profile'] == 0:
                return redirect(url_for('input_info'))
        else:
            return redirect(url_for('sign_in_get', type='confirmed'))

    @application.route('/sign_up', methods=['GET'])
    def sign_up_get():
        form = SignUpForm()
        return render_template('sign_up.html', form=form)

    @application.route('/sign_up', methods=['POST'])
    def sign_up_post():
        form = SignUpForm()
        if form.validate():
            sign_up = SignUp(application)
            sign_up.sign_up(form.username.data, form.email.data,
                            form.password.data)
            return root("Account created! Check you email for confirm it"
                        , 'alert-success')
        else:
            return render_template('sign_up.html', form=form)

    @application.route('/sign_out', methods=['GET'])
    def sign_out_post():
        auth = Auth()
        auth.sign_out()
        return redirect('/')

    @application.route('/confirm/<string:reason>/<string:seed>')
    def confirm_account(seed, reason='new'):
        if reason == 'new':
            Auth().mail_confirm(seed)
            return redirect(url_for('sign_in_get', type='confirmed'))
        else:
            return '<center><h1>BIBU PASASI</h1></center>'

    @application.route('/info', methods=['GET', 'POST'])
    def input_info():
        form = InputInfoForm()
        if session['id'] is None:
            redirect(url_for('sign_in_get'))
        if request.method == 'POST':
            if form.validate():
                info = CollectInfo()
                info.collect_all({
                    'uid': session['id'],
                    'first': request.form['first_name'],
                    'last': request.form['last_name'],
                    'gender': request.form['gender'],
                    'sex_pref': request.form['sex_pref'],
                    'age': request.form['age'],
                    'biography': request.form['biography'],
                    #   'tags': request.form['tags'],
                    'ip': request.remote_addr
                })
                return request.form
            else:
                return render_template('input_info.html', form=form)
        else:
            return render_template('input_info.html', form=form)
