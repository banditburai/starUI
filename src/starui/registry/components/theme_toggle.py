from starhtml import FT, Div, Icon
from starhtml import Span as HTMLSpan
from starhtml.datastar import ds_effect, ds_on_click, ds_on_load, ds_show, ds_signals, toggle_signal

from .button import Button


def ThemeToggle(alt_theme="dark", default_theme="light", **kwargs) -> FT:
    """Reactive theme toggle supporting arbitrary theme names."""

    return Div(
        Button(
            HTMLSpan(Icon("ph:moon-bold", width="20", height="20"), ds_show("!$isAlt")),
            HTMLSpan(Icon("ph:sun-bold", width="20", height="20"), ds_show("$isAlt")),
            ds_on_click(toggle_signal("isAlt")),
            variant="ghost",
            aria_label="Toggle theme",
            cls="h-9 px-4 py-2 flex-shrink-0",
        ),
        ds_signals(isAlt=False),
        ds_on_load(
            f"$isAlt = localStorage.getItem('theme') === '{alt_theme}' || "
            f"(!localStorage.getItem('theme') && window.matchMedia('(prefers-color-scheme: dark)').matches)"
        ),
        ds_effect(f"""
            const theme = $isAlt ? '{alt_theme}' : '{default_theme}';
            document.documentElement.classList.toggle('{alt_theme}', $isAlt);
            document.documentElement.setAttribute('data-theme', theme);
            localStorage.setItem('theme', theme);
        """),
        **kwargs,
    )
