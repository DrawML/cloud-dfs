from flask import Flask, g, render_template, request, jsonify, url_for


def _helpful_msg_json():
    return jsonify({
        "api_doc": "https://github.com/DrawML/cloud_dfs/wiki/Rest-API#drawml-cloud-rest-api",
        "drawml_repo": "https://github.com/DrawML",
        "who_are_we": "Stacker"
    })


def create_app():
    app = Flask(__name__)

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
        raise NotImplementedError

    @app.route('/data/<token>', methods=['GET'])
    def get_data(token):
        raise NotImplementedError

    @app.route('/data/<token>', methods=['DELETE'])
    def del_data(token):
        raise NotImplementedError

    return app
