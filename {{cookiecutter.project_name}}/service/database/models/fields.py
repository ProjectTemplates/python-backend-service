from typing import Any


class ModelField:
    """
    Field for SQLAlchemy ORM models, that binds to postgres JSON field,
    and can transform it into instance of pydantic model.
    """
    fields = ('__data', '__binding', '__model', '__field')

    def __init__(self, model: type, field: str) -> None:
        """
        model: pydantic model class for json data
        field: name of json field on orm model
        """
        self.__data = None
        self.__binding = None
        self.__model = model
        self.__field = field

    def save(self) -> None:
        if not self.__binding:
            raise RuntimeError('ModelField is not bound to an object!')
        if not self.__data:
            value = None
        else:
            value = self.__data.dict()
        setattr(self.__binding, self.__field, value)

    def populate(self, binding: Any) -> None:
        """
        Add call to this with argument *self*
        to orm class's method marked by *@orm.reconstructor*
        """
        value = getattr(binding, self.__field)
        self.__binding = binding
        if not value:
            self.__data = None
        else:
            self.__data = self.__model(**value)

    def __getattr__(self, item: str) -> Any:
        return getattr(self.__data, item)

    def __setattr__(self, key: str, value: Any) -> None:
        if any(filter(key.endswith, self.fields)):  # type: ignore
            super().__setattr__(key, value)
            return
        setattr(self.__data, key, value)
        self.save()

    def __repr__(self) -> str:
        return f"<ModelField representing: '{self.__data}'>"

    __str__ = __repr__
