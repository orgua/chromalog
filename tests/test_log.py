"""
Test colorized logging structures.
"""

import logging
import sys
from io import StringIO
from logging import DEBUG
from logging import LogRecord
from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import patch

from chromalog import basicConfig
from chromalog.colorizer import GenericColorizer
from chromalog.log import ColorizingFormatter
from chromalog.log import ColorizingStreamHandler
from chromalog.mark import Mark



def create_colorizer(format):
    # TODO: replace, transform
    def colorize(obj, context_color_tag=None):
        return format % obj

    result = MagicMock(spec=GenericColorizer)
    result.colorize = MagicMock(side_effect=colorize)

    return result

def test_colorizing_formatter_without_a_colorizer():
    formatter = ColorizingFormatter(fmt="%(message)s")
    record = LogRecord(
        name="my_record",
        level=DEBUG,
        pathname="my_path",
        lineno=42,
        msg="%d + %d gives %d",
        args=(
            4,
            5,
            4 + 5,
        ),
        exc_info=None,
    )
    assert "4 + 5 gives 9"== formatter.format(record)

def test_colorizing_formatter_without_a_colorizer_mapping():
    formatter = ColorizingFormatter(fmt="%(message)s")
    record = LogRecord(
        name="my_record",
        level=DEBUG,
        pathname="my_path",
        lineno=42,
        msg="%(summand1)d + %(summand2)d gives %(sum)d",
        args=({"summand1": 4, "summand2": 5, "sum": 4 + 5},),
        exc_info=None,
    )
    assert "4 + 5 gives 9"== formatter.format(record)

def test_colorizing_formatter_with_a_colorizer():
    formatter = ColorizingFormatter(fmt="%(message)s")
    record = LogRecord(
        name="my_record",
        level=DEBUG,
        pathname="my_path",
        lineno=42,
        msg="%s + %s gives %s",
        args=(
            4,
            5,
            4 + 5,
        ),
        exc_info=None,
    )
    setattr(
        record,
        ColorizingStreamHandler._RECORD_ATTRIBUTE_NAME,
        create_colorizer(format="[%s]"),
    )

    assert "[4] + [5] gives [9]"== formatter.format(record)

    colorizer = getattr(
        record,
        ColorizingStreamHandler._RECORD_ATTRIBUTE_NAME,
    )
    colorizer.colorize.assert_any_call(4, context_color_tag=None)
    colorizer.colorize.assert_any_call(5, context_color_tag=None)
    colorizer.colorize.assert_any_call(9, context_color_tag=None)

def test_colorizing_formatter_with_a_colorizer_mapping():
    formatter = ColorizingFormatter(fmt="%(message)s")
    record = LogRecord(
        name="my_record",
        level=DEBUG,
        pathname="my_path",
        lineno=42,
        msg="%(summand1)s + %(summand2)s gives %(sum)s",
        args=({"summand1": 4, "summand2": 5, "sum": 4 + 5},),
        exc_info=None,
    )
    setattr(
        record,
        ColorizingStreamHandler._RECORD_ATTRIBUTE_NAME,
        create_colorizer(format="[%s]"),
    )

    assert "[4] + [5] gives [9]"== formatter.format(record)

    colorizer = getattr(
        record,
        ColorizingStreamHandler._RECORD_ATTRIBUTE_NAME,
    )
    colorizer.colorize.assert_any_call(4, context_color_tag=None)
    colorizer.colorize.assert_any_call(5, context_color_tag=None)
    colorizer.colorize.assert_any_call(9, context_color_tag=None)

@patch("sys.stderr", spec=sys.stderr)
def test_csh_uses_stderr_as_default(stream):
    stream.isatty = lambda: False
    handler = ColorizingStreamHandler()
    assert stream== handler.stream

def test_csh_uses_streamwrapper():
    stream = StringIO()

    with patch(
        "chromalog.log.stream_has_color_support",
        return_value=True,
    ):
        handler = ColorizingStreamHandler(stream=stream)

    assert not(handler.stream is stream)

def test_csh_dont_uses_streamwrapper_if_no_color():
    stream = StringIO()
    handler = ColorizingStreamHandler(stream=stream)
    assert (handler.stream is stream)

def test_csh_format():
    colorizer = GenericColorizer(
        color_map={
            "bracket": ("[", "]"),
        }
    )
    highlighter = GenericColorizer(
        color_map={
            "bracket": ("<", ">"),
        }
    )
    formatter = ColorizingFormatter(fmt="%(message)s")
    color_stream = MagicMock()
    color_stream.isatty = lambda: True
    handler = ColorizingStreamHandler(
        stream=color_stream,
        colorizer=colorizer,
        highlighter=highlighter,
    )
    handler.setFormatter(formatter)

    record = LogRecord(
        name="my_record",
        level=DEBUG,
        pathname="my_path",
        lineno=42,
        msg="%s + %s gives %s",
        args=(
            4,
            5,
            Mark(4 + 5, color_tag="bracket"),
        ),
        exc_info=None,
    )

    assert "4 + 5 gives [9]"== handler.format(record)

    # Make sure that the colorizer attribute was removed after processing.
    assert not(hasattr(record, "colorizer"))

