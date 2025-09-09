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
from starui.registry.components.theme_toggle import ThemeToggle
from starui.registry.components.button import Button
from widgets.component_preview import ComponentPreview


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


def examples():
    """Generate Theme Toggle examples using ComponentPreview with tabs."""
    
    # Sizes example - showing different button sizes
    yield ComponentPreview(
        Div(
            Div(
                P("Different Sizes", cls="font-medium mb-4"),
                Div(
                    # Small size
                    Div(
                        IsolatedThemeToggle(cls="scale-75"),
                        P("Small", cls="text-xs text-muted-foreground mt-1"),
                        cls="flex flex-col items-center"
                    ),
                    # Default size
                    Div(
                        IsolatedThemeToggle(),
                        P("Default", cls="text-xs text-muted-foreground mt-1"),
                        cls="flex flex-col items-center"
                    ),
                    # Large size
                    Div(
                        IsolatedThemeToggle(cls="scale-125"),
                        P("Large", cls="text-xs text-muted-foreground mt-1"),
                        cls="flex flex-col items-center"
                    ),
                    cls="flex items-start gap-8 justify-center"
                ),
            ),
            cls="space-y-4"
        ),
        '''# Different sizes using CSS transforms
ThemeToggle(cls="scale-75")   # Small
ThemeToggle()                  # Default  
ThemeToggle(cls="scale-125")   # Large''',
        title="Size Variations",
        description="Theme toggle in different sizes for various UI contexts",
        use_iframe=True
    )
    
    # Custom icons example
    yield ComponentPreview(
        Div(
            Div(
                P("Custom Icons", cls="font-medium mb-4"),
                Div(
                    # Sun/Moon (default)
                    Div(
                        IsolatedThemeToggle(),
                        P("Sun/Moon", cls="text-xs text-muted-foreground mt-2"),
                        cls="flex flex-col items-center"
                    ),
                    # Day/Night with different icons
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
                    # Light/Dark text
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
        ),
        '''# Default icons
ThemeToggle()

# Custom icons
Button(
    Span(Icon("lucide:sun-medium"), ds_show("!$isDark")),
    Span(Icon("lucide:moon-star"), ds_show("$isDark")),
    ds_on_click(toggle_signal("isDark")),
    variant="ghost"
)

# Text labels instead of icons
Button(
    Span("Light", ds_show("!$isDark")),
    Span("Dark", ds_show("$isDark")),
    ds_on_click(toggle_signal("isDark")),
    variant="outline",
    size="sm"
)''',
        title="Custom Icons & Labels",
        description="Different icon sets and text labels for theme switching",
        use_iframe=True
    )
    
    # Integration example - in a settings panel
    yield ComponentPreview(
        Div(
            Div(
                H3("Appearance Settings", cls="text-lg font-semibold"),
                Div(
                    Div(
                        P("Theme", cls="text-sm font-medium"),
                        P("Choose your preferred color scheme", cls="text-xs text-muted-foreground mt-1"),
                        cls="flex-1"
                    ),
                    IsolatedThemeToggle(),
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
        ),
        '''# Example: Settings panel integration
Div(
    H3("Appearance Settings", cls="text-lg font-semibold"),
    Div(
        Div(
            P("Theme", cls="text-sm font-medium"),
            P("Choose your preferred color scheme", cls="text-xs text-muted-foreground"),
        ),
        ThemeToggle(),
        cls="flex items-center justify-between"
    ),
    cls="bg-muted/30 rounded-lg p-6"
)''',
        title="Settings Panel Integration",
        description="Theme toggle integrated into a settings interface",
        use_iframe=True,
        iframe_height="450px"
    )


def create_theme_toggle_docs():
    """Create theme toggle documentation page using convention-based approach."""
    from utils import auto_generate_page
    
    # Hero example - basic theme toggle
    hero_example = ComponentPreview(
        Div(
            IsolatedThemeToggle(),
            P("Click to toggle between light and dark themes", cls="text-sm text-muted-foreground mt-2"),
            cls="flex flex-col items-center"
        ),
        '''ThemeToggle()''',
        use_iframe=True
    )
    
    return auto_generate_page(
        TITLE,
        DESCRIPTION,
        list(examples()),
        cli_command="star add theme-toggle",
        hero_example=hero_example,
        component_slug="theme_toggle",
        api_reference={
            "props": [
                {
                    "name": "alt_theme",
                    "type": "str",
                    "default": "dark",
                    "description": "Alternative theme name (typically dark mode)"
                },
                {
                    "name": "default_theme", 
                    "type": "str",
                    "default": "light",
                    "description": "Default theme name (typically light mode)"
                },
                {
                    "name": "cls",
                    "type": "str",
                    "default": "''",
                    "description": "Additional CSS classes"
                }
            ]
        }
    )