from functools import wraps, partial

from app.main.models import Aquarium, AquariumTemperature, Fertilizer, Fertilization, Chemical, fertilizer_ingredients


def make_order_by(order_by_string):
    """
    Creates OderBy object out of an order string representation.

    :param order_by_string: Order by query parameter value
    :return: OderBy object
    """
    parts = order_by_string.split(':')
    ascending = True
    if parts[1] == 'desc':
        ascending = False

    name = parts[0]
    order_by = OrderBy(name, ascending)
    return order_by


class OrderBy:
    """
    Data class to represent http query parameter for sorting/ordering.
    """
    def __init__(self, value_name, ascending=True):
        """
        :param value_name: Attribute name to sort/order by.
        :param ascending: True for ascending and false for descending order.
        """
        self.value_name = value_name
        self.ascending = ascending

    def get_choices(self):
        """
        :return: Tuple of strings that represent this object as a string for both ascending and descending order.
        """
        choices = (self.to_asc_string(), self.to_desc_string())
        return choices

    def to_asc_string(self):
        return '{}:asc'.format(self.value_name)

    def to_desc_string(self):
        return '{}:desc'.format(self.value_name)

    def is_ascending(self):
        return self.ascending

    def __repr__(self):
        return '{},{}'.format(self.to_asc_string(), self.to_desc_string())


# utility decorator to attach a function as attribute of obj
def attach_wrapper(obj, func=None):
    if func is None:
        return partial(attach_wrapper, obj)
    setattr(obj, func.__name__, func)
    return func


def paginate(page=1, items_per_page=5):
    """
    Add pagination to a function which returns sql alchemy query objects. And returns database objects.

    :param page: Page number to display.
    :param items_per_page: Item limit per page.
    :return: Paginated database objects.
    """
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs).paginate(page, items_per_page, False).items

        @attach_wrapper(wrapper)
        def set_page(new_page):
            nonlocal page
            page = new_page

        @attach_wrapper(wrapper)
        def set_items_per_page(new_items_per_page):
            nonlocal items_per_page
            items_per_page = new_items_per_page

        return wrapper
    return decorate


class ResponseContent:
    def __init__(self, content, page, items_per_page, total_results):
        self.content = content
        self.page = page
        self.items_per_page = items_per_page
        self.total_results = total_results

    def __repr__(self):
        return '{} {} {} {}'.format(self.content, self.page, self.items_per_page, self.total_results)


class AquariumController:
    """
    Selects aquarium objects from the database.

    Adds functionality to filter, order by and paginate when selecting data from the database.
    Also allows counting of elements(rows) in table.
    """
    def count_all(self):
            return Aquarium.query.count()

    def get_by_id(self, aquarium_id):
        return Aquarium.query.get(aquarium_id)

    @paginate()
    def get_multiple(self, order_by: OrderBy, page=1):
        """
        :param order_by: OrderBy object which sets the sequence.
        :param page: Page number to display.
        :return: Ordered query for aquarium database objects.
        """

        # Apply order by query name/liter ascending descending and return aquarium query.
        if order_by.value_name == 'name':
            if order_by.is_ascending():
                return Aquarium.query.order_by(Aquarium.name.asc())

            return Aquarium.query.order_by(Aquarium.name.desc())

        if order_by.value_name == 'liter':
            if order_by.is_ascending():
                return Aquarium.query.order_by(Aquarium.volume_in_liter.asc())

            return Aquarium.query.order_by(Aquarium.volume_in_liter.desc())

        raise ValueError('Cant apply sorting with {}'.format(order_by))


class TemperatureController:
    """
    Selects temperature objects from the database.

    Adds functionality to filter, order by and paginate when selecting data from the database.
    Also allows counting of elements(rows) in table.
    """
    def count_all(self, aquarium_id=None):
        if aquarium_id:
            return AquariumTemperature.query.filter(AquariumTemperature.aquarium_id == aquarium_id).count()
        return AquariumTemperature.query.count()

    def get_by_id(self, temperature_id):
        return AquariumTemperature.query.get(temperature_id)

    @paginate()
    def get_multiple(self, order_by, aquarium_id=None):
        """
        :param order_by: OrderBy object which sets the sequence.
        :param aquarium_id: filter temperatures by aquarium id.
        :return: Ordered query of temperature database objects.
        """

        if aquarium_id:
            temperatures_query = AquariumTemperature.query.filter(AquariumTemperature.aquarium_id == aquarium_id)
        else:
            temperatures_query = AquariumTemperature.query

        # Apply order by query date/celsius ascending descending and return temperature query.
        if order_by.value_name == 'date':
            if order_by.is_ascending():
                return temperatures_query.order_by(AquariumTemperature.timestamp.asc())

            return temperatures_query.order_by(AquariumTemperature.timestamp.desc())

        if order_by.value_name == 'celsius':
            if order_by.is_ascending():
                return temperatures_query.order_by(AquariumTemperature.temperature.asc())

            return temperatures_query.order_by(AquariumTemperature.temperature.desc())

        raise ValueError('Cant apply sorting with {}'.format(order_by))


