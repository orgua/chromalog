"""
Stream tests.
"""

from unittest.mock import MagicMock

from chromalog.stream import stream_has_color_support


def test_csh_color_support_with_color_stream():
    color_stream = MagicMock(spec=object)
    color_stream.isatty = lambda: True
    assert stream_has_color_support(color_stream)


def test_csh_color_support_with_no_color_stream():
    no_color_stream = MagicMock(spec=object)
    no_color_stream.isatty = lambda: False
    assert not (stream_has_color_support(no_color_stream))


def test_csh_color_support_with_simple_stream():
    simple_stream = MagicMock(spec=object)
    assert not (stream_has_color_support(simple_stream))
