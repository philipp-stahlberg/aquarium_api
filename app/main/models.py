from datetime import datetime

from app import db

"""
This module contains all sqlalchemy models and contains all data altering methods within these models.
"""


class Aquarium(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True, nullable=False)
    volume_in_liter = db.Column(db.Integer, nullable=False)
    temperature_measurements = db.relationship('AquariumTemperature',
                                               backref='aquarium',
                                               cascade='all, delete',
                                               lazy='dynamic')
    fertilization = db.relationship('Fertilization',
                                    backref='aquarium',
                                    cascade='all, delete',
                                    lazy='dynamic')

    def update_attributes(self, name=None, volume_in_liter=None):
        if name and self.is_name_available(name):
            self.name = name
        if volume_in_liter:
            self.volume_in_liter = volume_in_liter

    @staticmethod
    def is_name_available(name):
        aquarium = Aquarium.query.filter(Aquarium.name == name).first()
        if aquarium:
            return False
        return True

    def add_temperature(self, temperature):
        self.temperature_measurements.append(temperature)

    def add_fertilization(self, fertilization):
        self.fertilization.append(fertilization)

    def add_water_change(self, water_change):
        self.water_changes.append(water_change)

    def __repr__(self):
        return '<Aquarium {}:{}, {} liter>'.format(self.id, self.name, self.volume_in_liter)


class AquariumTemperature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    aquarium_id = db.Column(db.Integer, db.ForeignKey('aquarium.id'), nullable=False)

    def update_attributes(self, celsius=None, aquarium_id=None):
        if celsius:
            self.temperature = celsius
        if aquarium_id:
            self.aquarium_id = aquarium_id

    def __repr__(self):
        return '<Aquarium_temp {} in AID {}:{}:{}>'.format(self.id, self.aquarium_id, self.celsius, self.timestamp)


class Fertilization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount_in_milliliter = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    aquarium_id = db.Column(db.Integer, db.ForeignKey('aquarium.id'), nullable=False)
    fertilizer_id = db.Column(db.Integer, db.ForeignKey('fertilizer.id'), nullable=False)

    def update_attributes(self, amount):
        if amount:
            self.amount_in_milliliter = amount

    def __repr__(self):
        return '<Fertilization {}: amount={}, aquarium_id={}, fertilizer_id={}>' \
               ''.format(self.id, self.amount_in_milliliter, self.aquarium_id, self.fertilizer_id)


fertilizer_ingredients = db.Table('fertilizer_ingredients',
                                  db.Column('fertilizer_id', db.Integer, db.ForeignKey('fertilizer.id'),
                                            primary_key=True),
                                  db.Column('chemical_id', db.Integer, db.ForeignKey('chemical.id'),
                                            primary_key=True)
                                  )


class Fertilizer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    chemicals = db.relationship('Chemical',
                                secondary=fertilizer_ingredients,
                                lazy='subquery',
                                backref=db.backref('fertilizer', lazy=True)
                                )
    fertilization = db.relationship('Fertilization',
                                    cascade='all, delete',
                                    lazy='dynamic',
                                    backref=db.backref('fertilizer', lazy=True)
                                    )

    @staticmethod
    def is_name_available(name):
        fertilizer = Fertilizer.query.filter(Fertilizer.name == name).first()
        if fertilizer:
            return False
        return True

    def update_attributes(self, name, chemical_ids):
        if name and self.is_name_available(name):
            self.name = name

        chemicals = []
        for i in chemical_ids:
            chemical = Chemical.query.get(i)
            if chemical:
                chemicals.append(chemical)

        # remove chemicals when not in chemical list
        for c in self.chemicals:
            if c not in chemicals:
                self.remove_chemicals(c)

        # add new chemicals
        for c in chemicals:
            if not self.contains(c):
                self.chemicals.append(c)

    def contains(self, *chemicals):
        for c in chemicals:
            if c not in self.chemicals:
                return False
        return True

    def add_chemicals(self, *chemicals):
        for c in chemicals:
            self.chemicals.append(c)

    def remove_chemicals(self, *chemicals):
        for c in chemicals:
            self.chemicals.remove(c)

    def __repr__(self):
        return '<Fertilizer {}: {}>'.format(self.id, self.name)


class Chemical(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)

    def update_attributes(self, name):
        if name and self.is_name_available(name):
            self.name = name

    @staticmethod
    def is_name_available(name):
        chemical = Chemical.query.filter(Chemical.name == name).first()
        if chemical:
            return False
        return True

    def get_associated_fertilizers(self):
        fertilizers = db.session.query(Fertilizer).\
            join(fertilizer_ingredients, (fertilizer_ingredients.c.fertilizer_id == Fertilizer.id)).\
            filter(fertilizer_ingredients.c.chemical_id == self.id).all()
        return fertilizers

    def __repr__(self):
        return '<Chemical {}: {}>'.format(self.id, self.name)