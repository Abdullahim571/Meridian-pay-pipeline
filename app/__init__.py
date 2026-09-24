from flask import Flask, jsonify


def create_app(config: dict | None = None) -> Flask:
    app = Flask(__name__)
    if config:
        app.config.update(config)

    @app.get("/")
    def index():
        return jsonify(service="meridian-pay", status="ok")

    @app.get("/health")
    def health():
        return jsonify(status="healthy"), 200

    return app
