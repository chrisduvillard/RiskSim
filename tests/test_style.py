"""Tests for utils.style module."""

from utils.style import metric_box


class TestMetricBox:
    """Tests for the metric_box helper."""

    def test_returns_string(self) -> None:
        result = metric_box("Title", "Value")
        assert isinstance(result, str)

    def test_contains_title(self) -> None:
        result = metric_box("Win Rate", "50%")
        assert "Win Rate" in result

    def test_contains_value(self) -> None:
        result = metric_box("Win Rate", "50%")
        assert "50%" in result

    def test_html_structure(self) -> None:
        result = metric_box("X", "Y")
        assert "<div" in result
        assert "<h4" in result
        assert "<p" in result
