import os
from flask import Flask, g, render_template, request, jsonify, url_for, send_file, Response, make_response
import sqlalchemy
from cloud_dfs.token import TokenManager, NotAvailableTokenError
from cloud_dfs.database.models import Data, DataGroup
from cloud_dfs.file import FileManager
from cloud_dfs.database import db_session, init_db


def _helpful_msg_json():
    return jsonify({
        "api_doc": "https://github.com/DrawML/cloud_dfs/wiki/Rest-API#drawml-cloud-rest-api",
        "drawml_repo": "https://github.com/DrawML",
        "who_are_we": "Stacker"
    })


def create_app():
    app = Flask(__name__)

    init_db()

    data_file_root_dir = os.path.dirname(os.sys.modules[__name__].__file__) + '/files'
    print("Data File Root Directory :", data_file_root_dir)
    FileManager(data_file_root_dir)

    data_obj_list = db_session.query(Data).all()
    allocated_tokens = [data_obj.token for data_obj in data_obj_list]
    token_manager = TokenManager(allocated_tokens)

    @app.errorhandler(404)
    def not_found(error):
        return '', 404

    @app.errorhandler(500)
    def server_error(error):
        return '', 500

    @app.route('/', methods=['GET'])
    def index():
        return _helpful_msg_json(), 200

    @app.route('/help', methods=['GET'])
    def help():
        return _helpful_msg_json(), 200

    @app.route('/group', methods=['POST'])
    def create_group():
        json_data = request.get_json()
        name = json_data['name']

        token = token_manager.get_avail_token()
        try:
            data_group = DataGroup(name, token)
            db_session.add(data_group)
            db_session.commit()

            print("Created Data Group :", data_group)
            return jsonify({
                'token': token.hex()
            }), 201
        except Exception:
            token_manager.del_token(token)
            raise

    @app.route('/group/<hex_token>', methods=['GET'])
    def get_group_info(hex_token):
        token = bytes.fromhex(hex_token)
        try:
            data_group = db_session.query(DataGroup).filter(DataGroup.token == token).one()
        except sqlalchemy.orm.exc.NoResultFound:
            return '', 404

        print("Got Data Group :", data_group)
        return jsonify({
            'name': data_group.name,
            'data_token_list': [data.token.hex() for data in data_group.data_list]
        }), 200

    @app.route('/group/<hex_token>', methods=['DELETE'])
    def remove_group(hex_token):
        token = bytes.fromhex(hex_token)
        try:
            data_group = db_session.query(DataGroup).filter(DataGroup.token == token).one()
            db_session.delete(data_group)
            db_session.commit()
        except sqlalchemy.orm.exc.NoResultFound:
            return '', 404

        print("Removed Data Group :", data_group)
        token_manager.del_token(token)
        return '', 204

    @app.route('/data', methods=['POST'])
    def put_data():
        content_type = request.headers.get('Content-Type')
        if 'application/json' in content_type:
            json_data = request.get_json()
            name = json_data['name']
            data = json_data['data']
            data_group_hex_token = json_data.get('group_token', None)
            data_type = 'text'
        elif 'multipart/form-data' in content_type:
            data_file = request.files['data']
            name = data_file.filename
            data = data_file.read()  # TODO: will be modified.
            data_group_hex_token = request.form.get('group_token', None)
            data_type = 'binary'
        else:
            print('Invalid Content-Type:', content_type)
            return 'invalid content-type', 400

        token = token_manager.get_avail_token()
        try:
            hex_token = token.hex()

            if data_group_hex_token is None:
                data_group = None
            else:
                data_group_token = bytes.fromhex(data_group_hex_token)
                try:
                    data_group = db_session.query(DataGroup).filter(DataGroup.token == data_group_token).one()
                except sqlalchemy.orm.exc.NoResultFound:
                    # TODO: Bad Code.. must be modified.
                    token_manager.del_token(token)
                    return '', 404

            path = FileManager().store(hex_token, data)

            data_obj = Data(name, token, path, data_type, data_group)
            db_session.add(data_obj)
            db_session.commit()

            print("Putted Data :", data_obj)
            return jsonify({
                'token': token.hex()
            }), 201
        except:
            token_manager.del_token(token)
            raise

    @app.route('/data/<hex_token>', methods=['GET'])
    def get_data(hex_token):
        token = bytes.fromhex(hex_token)
        try:
            data_obj = db_session.query(Data).filter(Data.token == token).one()
        except sqlalchemy.orm.exc.NoResultFound:
            return '', 404

        print("Got Data :", data_obj)

        if data_obj.data_type == 'binary':
            response = make_response(send_file(data_obj.path, mimetype='application/octet-stream',
                             as_attachment=True, attachment_filename=data_obj.name))
        elif data_obj.data_type == 'text':
            with open(data_obj.path, 'rt') as f:
                data = f.read()

            response = make_response(jsonify({
                'name': data_obj.name,
                'data': data
            }))
        else:
            return '', 500

        response.status_code = 200
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    @app.route('/data/<hex_token>', methods=['DELETE'])
    def del_data(hex_token):
        token = bytes.fromhex(hex_token)
        try:
            data_obj = db_session.query(Data).filter(Data.token == token).one()
            db_session.delete(data_obj)
            db_session.commit()
        except sqlalchemy.orm.exc.NoResultFound:
            return '', 404
        token_manager.del_token(token)

        print("Deleted Data :", data_obj)

        FileManager().remove(data_obj.path)

        return '', 204

    @app.teardown_request
    def shutdown_session(exception=None):
        db_session.remove()

    """
    @app.teardown_appcontext
    def shutdown_session(response_or_exc):
        try:
            if response_or_exc is None:
                db_session.commit()
        finally:
            db_session.remove()
        return response_or_exc
    """

    return app
