from flask import Flask, jsonify, render_template, request, Blueprint



def create_app():
    app=Flask(__name__)


    app.config['SECRET_KEY'] = 'i dont know why i have to choose this'

    from image.routes.predict import bp

    app.register_blueprint(bp)

    return app

if __name__ == "__main__":
  app = create_app()
  app.debug=True
  app.run()