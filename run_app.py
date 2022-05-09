from app import create_app
from app.config import Config
from app.main.models import db, Aquarium, AquariumTemperature


app = create_app(Config)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Aquarium': Aquarium,
            'AquariumTemperature': AquariumTemperature}

