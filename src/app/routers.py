import logging
import os
import hashlib
import requests
import jwt
from flask import Flask, jsonify, render_template, request, redirect, url_for, Response, flash
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from flask_wtf.csrf import generate_csrf, CSRFError
from injector import inject, Injector
from src.app.app_service.auth_service import LoginUser, PasswordService
from src.application.users.commands.create_new_user_request import CreateNewUserRequest
from src.application.users.commands.if_create_new_user_command import ICreateNewUserCommand
from src.application.users.queries.if_get_auth_data_by_email_and_pass import IGetAuthDataQuery
from src.application.users.queries.if_get_user_by_id import IGetUserQuery
from src.application.users.queries.user_auth_data_response import UserAuthDataResponse
from src.application.users.queries.user_data_response import UserDataResponse
from src.application.users.queries.if_get_auth_data_by_line_id import (
    UserAuthDataByLineResponse, IGetAuthDataByLineIdQuery
)
from src.application.users.commands.if_create_new_user_by_line_command import (
    ICreateNewUserByLineCommand, CreateNewUserByLineRequest
)

# 参考：https://qiita.com/yuta6234/items/95425ea862f4e9ab6def
# flask csrf https://agohack.com/create-form-with-flask-wtf/
# flask-login https://tomokichi.blog/%E3%80%90python%E3%80%91%E3%83%AD%E3%82%B0%E3%82%A4%E3%83%B3%E6%A9%9F%E8%83%BD%E3%82%92%E4%BD%9C%E3%82%8B%E3%80%8Cflask-login%E3%80%8D%E2%91%A4/

LINE_AUTH_URL = 'https://access.line.me/oauth2/v2.1/authorize'
LINE_TOKEN_URL = 'https://api.line.me/oauth2/v2.1/token'
LINE_PROFILE_URL = 'https://api.line.me/v2/profile'


@login_required
def home_page_load() -> str:
    return render_template('home.html')


def sign_up_page_load() -> str:
    return render_template('auth/sign_up.html', csrf_token=generate_csrf())


def login_page_load():
    return render_template('auth/login.html', csrf_token=generate_csrf())


@inject
def login_post_page(query_service: IGetAuthDataQuery):
    upn = request.form.get('upn')
    password = request.form.get('password')

    # パスワードをハッシュ化
    pwd_service: PasswordService = PasswordService(password=str(password))

    # upnとパスワードをキーにユーザを取得
    get_user_auth_data: UserAuthDataResponse = (
        query_service.execute(upn=upn, hashed_password=pwd_service.password_hash_it()))

    if not get_user_auth_data:
        failed_msg = "ログインに失敗しました。正しいユーザ名または、パスワードを入力してください。"
        flash(failed_msg)
        return redirect(url_for('login_page_load'))

    # flask_authを使用する
    login_user(user=LoginUser(user_id=get_user_auth_data.id,
                              user_name=get_user_auth_data.user_name))

    return redirect(url_for('home_page_load'))


def line_login():
    """LINEでログイン"""
    params = {
        'response_type': 'code',
        'client_id': os.environ['LINE_CHANNEL_ID'],
        'redirect_uri': os.environ['LINE_REDIRECT_URI'],
        'state': hashlib.sha256(os.urandom(32)).hexdigest(),
        'scope': 'profile openid email',
    }
    return redirect(f"{LINE_AUTH_URL}?{requests.compat.urlencode(params)}")


def line_callback(
        query_service: IGetAuthDataByLineIdQuery,
        create_new_user_command: ICreateNewUserByLineCommand):
    code = request.args.get('code')
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': os.environ['LINE_REDIRECT_URI'],
        'client_id': os.environ['LINE_CHANNEL_ID'],
        'client_secret': os.environ['LINE_CLIENT_SECRET'],
    }
    response = requests.post(LINE_TOKEN_URL, headers=headers, data=data)
    response_data = response.json()
    access_token = response_data.get('access_token')
    id_token = response_data.get('id_token')

    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(LINE_PROFILE_URL, headers=headers)
    profile = response.json()
    line_id = profile.get('userId')
    decoded = jwt.decode(id_token, options={"verify_signature": False}, algorithms=["HS256"])
    line_user_email = decoded.get('email')
    line_user_name = decoded.get('name')

    # LINEのユーザーIDを使用してアプリケーションのユーザーを検索
    login_user_by_line: UserAuthDataByLineResponse = (query_service.execute(line_id=line_id))
    # ユーザーが存在しない場合は新しいユーザーを作成
    if not login_user_by_line:
        req: CreateNewUserByLineRequest = CreateNewUserByLineRequest(
            line_id=line_id,
            user_name=line_user_name,
            mail_address=line_user_email)
        try:
            create_new_user_command.execute(req)

        except Exception as e:
            logging.error(e)
            failed_msg = f"アカウントの登録に失敗しました。\n{str(e)}"
            flash(failed_msg)
            return redirect(url_for('sign_up_page_load'))

    # ログインユーザの再検索
    login_user_by_line = (query_service.execute(line_id=line_id))

    # ユーザーをログイン状態にする
    login_user(user=LoginUser(user_id=login_user_by_line.id,
                              user_name=login_user_by_line.user_name))

    return redirect(url_for('home_page_load'))


