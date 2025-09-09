"""
Toggle Group component documentation - Interactive button groups for selections.
Flexible toggle groups for single or multiple selections.
"""

# Component metadata for auto-discovery
TITLE = "Toggle Group"
DESCRIPTION = "A set of two-state buttons that can be toggled on or off. Supports single and multiple selection modes."
CATEGORY = "ui"
ORDER = 40
STATUS = "stable"

from starhtml import Div, P, H3, H4, Span, Icon, Label, Input
from starhtml.datastar import ds_signals, ds_on_click, ds_text, ds_show, value, ds_bind, ds_class, toggle_signal
from starui.registry.components.toggle_group import ToggleGroup, SingleToggleGroup, MultipleToggleGroup
from starui.registry.components.button import Button
from starui.registry.components.separator import Separator
from widgets.component_preview import ComponentPreview


def examples():
    """Generate toggle group examples using ComponentPreview with tabs."""
    
    # Text formatting toolbar
    yield ComponentPreview(
        Div(
            # Rich text formatting
            P("Text Formatting", cls="font-medium mb-4"),
            SingleToggleGroup(
                ("bold", Icon("lucide:bold", cls="w-4 h-4")),
                ("italic", Icon("lucide:italic", cls="w-4 h-4")),
                ("underline", Icon("lucide:underline", cls="w-4 h-4")),
                ("strikethrough", Icon("lucide:strikethrough", cls="w-4 h-4")),
                variant="outline",
                signal="formatting"
            ),
            Div(
                P("Selected format: ", cls="text-sm inline"),
                Span(ds_text("$formatting_value || 'None'"), cls="font-mono text-sm bg-muted px-2 py-1 rounded"),
                cls="mt-4"
            ),
            cls="p-4 border rounded-lg"
        ),
        '''from starui.registry.components.toggle_group import SingleToggleGroup
from starhtml import Icon, Div, P, Span
from starhtml.datastar import ds_text

SingleToggleGroup(
    ("bold", Icon("lucide:bold", cls="w-4 h-4")),
    ("italic", Icon("lucide:italic", cls="w-4 h-4")),
    ("underline", Icon("lucide:underline", cls="w-4 h-4")),
    ("strikethrough", Icon("lucide:strikethrough", cls="w-4 h-4")),
    variant="outline",
    signal="formatting"
)

# Show selected value
Span(ds_text("$formatting_value || 'None'"))''',
        title="Text Formatting Toolbar",
        description="Single-selection toggle group for text formatting options"
    )
    
    # View switcher
    yield ComponentPreview(
        Div(
            P("View Mode", cls="font-medium mb-4"),
            SingleToggleGroup(
                ("grid", Div(Icon("lucide:grid-3x3", cls="w-4 h-4"), "Grid", cls="flex items-center gap-2")),
                ("list", Div(Icon("lucide:list", cls="w-4 h-4"), "List", cls="flex items-center gap-2")),
                ("card", Div(Icon("lucide:layout-grid", cls="w-4 h-4"), "Card", cls="flex items-center gap-2")),
                signal="view_mode"
            ),
            
            # Content area that changes based on selection
            Div(
                # Grid view
                Div(
                    Div("Item 1", cls="p-4 border rounded bg-muted"),
                    Div("Item 2", cls="p-4 border rounded bg-muted"),
                    Div("Item 3", cls="p-4 border rounded bg-muted"),
                    Div("Item 4", cls="p-4 border rounded bg-muted"),
                    ds_show("$view_mode_value === 'grid'"),
                    cls="grid grid-cols-2 gap-2"
                ),
                
                # List view
                Div(
                    Div("Item 1", cls="p-3 border rounded bg-muted mb-2"),
                    Div("Item 2", cls="p-3 border rounded bg-muted mb-2"),
                    Div("Item 3", cls="p-3 border rounded bg-muted mb-2"),
                    Div("Item 4", cls="p-3 border rounded bg-muted"),
                    ds_show("$view_mode_value === 'list'"),
                    cls=""
                ),
                
                # Card view
                Div(
                    Div(
                        H4("Item 1", cls="font-medium"),
                        P("Description for item 1", cls="text-sm text-muted-foreground"),
                        cls="p-4 border rounded bg-muted mb-3"
                    ),
                    Div(
                        H4("Item 2", cls="font-medium"),
                        P("Description for item 2", cls="text-sm text-muted-foreground"),
                        cls="p-4 border rounded bg-muted mb-3"
                    ),
                    ds_show("$view_mode_value === 'card'"),
                    cls=""
                ),
                
                cls="mt-6 min-h-[200px]"
            ),
            
            cls="p-4 border rounded-lg"
        ),
        '''from starui.registry.components.toggle_group import SingleToggleGroup
from starhtml import Div, Icon, H4, P
from starhtml.datastar import ds_show

SingleToggleGroup(
    ("grid", Div(Icon("lucide:grid-3x3"), "Grid", cls="flex items-center gap-2")),
    ("list", Div(Icon("lucide:list"), "List", cls="flex items-center gap-2")),
    ("card", Div(Icon("lucide:layout-grid"), "Card", cls="flex items-center gap-2")),
    signal="view_mode"
)

# Content that changes based on selection
Div(
    # Grid view
    Div(
        "Grid content...",
        ds_show("$view_mode_value === 'grid'"),
        cls="grid grid-cols-2 gap-2"
    ),
    
    # List view
    Div(
        "List content...",
        ds_show("$view_mode_value === 'list'")
    ),
    
    # Card view
    Div(
        "Card content...",
        ds_show("$view_mode_value === 'card'")
    ),
    cls="mt-6"
)''',
        title="View Mode Switcher",
        description="Toggle between different content layouts with dynamic content display"
    )
    
    # Multi-select filter options
    yield ComponentPreview(
        Div(
            P("Filter Options", cls="font-medium mb-4"),
            MultipleToggleGroup(
                ("featured", Div(Icon("lucide:star", cls="w-4 h-4"), "Featured", cls="flex items-center gap-2")),
                ("sale", Div(Icon("lucide:percent", cls="w-4 h-4"), "On Sale", cls="flex items-center gap-2")),
                ("new", Div(Icon("lucide:sparkles", cls="w-4 h-4"), "New", cls="flex items-center gap-2")),
                ("popular", Div(Icon("lucide:trending-up", cls="w-4 h-4"), "Popular", cls="flex items-center gap-2")),
                variant="outline",
                signal="filters"
            ),
            
            # Show selected filters
            Div(
                P("Active Filters:", cls="text-sm font-medium mb-2"),
                Div(
                    ds_text("$filters_value.length > 0 ? $filters_value.join(', ') : 'None selected'"),
                    cls="text-sm bg-muted p-3 rounded font-mono"
                ),
                cls="mt-6"
            ),
            
            cls="p-4 border rounded-lg"
        ),
        '''from starui.registry.components.toggle_group import MultipleToggleGroup
from starhtml import Div, Icon, P
from starhtml.datastar import ds_text

MultipleToggleGroup(
    ("featured", Div(Icon("lucide:star"), "Featured", cls="flex items-center gap-2")),
    ("sale", Div(Icon("lucide:percent"), "On Sale", cls="flex items-center gap-2")),
    ("new", Div(Icon("lucide:sparkles"), "New", cls="flex items-center gap-2")),
    ("popular", Div(Icon("lucide:trending-up"), "Popular", cls="flex items-center gap-2")),
    variant="outline",
    signal="filters"
)

# Show active filters
Div(ds_text("$filters_value.length > 0 ? $filters_value.join(', ') : 'None selected'"))''',
        title="Multi-Select Filters",
        description="Multiple selection toggle group for filtering options"
    )
    
    # Size variations
    yield ComponentPreview(
        Div(
            # Small size
            Div(
                P("Small", cls="text-sm font-medium mb-3"),
                SingleToggleGroup(
                    ("sm1", "One"),
                    ("sm2", "Two"), 
                    ("sm3", "Three"),
                    size="sm",
                    signal="small_group"
                ),
                cls="mb-6"
            ),
            
            # Default size
            Div(
                P("Default", cls="text-sm font-medium mb-3"),
                SingleToggleGroup(
                    ("def1", "One"),
                    ("def2", "Two"),
                    ("def3", "Three"),
                    signal="default_group"
                ),
                cls="mb-6"
            ),
            
            # Large size
            Div(
                P("Large", cls="text-sm font-medium mb-3"),
                SingleToggleGroup(
                    ("lg1", "One"),
                    ("lg2", "Two"),
                    ("lg3", "Three"),
                    size="lg",
                    signal="large_group"
                ),
                cls=""
            ),
            
            cls="p-4 border rounded-lg"
        ),
        '''from starui.registry.components.toggle_group import SingleToggleGroup

# Small size
SingleToggleGroup(
    ("one", "One"),
    ("two", "Two"),
    ("three", "Three"),
    size="sm"
)

# Default size
SingleToggleGroup(
    ("one", "One"),
    ("two", "Two"),
    ("three", "Three")
)

# Large size
SingleToggleGroup(
    ("one", "One"),
    ("two", "Two"),
    ("three", "Three"),
    size="lg"
)''',
        title="Size Variations",
        description="Toggle groups in different sizes for various use cases"
    )
    
    # Alignment and justification controls
    yield ComponentPreview(
        Div(
            P("Text Alignment", cls="font-medium mb-4"),
            SingleToggleGroup(
                ("left", Icon("lucide:align-left", cls="w-4 h-4")),
                ("center", Icon("lucide:align-center", cls="w-4 h-4")),
                ("right", Icon("lucide:align-right", cls="w-4 h-4")),
                ("justify", Icon("lucide:align-justify", cls="w-4 h-4")),
                variant="outline",
                signal="alignment"
            ),
            
            Separator(cls="my-6"),
            
            P("Text Decoration", cls="font-medium mb-4"),
            MultipleToggleGroup(
                ("bold", Icon("lucide:bold", cls="w-4 h-4")),
                ("italic", Icon("lucide:italic", cls="w-4 h-4")),
                ("underline", Icon("lucide:underline", cls="w-4 h-4")),
                signal="decoration"
            ),
            
            # Preview area
            Div(
                P(
                    "The quick brown fox jumps over the lazy dog. This sample text demonstrates the selected text alignment and decoration options.",
                    ds_class(**{
                        "text-left": "$alignment_value === 'left' || !$alignment_value",
                        "text-center": "$alignment_value === 'center'",
                        "text-right": "$alignment_value === 'right'",
                        "text-justify": "$alignment_value === 'justify'",
                        "font-bold": "$decoration_value && $decoration_value.includes('bold')",
                        "italic": "$decoration_value && $decoration_value.includes('italic')",
                        "underline": "$decoration_value && $decoration_value.includes('underline')"
                    }),
                    cls="p-4 bg-muted rounded transition-all"
                ),
                cls="mt-6"
            ),
            
            cls="p-4 border rounded-lg"
        ),
        '''from starui.registry.components.toggle_group import SingleToggleGroup, MultipleToggleGroup
from starhtml import Icon, Div, P

# Single selection for alignment
SingleToggleGroup(
    ("left", Icon("lucide:align-left")),
    ("center", Icon("lucide:align-center")),
    ("right", Icon("lucide:align-right")),
    ("justify", Icon("lucide:align-justify")),
    variant="outline",
    signal="alignment"
)

# Multiple selection for text decoration
MultipleToggleGroup(
    ("bold", Icon("lucide:bold")),
    ("italic", Icon("lucide:italic")),
    ("underline", Icon("lucide:underline")),
    signal="decoration"
)''',
        title="Editor Controls",
        description="Combine single and multiple selection groups for rich text editing"
    )
    
    # Theme and variant combinations
    yield ComponentPreview(
        Div(
            # Default variant
            Div(
                P("Default Variant", cls="text-sm font-medium mb-3"),
                SingleToggleGroup(
                    ("option1", "Option 1"),
                    ("option2", "Option 2"),
                    ("option3", "Option 3"),
                    variant="default",
                    signal="default_variant"
                ),
                cls="mb-6"
            ),
            
            # Outline variant
            Div(
                P("Outline Variant", cls="text-sm font-medium mb-3"),
                SingleToggleGroup(
                    ("option1", "Option 1"),
                    ("option2", "Option 2"),
                    ("option3", "Option 3"),
                    variant="outline",
                    signal="outline_variant"
                ),
                cls="mb-6"
            ),
            
            # Mixed with icons
            Div(
                P("With Icons", cls="text-sm font-medium mb-3"),
                SingleToggleGroup(
                    ("home", Div(Icon("lucide:home", cls="w-4 h-4"), "Home", cls="flex items-center gap-2")),
                    ("settings", Div(Icon("lucide:settings", cls="w-4 h-4"), "Settings", cls="flex items-center gap-2")),
                    ("profile", Div(Icon("lucide:user", cls="w-4 h-4"), "Profile", cls="flex items-center gap-2")),
                    variant="outline",
                    signal="icon_variant"
                ),
                cls=""
            ),
            
            cls="p-4 border rounded-lg"
        ),
        '''from starui.registry.components.toggle_group import SingleToggleGroup
from starhtml import Icon, Div

# Default variant
SingleToggleGroup(
    ("option1", "Option 1"),
    ("option2", "Option 2"),
    ("option3", "Option 3"),
    variant="default"
)

# Outline variant
SingleToggleGroup(
    ("option1", "Option 1"),
    ("option2", "Option 2"),
    ("option3", "Option 3"),
    variant="outline"
)

# With icons
SingleToggleGroup(
    ("home", Div(Icon("lucide:home"), "Home", cls="flex items-center gap-2")),
    ("settings", Div(Icon("lucide:settings"), "Settings", cls="flex items-center gap-2")),
    ("profile", Div(Icon("lucide:user"), "Profile", cls="flex items-center gap-2")),
    variant="outline"
)''',
        title="Variant Styles",
        description="Different visual styles and combinations with icons"
    )
    
    # Advanced form integration
    yield ComponentPreview(
        Div(
            P("Notification Preferences", cls="font-medium mb-4"),
            
            # Communication methods
            Div(
                Label("Communication Methods:", cls="text-sm font-medium mb-2 block"),
                MultipleToggleGroup(
                    ("email", Div(Icon("lucide:mail", cls="w-4 h-4"), "Email", cls="flex items-center gap-2")),
                    ("sms", Div(Icon("lucide:message-square", cls="w-4 h-4"), "SMS", cls="flex items-center gap-2")),
                    ("push", Div(Icon("lucide:bell", cls="w-4 h-4"), "Push", cls="flex items-center gap-2")),
                    variant="outline",
                    signal="communication_methods"
                ),
                cls="mb-6"
            ),
            
            # Frequency
            Div(
                Label("Notification Frequency:", cls="text-sm font-medium mb-2 block"),
                SingleToggleGroup(
                    ("immediate", "Immediate"),
                    ("daily", "Daily Digest"),
                    ("weekly", "Weekly Summary"),
                    ("never", "Never"),
                    signal="frequency"
                ),
                cls="mb-6"
            ),
            
            # Summary
            Div(
                P("Summary:", cls="text-sm font-medium mb-2"),
                Div(
                    P("Methods: ", ds_text("$communication_methods_value.length > 0 ? $communication_methods_value.join(', ') : 'None'"), 
                      cls="text-sm mb-1"),
                    P("Frequency: ", ds_text("$frequency_value || 'Not set'"), 
                      cls="text-sm"),
                    cls="bg-muted p-3 rounded text-sm"
                ),
                cls=""
            ),
            
            cls="p-4 border rounded-lg max-w-lg"
        ),
        '''from starui.registry.components.toggle_group import SingleToggleGroup, MultipleToggleGroup
from starhtml import Div, Label, P, Icon
from starhtml.datastar import ds_text

# Multiple selection for methods
Label("Communication Methods:")
MultipleToggleGroup(
    ("email", Div(Icon("lucide:mail"), "Email", cls="flex items-center gap-2")),
    ("sms", Div(Icon("lucide:message-square"), "SMS", cls="flex items-center gap-2")),
    ("push", Div(Icon("lucide:bell"), "Push", cls="flex items-center gap-2")),
    variant="outline",
    signal="communication_methods"
)

# Single selection for frequency
Label("Notification Frequency:")
SingleToggleGroup(
    ("immediate", "Immediate"),
    ("daily", "Daily Digest"),
    ("weekly", "Weekly Summary"),
    ("never", "Never"),
    signal="frequency"
)

# Display selections
P("Methods: ", ds_text("$communication_methods_value.join(', ')"))
P("Frequency: ", ds_text("$frequency_value"))''',
        title="Form Integration",
        description="Complex form scenarios with multiple toggle groups and live feedback"
    )
    
    # Disabled states
    yield ComponentPreview(
        Div(
            P("Disabled States", cls="font-medium mb-4"),
            
            # Partially disabled
            Div(
                P("Partially Disabled", cls="text-sm text-muted-foreground mb-2"),
                Div(
                    SingleToggleGroup(
                        ("available", "Available"),
                        ("busy", "Busy"),
                        ("away", "Away"),
                        signal="status_partial"
                    ),
                    Button("Disable", 
                           ds_on_click(toggle_signal("disabled_partial")),
                           variant="outline",
                           size="sm",
                           cls="ml-4"),
                    ds_signals(disabled_partial=False),
                    cls="flex items-center"
                ),
                cls="mb-6"
            ),
            
            # Fully disabled
            Div(
                P("Fully Disabled", cls="text-sm text-muted-foreground mb-2"),
                SingleToggleGroup(
                    ("option1", "Option 1"),
                    ("option2", "Option 2"),
                    ("option3", "Option 3"),
                    disabled=True,
                    variant="outline"
                ),
                cls=""
            ),
            
            cls="p-4 border rounded-lg"
        ),
        '''from starui.registry.components.toggle_group import SingleToggleGroup
from starui.registry.components.button import Button
from starhtml.datastar import ds_on_click, ds_signals

# Interactive disable/enable
Div(
    SingleToggleGroup(
        ("available", "Available"),
        ("busy", "Busy"), 
        ("away", "Away"),
        signal="status"
    ),
    Button("Toggle Disabled", ds_on_click(toggle_signal("disabled"))),
    ds_signals(disabled=False)
)

# Permanently disabled
SingleToggleGroup(
    ("option1", "Option 1"),
    ("option2", "Option 2"),
    ("option3", "Option 3"),
    disabled=True
)''',
        title="Disabled States",
        description="Toggle groups in disabled states for different scenarios"
    )


