"""Tests for markdown-lite parsing."""

from utils.markdown_lite import parse_markdown_lite, strip_markdown_lite


def test_parse_markdown_lite_styles_supported_markers():
    segments = parse_markdown_lite("plain **bold** *italic* __under__ <u>tag under</u>")

    styled = {(s.text, s.bold, s.italic, s.underline) for s in segments}

    assert ("plain ", False, False, False) in styled
    assert ("bold", True, False, False) in styled
    assert ("italic", False, True, False) in styled
    assert ("under", False, False, True) in styled
    assert ("tag under", False, False, True) in styled


def test_parse_markdown_lite_supports_nested_styles():
    segments = parse_markdown_lite("**bold and *italic too***")

    assert segments[0].text == "bold and "
    assert segments[0].bold is True
    assert segments[0].italic is False
    assert segments[1].text == "italic too"
    assert segments[1].bold is True
    assert segments[1].italic is True


def test_parse_markdown_lite_keeps_unmatched_markers_literal():
    assert strip_markdown_lite("Use * as multiplication") == "Use * as multiplication"
    assert strip_markdown_lite("Need **closing marker") == "Need **closing marker"


def test_strip_markdown_lite_preserves_newlines():
    text = "First paragraph\n\n**Second paragraph**"

    assert strip_markdown_lite(text) == "First paragraph\n\nSecond paragraph"
