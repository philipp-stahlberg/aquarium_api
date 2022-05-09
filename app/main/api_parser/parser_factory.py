from flask_restful.reqparse import RequestParser
from flask_restful import inputs

from .request_validator import Validator as Val
from app.main.resources.controller import OrderBy

#  allowed request types for parsing
_request_types = {
    'get': 'http get request',
    'post': 'http post request',
    'patch': 'http patch request'
}


def verify_request_type(request_type):
    if request_type not in _request_types:
        raise ValueError('Unknown request type {}. Available types {}'.format(request_type, _request_types))


_order_by_name = OrderBy('name')
_order_by_liter = OrderBy('liter')
_order_by_date = OrderBy('date')
_order_by_celsius = OrderBy('celsius')
_order_by_amount = OrderBy('amount')


class ParserFactory:
    """
    Factory to create different RequestParser from flask_restful for different resource endpoints.
    Also adds different arguments to the parser depending on resource endpoint and request type.
    """
    def __init__(self, bundle_errors=True):
        self.parser = RequestParser(bundle_errors=bundle_errors)

    def aquarium_parser(self, request_type):
        parser = self.parser.copy()
        verify_request_type(request_type)
        if request_type == 'get':
            choices = _order_by_name.get_choices() + _order_by_liter.get_choices()
            parser.add_argument(name='order-by', choices=choices, required=False, location='args',
                                help='Unknown order-by parameter. Valid choices are {}'.format(choices),
                                default=choices[0])
            parser.add_argument(name='page', type=inputs.positive, required=False, location='args', default=1)
        else:
            # add arguments for patch/post requests
            parser.add_argument(name='id', type=inputs.positive, required=True, location='json')
            parser.add_argument(name='name', type=str, required=True, location='json')
            parser.add_argument(name='volume_in_liter', type=Val.volume, required=True, location='json')

        if request_type == 'post':
            parser.remove_argument('id')

        return parser

    def temperature_parser(self, request_type):
        parser = self.parser.copy()
        verify_request_type(request_type)
        if request_type == 'get':
            choices = _order_by_celsius.get_choices() + _order_by_date.get_choices()
            parser.add_argument(name='order-by', choices=choices, required=False, location='args', default=choices[0])
            parser.add_argument(name='page', type=inputs.positive, required=False, location='args', default=1)
            parser.add_argument(name='aquarium-id', type=inputs.positive, required=False, location='args')
        else:
            # add arguments for patch/post requests
            parser.add_argument(name='id', type=inputs.positive, required=True, location='json')
            parser.add_argument(name='celsius', type=Val.temperature, required=True, location='json')
            parser.add_argument(name='aquarium_id', type=Val.aquarium_id, required=True, location='json')

        if request_type == 'post':
            parser.remove_argument('id')

        return parser

    def chemical_parser(self, request_type):
        parser = self.parser.copy()
        verify_request_type(request_type)
        if request_type == 'get':
            choices = _order_by_name.get_choices()
            parser.add_argument(name='order-by', choices=choices, required=False, location='args', default=choices[0])
            parser.add_argument(name='page', type=inputs.positive, required=False, location='args', default=1)
            parser.add_argument(name='fertilizer-id', type=inputs.positive, required=False, location='args')
        else:
            # add arguments for patch/post requests
            parser.add_argument(name='id', type=inputs.positive, required=True, location='json')
            parser.add_argument(name='name', type=str, required=True, location='json')

        if request_type == 'post':
            parser.remove_argument('id')

        return parser

    def fertilizer_parser(self, request_type):
        parser = self.parser.copy()
        verify_request_type(request_type)
        if request_type == 'get':
            choices = _order_by_name.get_choices()
            parser.add_argument(name='order-by', choices=choices, required=False, location='args', default=choices[0])
            parser.add_argument(name='page', type=inputs.positive, required=False, location='args', default=1)
            parser.add_argument(name='chemical-id', type=inputs.positive, required=False, location='args')
        else:
            # add arguments for patch/post requests
            parser.add_argument(name='id', type=inputs.positive, required=True, location='json')
            parser.add_argument(name='name', type=str, required=True, location='json')
            parser.add_argument(name='chemicals', type=inputs.positive, required=True, location='json', action='append')

        if request_type == 'post':
            parser.remove_argument('id')

        return parser

    def fertilization_parser(self, request_type):
        parser = self.parser.copy()
        verify_request_type(request_type)
        if request_type == 'get':
            choices = _order_by_amount.get_choices() + _order_by_date.get_choices()
            parser.add_argument(name='order-by', choices=choices, required=False, location='args', default=choices[0])
            parser.add_argument(name='page', type=inputs.positive, required=False, location='args', default=1)
            parser.add_argument(name='aquarium-id', type=inputs.positive, required=False, location='args')
        else:
            # add arguments for patch/post requests
            parser.add_argument(name='id', type=inputs.positive, required=True, location='json')
            parser.add_argument(name='amount_in_milliliter', type=inputs.positive, required=True, location='json')
            parser.add_argument(name='aquarium_id', type=Val.aquarium_id, required=True, location='json')
            parser.add_argument(name='fertilizer_id', type=Val.fertilizer_id, required=True, location='json')

        if request_type == 'post':
            parser.remove_argument('id')

        return parser
