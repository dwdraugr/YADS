from flask import render_template
from app.forms.SignInForm import SignInForm
from app.model.sign_in import SignIn

def init(application):
    @application.route('/')
    def root():
        return render_template('base.html')

    @application.route('/sign_in', methods=['GET'])
    def he():
        form = SignInForm()
        return render_template('sign_in.html', form=form)

    @application.route('/sign_in', methods=['POST'])
    def ke():
        form = SignInForm()
        if form.validate_on_submit():
            SignIn().sign_in(form.username.data, form.password.data)
            return render_template('sign_in.html', name=form.username.data, form=form)
