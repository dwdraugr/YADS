import mysql.connector
from flask import Flask, render_template, redirect, url_for, request
from werkzeug.exceptions import HTTPException


def init(application: Flask):
    @application.errorhandler(NameError)
    def name_error_exception(e: NameError):
        return render_template('base.html', message=e,
                               message_type='alert-danger')

    @application.errorhandler(TypeError)
    def name_error_exception(e: TypeError):
        return render_template('base.html', message=e,
                               message_type='alert-danger')

    @application.errorhandler(ValueError)
    def name_error_exception(e: ValueError):
        return render_template('base.html', message=e,
                               message_type='alert-danger')

    @application.errorhandler(mysql.connector.Error)
    def mysql_error_exception(e: mysql.connector.Error):
        return render_template('base.html', message=e,
                               message_type='alert-danger')
