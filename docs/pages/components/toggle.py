"""
Toggle component documentation - Convention-based functional approach.
Clean, minimal, and easy to extend.
"""

# Component metadata for auto-discovery
TITLE = "Toggle"
DESCRIPTION = "A two-state button that can be either on or off."
CATEGORY = "ui"
ORDER = 80
STATUS = "stable"

from starhtml import Div, P, Icon, Span, H3, Code
from starhtml.datastar import (
    ds_on_click, ds_show, ds_text, ds_signals, value,
    ds_bind, ds_disabled, ds_on_change, ds_effect, ds_class
)
from starui.registry.components.toggle import Toggle
from starui.registry.components.button import Button
from starui.registry.components.badge import Badge
from starui.registry.components.card import Card, CardHeader, CardContent, CardTitle, CardDescription
from starui.registry.components.separator import Separator
from utils import auto_generate_page
from widgets.component_preview import ComponentPreview


def examples():
    """Generate toggle examples using ComponentPreview with tabs."""
    
    # Basic toggle
    yield ComponentPreview(
        Div(
            Toggle(
                Icon("lucide:bold", cls="h-4 w-4"),
                variant="outline",
                signal="bold_toggle"
            ),
            P(
                "Bold is ",
                Span(ds_text("$bold_toggle ? 'ON' : 'OFF'"), cls="font-mono"),
                cls="text-sm text-muted-foreground mt-2"
            ),
            cls="flex flex-col items-center"
        ),
        '''Toggle(
    Icon("lucide:bold", cls="h-4 w-4"),
    variant="outline",
    signal="bold_toggle"
)''',
        title="Basic Toggle",
        description="Simple toggle button with icon"
    )
    
    # Text formatting toolbar
    yield ComponentPreview(
        Card(
            CardHeader(
                CardTitle("Text Editor"),
                CardDescription("Format your text")
            ),
            CardContent(
                Div(
                    Div(
                        Toggle(
                            Icon("lucide:bold", cls="h-4 w-4"),
                            variant="outline",
                            size="sm",
                            signal="format_bold",
                            aria_label="Bold"
                        ),
                        Toggle(
                            Icon("lucide:italic", cls="h-4 w-4"),
                            variant="outline",
                            size="sm",
                            signal="format_italic",
                            aria_label="Italic"
                        ),
                        Toggle(
                            Icon("lucide:underline", cls="h-4 w-4"),
                            variant="outline",
                            size="sm",
                            signal="format_underline",
                            aria_label="Underline"
                        ),
                        Separator(orientation="vertical", cls="h-6"),
                        Toggle(
                            Icon("lucide:align-left", cls="h-4 w-4"),
                            variant="outline",
                            size="sm",
                            signal="align_left",
                            pressed=True,
                            aria_label="Align left"
                        ),
                        Toggle(
                            Icon("lucide:align-center", cls="h-4 w-4"),
                            variant="outline",
                            size="sm",
                            signal="align_center",
                            aria_label="Align center"
                        ),
                        Toggle(
                            Icon("lucide:align-right", cls="h-4 w-4"),
                            variant="outline",
                            size="sm",
                            signal="align_right",
                            aria_label="Align right"
                        ),
                        cls="flex items-center gap-1"
                    ),
                    Div(
                        P(
                            "Sample text",
                            ds_class(**{
                                "font-bold": "$format_bold",
                                "italic": "$format_italic",
                                "underline": "$format_underline",
                                "text-left": "$align_left",
                                "text-center": "$align_center",
                                "text-right": "$align_right"
                            }),
                            cls="p-4 border rounded-md min-h-[60px]"
                        ),
                        cls="mt-4"
                    ),
                    ds_effect("""
                        // Ensure only one alignment is active
                        if ($align_left && ($align_center || $align_right)) {
                            $align_center = false;
                            $align_right = false;
                        } else if ($align_center && ($align_left || $align_right)) {
                            $align_left = false;
                            $align_right = false;
                        } else if ($align_right && ($align_left || $align_center)) {
                            $align_left = false;
                            $align_center = false;
                        }
                    """)
                )
            ),
            cls="max-w-md"
        ),
        '''// Text formatting toolbar
Div(
    Toggle(Icon("lucide:bold"), variant="outline", signal="format_bold"),
    Toggle(Icon("lucide:italic"), variant="outline", signal="format_italic"),
    Toggle(Icon("lucide:underline"), variant="outline", signal="format_underline"),
    Separator(orientation="vertical"),
    Toggle(Icon("lucide:align-left"), variant="outline", signal="align_left"),
    // ... more alignment options
    cls="flex items-center gap-1"
)
P(
    "Sample text",
    ds_class({
        "font-bold": "$format_bold",
        "italic": "$format_italic",
        "underline": "$format_underline"
    })
)''',
        title="Text Formatting",
        description="Rich text editor formatting toolbar"
    )
    
    # Feature toggles
    yield ComponentPreview(
        Card(
            CardHeader(
                CardTitle("Feature Flags"),
                CardDescription("Enable experimental features")
            ),
            CardContent(
                Div(
                    Div(
                        Toggle(
                            Icon("lucide:flask", cls="h-4 w-4 mr-2"),
                            Span("Experimental Mode"),
                            variant="outline",
                            signal="experimental"
                        ),
                        P("Enable beta features", cls="text-sm text-muted-foreground mt-1"),
                        cls="space-y-1"
                    ),
                    Div(
                        Toggle(
                            Icon("lucide:bug", cls="h-4 w-4 mr-2"),
                            Span("Debug Mode"),
                            variant="outline",
                            signal="debug"
                        ),
                        P("Show debug information", cls="text-sm text-muted-foreground mt-1"),
                        cls="space-y-1"
                    ),
                    Div(
                        Toggle(
                            Icon("lucide:zap", cls="h-4 w-4 mr-2"),
                            Span("Performance Mode"),
                            variant="outline",
                            signal="performance",
                            pressed=True
                        ),
                        P("Optimize for speed", cls="text-sm text-muted-foreground mt-1"),
                        cls="space-y-1"
                    ),
                    Separator(cls="my-4"),
                    Div(
                        Badge(
                            ds_text("[$experimental && 'Experimental', $debug && 'Debug', $performance && 'Performance'].filter(Boolean).join(' • ') || 'Standard Mode'"),
                            variant="secondary",
                            cls="w-full justify-center"
                        ),
                        cls="text-center"
                    ),
                    ds_signals(experimental=False, debug=False, performance=True),
                    cls="space-y-3"
                )
            ),
            cls="max-w-md"
        ),
        '''Card(
    CardContent(
        Toggle(
            Icon("lucide:flask"), "Experimental Mode",
            variant="outline",
            signal="experimental"
        ),
        Toggle(
            Icon("lucide:bug"), "Debug Mode",
            variant="outline",
            signal="debug"
        ),
        Toggle(
            Icon("lucide:zap"), "Performance Mode",
            variant="outline",
            signal="performance",
            pressed=True
        ),
        Badge(
            ds_text("active modes"),
            variant="secondary"
        )
    )
)''',
        title="Feature Toggles",
        description="Enable/disable features with descriptive toggles"
    )
    
    # Size variations
    yield ComponentPreview(
        Div(
            Div(
                H3("Small", cls="text-sm font-medium mb-2"),
                Toggle(
                    Icon("lucide:star", cls="h-3 w-3"),
                    variant="outline",
                    size="sm",
                    signal="star_sm"
                ),
                Toggle(
                    Icon("lucide:heart", cls="h-3 w-3"),
                    Span("Like", cls="text-xs"),
                    variant="outline",
                    size="sm",
                    signal="heart_sm"
                ),
                cls="space-y-2"
            ),
            Div(
                H3("Default", cls="text-sm font-medium mb-2"),
                Toggle(
                    Icon("lucide:star", cls="h-4 w-4"),
                    variant="outline",
                    signal="star_default"
                ),
                Toggle(
                    Icon("lucide:heart", cls="h-4 w-4"),
                    Span("Like"),
                    variant="outline",
                    signal="heart_default"
                ),
                cls="space-y-2"
            ),
            Div(
                H3("Large", cls="text-sm font-medium mb-2"),
                Toggle(
                    Icon("lucide:star", cls="h-5 w-5"),
                    variant="outline",
                    size="lg",
                    signal="star_lg"
                ),
                Toggle(
                    Icon("lucide:heart", cls="h-5 w-5"),
                    Span("Like", cls="text-lg"),
                    variant="outline",
                    size="lg",
                    signal="heart_lg"
                ),
                cls="space-y-2"
            ),
            cls="flex gap-8 justify-center"
        ),
        '''// Size variations
Toggle(Icon("lucide:star"), variant="outline", size="sm")
Toggle(Icon("lucide:heart"), "Like", variant="outline", size="sm")

Toggle(Icon("lucide:star"), variant="outline")  // default size
Toggle(Icon("lucide:heart"), "Like", variant="outline")

Toggle(Icon("lucide:star"), variant="outline", size="lg")
Toggle(Icon("lucide:heart"), "Like", variant="outline", size="lg")''',
        title="Size Variations",
        description="Small, default, and large toggle sizes"
    )
    
    # Social interaction toggles
    yield ComponentPreview(
        Card(
            CardContent(
                Div(
                    Div(
                        Icon("lucide:image", cls="h-48 w-full text-muted-foreground/20"),
                        cls="bg-muted rounded-md flex items-center justify-center mb-4"
                    ),
                    P("Beautiful sunset over the mountains", cls="font-medium mb-2"),
                    P("Posted 2 hours ago", cls="text-sm text-muted-foreground mb-4"),
                    Div(
                        Toggle(
                            Icon("lucide:heart", cls="h-4 w-4 mr-1"),
                            Span(ds_text("$liked ? '124' : '123'"), cls="text-sm"),
                            variant="outline",
                            signal="liked",
                            aria_label="Like post"
                        ),
                        Toggle(
                            Icon("lucide:message-circle", cls="h-4 w-4 mr-1"),
                            Span("8", cls="text-sm"),
                            variant="outline",
                            signal="comment",
                            aria_label="Comment"
                        ),
                        Toggle(
                            Icon("lucide:bookmark", cls="h-4 w-4"),
                            variant="outline",
                            signal="saved",
                            aria_label="Save post"
                        ),
                        Toggle(
                            Icon("lucide:share-2", cls="h-4 w-4"),
                            variant="outline",
                            signal="share",
                            aria_label="Share post"
                        ),
                        cls="flex gap-2"
                    ),
                    Div(
                        P(
                            ds_show("$liked"),
                            Icon("lucide:heart", cls="h-3 w-3 inline mr-1 text-red-500"),
                            "You liked this",
                            cls="text-xs text-muted-foreground"
                        ),
                        P(
                            ds_show("$saved"),
                            Icon("lucide:bookmark", cls="h-3 w-3 inline mr-1"),
                            "Saved to collection",
                            cls="text-xs text-muted-foreground"
                        ),
                        cls="mt-2 space-y-1"
                    ),
                    ds_signals(liked=False, comment=False, saved=False, share=False)
                )
            ),
            cls="max-w-sm"
        ),
        '''// Social media post interactions
Card(
    CardContent(
        // Post content
        Div(
            Toggle(
                Icon("lucide:heart"),
                Span(ds_text("$liked ? '124' : '123'")),
                variant="outline",
                signal="liked"
            ),
            Toggle(Icon("lucide:message-circle"), "8", variant="outline"),
            Toggle(Icon("lucide:bookmark"), variant="outline", signal="saved"),
            Toggle(Icon("lucide:share-2"), variant="outline"),
            cls="flex gap-2"
        ),
        P(ds_show("$liked"), Icon("lucide:heart"), "You liked this"),
        P(ds_show("$saved"), Icon("lucide:bookmark"), "Saved")
    )
)''',
        title="Social Interactions",
        description="Like, comment, save, and share toggles"
    )
    
    # Music player controls
    yield ComponentPreview(
        Card(
            CardHeader(
                CardTitle("Now Playing"),
                CardDescription("Sunset Dreams - Ambient Mix")
            ),
            CardContent(
                Div(
                    Div(
                        Div(cls="h-2 bg-secondary rounded-full"),
                        Div(cls="h-2 bg-primary rounded-full w-1/3"),
                        cls="relative"
                    ),
                    P("1:23 / 4:56", cls="text-xs text-muted-foreground mt-2 text-center"),
                    Div(
                        Toggle(
                            Icon("lucide:shuffle", cls="h-4 w-4"),
                            size="sm",
                            signal="shuffle",
                            aria_label="Shuffle"
                        ),
                        Toggle(
                            Icon("lucide:skip-back", cls="h-4 w-4"),
                            size="sm",
                            signal="prev",
                            aria_label="Previous"
                        ),
                        Toggle(
                            Icon("lucide:play", cls="h-5 w-5"),
                            signal="playing",
                            pressed=True,
                            aria_label="Play/Pause"
                        ),
                        Toggle(
                            Icon("lucide:skip-forward", cls="h-4 w-4"),
                            size="sm",
                            signal="next",
                            aria_label="Next"
                        ),
                        Toggle(
                            Icon("lucide:repeat", cls="h-4 w-4"),
                            size="sm",
                            signal="repeat",
                            pressed=True,
                            aria_label="Repeat"
                        ),
                        cls="flex items-center justify-center gap-2 mt-4"
                    ),
                    Div(
                        Badge(
                            ds_text("$shuffle ? 'Shuffle ON' : 'Shuffle OFF'"),
                            variant="outline",
                            cls="text-xs"
                        ),
                        Badge(
                            ds_text("$repeat ? 'Repeat ON' : 'Repeat OFF'"),
                            variant="outline",
                            cls="text-xs"
                        ),
                        cls="flex justify-center gap-2 mt-3"
                    ),
                    ds_signals(shuffle=False, prev=False, playing=True, next=False, repeat=True)
                )
            ),
            cls="max-w-sm"
        ),
        '''// Music player controls
Card(
    CardContent(
        // Progress bar
        Div(
            Toggle(Icon("lucide:shuffle"), size="sm", signal="shuffle"),
            Toggle(Icon("lucide:skip-back"), size="sm"),
            Toggle(Icon("lucide:play"), signal="playing", pressed=True),
            Toggle(Icon("lucide:skip-forward"), size="sm"),
            Toggle(Icon("lucide:repeat"), size="sm", signal="repeat"),
            cls="flex items-center justify-center gap-2"
        ),
        Badge(ds_text("$shuffle ? 'Shuffle ON' : 'OFF'"))
    )
)''',
        title="Music Player",
        description="Media player control toggles"
    )
    
    # Disabled states
    yield ComponentPreview(
        Div(
            Div(
                H3("Enabled", cls="text-sm font-medium mb-2"),
                Div(
                    Toggle(
                        Icon("lucide:wifi", cls="h-4 w-4"),
                        variant="outline",
                        signal="wifi_enabled"
                    ),
                    Toggle(
                        Icon("lucide:bluetooth", cls="h-4 w-4"),
                        "Bluetooth",
                        variant="outline",
                        signal="bluetooth_enabled"
                    ),
                    cls="flex gap-2"
                )
            ),
            Div(
                H3("Disabled", cls="text-sm font-medium mb-2"),
                Div(
                    Toggle(
                        Icon("lucide:wifi", cls="h-4 w-4"),
                        variant="outline",
                        disabled=True,
                        signal="wifi_disabled"
                    ),
                    Toggle(
                        Icon("lucide:bluetooth", cls="h-4 w-4"),
                        "Bluetooth",
                        variant="outline",
                        disabled=True,
                        pressed=True,
                        signal="bluetooth_disabled"
                    ),
                    cls="flex gap-2"
                )
            ),
            cls="space-y-4"
        ),
        '''// Disabled states
Toggle(Icon("lucide:wifi"), variant="outline")  // Enabled
Toggle(Icon("lucide:bluetooth"), "Bluetooth", variant="outline")

Toggle(Icon("lucide:wifi"), variant="outline", disabled=True)  // Disabled
Toggle(
    Icon("lucide:bluetooth"), "Bluetooth",
    variant="outline",
    disabled=True,
    pressed=True  // Disabled in pressed state
)''',
        title="Disabled States",
        description="Disabled toggles in different states"
    )