class ChemicalController:
    """
    Selects chemical objects from the database.

    Adds functionality to filter, order by and paginate when selecting data from the database.
    Also allows counting of elements(rows) in table.
    """
    def count_all(self):
        return Chemical.query.count()

    def get_by_id(self, chemical_id):
        return Chemical.query.get(chemical_id)

    @paginate()
    def get_multiple(self, order_by, fertilizer_id=None):
        """
        :param order_by: OrderBy object which sets the sequence.
        :param fertilizer_id: filter chemicals by fertilizer id.
        :return: Ordered query of chemical database objects.
        """

        if fertilizer_id:
            chemical_query = Chemical.query.\
                join(fertilizer_ingredients, (fertilizer_ingredients.c.chemical_id == Chemical.id)).\
                filter(fertilizer_ingredients.c.fertilizer_id == fertilizer_id)
        else:
            chemical_query = Chemical.query

        # Apply order by query name ascending descending and return chemical query.
        if order_by.value_name == 'name':
            if order_by.is_ascending():
                return chemical_query.order_by(Chemical.name.asc())

            return chemical_query.order_by(Chemical.name.desc())

        raise ValueError('Cant apply sorting with {}'.format(order_by))


class FertilizerController:
    """
    Selects fertilizer objects from the database.

    Adds functionality to filter, order by and paginate when selecting data from the database.
    Also allows counting of elements(rows) in table.
    """
    def count_all(self, chemical_id=None):
        if chemical_id:
            fertilizers_count = Fertilizer.query.\
                join(fertilizer_ingredients, (fertilizer_ingredients.c.fertilizer_id == Fertilizer.id)).\
                filter(fertilizer_ingredients.c.chemical_id == chemical_id).count()
            return fertilizers_count
        return Fertilizer.query.count()

    def get_by_id(self, fertilizer_id):
        return Fertilizer.query.get(fertilizer_id)

    @paginate()
    def get_multiple(self, order_by, chemical_id=None):
        """
        :param order_by: OrderBy object which sets the sequence.
        :param chemical_id: filter fertilizer by chemical id..
        :return: Ordered query of fertilizer database objects.
        """

        if chemical_id:
            # query for all fertilizers that contain a chemical with chemical_id
            fertilizer_query = Fertilizer.query.\
                join(fertilizer_ingredients, (fertilizer_ingredients.c.fertilizer_id == Fertilizer.id)).\
                filter(fertilizer_ingredients.c.chemical_id == chemical_id)
        else:
            # query for all fertilizers
            fertilizer_query = Fertilizer.query

        # Apply order by query name ascending descending and return fertilizer query.
        if order_by.value_name == 'name':
            if order_by.is_ascending():
                return fertilizer_query.order_by(Fertilizer.name.asc())

            return fertilizer_query.order_by(Fertilizer.name.desc())

        raise ValueError('Cant apply sorting with {}'.format(order_by))


class FertilizationController:
    """
    Selects fertilization objects from the database.

    Adds functionality to filter, order by and paginate when selecting data from the database.
    Also allows counting of elements(rows) in table.
    """
    def count_all(self, aquarium_id=None):
        if aquarium_id:
            aquarium = Aquarium.query.get(aquarium_id)
            return aquarium.fertilization.count()
        return Fertilization.query.count()

    def get_by_id(self, fertilization_id):
        return Fertilization.query.get(fertilization_id)

    @paginate()
    def get_multiple(self, order_by, aquarium_id=None):
        """
        :param order_by: OrderBy object which sets the sequence.
        :param aquarium_id: filter fertilization by aquarium id.
        :return: Ordered query of fertilization database objects.
        """

        if aquarium_id:
            fertilization_query = Fertilization.query.filter(Fertilization.aquarium_id == aquarium_id)
        else:
            fertilization_query = Fertilization.query

        # Apply order by query date/amount ascending descending and return fertilization query.
        if order_by.value_name == 'date':
            if order_by.is_ascending():
                return fertilization_query.order_by(Fertilization.timestamp.asc())

            return fertilization_query.order_by(Fertilization.timestamp.desc())

        if order_by.value_name == 'amount':
            if order_by.is_ascending():
                return fertilization_query.order_by(Fertilization.amount_in_milliliter.asc())

            return fertilization_query.order_by(Fertilization.amount_in_milliliter.desc())
        raise ValueError('Cant apply sorting with {}'.format(order_by))
