import flask

message = flask.Blueprint(
    name= "message",
    import_name= "message",
    template_folder= "templates",
    static_folder= "static",
    static_url_path= "/message/static/"
)