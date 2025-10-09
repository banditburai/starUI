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
            HTMLSpan(Icon("ph:moon-bold", width="20", height="20"), data_show=js("!$is_alt")),
            HTMLSpan(Icon("ph:sun-bold", width="20", height="20"), data_show=js("$is_alt")),
            variant="ghost",
            aria_label="Toggle theme",
            cls="h-9 px-4 py-2 flex-shrink-0",
            data_on_click=js("$is_alt = !$is_alt")
        ),
        data_on_load=js(f"""
            // Check iframe-specific storage first
            const iframeKey = 'iframe-theme-' + window.location.pathname.split('/').pop();
            const savedTheme = localStorage.getItem(iframeKey);
            if (savedTheme) {{
                $is_alt = savedTheme === '{alt_theme}';
            }} else {{
                // Fall back to system preference
                $is_alt = window.matchMedia('(prefers-color-scheme: dark)').matches;
            }}
        """),
        data_effect=js(f"""
            const theme = $is_alt ? '{alt_theme}' : '{default_theme}';
            // Only affect the current document (iframe), not parent
            document.documentElement.classList.toggle('{alt_theme}', $is_alt);
            document.documentElement.setAttribute('data-theme', theme);

            // Store in iframe-specific key
            const iframeKey = 'iframe-theme-' + window.location.pathname.split('/').pop();
            localStorage.setItem(iframeKey, theme);
        """),
        **kwargs,
    )


# Alias for docs rendering: use isolated behavior while examples show ThemeToggle()
ThemeToggle = IsolatedThemeToggle


# ============================================================================
# EXAMPLE FUNCTIONS (decorated with @with_code for markdown generation)
# ============================================================================

# Sizes example - showing different button sizes
@with_code
def size_variations_example():
    return Div(
        Div(
            P("Different Sizes", cls="font-medium mb-4"),
            Div(
                Div(
                    ThemeToggle(cls="scale-75"),
                    P("Small", cls="text-xs text-muted-foreground mt-1"),
                    cls="flex flex-col items-center"
                ),
                Div(
                    ThemeToggle(),
                    P("Default", cls="text-xs text-muted-foreground mt-1"),
                    cls="flex flex-col items-center"
                ),
                Div(
                    ThemeToggle(cls="scale-125"),
                    P("Large", cls="text-xs text-muted-foreground mt-1"),
                    cls="flex flex-col items-center"
                ),
                cls="flex items-start gap-8 justify-center"
            ),
        ),
        cls="space-y-4"
    )


# Custom icons example
@with_code
def custom_icons_labels_example():
    is_dark1 = Signal("is_dark1", False)
    is_dark2 = Signal("is_dark2", False)

    return Div(
        Div(
            P("Custom Icons", cls="font-medium mb-4"),
            Div(
                Div(
                    ThemeToggle(),
                    P("Sun/Moon", cls="text-xs text-muted-foreground mt-2"),
                    cls="flex flex-col items-center"
                ),
                Div(
                    is_dark1,
                    Button(
                        Span(Icon("lucide:sun-medium", width="20", height="20"), data_show=js("!$is_dark1")),
                        Span(Icon("lucide:moon-star", width="20", height="20"), data_show=js("$is_dark1")),
                        variant="ghost",
                        aria_label="Toggle theme",
                        cls="h-9 px-4 py-2",
                        data_on_click=js("$is_dark1 = !$is_dark1")
                    ),
                    P("Day/Night", cls="text-xs text-muted-foreground mt-2"),
                    data_on_load=js("$is_dark1 = localStorage.getItem('theme') === 'dark'"),
                    data_effect=js("""
                        const theme = $is_dark1 ? 'dark' : 'light';
                        document.documentElement.setAttribute('data-theme', theme);
                        localStorage.setItem('theme', theme);
                    """),
                    cls="flex flex-col items-center"
                ),
                Div(
                    is_dark2,
                    Button(
                        Span("Light", data_show=js("!$is_dark2")),
                        Span("Dark", data_show=js("$is_dark2")),
                        variant="outline",
                        size="sm",
                        aria_label="Toggle theme",
                        data_on_click=js("$is_dark2 = !$is_dark2")
                    ),
                    P("Text Labels", cls="text-xs text-muted-foreground mt-2"),
                    data_on_load=js("$is_dark2 = localStorage.getItem('theme') === 'dark'"),
                    data_effect=js("""
                        const theme = $is_dark2 ? 'dark' : 'light';
                        document.documentElement.setAttribute('data-theme', theme);
                        localStorage.setItem('theme', theme);
                    """),
                    cls="flex flex-col items-center"
                ),
                cls="flex items-start gap-8 justify-center"
            )
        ),
        cls="space-y-4"
    )


# Integration example - in a settings panel
@with_code
def settings_panel_integration_example():
    return Div(
        Div(
            H3("Appearance Settings", cls="text-lg font-semibold"),
            Div(
                Div(
                    P("Theme", cls="text-sm font-medium"),
                    P("Choose your preferred color scheme", cls="text-xs text-muted-foreground mt-1"),
                    cls="flex-1"
                ),
                ThemeToggle(),
                cls="flex items-center justify-between"
            ),
            Div(
                Div(
                    P("Auto-switch", cls="text-sm font-medium"),
                    P("Follow system theme preference", cls="text-xs text-muted-foreground mt-1"),
                    cls="flex-1 pr-4"
                ),
                Button(
                    "Configure",
                    variant="outline",
                    size="sm",
                    data_on_click=js("alert('System preference settings')")
                ),
                cls="flex items-start justify-between border-t pt-4 gap-4"
            ),
            cls="bg-muted/30 rounded-lg p-6 w-full max-w-lg mx-auto space-y-4"
        ),
        cls="flex items-center justify-center min-h-[350px]"
    )


# ============================================================================
# MODULE-LEVEL DATA (for markdown API)
# ============================================================================

EXAMPLES_DATA = [
    {"title": "Size Variations", "description": "Theme toggle in different sizes for various UI contexts", "code": size_variations_example.code},
    {"title": "Custom Icons & Labels", "description": "Different icon sets and text labels for theme switching", "code": custom_icons_labels_example.code},
    {"title": "Settings Panel Integration", "description": "Theme toggle integrated into a settings interface", "code": settings_panel_integration_example.code},
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
        use_iframe=True
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
        use_iframe=True,
        iframe_height="450px"
    )


def create_theme_toggle_docs():
    
    # Hero example - basic theme toggle
    @with_code
    def hero_theme_toggle_example():
        return Div(
            ThemeToggle(),
            P("Click to toggle between light and dark themes", cls="text-sm text-muted-foreground mt-2"),
            cls="flex flex-col items-center"
        )

    hero_example = ComponentPreview(
        hero_theme_toggle_example(),
        hero_theme_toggle_example.code,
        use_iframe=True
    )
    
    return auto_generate_page(
        TITLE,
        DESCRIPTION,
        list(examples()),
        cli_command="star add theme-toggle",
        hero_example=hero_example,
        component_slug="theme_toggle",
        api_reference=API_REFERENCE
    )