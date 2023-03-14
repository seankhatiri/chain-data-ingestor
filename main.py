from flask_migrate import Migrate
from configuration.configs import Configs
from flask_app import create_app, db
from flask_app.base.models import User
from utility.logger import Logger

app = create_app(Configs)
Migrate(app, db)



@app.before_first_request
def set_admin_user():
    user = User.query.filter_by(username='socialBlock').first()
    if not user:
        user = User(username='socialBlock', email='socialblock@gmail.com', password='admin@socialblock2023')
        db.session.add(user)
        db.session.commit()


if __name__ == "__main__":
    Logger().info('App is started!')
    app.run(host='0.0.0.0', port=Configs.port, debug=True, load_dotenv=True, use_reloader=True, use_debugger=False) 
