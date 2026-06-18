"""Small markdown-like parser used for question and answer text."""

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class TextSegment:
    """A run of text with simple inline style flags."""

    text: str
    bold: bool = False
    italic: bool = False
    underline: bool = False


def parse_markdown_lite(text: str) -> List[TextSegment]:
    """Parse a conservative inline formatting subset.

    Supported markers:
        **bold**
        *italic*
        __underline__
        <u>underline</u>

    Unmatched opening markers are treated as literal text so normal asterisks
    and underscores do not disappear from study material.
    """
    segments: List[TextSegment] = []
    buffer: List[str] = []
    bold = False
    italic = False
    underline = False
    i = 0

    def flush() -> None:
        nonlocal buffer
        if not buffer:
            return
        _append_segment(
            segments,
            TextSegment("".join(buffer), bold=bold, italic=italic, underline=underline),
        )
        buffer = []

    while i < len(text):
        if text[i] == "\\" and i + 1 < len(text):
            buffer.append(text[i + 1])
            i += 2
            continue

        if text.startswith("**", i):
            if bold or _has_closing_marker(text, "**", i + 2):
                flush()
                bold = not bold
                i += 2
                continue
            buffer.append("**")
            i += 2
            continue

        if text.startswith("__", i):
            if underline or _has_closing_marker(text, "__", i + 2):
                flush()
                underline = not underline
                i += 2
                continue
            buffer.append("__")
            i += 2
            continue

        if text.startswith("<u>", i):
            if _has_closing_marker(text, "</u>", i + 3):
                flush()
                underline = True
                i += 3
                continue

        if text.startswith("</u>", i):
            if underline:
                flush()
                underline = False
                i += 4
                continue

        if text[i] == "*":
            if italic or _has_closing_marker(text, "*", i + 1):
                flush()
                italic = not italic
                i += 1
                continue

        buffer.append(text[i])
        i += 1

    flush()
    return segments


def strip_markdown_lite(text: str) -> str:
    """Return display text with supported formatting markers removed."""
    return "".join(segment.text for segment in parse_markdown_lite(text))


def _append_segment(segments: List[TextSegment], segment: TextSegment) -> None:
    if not segment.text:
        return
    if segments and _same_style(segments[-1], segment):
        previous = segments[-1]
        segments[-1] = TextSegment(
            previous.text + segment.text,
            bold=previous.bold,
            italic=previous.italic,
            underline=previous.underline,
        )
        return
    segments.append(segment)


def _same_style(left: TextSegment, right: TextSegment) -> bool:
    return (
        left.bold == right.bold
        and left.italic == right.italic
        and left.underline == right.underline
    )


def _has_closing_marker(text: str, marker: str, start: int) -> bool:
    return text.find(marker, start) != -1