def create_toggle_group_docs():
    """Create toggle group documentation page using convention-based approach."""
    from utils import auto_generate_page
    
    # Hero example showcasing both single and multiple selection
    hero_example = ComponentPreview(
        Div(
            # Single selection
            Div(
                P("Single Selection", cls="text-sm font-medium mb-2"),
                SingleToggleGroup(
                    ("left", Icon("lucide:align-left", cls="w-4 h-4")),
                    ("center", Icon("lucide:align-center", cls="w-4 h-4")),
                    ("right", Icon("lucide:align-right", cls="w-4 h-4")),
                    variant="outline"
                ),
                cls="mb-6"
            ),
            
            # Multiple selection
            Div(
                P("Multiple Selection", cls="text-sm font-medium mb-2"),
                MultipleToggleGroup(
                    ("bold", Icon("lucide:bold", cls="w-4 h-4")),
                    ("italic", Icon("lucide:italic", cls="w-4 h-4")),
                    ("underline", Icon("lucide:underline", cls="w-4 h-4")),
                    variant="outline"
                ),
                cls=""
            ),
            
            cls="flex flex-col items-center"
        ),
        '''from starui.registry.components.toggle_group import SingleToggleGroup, MultipleToggleGroup
from starhtml import Icon

# Single selection (radio-like behavior)
SingleToggleGroup(
    ("left", Icon("lucide:align-left", cls="w-4 h-4")),
    ("center", Icon("lucide:align-center", cls="w-4 h-4")),
    ("right", Icon("lucide:align-right", cls="w-4 h-4")),
    variant="outline"
)

# Multiple selection (checkbox-like behavior)  
MultipleToggleGroup(
    ("bold", Icon("lucide:bold", cls="w-4 h-4")),
    ("italic", Icon("lucide:italic", cls="w-4 h-4")),
    ("underline", Icon("lucide:underline", cls="w-4 h-4")),
    variant="outline"
)''',
        copy_button=True
    )
    
    api_reference = {
        "components": [
            {
                "name": "ToggleGroup",
                "description": "Base toggle group component supporting both single and multiple selection modes",
                "props": [
                    {
                        "name": "type",
                        "type": "Literal['single', 'multiple']",
                        "default": "'single'",
                        "description": "Selection mode - 'single' allows one selection, 'multiple' allows many"
                    },
                    {
                        "name": "signal",
                        "type": "str",
                        "default": "''",
                        "description": "Datastar signal name for state management"
                    },
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
                        "description": "Size of toggle buttons"
                    },
                    {
                        "name": "disabled",
                        "type": "bool",
                        "default": "False",
                        "description": "Whether the entire group is disabled"
                    }
                ]
            },
            {
                "name": "SingleToggleGroup",
                "description": "Convenience component for single-selection toggle groups (radio-like behavior)",
                "props": [
                    {
                        "name": "signal",
                        "type": "str",
                        "default": "''",
                        "description": "Datastar signal name for state management"
                    },
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
                        "description": "Size of toggle buttons"
                    },
                    {
                        "name": "disabled",
                        "type": "bool",
                        "default": "False",
                        "description": "Whether the group is disabled"
                    }
                ]
            },
            {
                "name": "MultipleToggleGroup", 
                "description": "Convenience component for multiple-selection toggle groups (checkbox-like behavior)",
                "props": [
                    {
                        "name": "signal",
                        "type": "str",
                        "default": "''",
                        "description": "Datastar signal name for state management"
                    },
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
                        "description": "Size of toggle buttons"
                    },
                    {
                        "name": "disabled",
                        "type": "bool",
                        "default": "False",
                        "description": "Whether the group is disabled"
                    }
                ]
            }
        ]
    }
    
    return auto_generate_page(
        TITLE,
        DESCRIPTION,
        list(examples()),
        cli_command="star add toggle-group",
        api_reference=api_reference,
        hero_example=hero_example,
        component_slug="toggle-group"
    )