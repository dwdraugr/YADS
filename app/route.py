from flask import render_template, url_for, session, redirect, request, \
    make_response
import re
from werkzeug.utils import secure_filename
from datetime import datetime
from app.forms.input_info_form import InputInfoForm
from app.forms.search import Search
from app.forms.sign_in_form import SignInForm
from app.forms.sign_up_form import SignUpForm
from app.forms.upload_img import UploadImage
from app.model.auth import Auth
from app.model.collect_info import CollectInfo
from app.model.get_user_data import UserData
from app.model.image_exchange import ImageExchange
from app.model.search_users import SearchUser
from app.model.sign_up import SignUp
from app.model.like import Like
from app.model.online import Online
from app.forms.settings import *  # new settings forms added
from app.model.settings import *  # new settings models added
from app.model.dialogs import Dialogs
from app.model.messages import Messages
from app.model.compare_users import CompareUsers
from app.model.guests import GuestsCheck


def init(application):
    @application.before_request
    def before_request():
        # if 'id' not in session and re.search(r"[\S]+api$", request.endpoint):
        #     return {}, 204
        # if 'id' in session and re.search(r"[\S]+api$", request.endpoint):
        #     return {}, 204
        if 'id' in session and session['full_profile'] == 0 \
                and request.endpoint != 'input_info':
            if request.endpoint == 'sign_out':
                pass
            else:
                print('bob')
                return redirect(url_for('input_info'))
        if 'id' not in session \
                and request.endpoint != 'root' \
                and request.endpoint != 'sign_in_get' \
                and request.endpoint != 'sign_in_post' \
                and request.endpoint != 'sign_up_get' \
                and request.endpoint != 'static' \
                and request.endpoint != 'confirm_account' \
                and request.endpoint != 'sign_up_post':
            return redirect(url_for('sign_in_get'))
        if 'id' in session:
            Online().set_online(session['id'])

    @application.route('/')
    def root(message=None, message_type=None):
        if 'id' in session:
            searchl = SearchUser()
            userdb = UserData()
            user = userdb.get_data(session['id'])
            users = searchl.preferences(user)
            users = userdb.get_users(users)
            return render_template('search.html',
                                   users=users, d_message='5')
        elif message is not None:
            return render_template('start_page.html', message=message,
                                   message_type=message_type)
        else:
            return render_template('start_page.html')

    @application.route('/main', methods=['GET'])
    def main_get():
        if 'id' in session:
            upload_form = UploadImage()
            user = UserData().get_data(session['id'])
            return render_template('profile_page.html', user=user,

                                   form=upload_form)
        else:
            return redirect(url_for('root'))

    @application.route('/main', methods=['POST'])  # TODO: Вынести в мини-апи
    def main_post():
        if 'id' in session:
            upload_form = UploadImage()
            exchange = ImageExchange()
            if request.files:
                f = request.files['img']
                f.save(secure_filename(f.filename))
                url = f.filename
                exchange.upload_img(url, session['id'])
                return secure_filename(request.files['img'].filename)
            else:
                return render_template('profile_page.html', form=upload_form,
                                       user=UserData()
                                       .get_data(session['id']),
                                       name=session['username'])
        else:
            return redirect(url_for('root'))

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
                return redirect(url_for('main_get'))
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
    def sign_out():
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
        if 'id' not in session:
            return redirect(url_for('sign_in_get'))
        if request.method == 'POST':
            if form.validate():
                info = CollectInfo()
                print(form.tags.data)
                print(type(form.tags.data))
                info.collect_all({
                    'uid': session['id'],
                    'first': form.first_name.data,
                    'last': form.last_name.data,
                    'gender': form.gender.data,
                    'sex_pref': form.sex_pref.data,
                    'age': form.age.data,
                    'biography': form.biography.data,
                    'tags': form.tags.data,
                    'ip': request.remote_addr
                })
                return redirect(url_for('main_get'))
            else:
                return render_template('input_info.html', form=form,
                                       name=session['username'])
        else:
            return render_template('input_info.html', form=form,
                                   name=session['username'])

    @application.route('/search', methods=['GET'])
    def search_get():
        form = Search()
        return render_template('search.html', form=form)

    @application.route('/search', methods=['POST'])
    def search_post():
        form = Search()
        if form.validate():
            searchl = SearchUser()
            print(searchl.search(tuple(form.tags.data), None, form.min_age.data,
                                 form.max_age.data, sex_pref='Male'))
            users = searchl.search(form.tags.data,
                                   (form.country.data, form.region.data,
                                    form.city.data),
                                   form.min_age.data, form.max_age.data,
                                   form.min_rating.data, form.max_rating.data,
                                   form.sex_pref.data)
            users = UserData().get_users(users, form.sort_age.data,
                                         form.sort_rating.data)
            print(users)
            return render_template('search.html', users=users,

                                   search={'age': form.sort_age.data,
                                           'rating': form.sort_rating.data})
        else:
            return render_template('search.html', form=form,
                                   name=session['username'])

    @application.route('/settings', methods=['GET'])
    def settings_get():
        json = dict(request.args)
        if 'type' in json and json['type'] == 'email':
            form = SettingsEmailForm()
        elif 'type' in json and json['type'] == 'password':
            form = SettingsPasswordForm()
        else:
            form = SettingGeneralForm()
        return render_template('settings.html', form=form)

    @application.route('/settings', methods=['GET', 'POST'])
    def settings_post():
        message = ''
        json = dict(request.args)
        if 'type' in json and json['type'] == 'email':
            form = SettingsEmailForm()
        elif 'type' in json and json['type'] == 'password':
            form = SettingsPasswordForm()
        else:
            form = SettingGeneralForm()
        if form.validate():
            if 'type' in json and json['type'] == 'email':
                settings = EmailSettings()
                try:
                    message = settings.update_settings(form.new_email.data)
                except NameError as err:
                    return render_template('settings.html', form=form,
                                           message=err,
                                           message_type='alert-danger')
            elif 'type' in json and json['type'] == 'password':
                settings = PasswordSettings()
                try:
                    message = settings.update_settings(form.old_password.data,
                                                       form.new_password.data)
                except NameError as err:
                    return render_template('settings.html', form=form,
                                           message=err,
                                           message_type='alert-danger')
            else:
                settings = GeneralSettings()
                data = {
                    'first': form.first_name.data,
                    'last': form.last_name.data,
                    'gender': form.gender.data,
                    'sex_pref': form.sex_pref.data,
                    'age': form.age.data,
                    'biography': form.biography.data,
                    'tags': form.tags.data
                }
                message = settings.update_settings(data)
            return render_template('settings.html', form=form, message=message,
                                   message_type='alert-success')
        else:
            return render_template('settings.html', form=form)

    @application.route('/user/<int:uid>')
    def user(uid: int):
        user = UserData().get_data(uid)
        GuestsCheck().add_guest(session['id'], uid)
        return render_template('profile_page.html', user=user,
                               like='like')

    @application.route('/dialogs')
    def dialogs():
        dialogs = Dialogs()
        contacts = dialogs.get_contacts()
        return render_template('dialogs.html', contacts=contacts)

    @application.route('/chat', methods=['GET'])
    def dialogs_get():
        get_data = dict(request.args)
        if 'uid' in get_data and get_data['uid'].isnumeric():
            interlocutor_id = get_data['uid']
            messages_model = Messages()
            my_data, interlocutor_data = messages_model.get_data(interlocutor_id)
            messages = messages_model.get_messages(interlocutor_id)
            return render_template('chat.html', my_data=my_data, interlocutor_data=interlocutor_data, messages=messages)
        return redirect(url_for('dialogs'))
