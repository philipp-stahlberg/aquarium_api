from flask import Blueprint

from app.extensions import api
from app.main.resources import AquariumResource, AquariumListResource, TemperatureResource, TemperatureListResource, \
    ChemicalResource, ChemicalListResource, FertilizerResource, FertilizerListResource, FertilizationResource, \
    FertilizationListResource

aquarium_bp = Blueprint('aquarium_bp', __name__)

api.add_resource(AquariumListResource, '/aquariums',)
api.add_resource(AquariumResource, '/aquariums/<string:aquarium_id>')
api.add_resource(TemperatureListResource, '/temperatures')
api.add_resource(TemperatureResource, '/temperatures/<string:temperature_id>')
api.add_resource(ChemicalListResource, '/chemicals')
api.add_resource(ChemicalResource, '/chemicals/<string:chemical_id>')
api.add_resource(FertilizerListResource, '/fertilizers')
api.add_resource(FertilizerResource, '/fertilizers/<string:fertilizer_id>')
api.add_resource(FertilizationListResource, '/fertilization')
api.add_resource(FertilizationResource, '/fertilization/<string:fertilization_id>')
