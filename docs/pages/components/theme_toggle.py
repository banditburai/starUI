"""
Theme Toggle component documentation — light/dark mode switching.
"""

# Component metadata for auto-discovery
TITLE = "Theme Toggle"
DESCRIPTION = "A button that switches between light and dark mode."
CATEGORY = "ui"
ORDER = 95
STATUS = "stable"

from starhtml import A, Div, Icon, Span, Style, FT, js
from starui.registry.components.button import Button
from starui.registry.components.dropdown_menu import (
    DropdownMenu, DropdownMenuTrigger, DropdownMenuContent, DropdownMenuItem,
)
from utils import auto_generate_page, with_code, Prop, build_api_reference

ALT_THEME = "dark"
DEFAULT_THEME = "light"


def IsolatedThemeToggle(**kwargs) -> FT:
    """Theme toggle for iframe previews — CSS approach with isolated localStorage key.

    Derives the storage key from the iframe URL path, matching the iframe_app
    init script so theme persists across reloads.
    """

    return Div(
        Style(f"""
            [data-theme="{DEFAULT_THEME}"] .theme-icon-alt,
            [data-theme="{ALT_THEME}"] .theme-icon-default {{
                display: none;
            }}
        """),
        Button(
            Icon("ph:moon-bold", width="20", height="20", cls="theme-icon-default"),
            Icon("ph:sun-bold", width="20", height="20", cls="theme-icon-alt"),
            data_on_click=js(f"""
                const currentTheme = document.documentElement.getAttribute('data-theme');
                const newTheme = currentTheme === '{ALT_THEME}' ? '{DEFAULT_THEME}' : '{ALT_THEME}';
                document.documentElement.setAttribute('data-theme', newTheme);
                const iframeKey = 'iframe-theme-' + window.location.pathname.split('/').pop();
                localStorage.setItem(iframeKey, newTheme);
            """),
            variant="ghost",
            size="icon",
            aria_label="Toggle theme",
        ),
        **kwargs,
    )


# Alias pattern: examples show ThemeToggle() matching registry, but use isolated version
ThemeToggle = IsolatedThemeToggle


@with_code
def default_example():
    return Div(
        ThemeToggle(),
        cls="flex items-center justify-center py-6",
    )


@with_code
def header_example():
    return Div(
        Span("acme", cls="font-semibold tracking-tight"),
        Div(
            A("Docs", href="#", cls="text-sm text-muted-foreground hover:text-foreground transition-colors"),
            A("Blog", href="#", cls="text-sm text-muted-foreground hover:text-foreground transition-colors"),
            ThemeToggle(),
            cls="flex items-center gap-4",
        ),
        cls="flex items-center justify-between w-full px-4 py-3 border-b",
    )


@with_code
def dropdown_example():
    theme_options = [
        {"value": "light", "label": "Light", "icon": "lucide:sun"},
        {"value": "dark", "label": "Dark", "icon": "lucide:moon"},
        {"value": "system", "label": "System", "icon": "lucide:laptop"},
    ]

    def set_theme_js(theme_value):
        return js(f"""
            let newTheme = '{theme_value}';
            if (newTheme === 'system') {{
                newTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
            }}
            document.documentElement.setAttribute('data-theme', newTheme);
            const iframeKey = 'iframe-theme-' + window.location.pathname.split('/').pop();
            localStorage.setItem(iframeKey, newTheme);
        """)

    return Div(
        Style(f"""
            [data-theme="{DEFAULT_THEME}"] .dropdown-icon-alt,
            [data-theme="{ALT_THEME}"] .dropdown-icon-default {{
                display: none;
            }}
        """),
        DropdownMenu(
            DropdownMenuTrigger(
                Icon("lucide:sun", cls="h-[1.2rem] w-[1.2rem] dropdown-icon-default"),
                Icon("lucide:moon", cls="h-[1.2rem] w-[1.2rem] dropdown-icon-alt"),
                Span("Theme", cls="sr-only"),
                variant="outline",
                size="icon",
            ),
            DropdownMenuContent(
                *[
                    DropdownMenuItem(
                        Icon(opt["icon"], cls="mr-2 h-4 w-4"),
                        Span(opt["label"]),
                        data_on_click=set_theme_js(opt["value"]),
                    )
                    for opt in theme_options
                ],
                align="end",
            ),
        ),
        cls="flex items-center justify-center py-6",
    )


EXAMPLES_DATA = [
    {"title": "Default", "description": "Zero-config toggle — click to switch between light and dark mode", "fn": default_example, "use_iframe": True, "iframe_height": "130px", "preview_class": "!min-h-0 !p-4"},
    {"title": "In a Header", "description": "Positioned in a navbar alongside navigation links", "fn": header_example, "use_iframe": True, "iframe_height": "105px", "preview_class": "!min-h-0 !p-4"},
    {"title": "Dropdown Selector", "description": "Light, Dark, and System selector built from DropdownMenu", "fn": dropdown_example, "use_iframe": True, "iframe_height": "200px", "preview_class": "!min-h-0 !p-4"},
]

API_REFERENCE = build_api_reference(
    main_props=[
        Prop("cls", "str", "Additional CSS classes forwarded to the wrapper Div", "''"),
        Prop("**kwargs", "", "Any HTML attribute — forwarded to the wrapper Div", ""),
    ]
)


def create_theme_toggle_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)
