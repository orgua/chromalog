"""Mark log entries."""

from typing import Generic
from typing import Self
from typing import TypeVar

from chromalog.colorizer import ColorizableMixin

T = TypeVar("T", default=str)


class Mark(ColorizableMixin, Generic[T]):
    """Wraps any object and mark it for colored output."""

    def __init__(self, obj: Self | T, color_tag: str | list[str]) -> None:
        """
        Mark ``obj`` for coloration.

        :param obj: The object to mark for colored output.
        :param color_tag: The color tag to use for coloring. Can be either a
            list of a string. If ``color_tag`` is a string it will be converted
            into a single-element list automatically.

        .. note:: Nested :class:`chromalog.mark.Mark` objects are flattened
            automatically and their ``color_tag`` are appended.

        >>> from chromalog.mark.objects import Mark

        >>> Mark(42, "a").color_tag
        ['a']

        >>> Mark(42, ["a"]).color_tag
        ['a']

        >>> Mark(42, ["a", "b"]).color_tag
        ['a', 'b']

        >>> Mark(Mark(42, "c"), ["a", "b"]) == Mark(42, ["a", "b", "c"])
        True
        """
        if isinstance(color_tag, str):
            color_tag = [color_tag]

        if isinstance(obj, Mark):
            color_tag.extend(obj.color_tag)
            obj = obj.obj

        super().__init__(color_tag=color_tag)
        self.obj = obj

    def __repr__(self) -> str:
        """
        Gives a representation of the marked object.

        >>> repr(Mark("a", "b"))
        "Mark('a', ['b'])"
        """
        return f"{self.__class__.__name__}({self.obj!r}, {self.color_tag!r})"

    def __str__(self) -> str:
        """
        Gives a string representation of the marked object.

        >>> str(Mark("hello", []))
        'hello'
        """
        return str(self.obj)

    def __unicode__(self) -> str:
        """Gives a string representation of the marked object."""
        return str(self.obj)

    def __int__(self) -> int:
        """
        Gives an integer representation of the marked object.

        >>> int(Mark(42, []))
        42
        """
        return int(self.obj)

    def __float__(self) -> float:
        """
        Gives a float representation of the marked object.

        >>> float(Mark(3.14, []))
        %f
        """
        return float(self.obj)

    def __bool__(self) -> bool:
        """
        Gives a boolean representation of the marked object.

        >>> bool(Mark(True, []))
        True
        """
        return bool(self.obj)

    def __eq__(self, other: object) -> bool:
        """
        Compares this marked object with another.

        :param other: The other instance to compare with.
        :returns: True if `other` is a :class:`chromalog.mark.Mark` instance
            with equal `obj` and `color_tag` members.

        >>> Mark(42, color_tag=[]) == Mark(42, color_tag=[])
        True

        >>> Mark(42, color_tag=["a"]) == Mark(42, color_tag=["b"])
        False
        """
        if isinstance(other, self.__class__):
            return other.obj == self.obj and other.color_tag == self.color_tag
        return other == self.obj


# offer default specialized types
fMark = Mark[float]
iMark = Mark[int]
