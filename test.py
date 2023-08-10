from flask import Flask, request
import os

def restart_app():
    import os
    os.environ["WERKZEUG_RUN_MAIN"] = "true"
    func = request.environ.get("werkzeug.server.shutdown")
    if func is not None:
        func()

# You can call the `restart_app` function when you want to clear the cache (restart the app):
# Example:
restart_app()
# app.run()