import os
from flask import Flask, g, render_template, request, jsonify, url_for, send_file
import sqlalchemy
from cloud_dfs.token import TokenManager, NotAvailableTokenError
from cloud_dfs.database.models import Data
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

    @app.route('/data', methods=['POST'])
    def put_data():
        content_type = request.headers.get('Content-Type')
        if 'application/json' in content_type:
            json_data = request.get_json()
            name = json_data['name']
            data = json_data['data']
            data_type = 'text'
        elif 'multipart/form-data' in content_type:
            data_file = request.files['data']
            name = data_file.filename
            data = data_file.read()  # will be modified.
            data_type = 'binary'
        else:
            print('Invalid Content-Type:', content_type)
            return 'invalid content-type', 400

        token = token_manager.get_avail_token()
        try:
            hex_token = token.hex()

            path = FileManager().store(hex_token, data, data_type)

            data_obj = Data(name, token, path, data_type)
            db_session.add(data_obj)
            db_session.commit()

            print(token)
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

        print(data_obj)

        if data_obj.data_type == 'binary':
            return send_file(data_obj.path, mimetype='application/octet-stream',
                             as_attachment=True, attachment_filename=data_obj.name), 200
        elif data_obj.data_type == 'text':
            with open(data_obj.path, 'r') as f:
                data = f.read()
            return jsonify({
                'name': data_obj.name,
                'data': data
            }), 200
        else:
            return '', 500

    @app.route('/data/<hex_token>', methods=['DELETE'])
    def del_data(hex_token):
        token = bytes.fromhex(hex_token)
        try:
            data_obj = db_session.query(Data).filter(Data.token == token).one()
            db_session.query(Data).filter(Data.token == token).delete()
            db_session.commit()
        except sqlalchemy.orm.exc.NoResultFound:
            return '', 404

        token_manager.del_token(token)

        print(data_obj)

        FileManager().remove(data_obj.path)

        return '', 204

    return app
