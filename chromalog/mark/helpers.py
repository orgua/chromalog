"""Automatically generate marking helpers functions."""

import sys

from .objects import Mark


class SimpleHelpers:
    """
    A class that is designed to act as a module and implement magic helper
    generation.
    """

    def __init__(self) -> None:
        self.__helpers = {}

    def make_helper(self, color_tag):
        """
        Make a simple helper.

        :param color_tag: The color tag to make a helper for.
        :returns: The helper function.
        """
        helper = self.__helpers.get(color_tag)

        if not helper:

            def helper(obj):
                return Mark(obj=obj, color_tag=color_tag)

            helper.__name__ = color_tag
            helper.__doc__ = f"""
            Mark an object for coloration.

            The color tag is set to {color_tag!r}.

            :param obj: The object to mark for coloration.
            :returns: A :class:`Mark<chromalog.mark.objects.Mark>` instance.

            >>> from chromalog.mark.helpers.simple import {color_tag}

            >>> {color_tag}(42).color_tag
            ['{color_tag}']
            """

            self.__helpers[color_tag] = helper

        return helper

    def __getattr__(self, name):
        """
        Get a magic helper.

        :param name: The name of the helper to get.

        >>> SimpleHelpers().alpha(42).color_tag
        ['alpha']

        >>> getattr(SimpleHelpers(), "_incorrect", None)
        """
        if name.startswith("_"):
            raise AttributeError(name)

        return self.make_helper(color_tag=name)


class ConditionalHelpers:
    """
    A class that is designed to act as a module and implement magic helper
    generation.
    """

    def __init__(self) -> None:
        self.__helpers = {}

    def make_helper(self, color_tag_true, color_tag_false):
        """
        Make a conditional helper.

        :param color_tag_true: The color tag if the condition is met.
        :param color_tag_false: The color tag if the condition is not met.
        :returns: The helper function.
        """
        helper = self.__helpers.get(
            (color_tag_true, color_tag_false),
        )

        if not helper:

            def helper(obj, condition=None):
                if condition is None:
                    condition = obj

                return Mark(
                    obj=obj,
                    color_tag=color_tag_true if condition else color_tag_false,
                )

            helper.__name__ = f"{color_tag_true}_or_{color_tag_false}"
            helper.__doc__ = f"""
            Convenience helper method that marks an object with the
            {color_tag_true!r} color tag if `condition` is truthy, and with the
            {color_tag_false!r} color tag otherwise.

            :param obj: The object to mark for coloration.
            :param condition: The condition to verify. If `condition` is
                :const:`None`, the `obj` is evaluated instead.
            :returns: A :class:`Mark<chromalog.mark.objects.Mark>` instance.

            >>> from chromalog.mark.helpers.conditional import {helper.__name__}

            >>> {helper.__name__}(42, True).color_tag
            ['{color_tag_true}']

            >>> {helper.__name__}(42, False).color_tag
            ['{color_tag_false}']

            >>> {helper.__name__}(42).color_tag
            ['{color_tag_true}']

            >>> {helper.__name__}(0).color_tag
            ['{color_tag_false}']
            """

            self.__helpers[(color_tag_true, color_tag_false),] = helper

        return helper

    def __getattr__(self, name):
        """
        Get a magic helper.

        :param name: The name of the helper to get. Must be of the form
        'a_or_b' where `a` and `b` are color tags.

        >>> ConditionalHelpers().alpha_or_beta(42, True).color_tag
        ['alpha']

        >>> ConditionalHelpers().alpha_or_beta(42, False).color_tag
        ['beta']

        >>> ConditionalHelpers().alpha_or_beta(42).color_tag
        ['alpha']

        >>> ConditionalHelpers().alpha_or_beta(0).color_tag
        ['beta']

        >>> getattr(ConditionalHelpers(), "alpha_beta", None)
        >>> getattr(ConditionalHelpers(), "_incorrect", None)
        """
        if name.startswith("_"):
            raise AttributeError(name)

        try:
            color_tag_true, color_tag_false = name.split("_or_")
        except ValueError:
            raise AttributeError(name)

        return self.make_helper(
            color_tag_true=color_tag_true,
            color_tag_false=color_tag_false,
        )


simple = SimpleHelpers()
simple.__doc__ = """
Pseudo-module that generates simple helpers.

See :class:`SimpleHelpers<chromalog.mark.helpers.SimpleHelpers>`.
"""

conditional = ConditionalHelpers()
conditional.__doc__ = """
Pseudo-module that generates conditional helpers.

See :class:`ConditionalHelpers<chromalog.mark.helpers.ConditionalHelpers>`.
"""

sys.modules[f"{__name__}.simple"] = simple
sys.modules[f"{__name__}.conditional"] = conditional
