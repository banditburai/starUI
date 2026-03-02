"""Test package initialization and basic functionality."""


def test_package_importable():
    """Test that starui package can be imported."""
    import starui

    assert starui.__version__ is not None


def test_package_version_is_string():
    """Test that package version is a valid semver-like string."""
    import starui

    parts = starui.__version__.split(".")
    assert len(parts) >= 2, "Version should have at least major.minor"
    assert all(p.isdigit() for p in parts), "Version parts should be numeric"


def test_cli_entry_point_importable():
    """Test that the CLI entry point module and app object exist."""
    from starui.cli.main import app

    assert app is not None
    assert hasattr(app, "command")


def test_utilities_work():
    """Test that utility functions are importable and produce expected output."""
    from starui import cn, cva, gen_id

    assert cn("foo", "bar") == "foo bar"
    assert cn("foo", None, "bar") == "foo bar"

    id1 = gen_id("test")
    id2 = gen_id("test")
    assert id1.startswith("test_")
    assert id1 != id2

    assert callable(cva)


def test_themes_importable():
    """Test that theme constants are importable from starui."""
    from starui import ALT_THEME, DEFAULT_THEME

    assert DEFAULT_THEME == "light"
    assert ALT_THEME == "dark"


def test_all_exports_in_dunder_all():
    """__all__ includes utility functions."""
    import starui

    assert "cn" in starui.__all__
    assert "cva" in starui.__all__
    assert "gen_id" in starui.__all__
    assert "DEFAULT_THEME" in starui.__all__
    assert "ALT_THEME" in starui.__all__