def test_csh_format_with_context():
    colorizer = GenericColorizer(
        color_map={
            "bracket": ("[", "]"),
            "context": ("{", "}"),
        }
    )
    highlighter = GenericColorizer(
        color_map={
            "bracket": ("<", ">"),
            "context": ("(", ")"),
        }
    )
    formatter = ColorizingFormatter(fmt="%(levelname)s %(message)s")
    color_stream = MagicMock()
    color_stream.isatty = lambda: True
    handler = ColorizingStreamHandler(
        stream=color_stream,
        colorizer=colorizer,
        highlighter=highlighter,
        attributes_map={
            "message": "context",
            "levelname": "bracket",
        },
    )
    handler.setFormatter(formatter)

    record = LogRecord(
        name="my_record",
        level=DEBUG,
        pathname="my_path",
        lineno=42,
        msg="%s + %s gives %s",
        args=(
            4,
            5,
            Mark(4 + 5, color_tag="bracket"),
        ),
        exc_info=None,
    )

    assert "[DEBUG] {4 + 5 gives }{[9]}{}"==handler.format(record)

    # Make sure that the colorizer attribute was removed after processing.
    assert not(hasattr(record, "colorizer"))

def test_csh_format_no_color_support():
    colorizer = GenericColorizer(
        color_map={
            "bracket": ("[", "]"),
        }
    )
    highlighter = GenericColorizer(
        color_map={
            "bracket": ("<", ">"),
        }
    )
    formatter = ColorizingFormatter(fmt="%(message)s")
    no_color_stream = MagicMock()
    no_color_stream.isatty = lambda: False
    handler = ColorizingStreamHandler(
        stream=no_color_stream,
        colorizer=colorizer,
        highlighter=highlighter,
    )
    handler.setFormatter(formatter)

    record = LogRecord(
        name="my_record",
        level=DEBUG,
        pathname="my_path",
        lineno=42,
        msg="%s + %s gives %s",
        args=(
            4,
            5,
            Mark(4 + 5, color_tag="bracket"),
        ),
        exc_info=None,
    )

    assert "4 + 5 gives <9>"== handler.format(record)

    # Make sure that the colorizer attribute was removed after processing.
    assert not(hasattr(record, "colorizer"))

def test_csh_format_no_highlighter():
    colorizer = GenericColorizer(
        color_map={
            "bracket": ("[", "]"),
        }
    )
    formatter = ColorizingFormatter(fmt="%(message)s")
    color_stream = MagicMock()
    color_stream.isatty = lambda: True
    handler = ColorizingStreamHandler(
        stream=color_stream,
        colorizer=colorizer,
    )
    handler.setFormatter(formatter)

    record = LogRecord(
        name="my_record",
        level=DEBUG,
        pathname="my_path",
        lineno=42,
        msg="%s + %s gives %s",
        args=(
            4,
            5,
            Mark(4 + 5, color_tag="bracket"),
        ),
        exc_info=None,
    )

    assert "4 + 5 gives [9]"== handler.format(record)

    # Make sure that the colorizer attribute was removed after processing.
    assert not(hasattr(record, "colorizer"))

def test_csh_format_no_highlighter_no_color_support():
    colorizer = GenericColorizer(
        color_map={
            "bracket": ("[", "]"),
        }
    )
    formatter = ColorizingFormatter(fmt="%(message)s")
    color_stream = MagicMock()
    color_stream.isatty = lambda: False
    handler = ColorizingStreamHandler(
        stream=color_stream,
        colorizer=colorizer,
    )
    handler.setFormatter(formatter)

    record = LogRecord(
        name="my_record",
        level=DEBUG,
        pathname="my_path",
        lineno=42,
        msg="%s + %s gives %s",
        args=(
            4,
            5,
            Mark(4 + 5, color_tag="bracket"),
        ),
        exc_info=None,
    )

    assert "4 + 5 gives 9"== handler.format(record)

    # Make sure that the colorizer attribute was removed after processing.
    assert not(hasattr(record, "colorizer"))

def test_csh_format_disabled_color_support():
    colorizer = GenericColorizer(
        color_map={
            "bracket": ("[", "]"),
        }
    )
    highlighter = GenericColorizer(
        color_map={
            "bracket": ("<", ">"),
        }
    )
    formatter = ColorizingFormatter(fmt="%(message)s")
    color_stream = MagicMock()
    color_stream.isatty = lambda: True
    handler = ColorizingStreamHandler(
        stream=color_stream,
        colorizer=colorizer,
        highlighter=highlighter,
    )
    handler.color_disabled = True
    handler.setFormatter(formatter)

    record = LogRecord(
        name="my_record",
        level=DEBUG,
        pathname="my_path",
        lineno=42,
        msg="%s + %s gives %s",
        args=(
            4,
            5,
            Mark(4 + 5, color_tag="bracket"),
        ),
        exc_info=None,
    )

    assert "4 + 5 gives <9>"== handler.format(record)

    # Make sure that the colorizer attribute was removed after processing.
    assert not(
        hasattr(
            record,
            ColorizingStreamHandler._RECORD_ATTRIBUTE_NAME,
        )
    )

def test_basic_config_add_a_stream_handler():
    logger = logging.Logger("test")

    assert []== logger.handlers

    with patch("logging.getLogger", new=lambda: logger):
        basicConfig()
        assert 1== len(logger.handlers)

def test_basic_config_sets_level():
    logger = logging.Logger("test")

    with patch("logging.getLogger", new=lambda: logger):
        basicConfig(level=logging.DEBUG)
        assert logging.DEBUG== logger.level

def test_basic_config_sets_format():
    logger = logging.Logger("test")

    with patch("logging.getLogger", new=lambda: logger):
        basicConfig(format="my format")
        assert "my format"== logger.handlers[0].formatter._fmt
