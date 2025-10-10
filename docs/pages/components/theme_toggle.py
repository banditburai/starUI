"""
Theme Toggle component documentation - Light and dark mode switching.
"""

# Component metadata for auto-discovery
TITLE = "Theme Toggle"
DESCRIPTION = "Toggle between light and dark themes with Datastar reactivity."
CATEGORY = "ui"
ORDER = 95
STATUS = "stable"

from starhtml import Div, H3, Icon, P, Span, FT, Signal, js
from starhtml import Span as HTMLSpan
from starui.registry.components.button import Button
from widgets.component_preview import ComponentPreview
from utils import auto_generate_page, with_code, Prop, build_api_reference


def IsolatedThemeToggle(alt_theme="dark", default_theme="light", **kwargs) -> FT:
    """Theme toggle that only affects its iframe container, not the parent document."""
    is_alt = Signal("is_alt", False)

    return Div(
        is_alt,
        Button(
            Span(Icon("ph:moon-bold", width="20", height="20"), data_show=js("!$is_alt")),
            Span(Icon("ph:sun-bold", width="20", height="20"), data_show=js("$is_alt")),
            variant="ghost",
            aria_label="Toggle theme",
            cls="h-9 px-4 py-2 flex-shrink-0",
            data_on_click=js("$is_alt = !$is_alt")
        ),
        data_on_load=js(f"""
            const iframeId = window.location.pathname.split('/').pop();
            const iframeKey = 'iframe-theme-' + iframeId;
            const savedTheme = localStorage.getItem(iframeKey);

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

            const iframeId = window.location.pathname.split('/').pop();
            const iframeKey = 'iframe-theme-' + iframeId;
            localStorage.setItem(iframeKey, theme);
        """),
        **kwargs,
    )


# Alias pattern: examples show ThemeToggle() matching registry, but use isolated version
ThemeToggle = IsolatedThemeToggle


# ============================================================================
# EXAMPLE FUNCTIONS (decorated with @with_code for markdown generation)
# ============================================================================

# Sizes example - showing different button sizes
@with_code
def size_variations_example():
    return Div(
        P("Theme Toggle Sizes", cls="font-medium mb-4 text-center"),
        P("Click any toggle below to change this preview's theme independently",
          cls="text-sm text-muted-foreground mb-6 text-center"),
        Div(
            Div(
                ThemeToggle(cls="scale-75"),
                P("Small", cls="text-xs text-muted-foreground mt-2"),
                cls="flex flex-col items-center"
            ),
            Div(
                ThemeToggle(),
                P("Default", cls="text-xs text-muted-foreground mt-2"),
                cls="flex flex-col items-center"
            ),
            Div(
                ThemeToggle(cls="scale-125"),
                P("Large", cls="text-xs text-muted-foreground mt-2"),
                cls="flex flex-col items-center"
            ),
            cls="flex items-center gap-8 justify-center"
        ),
        cls="space-y-4 py-8"
    )


# Custom icons example - visual demonstration only
@with_code
def custom_icons_labels_example():
    return Div(
        P("Custom Theme Toggle Styles", cls="font-medium mb-4 text-center"),
        P("Different icon sets and label styles for theme switching",
          cls="text-sm text-muted-foreground mb-6 text-center"),
        Div(
            Div(
                ThemeToggle(),
                P("Default (Sun/Moon)", cls="text-xs text-muted-foreground mt-2"),
                cls="flex flex-col items-center"
            ),
            Div(
                Button(
                    Span(
                        Icon("lucide:sun-medium", width="20", height="20"),
                        cls="theme-icon-default"
                    ),
                    Span(
                        Icon("lucide:moon-star", width="20", height="20"),
                        cls="theme-icon-alt"
                    ),
                    variant="ghost",
                    aria_label="Toggle theme",
                    cls="h-9 px-4 py-2",
                    data_on_click=js("""
                        const currentTheme = document.documentElement.getAttribute('data-theme');
                        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
                        document.documentElement.setAttribute('data-theme', newTheme);

                        const iframeId = window.location.pathname.split('/').pop();
                        localStorage.setItem('iframe-theme-' + iframeId, newTheme);
                    """)
                ),
                P("Custom (Day/Night)", cls="text-xs text-muted-foreground mt-2"),
                cls="flex flex-col items-center"
            ),
            Div(
                Button(
                    Span("Light", cls="theme-icon-default text-sm"),
                    Span("Dark", cls="theme-icon-alt text-sm"),
                    variant="outline",
                    size="sm",
                    aria_label="Toggle theme",
                    data_on_click=js("""
                        const currentTheme = document.documentElement.getAttribute('data-theme');
                        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
                        document.documentElement.setAttribute('data-theme', newTheme);

                        const iframeId = window.location.pathname.split('/').pop();
                        localStorage.setItem('iframe-theme-' + iframeId, newTheme);
                    """)
                ),
                P("Text Labels", cls="text-xs text-muted-foreground mt-2"),
                cls="flex flex-col items-center"
            ),
            cls="flex items-center gap-8 justify-center"
        ),
        cls="space-y-4 py-8"
    )


