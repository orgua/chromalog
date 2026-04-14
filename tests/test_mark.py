"""
Test object marking.
"""

import pytest

from chromalog.mark import Mark
from chromalog.mark import fMark
from chromalog.mark import iMark

from .conftest import values_integral
from .conftest import values_various


@pytest.mark.parametrize("value", values_various.values())
def test_string_rendering_of_marked(value) -> None:
    assert f"{value}" == "{}".format(Mark(value, "a"))


@pytest.mark.parametrize("value", values_integral.values())
def test_int_rendering_of_marked(value) -> None:
    assert "%d" % value == "%d" % iMark(value, "a")
    assert f"{value}" == f"{iMark(value, 'a')}"

@pytest.mark.xfail
@pytest.mark.parametrize("value", values_integral.values())
def test_hexadecimal_int_rendering_of_marked(value) -> None:
    # Apparently in Python 3, %x expects a real integer. If you know how to
    # make it work with a Marked integer, please let me know !
    assert "%x" % value == "%x" % iMark(value, "a")
    assert f"{value:x}" == f"{iMark(value, 'a'):x}"
    # TODO: repair, mark does not behave like int


@pytest.mark.parametrize("value", values_integral.values())
def test_float_rendering_of_marked(value) -> None:
    assert "%f" % value == "%f" % fMark(value, "a")
    assert f"{value}" == f"{fMark(value, 'a')}"


@pytest.mark.parametrize("value", values_various.values())
def test_marked_objects_dont_compare_to_their_value_as(value) -> None:
    assert value == Mark(value, "a")


@pytest.mark.parametrize("value", values_various.values())
def test_marked_objects_have_a_color_tag_attribute_for(value) -> None:
    assert hasattr(Mark(value, "a"), "color_tag")
    assert hasattr(Mark(value, color_tag="info"), "color_tag")


@pytest.mark.parametrize("value", values_various.values())
def test_marked_objects_can_be_nested_for(value) -> None:
    obj = Mark(Mark(value, "b"), "a")
    assert obj.color_tag == ["a", "b"]
    assert value == obj.obj

    obj = Mark(Mark(value, ["b", "c"]), "a")
    assert obj.color_tag == ["a", "b", "c"]
    assert value == obj.obj

    obj = Mark(Mark(value, "c"), ["a", "b"])
    assert obj.color_tag == ["a", "b", "c"]
    assert value == obj.obj

    obj = Mark(Mark(value, ["c", "d"]), ["a", "b"])
    assert obj.color_tag == ["a", "b", "c", "d"]
    assert value == obj.obj


@pytest.mark.parametrize(
    "name",
    {
        "simple_name": "alpha",
        "underscore_name": "alpha_beta",
    }.values(),
)
def test_simple_helpers_with(name) -> None:
    import chromalog.mark.helpers.simple as helpers

    helper = getattr(helpers, name)
    assert [name] == helper(42).color_tag


@pytest.mark.parametrize(
    "name",
    {
        "simple_name": "alpha_or_beta",
        "underscore_name": "alpha_beta_or_gamma_delta",
    }.values(),
)
def test_conditional_helpers_with(name) -> None:
    import chromalog.mark.helpers.conditional as helpers

    helper = getattr(helpers, name)
    true_color_tag, false_color_tag = name.split("_or_")
    assert [true_color_tag] == helper(42, True).color_tag
    assert [false_color_tag] == helper(42, False).color_tag
    assert [true_color_tag] == helper(True).color_tag
    assert [false_color_tag] == helper(False).color_tag


def test_explicit_unicode() -> None:
    assert Mark("test", "foo").__unicode__() == "test"
