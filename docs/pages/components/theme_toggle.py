"""
Theme Toggle component documentation - Light and dark mode switching.
"""

# Component metadata for auto-discovery
TITLE = "Theme Toggle"
DESCRIPTION = "Toggle between light and dark themes with Datastar reactivity."
CATEGORY = "ui"
ORDER = 95
STATUS = "stable"

from starhtml import Div, Icon, P, Span, Style, FT, js
from starui.registry.components.button import Button
from starui.registry.components.dropdown_menu import DropdownMenu, DropdownMenuTrigger, DropdownMenuContent, DropdownMenuItem
from utils import auto_generate_page, with_code, Prop, build_api_reference

ALT_THEME = "dark"
DEFAULT_THEME = "light"


def IsolatedThemeToggle(alt_theme=ALT_THEME, default_theme=DEFAULT_THEME, **kwargs) -> FT:
    """Theme toggle for iframe previews — CSS approach with isolated localStorage key.

    Derives the storage key from the iframe URL path, matching the iframe_app
    init script so theme persists across reloads.
    """

    return Div(
        Style(f"""
            [data-theme="{default_theme}"] .theme-icon-alt,
            [data-theme="{alt_theme}"] .theme-icon-default {{
                display: none;
            }}
        """),
        Button(
            Icon("ph:moon-bold", width="20", height="20", cls="theme-icon-default"),
            Icon("ph:sun-bold", width="20", height="20", cls="theme-icon-alt"),
            data_on_click=js(f"""
                const currentTheme = document.documentElement.getAttribute('data-theme');
                const newTheme = currentTheme === '{alt_theme}' ? '{default_theme}' : '{alt_theme}';
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
def size_variations_example():
    sizes = [
        {"scale": "scale-75", "label": "Small"},
        {"scale": "", "label": "Default"},
        {"scale": "scale-125", "label": "Large"},
    ]

    return Div(
        P("Theme Toggle Sizes", cls="font-medium mb-4 text-center"),
        P("Click any toggle below to change this preview's theme independently",
          cls="text-sm text-muted-foreground mb-6 text-center"),
        Div(
            *[
                Div(
                    ThemeToggle(cls=size["scale"]),
                    P(size["label"], cls="text-xs text-muted-foreground mt-2"),
                    cls="flex flex-col items-center"
                )
                for size in sizes
            ],
            cls="flex items-center gap-8 justify-center"
        ),
        cls="space-y-4 py-8"
    )


@with_code
def dropdown_theme_selector_example():
    theme_options = [
        {"value": "light", "label": "Light", "icon": "lucide:sun"},
        {"value": "dark", "label": "Dark", "icon": "lucide:moon"},
        {"value": "system", "label": "System", "icon": "lucide:laptop"},
    ]

    def set_theme_js(theme_value):
        return js(f"""
            const newTheme = '{theme_value}';
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
        P("Dropdown Theme Selector", cls="font-medium mb-4 text-center"),
        P("Common pattern with Light, Dark, and System options",
          cls="text-sm text-muted-foreground mb-6 text-center"),
        Div(
            DropdownMenu(
                DropdownMenuTrigger(
                    Icon("lucide:sun", cls="h-[1.2rem] w-[1.2rem] dropdown-icon-default"),
                    Icon("lucide:moon", cls="h-[1.2rem] w-[1.2rem] dropdown-icon-alt"),
                    Span("Theme", cls="sr-only"),
                    variant="outline",
                    size="icon"
                ),
                DropdownMenuContent(
                    *[
                        DropdownMenuItem(
                            Icon(opt["icon"], cls="mr-2 h-4 w-4"),
                            Span(opt["label"]),
                            data_on_click=set_theme_js(opt["value"])
                        )
                        for opt in theme_options
                    ],
                    align="end"
                )
            ),
            cls="flex justify-center"
        ),
        cls="space-y-4 py-8"
    )



EXAMPLES_DATA = [
    {"title": "Size Variations", "description": "Theme toggle in different sizes for various UI contexts", "fn": size_variations_example, "use_iframe": True},
    {"title": "Dropdown Theme Selector", "description": "Common shadcn-style dropdown with Light, Dark, and System options", "fn": dropdown_theme_selector_example, "use_iframe": True},
]

API_REFERENCE = build_api_reference(
    main_props=[
        Prop("alt_theme", "str", "Alternative theme name (usually dark)", "dark"),
        Prop("default_theme", "str", "Default theme name (usually light)", "light"),
        Prop("cls", "str", "Additional CSS classes", "''"),
    ]
)




def create_theme_toggle_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)