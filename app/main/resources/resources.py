from flask_restful import Resource, marshal_with, abort
from flask import current_app

from app.main.models import Aquarium, AquariumTemperature, Chemical, Fertilizer, Fertilization, db
from app.http_status_codes import HttpStatus as Status
from .resource_fields import Fields
from app.main.api_parser import ParserFactory
from .controller import make_order_by, ResponseContent, AquariumController, TemperatureController, \
    ChemicalController, FertilizerController, FertilizationController

# Can create parser with different arguments and request types
parser_factory = ParserFactory()

# Utility objects to count, select, order by and filter data from the database for all resources.
aquarium_controller = AquariumController()
temperature_controller = TemperatureController()
chemical_controller = ChemicalController()
fertilizer_controller = FertilizerController()
fertilization_controller = FertilizationController()


def abort_if_resource_not_found(resource, message='Resource not found'):
    if not resource:
        abort(Status.not_found_404, message=message)


class AquariumListResource(Resource):
    """
    Gives access to GET and POST HTTP methods to get multiple aquarium resources or create a new aquarium resource.
    """
    @marshal_with(Fields.aquarium_list_field)
    def get(self):

        parser = parser_factory.aquarium_parser('get')
        args = parser.parse_args()
        order_by = make_order_by(args['order-by'])
        page = args['page']

        items_per_page = current_app.config['ITEMS_PER_PAGE']
        # set pagination attributes for decorator
        aquarium_controller.get_multiple.set_page(page)
        aquarium_controller.get_multiple.set_items_per_page(items_per_page)

        aquariums = aquarium_controller.get_multiple(order_by=order_by)
        aquarium_count = aquarium_controller.count_all()

        response = ResponseContent(aquariums, page, items_per_page, aquarium_count)
        return response, Status.ok_200

    @marshal_with(Fields.aquarium_field)
    def post(self):
        parser = parser_factory.aquarium_parser('post')
        args = parser.parse_args()

        name = args['name']
        if not Aquarium.is_name_available(name):
            abort(Status.conflict_409, message='Name not available')

        new_aquarium = Aquarium(name=args['name'], volume_in_liter=args['volume_in_liter'])
        db.session.add(new_aquarium)
        db.session.commit()
        return new_aquarium, Status.created_201


class AquariumResource(Resource):
    """
    Gives access to GET, PATCH, DELETE HTTP methods to get, update or delete a single aquarium resource.
    """
    @marshal_with(Fields.aquarium_field)
    def get(self, aquarium_id):
        aquarium = aquarium_controller.get_by_id(aquarium_id)
        abort_if_resource_not_found(aquarium)
        return aquarium, Status.ok_200

    @marshal_with(Fields.aquarium_field)
    def patch(self, aquarium_id):
        aquarium = aquarium_controller.get_by_id(aquarium_id)
        abort_if_resource_not_found(aquarium)

        parser = parser_factory.aquarium_parser('patch')
        args = parser.parse_args()

        volume_in_liter = args['volume_in_liter']
        name = args['name']
        if not Aquarium.is_name_available(name):
            abort(Status.conflict_409, message='Name not available')

        aquarium.update_attributes(name=name, volume_in_liter=volume_in_liter)
        db.session.commit()
        return aquarium, Status.ok_200

    def delete(self, aquarium_id):
        aquarium = aquarium_controller.get_by_id(aquarium_id)
        abort_if_resource_not_found(aquarium)
        db.session.delete(aquarium)
        db.session.commit()
        return '', Status.no_content_204


class TemperatureListResource(Resource):
    """
    Gives access to GET and POST HTTP methods to get multiple temperature resources
    or create a new temperature resource.
    """
    @marshal_with(Fields.temperature_list_field)
    def get(self):
        parser = parser_factory.temperature_parser('get')
        args = parser.parse_args()
        order_by = make_order_by(args['order-by'])
        page = args['page']
        aquarium_id = args['aquarium-id']

        items_per_page = current_app.config['ITEMS_PER_PAGE']
        # set pagination attributes for decorator
        temperature_controller.get_multiple.set_page(page)
        temperature_controller.get_multiple.set_items_per_page(items_per_page)

        temperatures = temperature_controller.get_multiple(order_by=order_by, aquarium_id=aquarium_id)
        aquarium_count = temperature_controller.count_all(aquarium_id)
        response = ResponseContent(temperatures, page, items_per_page, aquarium_count)
        return response, Status.ok_200

    @marshal_with(Fields.temperature_field)
    def post(self):
        parser = parser_factory.temperature_parser('post')
        args = parser.parse_args()
        celsius = args['celsius']
        aquarium_id = args['aquarium_id']

        aquarium = aquarium_controller.get_by_id(aquarium_id)
        abort_if_resource_not_found(aquarium)

        temperature = AquariumTemperature(temperature=celsius)
        aquarium.add_temperature(temperature)
        db.session.commit()
        return temperature, Status.created_201


