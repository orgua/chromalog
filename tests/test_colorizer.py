"""
Test colorizers.
"""

import pytest

from chromalog.colorizer import ColorizableMixin
from chromalog.colorizer import ColorizedObject
from chromalog.colorizer import Colorizer
from chromalog.mark import Mark
from tests.conftest import values_various


def test_colorizer_get_color_pair_not_found() -> None:
    colorizer = Colorizer({})
    assert colorizer.get_color_pair(color_tag=["a"]) == ("", "")


def test_colorizer_get_color_pair_found() -> None:
    colorizer = Colorizer({"a": ("[", "]")})
    assert colorizer.get_color_pair(color_tag=["a"]) == ("[", "]")


def test_colorizer_get_color_pair_found_double() -> None:
    colorizer = Colorizer(
        {
            "a": ("[", "]"),
            "b": ("<", ">"),
        }
    )
    assert colorizer.get_color_pair(color_tag=["a", "b"]) == ("[<", ">]")


def test_colorizer_get_color_pair_not_found_with_default() -> None:
    colorizer = Colorizer(
        {
            "a": ("[", "]"),
            "b": ("<", ">"),
        },
        default_color_tag="b",
    )
    assert colorizer.get_color_pair(color_tag=["c"]) == ("<", ">")


def test_colorizer_get_color_pair_not_found_with_disabled_default() -> None:
    colorizer = Colorizer(
        {
            "a": ("[", "]"),
            "b": ("<", ">"),
        },
        default_color_tag="b",
    )
    assert colorizer.get_color_pair(color_tag=["c"], use_default=False) == ("", "")


def test_colorizer_get_color_pair_found_with_context() -> None:
    colorizer = Colorizer(
        {
            "a": ("[", "]"),
            "b": ("<", ">"),
        },
    )
    assert colorizer.get_color_pair(color_tag=["a"], context_color_tag="b") == ("><[", "]><")


def test_colorizer_get_color_pair_found_with_list_context() -> None:
    colorizer = Colorizer(
        {
            "a": ("[", "]"),
            "b": ("<", ">"),
            "c": ("(", ")"),
        },
    )
    assert colorizer.get_color_pair(
        color_tag=["a"],
        context_color_tag=["b", "c"],
    ) == (")><([", "])><(")


@pytest.mark.parametrize("value", values_various.values())
def test_colorizer_converts_unknown_types(value) -> None:
    colorizer = Colorizer(
        color_map={
            "a": ("[", "]"),
            "b": ("<", ">"),
        }
    )
    assert ColorizedObject(value) == colorizer.colorize(value)


@pytest.mark.parametrize("value", values_various.values())
def test_colorizer_changes_colorizable_types(value) -> None:
    colorizer = Colorizer(
        color_map={
            "a": ("[", "]"),
        }
    )
    assert ColorizedObject(Mark(value, "a"), ("[", "]")) == colorizer.colorize(Mark(value, "a"))


@pytest.mark.parametrize("value", values_various.values())
def test_colorizer_changes_colorizable_types_with_tags(value) -> None:
    colorizer = Colorizer(
        color_map={
            "a": ("[", "]"),
            "b": ("<", ">"),
        }
    )
    assert ColorizedObject(Mark(value, ["a", "b"]), ("[<", ">]")) == colorizer.colorize(
        Mark(value, ["a", "b"])
    )


@pytest.mark.parametrize("value", values_various.values())
def test_colorizer_changes_colorizable_types_with_context(value) -> None:
    colorizer = Colorizer(
        color_map={
            "a": ("[", "]"),
            "b": ("<", ">"),
        }
    )
    assert ColorizedObject(Mark(value, "a"), ("><[", "]><")) == colorizer.colorize(
        Mark(value, "a"), context_color_tag="b"
    )


@pytest.mark.parametrize("value", values_various.values())
def test_colorizer_changes_colorizable_types_with_tags_and_context(value) -> None:
    colorizer = Colorizer(
        color_map={
            "a": ("[", "]"),
            "b": ("(", ")"),
            "c": ("<", ">"),
        }
    )
    assert ColorizedObject(Mark(value, ["a", "b"]), ("><[(", ")]><")) == colorizer.colorize(
        Mark(value, ["a", "b"]), context_color_tag="c"
    )


@pytest.mark.parametrize(
    "value",
    {
        "default_colorizable": ColorizableMixin(),
        "specific_colorizable": ColorizableMixin(color_tag="info"),
    }.values(),
)
def test_colorizable_mixin_has_a_color_tag_attribute_for(value) -> None:
    assert hasattr(value, "color_tag")


