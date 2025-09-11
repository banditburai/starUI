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
from utils import auto_generate_page, with_code, Component, Prop, build_api_reference


def examples():
    """Generate toggle group examples using ComponentPreview with tabs."""
    
    # Text formatting toolbar
    @with_code
    def text_formatting_toolbar_example():
        return Div(
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
        )

    yield ComponentPreview(
        text_formatting_toolbar_example(),
        text_formatting_toolbar_example.code,
        title="Text Formatting Toolbar",
        description="Single-selection toggle group for text formatting options"
    )
    
    # View switcher
    @with_code
    def view_mode_switcher_example():
        return Div(
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
        )

    yield ComponentPreview(
        view_mode_switcher_example(),
        view_mode_switcher_example.code,
        title="View Mode Switcher",
        description="Toggle between different content layouts with dynamic content display"
    )
    
    # Multi-select filter options
    @with_code
    def multi_select_filters_example():
        return Div(
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
        )

    yield ComponentPreview(
        multi_select_filters_example(),
        multi_select_filters_example.code,
        title="Multi-Select Filters",
        description="Multiple selection toggle group for filtering options"
    )
    
    # Size variations
    @with_code
    def size_variations_example():
        return Div(
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
        )

    yield ComponentPreview(
        size_variations_example(),
        size_variations_example.code,
        title="Size Variations",
        description="Toggle groups in different sizes for various use cases"
    )
    
    # Alignment and justification controls
    @with_code
    def editor_controls_example():
        return Div(
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
        )

    yield ComponentPreview(
        editor_controls_example(),
        editor_controls_example.code,
        title="Editor Controls",
        description="Combine single and multiple selection groups for rich text editing"
    )
    
    # Theme and variant combinations
    @with_code
    def variant_styles_example():
        return Div(
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
        )

    yield ComponentPreview(
        variant_styles_example(),
        variant_styles_example.code,
        title="Variant Styles",
        description="Different visual styles and combinations with icons"
    )
    
    # Advanced form integration
    @with_code
    def form_integration_example():
        return Div(
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
        )

    yield ComponentPreview(
        form_integration_example(),
        form_integration_example.code,
        title="Form Integration",
        description="Complex form scenarios with multiple toggle groups and live feedback"
    )
    
    # Disabled states
    @with_code
    def disabled_states_example():
        return Div(
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
        )

    yield ComponentPreview(
        disabled_states_example(),
        disabled_states_example.code,
        title="Disabled States",
        description="Toggle groups in disabled states for different scenarios"
    )


def create_toggle_group_docs():
    """Create toggle group documentation page using convention-based approach."""
    
    # Hero example showcasing both single and multiple selection
    @with_code
    def hero_toggle_group_example():
        return Div(
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
        )

    hero_example = ComponentPreview(
        hero_toggle_group_example(),
        hero_toggle_group_example.code,
        copy_button=True
    )
    
    api_reference = build_api_reference(
        components=[
            Component(
                name="SingleToggleGroup",
                description=(
                    "Single-select group (radio-like). Pass items as (value, content) tuples. "
                    "Current selection is exposed as `{signal}_value` (str)."
                ),
                props=[
                    Prop("signal", "str", "Datastar signal for the group", "''"),
                    Prop("variant", "Literal['default','outline']", "Visual style", "'default'"),
                    Prop("size", "Literal['default','sm','lg']", "Button size", "'default'"),
                    Prop("disabled", "bool", "Disable all items", "False"),
                    Prop("cls", "str", "Additional CSS classes", "''"),
                ],
            ),
            Component(
                name="MultipleToggleGroup",
                description=(
                    "Multi-select group (checkbox-like). Pass items as (value, content) tuples. "
                    "Selections are exposed as `{signal}_value` (list[str])."
                ),
                props=[
                    Prop("signal", "str", "Datastar signal for the group", "''"),
                    Prop("variant", "Literal['default','outline']", "Visual style", "'default'"),
                    Prop("size", "Literal['default','sm','lg']", "Button size", "'default'"),
                    Prop("disabled", "bool", "Disable all items", "False"),
                    Prop("cls", "str", "Additional CSS classes", "''"),
                ],
            ),
        ]
    )
    
    return auto_generate_page(
        TITLE,
        DESCRIPTION,
        list(examples()),
        cli_command="star add toggle-group",
        api_reference=api_reference,
        hero_example=hero_example,
        component_slug="toggle-group"
    )