class TemperatureResource(Resource):
    """
    Gives access to GET, PATCH, DELETE HTTP methods to get, update or delete a single temperature resource.
    """
    @marshal_with(Fields.temperature_field)
    def get(self, temperature_id):
        temperature = temperature_controller.get_by_id(temperature_id)
        abort_if_resource_not_found(temperature)
        return temperature, Status.ok_200

    @marshal_with(Fields.temperature_field)
    def patch(self, temperature_id):
        temperature = temperature_controller.get_by_id(temperature_id)
        abort_if_resource_not_found(temperature)

        parser = parser_factory.temperature_parser('patch')
        args = parser.parse_args()
        celsius = args['celsius']
        aquarium_id = args['aquarium_id']
        temperature.update_attributes(celsius=celsius, aquarium_id=aquarium_id)
        db.session.commit()
        return temperature, Status.ok_200

    def delete(self, temperature_id):
        temperature = temperature_controller.get_by_id(temperature_id)
        abort_if_resource_not_found(temperature)
        db.session.delete(temperature)
        db.session.commit()
        return '', Status.no_content_204


class ChemicalListResource(Resource):
    """
    Gives access to GET and POST HTTP methods to get multiple chemical resources or create a new chemical resource.
    """
    @marshal_with(Fields.chemical_list_field)
    def get(self):
        parser = parser_factory.chemical_parser('get')
        args = parser.parse_args()
        order_by = make_order_by(args['order-by'])
        page = args['page']
        fertilizer_id = args['fertilizer-id']

        items_per_page = current_app.config['ITEMS_PER_PAGE']
        # set pagination attributes for decorator
        chemical_controller.get_multiple.set_page(page)
        chemical_controller.get_multiple.set_items_per_page(items_per_page)

        chemicals = chemical_controller.get_multiple(order_by=order_by, fertilizer_id=fertilizer_id)
        chemical_count = chemical_controller.count_all()
        response = ResponseContent(chemicals, page, items_per_page, chemical_count)
        return response, Status.ok_200

    @marshal_with(Fields.chemical_field)
    def post(self):
        parser = parser_factory.chemical_parser('post')
        args = parser.parse_args()
        name = args['name']

        if not Chemical.is_name_available(name):
            abort(Status.conflict_409, message='Name not available')

        chemical = Chemical(name=name)
        db.session.add(chemical)
        db.session.commit()
        return chemical, Status.created_201


class ChemicalResource(Resource):
    """
    Gives access to GET, PATCH, DELETE HTTP methods to get, update or delete a single chemical resource.
    """
    @marshal_with(Fields.chemical_field)
    def get(self, chemical_id):
        chemical = chemical_controller.get_by_id(chemical_id)
        abort_if_resource_not_found(chemical)
        return chemical, Status.ok_200

    @marshal_with(Fields.chemical_field)
    def patch(self, chemical_id):
        chemical = chemical_controller.get_by_id(chemical_id)
        abort_if_resource_not_found(chemical)

        parser = parser_factory.chemical_parser('patch')
        args = parser.parse_args()

        name = args['name']
        if not Chemical.is_name_available(name):
            abort(Status.conflict_409, message='Name not available')

        chemical.update_attributes(name=name)
        db.session.commit()
        return chemical, Status.ok_200

    def delete(self, chemical_id):
        chemical = chemical_controller.get_by_id(chemical_id)
        abort_if_resource_not_found(chemical)
        db.session.delete(chemical)
        db.session.commit()
        return '', Status.no_content_204


class FertilizerListResource(Resource):
    """
    Gives access to GET and POST HTTP methods to get multiple fertilizer resources or create a new fertilizer resource.
    """
    @marshal_with(Fields.fertilizer_list_field)
    def get(self):
        parser = parser_factory.fertilizer_parser('get')
        args = parser.parse_args()
        order_by = make_order_by(args['order-by'])
        page = args['page']
        chemical_id = args['chemical-id']

        items_per_page = current_app.config['ITEMS_PER_PAGE']
        # set pagination attributes for decorator
        fertilizer_controller.get_multiple.set_page(page)
        fertilizer_controller.get_multiple.set_items_per_page(items_per_page)

        fertilizers = fertilizer_controller.get_multiple(order_by=order_by, chemical_id=chemical_id)
        fertilizer_count = fertilizer_controller.count_all(chemical_id)
        response = ResponseContent(fertilizers, page, items_per_page, fertilizer_count)
        return response, Status.ok_200

    @marshal_with(Fields.fertilizer_field)
    def post(self):
        parser = parser_factory.fertilizer_parser('post')
        args = parser.parse_args()

        name = args['name']
        if not Fertilizer.is_name_available(name):
            abort(Status.conflict_409, message='Name not available')

        fertilizer = Fertilizer(name=name)
        db.session.add(fertilizer)
        db.session.commit()
        return fertilizer, Status.created_201


