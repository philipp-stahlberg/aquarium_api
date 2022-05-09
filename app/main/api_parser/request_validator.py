from app.main.models import Aquarium, Fertilizer, Chemical


MAX_TEMPERATURE = 40
MIN_TEMPERATURE = 0


class Validator:
    """
    Custom validator for flask_restful reqparse.Argument parameter type
    Returns input value when valid, otherwise raises ValueError.
    """
    @staticmethod
    def temperature(value):
        if not Validator._is_valid_temperature(value):
            raise ValueError('Aquarium temperatures must be greater than {} and smaller than {} !'.
                             format(MIN_TEMPERATURE, MAX_TEMPERATURE))
        return value

    @staticmethod
    def _is_valid_temperature(value):
        if MIN_TEMPERATURE < value < MAX_TEMPERATURE:
            return True
        return False

    @staticmethod
    def volume(value):
        if not Validator._is_valid_volume(value):
            raise ValueError('Volume must be greater than 0.')
        return value

    @staticmethod
    def _is_valid_volume(value):
        if value > 0:
            return True
        return False

    @staticmethod
    def aquarium_id(value):
        if not Validator._is_valid_aquarium_id(value):
            raise ValueError('Invalid aquarium id')
        return value

    @staticmethod
    def _is_valid_aquarium_id(value):
        if isinstance(value, int):
            if value > 0:
                aquarium = Aquarium.query.get(value)
                if aquarium:
                    return True
        return False

    @staticmethod
    def fertilizer_id(value):
        if not Validator._is_valid_fertilizer_id(value):
            raise ValueError('Invalid fertilizer id')
        return value

    @staticmethod
    def _is_valid_fertilizer_id(value):
        if isinstance(value, int):
            if value > 0:
                fertilizer = Fertilizer.query.get(value)
                if fertilizer:
                    return True
        return False

    @staticmethod
    def chemical_id(value):
        if not Validator._is_valid_chemical_id(value):
            raise ValueError('Invalid chemical id')
        return value

    @staticmethod
    def _is_valid_chemical_id(value):
        if isinstance(value, int):
            if value > 0:
                chemical = Chemical.query.get(value)
                if chemical:
                    return True
        return False

    @staticmethod
    def chemicals(value):
        for c_id in value:
            if not Validator._is_valid_chemical_id(c_id):
                raise ValueError('At least one invalid chemical id.')
        return value



