from flask import render_template, url_for, session, redirect
from app.forms.sign_in_form import SignInForm
from app.forms.sign_up_form import SignUpForm
from app.model.auth import Auth
from app.model.sign_up import SignUp


def init(application):
    @application.route('/')
    def root():
        if 'id' in session:
            return render_template('base.html', name=session['username'])
        else:
            return render_template('base.html')

    @application.route('/sign_in', methods=['GET'])
    def sign_in_get(message=None, message_type=None):
        form = SignInForm()
        if message is None:
            return render_template('sign_in.html', form=form)
        else:
            return render_template('sign_in.html', form=form, message=message,
                                   message_type=message_type)

    @application.route('/sign_in', methods=['POST'])
    def sign_in_post():
        form = SignInForm()
        if form.validate():
            Auth().sign_in(form.username.data, form.password.data)
            return redirect('/')
        else:
            render_template('sign_in.html', form=form)

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
            return sign_in_get("Account created! Check you email for confirm it"
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
            return sign_in_get("Account confirmed!", "alert-success")
        else:
            return '<center><h1>BIBU PASASI</h1></center>'