class FertilizerResource(Resource):
    """
    Gives access to GET, PATCH, DELETE HTTP methods to get, update or delete a single fertilizer resource.
    """
    @marshal_with(Fields.fertilizer_field)
    def get(self, fertilizer_id):
        fertilizer = fertilizer_controller.get_by_id(fertilizer_id)
        abort_if_resource_not_found(fertilizer)
        return fertilizer, Status.ok_200

    @marshal_with(Fields.fertilizer_field)
    def patch(self, fertilizer_id):
        fertilizer = fertilizer_controller.get_by_id(fertilizer_id)
        abort_if_resource_not_found(fertilizer)

        parser = parser_factory.fertilizer_parser('patch')
        args = parser.parse_args()
        chemical_ids = args['chemicals']
        name = args['name']
        fertilizer.update_attributes(name=name, chemical_ids=chemical_ids)

        db.session.commit()
        return fertilizer, Status.ok_200

    def delete(self, fertilizer_id):
        fertilizer = fertilizer_controller.get_by_id(fertilizer_id)
        abort_if_resource_not_found(fertilizer)
        db.session.delete(fertilizer)
        db.session.commit()
        return '', Status.no_content_204


class FertilizationListResource(Resource):
    """
    Gives access to GET and POST HTTP methods to get multiple fertilization resources or
    create a new fertilization resource.
    """
    @marshal_with(Fields.fertilization_list_field)
    def get(self):
        parser = parser_factory.fertilization_parser('get')
        args = parser.parse_args()
        order_by = make_order_by(args['order-by'])
        page = args['page']
        aquarium_id = args['aquarium-id']

        items_per_page = current_app.config['ITEMS_PER_PAGE']
        # set pagination attributes for decorator
        fertilization_controller.get_multiple.set_page(page)
        fertilization_controller.get_multiple.set_items_per_page(items_per_page)

        fertilization = fertilization_controller.get_multiple(order_by=order_by, aquarium_id=aquarium_id)
        fertilization_count = fertilization_controller.count_all(aquarium_id)
        response = ResponseContent(fertilization, page, items_per_page, fertilization_count)
        return response, Status.ok_200

    @marshal_with(Fields.fertilization_field)
    def post(self):
        parser = parser_factory.fertilization_parser('post')
        args = parser.parse_args()
        amount = args['amount_in_milliliter']
        aquarium_id = args['aquarium_id']
        fertilizer_id = args['fertilizer_id']

        aquarium = aquarium_controller.get_by_id(aquarium_id)
        abort_if_resource_not_found(aquarium)
        fertilizer = fertilizer_controller.get_by_id(fertilizer_id)
        abort_if_resource_not_found(fertilizer)

        fertilization = Fertilization(amount_in_milliliter=amount, fertilizer_id=fertilizer_id)
        aquarium.add_fertilization(fertilization)
        db.session.commit()
        return fertilization, Status.created_201


class FertilizationResource(Resource):
    """
    Gives access to GET, PATCH, DELETE HTTP methods to get, update or delete a single fertilization resource.
    """
    @marshal_with(Fields.fertilization_field)
    def get(self, fertilization_id):
        fertilization = fertilization_controller.get_by_id(fertilization_id)
        abort_if_resource_not_found(fertilization)
        return fertilization, Status.ok_200

    @marshal_with(Fields.fertilization_field)
    def patch(self, fertilization_id):
        fertilization = fertilization_controller.get_by_id(fertilization_id)
        abort_if_resource_not_found(fertilization)

        parser = parser_factory.fertilization_parser('patch')
        args = parser.parse_args()
        amount = args['amount_in_milliliter']
        fertilization.update_attributes(amount)
        db.session.commit()
        return fertilization, Status.ok_200

    def delete(self, fertilization_id):
        fertilization = fertilization_controller.get_by_id(fertilization_id)
        abort_if_resource_not_found(fertilization)
        db.session.delete(fertilization)
        db.session.commit()
        return '', Status.no_content_204
