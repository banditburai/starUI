"""
Theme Toggle component documentation - Light and dark mode switching.
"""

# Component metadata for auto-discovery
TITLE = "Theme Toggle"
DESCRIPTION = "Toggle between light and dark themes with Datastar reactivity."
CATEGORY = "ui"
ORDER = 95
STATUS = "stable"

from starhtml import Div, Icon, P, Span, FT, Signal, js
from starui.registry.components.button import Button
from starui.registry.components.dropdown_menu import DropdownMenu, DropdownMenuTrigger, DropdownMenuContent, DropdownMenuItem
from utils import auto_generate_page, with_code, Prop, build_api_reference

THEME_STORAGE_KEY = "iframe-theme-theme_toggle"


def IsolatedThemeToggle(alt_theme="dark", default_theme="light", **kwargs) -> FT:
    """Theme toggle that only affects its iframe container, not the parent document."""
    is_alt = Signal("is_alt", False)

    return Div(
        is_alt,
        Button(
            Span(Icon("ph:moon-bold", width="20", height="20"), data_show=~is_alt),
            Span(Icon("ph:sun-bold", width="20", height="20"), data_show=is_alt),
            variant="ghost",
            aria_label="Toggle theme",
            cls="h-9 px-4 py-2 flex-shrink-0",
            data_on_click=is_alt.toggle()
        ),
        data_on_load=js(f"""
            const savedTheme = localStorage.getItem('{THEME_STORAGE_KEY}');

            if (savedTheme) {{
                $is_alt = savedTheme === '{alt_theme}';
            }} else {{
                const parentTheme = localStorage.getItem('theme') ||
                    document.documentElement.getAttribute('data-theme');
                $is_alt = parentTheme === '{alt_theme}';
            }}
        """),
        data_effect=js(f"""
            const theme = $is_alt ? '{alt_theme}' : '{default_theme}';
            document.documentElement.setAttribute('data-theme', theme);
            localStorage.setItem('{THEME_STORAGE_KEY}', theme);
        """),
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
    is_dark = Signal("is_dark", _ref_only=True)

    theme_options = [
        {"value": "light", "label": "Light", "icon": "lucide:sun"},
        {"value": "dark", "label": "Dark", "icon": "lucide:moon"},
        {"value": "system", "label": "System", "icon": "lucide:laptop"},
    ]

    def set_theme_js(theme_value):
        return js(f"""
            const newTheme = '{theme_value}';
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('{THEME_STORAGE_KEY}', newTheme);
            $is_dark = newTheme === 'dark';
        """)

    return Div(
        is_dark,
        P("Dropdown Theme Selector", cls="font-medium mb-4 text-center"),
        P("Common pattern with Light, Dark, and System options",
          cls="text-sm text-muted-foreground mb-6 text-center"),
        Div(
            DropdownMenu(
                DropdownMenuTrigger(
                    Span(
                        Icon("lucide:sun", cls="h-[1.2rem] w-[1.2rem]"),
                        style="display: none",
                        data_show=is_dark
                    ),
                    Span(
                        Icon("lucide:moon", cls="h-[1.2rem] w-[1.2rem]"),
                        style="display: none",
                        data_show=~is_dark
                    ),
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
        data_on_load=js(f"""
            const savedTheme = localStorage.getItem('{THEME_STORAGE_KEY}');

            let theme;
            if (savedTheme) {{
                theme = savedTheme;
            }} else {{
                theme = localStorage.getItem('theme') ||
                    document.documentElement.getAttribute('data-theme') ||
                    'light';
            }}

            document.documentElement.setAttribute('data-theme', theme);
            $is_dark = theme === 'dark';
        """),
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