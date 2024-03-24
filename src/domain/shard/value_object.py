from dataclasses import dataclass


@dataclass(frozen=True)
class ValueObject:

    def __eq__(self, other):
        if isinstance(other, ValueObject):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))
