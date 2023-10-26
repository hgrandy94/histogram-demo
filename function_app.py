import azure.functions as func

from histogram_generator import app

app = func.WsgiFunctionApp(app=app.wsgi_app, http_auth_level=func.AuthLevel.ANONYMOUS)