def test_colorizer_colorizes_with_known_color_tag() -> None:
    colorizer = Colorizer(
        color_map={
            "my_tag": ("START_MARK", "STOP_MARK"),
        },
    )
    result = colorizer.colorize(Mark("hello", color_tag="my_tag"))
    assert (
        ColorizedObject(
            Mark(
                "hello",
                "my_tag",
            ),
            (
                "START_MARK",
                "STOP_MARK",
            ),
        )
        == result
    )


def test_colorizer_colorizes_with_known_color_tag_and_default() -> None:
    colorizer = Colorizer(
        color_map={
            "my_tag": ("START_MARK", "STOP_MARK"),
            "default": ("START_DEFAULT_MARK", "STOP_DEFAULT_MARK"),
        },
        default_color_tag="default",
    )
    result = colorizer.colorize(Mark("hello", color_tag="my_tag"))
    assert (
        ColorizedObject(
            Mark(
                "hello",
                "my_tag",
            ),
            (
                "START_MARK",
                "STOP_MARK",
            ),
        )
        == result
    )


def test_colorizer_doesnt_colorize_with_unknown_color_tag() -> None:
    colorizer = Colorizer(
        color_map={
            "my_tag": ("START_MARK", "STOP_MARK"),
        },
    )
    result = colorizer.colorize(Mark("hello", color_tag="my_unknown_tag"))
    assert ColorizedObject(Mark("hello", "my_unknown_tag"), ("", "")) == result


def test_colorizer_colorizes_with_unknown_color_tag_and_default() -> None:
    colorizer = Colorizer(
        color_map={
            "my_tag": ("START_MARK", "STOP_MARK"),
            "default": ("START_DEFAULT_MARK", "STOP_DEFAULT_MARK"),
        },
        default_color_tag="default",
    )
    result = colorizer.colorize(Mark("hello", color_tag="my_unknown_tag"))
    assert (
        ColorizedObject(
            Mark(
                "hello",
                "my_unknown_tag",
            ),
            (
                "START_DEFAULT_MARK",
                "STOP_DEFAULT_MARK",
            ),
        )
        == result
    )


def test_colorize_message() -> None:
    colorizer = Colorizer(
        color_map={
            "a": ("[", "]"),
            "b": ("(", ")"),
        }
    )
    message = "{0}-{1}_{a}~{b}"
    args = [42, Mark(42, ["a", "b"])]
    kwargs = {
        "a": 0,
        "b": Mark(0, ["b", "a"]),
    }
    assert colorizer.colorize_message(message, *args, **kwargs) == "42-[(42)]_0~([0])"


def test_colorize_message_with_context() -> None:
    colorizer = Colorizer(
        color_map={
            "a": ("[", "]"),
            "b": ("(", ")"),
            "c": ("<", ">"),
        }
    )
    message = Mark("{0}-{1}_{a}~{b}", "c")
    args = [42, Mark(42, ["a", "b"])]
    kwargs = {
        "a": 0,
        "b": Mark(0, ["b", "a"]),
    }
    assert colorizer.colorize_message(message, *args, **kwargs) == "<42-><[(42)]><_0~><([0])><>"


@pytest.mark.parametrize("value", values_various.values())
def test_colorized_object_conversion(value) -> None:
    assert f"{value}" == f"{ColorizedObject(value)}"


@pytest.mark.parametrize("value", values_various.values())
def test_colorized_object_conversion_with_color_pair(value) -> None:
    assert f"<{value}>" == "{}".format(ColorizedObject(value, color_pair=("<", ">")))


@pytest.mark.parametrize("value", values_various.values())
def test_colorized_object_representation(value) -> None:
    assert repr(value) == repr(ColorizedObject(value))


@pytest.mark.parametrize("value", values_various.values())
def test_colorized_object_representation_with_color_pair(value) -> None:
    assert f"<{value!r}>" == repr(ColorizedObject(value, color_pair=("<", ">")))


@pytest.mark.parametrize("type_", {int, float, bool})
def test_colorized_object_cast(type_) -> None:
    assert type_() == type_(ColorizedObject(type_()))


@pytest.mark.parametrize("type_", {int, float, bool})
def test_colorized_object_cast_with_color_pair(type_) -> None:
    assert type_() == type_(ColorizedObject(type_(), color_pair=("<", ">")))


def test_explicit_unicode_in_python3() -> None:
    assert ColorizedObject("test").__unicode__() == "test"
    assert ColorizedObject("test", color_pair=("<", ">")).__unicode__() == "<test>"
