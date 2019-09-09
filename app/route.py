from flask import render_template, url_for, session, redirect, request, \
    make_response
from werkzeug.utils import secure_filename

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
from like import Like


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
            searchl = SearchUser(application)
            userdb = UserData(application)
            user = userdb.get_data(session['id'])
            users = searchl.preferences(user)
            users = userdb.get_users(users)
            return render_template('search.html', name=session['username'],
                                   users=users)
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
            print(searchl.search(tuple(form.tags.data), None, form.min_age.data,
                                 form.max_age.data, sex_pref='Male'))
            users = searchl.search(form.tags.data,
                                   (form.country.data, form.region.data,
                                    form.city.data),
                                   form.min_age.data, form.max_age.data,
                                   form.min_rating.data, form.max_rating.data,
                                   form.sex_pref.data)
            users = UserData(application).get_users(users, form.sort_age.data,
                                                    form.sort_rating.data)
            print(users)
            return render_template('search.html', users=users,
                                   name=session['username'],
                                   search={'age': form.sort_age.data,
                                           'rating': form.sort_rating.data})
        else:
            return render_template('search.html', form=form,
                                   name=session['username'])

    @application.route('/test/<int:phid>')  # TODO: Вынести в мини-апи
    def test(phid: int):
        exchange = ImageExchange(application)
        img = exchange.download_img(phid)
        response = make_response(img)
        response.headers.set('Content-type', 'image')
        return response

    @application.route('/user/<int:uid>')
    def user(uid: int):
        user = UserData(application).get_data(uid)
        return render_template('profile_page.html', user=user,
                               name=session['username'], like='like')

    @application.route('/test_like/<int:uid>', methods=['GET'])
    def test_like(uid: int):
        if uid == session['id']:
            return {'request': 'success', 'like': 'false',
                    'reason': 'self-like'}, 403
        if Like(application).add_like(session['id'], uid):
            return {'request': 'success', 'like': 'true'}
        else:
            return "biba"



