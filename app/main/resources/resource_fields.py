from flask_restful import fields


class NestedResourceLink(fields.Raw):
    def format(self, resource_id):
        link = '{}?aquarium_id={}'.format(fields.Url('temperaturelistapi'), resource_id)
        return link


class Fields:
    """
    Data class used to marshall sqlalchemy data objects for transmission.
    """
    aquarium_field = {
        'id': fields.Integer,
        'name': fields.String,
        'volume_in_liter': fields.Integer,
        'temperatures': fields.Url('temperaturelistresource')
    }

    aquarium_list_field = {
        'content': fields.List(fields.Nested(aquarium_field)),
        'page': fields.Integer,
        'items_per_page': fields.Integer,
        'total_results': fields.Integer,
    }

    temperature_field = {
        'id': fields.Integer,
        'temperature': fields.Float,
        'timestamp': fields.DateTime,
        'aquarium_id': fields.Integer
    }

    temperature_list_field = {
        'content': fields.List(fields.Nested(temperature_field)),
        'page': fields.Integer,
        'items_per_page': fields.Integer,
        'total_results': fields.Integer,
    }

    chemical_field = {
        'id': fields.Integer,
        'name': fields.String
    }

    chemical_list_field = {
        'content': fields.List(fields.Nested(chemical_field)),
        'page': fields.Integer,
        'items_per_page': fields.Integer,
        'total_results': fields.Integer,
    }

    fertilizer_field = {
        'id': fields.Integer,
        'name': fields.String,
        'chemicals': fields.List(fields.Nested(chemical_field))
    }

    fertilizer_list_field = {
        'content': fields.List(fields.Nested(fertilizer_field)),
        'page': fields.Integer,
        'items_per_page': fields.Integer,
        'total_results': fields.Integer,
    }

    fertilization_field = {
        'id': fields.Integer,
        'amount_in_milliliter': fields.Integer,
        'timestamp': fields.DateTime,
        'aquarium_id': fields.Integer,
        'fertilizer_id': fields.Integer,
    }

    fertilization_list_field = {
        'content': fields.List(fields.Nested(fertilization_field)),
        'page': fields.Integer,
        'items_per_page': fields.Integer,
        'total_results': fields.Integer,
    }

    water_change_field = {
        'id': fields.Integer,
        'liter_amount': fields.Integer,
        'timestamp': fields.DateTime,
        'aquarium_id': fields.Integer,
    }

    water_change_list_field = {
        'content': fields.List(fields.Nested(water_change_field)),
        'page': fields.Integer,
        'items_per_page': fields.Integer,
        'total_results': fields.Integer,
    }
