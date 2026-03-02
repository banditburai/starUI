"""Tests for optimized CSS input template generation."""

from pathlib import Path

from starui.config import ProjectConfig
from starui.templates import generate_css_input


class TestCSSInput:
    """Test the optimized CSS input generation."""

    def test_generate_optimized_css_input(self):
        """Test optimized CSS generation with hybrid theming."""
        css = generate_css_input()

        assert '@import "tailwindcss";' in css
        assert "@custom-variant dark" in css
        assert "@theme {" in css
        assert ":root {" in css
        assert "--background:" in css
        assert "--foreground:" in css
        assert "oklch(" in css

    def test_css_reset_not_included_by_default(self):
        """Test CSS reset is not included since Tailwind v4 handles it."""
        css = generate_css_input()

        assert "box-sizing: border-box" not in css
        assert ":root {" in css  # Theme variables should still be there

    def test_generate_css_input_with_config(self):
        """Test CSS generation with a config (though it's unused)."""
        config = ProjectConfig(
            project_root=Path("/tmp/test"),
            css_output=Path("dist/styles.css"),
            component_dir=Path("components/ui"),
        )
        css = generate_css_input(config)

        assert ":root {" in css
        assert "--background:" in css

    def test_hybrid_theming_support(self):
        """Test that both .dark class and data-theme attributes are supported."""
        css = generate_css_input()

        assert '.dark, [data-theme="dark"]' in css
        assert "@custom-variant dark" in css
        assert '[data-theme="blue"]' in css  # Custom theme example
        assert '[data-theme="green"]' in css  # Custom theme example

    def test_wcag_compliant_colors(self):
        """Test that colors use WCAG AA compliant oklch values."""
        css = generate_css_input()

        # Check for WCAG AA compliant color values
        assert "oklch(1 0 0)" in css  # Light background
        assert "oklch(0.145 0 0)" in css  # Dark foreground for contrast
        assert "oklch(0.985 0 0)" in css  # Light foreground for dark mode
        assert "oklch(0.205 0 0)" in css  # Dark mode card background

    def test_font_system_tokens(self):
        """Test that font system tokens are included."""
        css = generate_css_input()

        assert "--font-sans:" in css
        assert "--font-mono:" in css
        assert "SF Mono" in css
        assert "Roboto" in css
