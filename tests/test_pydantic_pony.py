from datetime import datetime
from typing import List

from pony.orm import *
from pydantic_pony import pony_to_pydantic

db = Database()


class Person(db.Entity):
    name = Required(str)
    age = Required(int)
    cars = Set('Car')
    passport = Optional("Passport")
    created = Required(datetime, default=datetime.now)
    updated = Required(datetime, default=datetime.now)


class Car(db.Entity):
    make = Required(str)
    model = Required(str)
    owner = Required(Person)


class Passport(db.Entity):
    person = Required("Person")


db.bind(provider='sqlite', filename=':memory:')
db.generate_mapping(create_tables=True)

with db_session:
    tommy = Person(name='Tommy', age=18)

    car1 = Car(make='AlfaRomeo', model='STELVIO', owner=tommy)
    car2 = Car(make='Mercedes-Benz', model='GLA', owner=tommy)

    passport = Passport(person=tommy)

    commit()


@db_session
def test_defaults() -> None:
    PydanticPerson = pony_to_pydantic(Person)
    PydanticCar = pony_to_pydantic(Car)

    class PydanticPersonWithCars(PydanticPerson):
        cars: List[PydanticCar] = []

    person = select(p for p in Person).first()
    pydantic_person = PydanticPerson.from_orm(person)
    data = pydantic_person.dict()
    assert isinstance(data["created"], datetime)
    assert isinstance(data["updated"], datetime)
    check_data = data.copy()
    del check_data["created"]
    del check_data["updated"]
    assert check_data == {'age': 18, 'id': 1, 'name': 'Tommy', 'passport': 1}
    pydantic_person_with_cars = PydanticPersonWithCars.from_orm(person)
    data = pydantic_person_with_cars.dict()
    assert isinstance(data["updated"], datetime)
    assert isinstance(data["created"], datetime)
    check_data = data.copy()
    del check_data["updated"]
    del check_data["created"]
    assert check_data == {
        'age': 18,
        'cars': [{
            'id': 1,
            'make': 'AlfaRomeo',
            'model': 'STELVIO',
            'owner': 1
        }, {
            'id': 2,
            'make': 'Mercedes-Benz',
            'model': 'GLA',
            'owner': 1
        }],
        'id': 1,
        'name': 'Tommy',
        'passport': 1
    }


@db_session
def test_schema() -> None:
    PydanticPersion = pony_to_pydantic(Person)
    PydanticCar = pony_to_pydantic(Car)
    assert PydanticPersion.schema() == {
        'properties': {
            'age': {
                'title': 'Age',
                'type': 'integer'
            },
            'created': {
                'format': 'date-time',
                'title': 'Created',
                'type': 'string'
            },
            'id': {
                'title': 'Id',
                'type': 'integer'
            },
            'name': {
                'title': 'Name',
                'type': 'string'
            },
            'passport': {
                'title': 'Passport',
                'type': 'integer'
            },
            'updated': {
                'format': 'date-time',
                'title': 'Updated',
                'type': 'string'
            }
        },
        'required': ['id', 'name', 'age'],
        'title': 'Person',
        'type': 'object'
    }
    assert PydanticCar.schema() == {
        'properties': {
            'id': {
                'title': 'Id',
                'type': 'integer'
            },
            'make': {
                'title': 'Make',
                'type': 'string'
            },
            'model': {
                'title': 'Model',
                'type': 'string'
            },
            'owner': {
                'title': 'Owner',
                'type': 'integer'
            }
        },
        'required': ['id', 'make', 'model', 'owner'],
        'title': 'Car',
        'type': 'object'
    }


@db_session
def test_exclude() -> None:
    PydanticPerson = pony_to_pydantic(Person, exclude={"name"})
    PydanticCar = pony_to_pydantic(Car, exclude={"owner"})

    class PydanticPersonWithCares(PydanticPerson):
        cars: List[PydanticCar] = []

    person = select(p for p in Person).first()
    pydantic_person_with_addresses = PydanticPersonWithCares.from_orm(person)
    data = pydantic_person_with_addresses.dict(by_alias=True)
    assert isinstance(data["created"], datetime)
    assert isinstance(data["updated"], datetime)
    check_data = data.copy()
    del check_data["created"]
    del check_data["updated"]
    assert check_data == {
        'age': 18,
        'cars': [{
            'id': 1,
            'make': 'AlfaRomeo',
            'model': 'STELVIO'
        }, {
            'id': 2,
            'make': 'Mercedes-Benz',
            'model': 'GLA'
        }],
        'id': 1,
        'passport': 1
    }
