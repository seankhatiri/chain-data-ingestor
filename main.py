from flask_migrate import Migrate
from configuration.configs import Configs
from flask_app import create_app, db
from flask_app.base.models import User
from utility.logger import Logger
from flask_cors import CORS
import pickle
import requests
from middleware import CORSMiddleware

app = create_app(Configs)
# Use the custom CORS middleware
app.wsgi_app = CORSMiddleware(app.wsgi_app)
Migrate(app, db)

@app.before_first_request
def set_admin_user():
    user = User.query.filter_by(username='socialBlock').first()
    if not user:
        user = User(username='socialBlock', password='admin@socialblock2023', is_admin= True)
        db.session.add(user)
        db.session.commit()


if __name__ == "__main__":
    Logger().info('App is started!')
    app.run(host='0.0.0.0', port=Configs.port, debug=False, load_dotenv=True, use_reloader=False, use_debugger=False) 
