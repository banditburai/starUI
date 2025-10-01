from starhtml import FT, Icon, Style, js
from starhtml import Span as HTMLSpan

from .button import Button


def ThemeToggle(alt_theme="dark", default_theme="light", **kwargs) -> FT:
    """Theme toggle button."""

    return Button(
        Style(f"""
            [data-theme="{default_theme}"] .theme-icon-alt,
            [data-theme="{alt_theme}"] .theme-icon-default {{
                display: none;
            }}
        """),
        HTMLSpan(Icon("ph:moon-bold", width="20", height="20"), cls="theme-icon-default"),
        HTMLSpan(Icon("ph:sun-bold", width="20", height="20"), cls="theme-icon-alt"),
        data_on_click=js(f"""
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === '{alt_theme}' ? '{default_theme}' : '{alt_theme}';
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
        """),
        variant="ghost",
        aria_label="Toggle theme",
        cls="h-9 px-4 py-2 flex-shrink-0",
        **kwargs,
    )
