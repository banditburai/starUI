from starhtml import FT, Div, Icon, Span, Style, js

from .button import Button
from .utils import DEFAULT_THEME, ALT_THEME


def ThemeToggle(**kwargs) -> FT:
    """Theme toggle button with CSS-only icon switching."""

    return Div(
        Style(f"""
            [data-theme="{DEFAULT_THEME}"] .theme-icon-alt,
            [data-theme="{ALT_THEME}"] .theme-icon-default {{
                display: none;
            }}
        """),
        Button(
            Span(Icon("ph:moon-bold", width="20", height="20"), cls="theme-icon-default"),
            Span(Icon("ph:sun-bold", width="20", height="20"), cls="theme-icon-alt"),
            data_on_click=js(f"""
                const currentTheme = document.documentElement.getAttribute('data-theme');
                const newTheme = currentTheme === '{ALT_THEME}' ? '{DEFAULT_THEME}' : '{ALT_THEME}';
                document.documentElement.setAttribute('data-theme', newTheme);
                localStorage.setItem('theme', newTheme);
            """),
            variant="ghost",
            size="icon",
            aria_label="Toggle theme",
        ),
        **kwargs,
    )
