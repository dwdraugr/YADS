import io
from base64 import b64encode

from flask import render_template, url_for, session, redirect, request, flash, \
    send_file, make_response
from werkzeug.utils import secure_filename
from app.model.search_users import SearchUser
from app.forms.sign_in_form import SignInForm
from app.forms.sign_up_form import SignUpForm
from app.forms.input_info_form import InputInfoForm
from app.forms.upload_img import UploadImage
from app.model.auth import Auth
from app.model.sign_up import SignUp
from app.model.collect_info import CollectInfo
from get_user_data import UserData
from image_exchange import ImageExchange
from search import Search


def init(application):
    @application.before_request
    def before_request():
        if 'id' in session and session['full_profile'] == 0 \
                and request.endpoint != 'input_info':
            if request.endpoint == 'sign_out':
                pass
            else:
                print('bob')
                return redirect(url_for('input_info'))

    @application.route('/')
    def root(message=None, message_type=None):
        if 'id' in session:
            return render_template('base.html', name=session['username'])
        else:
            return render_template('start_page.html')

    @application.route('/main', methods=['GET'])
    def main_get():
        if 'id' in session:
            upload_form = UploadImage()
            user = UserData(application).get_data(session['id'])
            return render_template('profile_page.html', user=user,
                                   name=session['username'],
                                   form=upload_form)
        else:
            return redirect(url_for('root'))

    @application.route('/main', methods=['POST'])  # TODO: Вынести в мини-апи
    def main_post():
        if 'id' in session:
            upload_form = UploadImage()
            exchange = ImageExchange(application)
            if request.files:
                f = request.files['img']
                f.save(secure_filename(f.filename))
                url = f.filename
                exchange.upload_img(url, session['id'])
                return secure_filename(request.files['img'].filename)
            else:
                return render_template('profile_page.html', form=upload_form,
                                       user=UserData(application)
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
            Auth(application).sign_in(form.username.data, form.password.data)
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
        auth = Auth(application)
        auth.sign_out()
        return redirect('/')

    @application.route('/confirm/<string:reason>/<string:seed>')
    def confirm_account(seed, reason='new'):
        if reason == 'new':
            Auth(application).mail_confirm(seed)
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
                info = CollectInfo(application)
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

            searchl = SearchUser(application)
            return {
                'tags': searchl.search_by_tags(tuple(form.tags.data)),
                'geo': searchl.search_by_geo(city='Moscow'),
                'age': searchl.search_by_age(form.min_age.data, form.max_age.data),
                'sex pref': searchl.search_by_gender('Femae')
            }

    @application.route('/test/<int:phid>')  # TODO: Вынести в мини-апи
    def test(phid: int):
        exchange = ImageExchange(application)
        img = exchange.download_img(phid)
        response = make_response(img)
        response.headers.set('Content-type', 'image')
        return response
