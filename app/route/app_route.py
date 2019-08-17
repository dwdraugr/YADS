from flask import render_template

def init(application):
    @application.route('/')
    def he():
        return render_template('base.html')
