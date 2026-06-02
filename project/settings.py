import flask, os
import flask_socketio

main_app = flask.Flask(
    import_name = 'project',
    static_folder = 'static',
    template_folder = 'templates',
    instance_path = os.path.abspath(os.path.join(__file__, '..', 'instance'))
)
socketio = flask_socketio.SocketIO(app= main_app)