def create_toggle_docs():
    """Create toggle documentation page using convention-based approach."""
    
    api_reference = {
        "props": [
            {
                "name": "variant",
                "type": "Literal['default', 'outline']",
                "default": "'default'",
                "description": "Visual style variant"
            },
            {
                "name": "size",
                "type": "Literal['default', 'sm', 'lg']",
                "default": "'default'",
                "description": "Size of the toggle button"
            },
            {
                "name": "pressed",
                "type": "bool",
                "default": "False",
                "description": "Initial pressed state"
            },
            {
                "name": "signal",
                "type": "str",
                "default": "auto-generated",
                "description": "Datastar signal name for state management"
            },
            {
                "name": "disabled",
                "type": "bool",
                "default": "False",
                "description": "Whether the toggle is disabled"
            },
            {
                "name": "aria_label",
                "type": "str | None",
                "default": "None",
                "description": "Accessibility label for screen readers"
            },
            {
                "name": "cls",
                "type": "str",
                "default": "''",
                "description": "Additional CSS classes"
            }
        ]
    }
    
    # Hero example
    hero_example = ComponentPreview(
        Div(
            Toggle(
                Icon("lucide:bold", cls="h-4 w-4"),
                Span("Bold"),
                variant="outline",
                signal="hero_toggle"
            ),
            P(
                "Toggle is ",
                Span(ds_text("$hero_toggle ? 'pressed' : 'not pressed'"), cls="font-mono"),
                cls="text-sm text-muted-foreground mt-2"
            ),
            cls="flex flex-col items-center"
        ),
        '''Toggle(
    Icon("lucide:bold", cls="h-4 w-4"),
    Span("Bold"),
    variant="outline",
    signal="hero_toggle"
)''',
        copy_button=True
    )
    
    return auto_generate_page(
        TITLE,
        DESCRIPTION,
        list(examples()),
        cli_command="star add toggle",
        api_reference=api_reference,
        hero_example=hero_example,
        component_slug="toggle"
    )