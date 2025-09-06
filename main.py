from flask import Flask, request
import os

def create_app():
    app = Flask(__name__)

    @app.get("/")
    def index():
        message = os.getenv("MESSAGE", "Hello from Dockerized Python! 🚀")
        # Return HTML with green message
        return f"""
        <html>
            <head><title>Python Docker App</title></head>
            <body style="font-family: Arial, sans-serif; text-align: center; margin-top: 50px;">
                <h1 style="color: yellow;">{message}</h1>
            </body>
        </html>
        """

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8000")), debug=True)