def execute_logout():
    logout_user()
    return redirect(url_for('login_page_load'))


@inject
def post_new_login_user(
        create_new_user_command: ICreateNewUserCommand,
        query_service: IGetAuthDataQuery):
    # パスワードハッシュ化サービスの初期化
    pwd_service: PasswordService = PasswordService(request.form.get('password'))
    # メールアドレスは登録した情報を取得する際に作成するため保持
    email_address: str = request.form.get('email')

    req: CreateNewUserRequest = CreateNewUserRequest(
        user_name=request.form.get('user_name'),
        mail_address=email_address,
        password=pwd_service.password_hash_it()
    )
    try:
        create_new_user_command.execute(request=req)
    except Exception as e:
        logging.error(e)
        failed_msg = f"アカウントの登録に失敗しました。\n{str(e)}"
        flash(failed_msg)
        return redirect(url_for('sign_up_page_load'))

    # 登録したユーザを再度取得 idはドメイン層で発行されるため
    registered_login_user: UserAuthDataResponse = (
        query_service.execute(upn=email_address, hashed_password=pwd_service.password_hash_it()))

    if not registered_login_user:
        failed_msg = f"アカウントの登録に成功しましたが、そのアカウントでのログインに失敗しました。ログインして失敗した場合問い合わせてください。"
        flash(failed_msg)
        return redirect(url_for('login_page_load'))

    # flask_authを使用する
    login_user(user=LoginUser(user_id=registered_login_user.id, user_name=registered_login_user.user_name))
    return redirect(url_for('home_page_load'))


@inject
def get_user(user_id: str, query_service: IGetUserQuery) -> tuple[Response, int]:
    try:
        return_user: UserDataResponse = query_service.execute(user_id)
        if return_user:
            return jsonify(return_user), 200
        return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        logging.error(f'Error adding user: {e}')
        return jsonify({'error': 'Internal server error'}), 500


def configure_routing(app: Flask, login_manager: LoginManager, injector: Injector) -> None:
    def _load_login_user(login_user_id: str) -> LoginUser:
        """
        ログインユーザ情報をロードします。
        :param login_user_id: str
        :return: LoginUser *UserMixinを継承している
        """
        user: UserDataResponse = (
            injector.get(IGetUserQuery).execute(user_id=login_user_id))
        # やること: ユーザをis_activeにする

        return LoginUser(user_id=login_user_id, user_name=user.user_name)

    def _login_post_page():
        return login_post_page(query_service=injector.get(IGetAuthDataQuery))

    def _line_callback():
        return line_callback(query_service=injector.get(IGetAuthDataByLineIdQuery),
                             create_new_user_command=injector.get(ICreateNewUserByLineCommand))

    def _get_user(user_id: str):
        return get_user(user_id, query_service=injector.get(IGetUserQuery))

    def _post_new_login_user():
        return post_new_login_user(
            create_new_user_command=injector.get(ICreateNewUserCommand),
            query_service=injector.get(IGetAuthDataQuery))

    def _handle_csrf_error(e):
        return render_template('404.html', reason=e.description), 400

    # ログイン画面のビューをflask-loginにインプットする
    login_manager.login_view = "login_page_load"
    # flask-loginでログインのユーザをロードする
    login_manager.user_loader(_load_login_user)

    # 以下ルーティング
    app.errorhandler(CSRFError)(_handle_csrf_error)
    # 通常ログイン
    app.route('/', methods=['GET'])(home_page_load)
    app.route('/signup', methods=['GET'])(sign_up_page_load)
    app.route('/signup', methods=['POST'])(_post_new_login_user)
    app.route('/login', methods=['GET'])(login_page_load)
    app.route('/login', methods=['POST'])(_login_post_page)
    # lineでのログイン
    app.route('/login/line')(line_login)
    app.route('/callback/line')(_line_callback)

    app.route('/logout')(execute_logout)
    app.route('/user/<string:user_id>', methods=['GET'])(_get_user)