# Integration example - in a settings panel
@with_code
def settings_panel_integration_example():
    return Div(
        Div(
            H3("Appearance Settings", cls="text-lg font-semibold mb-6"),
            Div(
                Div(
                    P("Theme", cls="text-sm font-medium"),
                    P("Choose your preferred color scheme", cls="text-xs text-muted-foreground mt-1"),
                    cls="flex-1"
                ),
                ThemeToggle(),
                cls="flex items-center justify-between pb-4 border-b"
            ),
            Div(
                Div(
                    P("Accent Color", cls="text-sm font-medium"),
                    P("Customize your interface color", cls="text-xs text-muted-foreground mt-1"),
                    cls="flex-1"
                ),
                Div(
                    Div(cls="h-6 w-6 rounded-full bg-blue-500 border-2 border-primary cursor-pointer"),
                    Div(cls="h-6 w-6 rounded-full bg-green-500 border-2 border-transparent cursor-pointer hover:border-border"),
                    Div(cls="h-6 w-6 rounded-full bg-purple-500 border-2 border-transparent cursor-pointer hover:border-border"),
                    cls="flex gap-2"
                ),
                cls="flex items-center justify-between pt-4"
            ),
            cls="bg-muted/30 rounded-lg p-6 w-full max-w-lg space-y-4"
        ),
        cls="flex items-center justify-center min-h-[350px]"
    )


# ============================================================================
# MODULE-LEVEL DATA (for markdown API)
# ============================================================================

EXAMPLES_DATA = [
    {"title": "Size Variations", "description": "Theme toggle in different sizes for various UI contexts", "fn": size_variations_example, "use_iframe": True},
    {"title": "Custom Icons & Labels", "description": "Different icon sets and text labels for theme switching", "fn": custom_icons_labels_example, "use_iframe": True},
    {"title": "Settings Panel Integration", "description": "Theme toggle integrated into a settings interface", "fn": settings_panel_integration_example, "use_iframe": True},
]

API_REFERENCE = build_api_reference(
    main_props=[
        Prop("alt_theme", "str", "Alternative theme name (usually dark)", "dark"),
        Prop("default_theme", "str", "Default theme name (usually light)", "light"),
        Prop("cls", "str", "Additional CSS classes", "''"),
    ]
)


def examples():
    """Generate all theme toggle examples."""
    yield ComponentPreview(
        size_variations_example(),
        size_variations_example.code,
        title="Size Variations",
        description="Theme toggle in different sizes for various UI contexts",
        use_iframe=True  # Isolate to prevent affecting parent page
    )

    yield ComponentPreview(
        custom_icons_labels_example(),
        custom_icons_labels_example.code,
        title="Custom Icons & Labels",
        description="Different icon sets and text labels for theme switching",
        use_iframe=True
    )

    yield ComponentPreview(
        settings_panel_integration_example(),
        settings_panel_integration_example.code,
        title="Settings Panel Integration",
        description="Theme toggle integrated into a settings interface",
        use_iframe=True
    )


def create_theme_toggle_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)