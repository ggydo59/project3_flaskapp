from flask import Flask



def create_app():
    app=Flask(__name__)


    app.config['SECRET_KEY'] = 'i dont know why i have to choose this'

    from predict import bp
    from prepare import pre_bp
    app.register_blueprint(bp)
    app.register_blueprint(pre_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port='5000')