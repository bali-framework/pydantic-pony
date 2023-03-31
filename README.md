# pydantic-pony

<a href="https://pypi.org/project/pydantic-pony" target="_blank">
    <img src="https://img.shields.io/pypi/v/pydantic-pony?color=%2334D058&label=pypi%20package" alt="Package version">
</a>

Tools to generate Pydantic models from Pony ORM models.

## How to use

Quick example:

```python
# ... other imports 

from pydantic_pony import pony_to_pydantic


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


# Transform Pony Model to Pydantic
PydanticPerson = pony_to_pydantic(Person)
PydanticCar = pony_to_pydantic(Car)

person = select(p for p in Person).first()
pydantic_person = PydanticPerson.from_orm(person)


# Inherit
class PydanticPersonWithCars(PydanticPerson):
    cars: List[PydanticCar] = []

    
pydantic_person_with_cars = PydanticPersonWithCars.from_orm(person)
```

## Release Notes

### Latest Changes

### 0.0.1

* Added main function `pony_to_pydantic`.

## License

This project is licensed under the terms of the MIT license.
