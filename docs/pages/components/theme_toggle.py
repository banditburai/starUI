"""
Theme Toggle component documentation - Light and dark mode switching.
"""

# Component metadata for auto-discovery
TITLE = "Theme Toggle"
DESCRIPTION = "Toggle between light and dark themes with Datastar reactivity."
CATEGORY = "ui"
ORDER = 95
STATUS = "stable"

from starhtml import Div, H3, Icon, P, Span, FT
from starhtml import Span as HTMLSpan
from starhtml.datastar import ds_show, ds_on_click, ds_on_load, ds_signals, ds_effect, toggle_signal
from starui.registry.components.button import Button
from widgets.component_preview import ComponentPreview
from utils import auto_generate_page, with_code, Prop, build_api_reference


def IsolatedThemeToggle(alt_theme="dark", default_theme="light", **kwargs) -> FT:
    """Theme toggle that only affects its iframe container, not the parent document."""

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
            f"""
            // Check iframe-specific storage first
            const iframeKey = 'iframe-theme-' + window.location.pathname.split('/').pop();
            const savedTheme = localStorage.getItem(iframeKey);
            if (savedTheme) {{
                $isAlt = savedTheme === '{alt_theme}';
            }} else {{
                // Fall back to system preference
                $isAlt = window.matchMedia('(prefers-color-scheme: dark)').matches;
            }}
            """
        ),
        ds_effect(f"""
            const theme = $isAlt ? '{alt_theme}' : '{default_theme}';
            // Only affect the current document (iframe), not parent
            document.documentElement.classList.toggle('{alt_theme}', $isAlt);
            document.documentElement.setAttribute('data-theme', theme);
            
            // Store in iframe-specific key
            const iframeKey = 'iframe-theme-' + window.location.pathname.split('/').pop();
            localStorage.setItem(iframeKey, theme);
        """),
        **kwargs,
    )


# Alias for docs rendering: use isolated behavior while examples show ThemeToggle()
ThemeToggle = IsolatedThemeToggle

def examples():
    """Generate Theme Toggle examples using ComponentPreview with tabs."""
    
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

    yield ComponentPreview(
        size_variations_example(),
        size_variations_example.code,
        title="Size Variations",
        description="Theme toggle in different sizes for various UI contexts",
        use_iframe=True
    )
    
    # Custom icons example
    @with_code
    def custom_icons_labels_example():
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
                        Button(
                            Span(Icon("lucide:sun-medium", width="20", height="20"), ds_show("!$isDark1")),
                            Span(Icon("lucide:moon-star", width="20", height="20"), ds_show("$isDark1")),
                            ds_on_click(toggle_signal("isDark1")),
                            variant="ghost",
                            aria_label="Toggle theme",
                            cls="h-9 px-4 py-2"
                        ),
                        P("Day/Night", cls="text-xs text-muted-foreground mt-2"),
                        ds_signals(isDark1=False),
                        ds_on_load("$isDark1 = localStorage.getItem('theme') === 'dark'"),
                        ds_effect("""
                            const theme = $isDark1 ? 'dark' : 'light';
                            document.documentElement.setAttribute('data-theme', theme);
                            localStorage.setItem('theme', theme);
                        """),
                        cls="flex flex-col items-center"
                    ),
                    Div(
                        Button(
                            Span("Light", ds_show("!$isDark2")),
                            Span("Dark", ds_show("$isDark2")),
                            ds_on_click(toggle_signal("isDark2")),
                            variant="outline",
                            size="sm",
                            aria_label="Toggle theme",
                        ),
                        P("Text Labels", cls="text-xs text-muted-foreground mt-2"),
                        ds_signals(isDark2=False),
                        ds_on_load("$isDark2 = localStorage.getItem('theme') === 'dark'"),
                        ds_effect("""
                            const theme = $isDark2 ? 'dark' : 'light';
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

    yield ComponentPreview(
        custom_icons_labels_example(),
        custom_icons_labels_example.code,
        title="Custom Icons & Labels",
        description="Different icon sets and text labels for theme switching",
        use_iframe=True
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
                        ds_on_click="alert('System preference settings')"
                    ),
                    cls="flex items-start justify-between border-t pt-4 gap-4"
                ),
                cls="bg-muted/30 rounded-lg p-6 w-full max-w-lg mx-auto space-y-4"
            ),
            cls="flex items-center justify-center min-h-[350px]"
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
    """Create theme toggle documentation page using convention-based approach."""
    
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
        api_reference=build_api_reference(
            main_props=[
                Prop("alt_theme", "str", "Alternative theme name (usually dark)", "dark"),
                Prop("default_theme", "str", "Default theme name (usually light)", "light"),
                Prop("cls", "str", "Additional CSS classes", "''"),
            ]
        )
    )