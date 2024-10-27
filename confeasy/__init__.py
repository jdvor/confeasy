"""Lorem ipsum dolor sit."""

__version__ = "0.0.1"

import re
from typing import Protocol, TypeVar, Any

T = TypeVar("T")
VALID_KEY_PATTERN = re.compile(r"^[a-z]+(\\.[a-z]+)*$")

class Configuration:

    def __init__(self, data: dict[str, str | int | float | bool]):
        self._data = data

    @property
    def data(self) -> dict[str, str | int | float | bool]:
        return self._data

    def get_value(self, key: str) -> str | int | float | bool | None:
        return self._data[key] if key in self._data else None

    def bind(self, instance: T, filter: str | None = None) -> T:
        return instance


T = typing.TypeVar("T")

class Configuration2:

    def __init__(self, data: dict[str, str | int | float | bool]):
        self._data = data

    def bind(self, instance: T, prefix: str | None = None) -> T:
        for key, value in self._data.items():
            if prefix and not key.startswith(prefix):
                continue
            prop_name = key[len(prefix):]
            prop_name = prop_name[1:] if prop_name[0] == '.' else prop_name
            if hasattr(instance, key):
                attr = getattr(type(instance), key, None)
                # Ensure it's either a property with a setter or a regular attribute
                if not isinstance(attr, property) or (isinstance(attr, property) and attr.fset is not None):
                    setattr(instance, key, value)  # Set the attribute/property

        return instance


class Source(Protocol):

    def get_data(self) -> dict[str, str | int | float | bool]:
        pass


class Builder:

    def __init__(self, drop_invalid_keys: bool = True):
        self._sources: list[Source] = []
        self._data: dict[str, str | int | float | bool] = {}
        self._drop_invalid_keys = drop_invalid_keys

    def add_source(self, source: Source) -> 'Builder':
        self._sources.append(source)
        return self

    def add_data(self, data: dict[str, Any]) -> 'Builder':
        sanitized = _sanitize(data, self._drop_invalid_keys)
        self._data.update(sanitized)
        return self

    def build(self) -> Configuration:
        merged = self._data.copy()
        for source in self._sources:
            src = source.get_data()
            sanitized = _sanitize(src, self._drop_invalid_keys)
            merged.update(sanitized)
        return Configuration(merged)


def _sanitize(data: dict[str, Any], drop_invalid_keys: bool = True) -> dict[str, str | int | float | bool]:
    sanitized = {}
    for key, value in data.items():
        key = key.lower()
        if not VALID_KEY_PATTERN.match(key):
            if drop_invalid_keys:
                continue
            else:
                raise ValueError(f"invalid key '{key}'")

        if isinstance(value, (str, int, float, bool)):
            sanitized[key] = value
        else:
            sanitized[key] = str(value)

    return sanitized