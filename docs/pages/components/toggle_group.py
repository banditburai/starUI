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

from starhtml import Div, P, H3, H4, Span, Icon, Label, Input, Signal, js
from starui.registry.components.toggle_group import ToggleGroup
from starui.registry.components.button import Button
from starui.registry.components.separator import Separator
from widgets.component_preview import ComponentPreview
from utils import auto_generate_page, with_code, Component, Prop, build_api_reference


# ============================================================================
# EXAMPLE FUNCTIONS (decorated with @with_code for markdown generation)
# ============================================================================

# Text formatting toolbar
@with_code
def text_formatting_toolbar_example():
    return Div(
        P("Text Formatting", cls="font-medium mb-4"),
        ToggleGroup(
            ("bold", Icon("lucide:bold", cls="w-4 h-4")),
            ("italic", Icon("lucide:italic", cls="w-4 h-4")),
            ("underline", Icon("lucide:underline", cls="w-4 h-4")),
            ("strikethrough", Icon("lucide:strikethrough", cls="w-4 h-4")),
            type="single",
            variant="outline",
            signal="formatting"
        ),
        Div(
            P("Selected format: ", cls="text-sm inline"),
            Span(data_text=js("$formatting_value || 'None'"), cls="font-mono text-sm bg-muted px-2 py-1 rounded"),
            cls="mt-4"
        ),
        cls="p-4 border rounded-lg"
    )


# View switcher
@with_code
def view_mode_switcher_example():
    return Div(
        P("View Mode", cls="font-medium mb-4"),
        ToggleGroup(
            ("grid", Div(Icon("lucide:grid-3x3", cls="w-4 h-4"), "Grid", cls="flex items-center gap-2")),
            ("list", Div(Icon("lucide:list", cls="w-4 h-4"), "List", cls="flex items-center gap-2")),
            ("card", Div(Icon("lucide:layout-grid", cls="w-4 h-4"), "Card", cls="flex items-center gap-2")),
            type="single",
            signal="view_mode",
            default_value="grid"
        ),

        # Content area that changes based on selection
        Div(
            # Grid view
            Div(
                Div("Item 1", cls="p-4 border rounded bg-muted"),
                Div("Item 2", cls="p-4 border rounded bg-muted"),
                Div("Item 3", cls="p-4 border rounded bg-muted"),
                Div("Item 4", cls="p-4 border rounded bg-muted"),
                cls="grid grid-cols-2 gap-2",
                data_show=js("$view_mode_value === 'grid'")
            ),

            # List view
            Div(
                Div("Item 1", cls="p-3 border rounded bg-muted mb-2"),
                Div("Item 2", cls="p-3 border rounded bg-muted mb-2"),
                Div("Item 3", cls="p-3 border rounded bg-muted mb-2"),
                Div("Item 4", cls="p-3 border rounded bg-muted"),
                cls="",
                data_show=js("$view_mode_value === 'list'")
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
                cls="",
                data_show=js("$view_mode_value === 'card'")
            ),

            cls="mt-6 min-h-[200px]"
        ),

        cls="p-4 border rounded-lg"
    )


# Multi-select filter options
@with_code
def multi_select_filters_example():
    return Div(
        P("Filter Options", cls="font-medium mb-4"),
        ToggleGroup(
            ("featured", Div(Icon("lucide:star", cls="w-4 h-4"), "Featured", cls="flex items-center gap-2")),
            ("sale", Div(Icon("lucide:percent", cls="w-4 h-4"), "On Sale", cls="flex items-center gap-2")),
            ("new", Div(Icon("lucide:sparkles", cls="w-4 h-4"), "New", cls="flex items-center gap-2")),
            ("popular", Div(Icon("lucide:trending-up", cls="w-4 h-4"), "Popular", cls="flex items-center gap-2")),
            type="multiple",
            variant="outline",
            signal="filters"
        ),

        # Show selected filters
        Div(
            P("Active Filters:", cls="text-sm font-medium mb-2"),
            Div(
                data_text=js("$filters_value.length > 0 ? $filters_value.join(', ') : 'None selected'"),
                cls="text-sm bg-muted p-3 rounded font-mono"
            ),
            cls="mt-6"
        ),

        cls="p-4 border rounded-lg"
    )


# Size variations
@with_code
def size_variations_example():
    return Div(
        # Small size
        Div(
            P("Small", cls="text-sm font-medium mb-3"),
            ToggleGroup(
                ("sm1", "One"),
                ("sm2", "Two"),
                ("sm3", "Three"),
                type="single",
                size="sm",
                signal="small_group"
            ),
            cls="mb-6"
        ),

        # Default size
        Div(
            P("Default", cls="text-sm font-medium mb-3"),
            ToggleGroup(
                ("def1", "One"),
                ("def2", "Two"),
                ("def3", "Three"),
                type="single",
                signal="default_group"
            ),
            cls="mb-6"
        ),

        # Large size
        Div(
            P("Large", cls="text-sm font-medium mb-3"),
            ToggleGroup(
                ("lg1", "One"),
                ("lg2", "Two"),
                ("lg3", "Three"),
                type="single",
                size="lg",
                signal="large_group"
            ),
            cls=""
        ),

        cls="p-4 border rounded-lg"
    )


# Alignment and justification controls
@with_code
def editor_controls_example():
    return Div(
        P("Text Alignment", cls="font-medium mb-4"),
        ToggleGroup(
            ("left", Icon("lucide:align-left", cls="w-4 h-4")),
            ("center", Icon("lucide:align-center", cls="w-4 h-4")),
            ("right", Icon("lucide:align-right", cls="w-4 h-4")),
            ("justify", Icon("lucide:align-justify", cls="w-4 h-4")),
            type="single",
            variant="outline",
            signal="alignment"
        ),

        Separator(cls="my-6"),

        P("Text Decoration", cls="font-medium mb-4"),
        ToggleGroup(
            ("bold", Icon("lucide:bold", cls="w-4 h-4")),
            ("italic", Icon("lucide:italic", cls="w-4 h-4")),
            ("underline", Icon("lucide:underline", cls="w-4 h-4")),
            type="multiple",
            signal="decoration"
        ),

        # Preview area
        Div(
            P(
                "The quick brown fox jumps over the lazy dog. This sample text demonstrates the selected text alignment and decoration options.",
                cls="p-4 bg-muted rounded transition-all",
                data_class=js("""
                    {
                        'text-left': $alignment_value === 'left' || !$alignment_value,
                        'text-center': $alignment_value === 'center',
                        'text-right': $alignment_value === 'right',
                        'text-justify': $alignment_value === 'justify',
                        'font-bold': $decoration_value && $decoration_value.includes('bold'),
                        'italic': $decoration_value && $decoration_value.includes('italic'),
                        'underline': $decoration_value && $decoration_value.includes('underline')
                    }
                """)
            ),
            cls="mt-6"
        ),

        cls="p-4 border rounded-lg"
    )


# Theme and variant combinations
@with_code
def variant_styles_example():
    return Div(
        # Default variant
        Div(
            P("Default Variant", cls="text-sm font-medium mb-3"),
            ToggleGroup(
                ("option1", "Option 1"),
                ("option2", "Option 2"),
                ("option3", "Option 3"),
                type="single",
                variant="default",
                signal="default_variant"
            ),
            cls="mb-6"
        ),

        # Outline variant
        Div(
            P("Outline Variant", cls="text-sm font-medium mb-3"),
            ToggleGroup(
                ("option1", "Option 1"),
                ("option2", "Option 2"),
                ("option3", "Option 3"),
                type="single",
                variant="outline",
                signal="outline_variant"
            ),
            cls="mb-6"
        ),

        # Mixed with icons
        Div(
            P("With Icons", cls="text-sm font-medium mb-3"),
            ToggleGroup(
                ("home", Div(Icon("lucide:home", cls="w-4 h-4"), "Home", cls="flex items-center gap-2")),
                ("settings", Div(Icon("lucide:settings", cls="w-4 h-4"), "Settings", cls="flex items-center gap-2")),
                ("profile", Div(Icon("lucide:user", cls="w-4 h-4"), "Profile", cls="flex items-center gap-2")),
                type="single",
                variant="outline",
                signal="icon_variant"
            ),
            cls=""
        ),

        cls="p-4 border rounded-lg"
    )


# Advanced form integration
@with_code
def form_integration_example():
    return Div(
        P("Notification Preferences", cls="font-medium mb-4"),

        # Communication methods
        Div(
            Label("Communication Methods:", cls="text-sm font-medium mb-2 block"),
            ToggleGroup(
                ("email", Div(Icon("lucide:mail", cls="w-4 h-4"), "Email", cls="flex items-center gap-2")),
                ("sms", Div(Icon("lucide:message-square", cls="w-4 h-4"), "SMS", cls="flex items-center gap-2")),
                ("push", Div(Icon("lucide:bell", cls="w-4 h-4"), "Push", cls="flex items-center gap-2")),
                type="multiple",
                variant="outline",
                signal="communication_methods"
            ),
            cls="mb-6"
        ),

        # Frequency
        Div(
            Label("Notification Frequency:", cls="text-sm font-medium mb-2 block"),
            ToggleGroup(
                ("immediate", "Immediate"),
                ("daily", "Daily Digest"),
                ("weekly", "Weekly Summary"),
                ("never", "Never"),
                type="single",
                signal="frequency"
            ),
            cls="mb-6"
        ),

        # Summary
        Div(
            P("Summary:", cls="text-sm font-medium mb-2"),
            Div(
                P("Methods: ", data_text=js("$communication_methods_value.length > 0 ? $communication_methods_value.join(', ') : 'None'"),
                  cls="text-sm mb-1"),
                P("Frequency: ", data_text=js("$frequency_value || 'Not set'"),
                  cls="text-sm"),
                cls="bg-muted p-3 rounded text-sm"
            ),
            cls=""
        ),

        cls="p-4 border rounded-lg max-w-lg"
    )


# Disabled states
@with_code
def disabled_states_example():
    disabled_partial = Signal("disabled_partial", False)

    return Div(
        P("Disabled States", cls="font-medium mb-4"),

        # Dynamic disabling
        Div(
            P("Dynamic Disabling", cls="text-sm text-muted-foreground mb-2"),
            Div(
                disabled_partial,
                ToggleGroup(
                    ("available", "Available"),
                    ("busy", "Busy"),
                    ("away", "Away"),
                    type="single",
                    slot_attrs={"toggle_group_item": {"data-attr-disabled": "$disabled_partial"}}
                ),
                Button(
                    data_text=js("$disabled_partial ? 'Enable' : 'Disable'"),
                    variant="outline",
                    size="sm",
                    cls="ml-4",
                    data_on_click=js("$disabled_partial = !$disabled_partial")
                ),
                cls="flex items-center"
            ),
            cls="mb-6"
        ),

        # Fully disabled
        Div(
            P("Fully Disabled", cls="text-sm text-muted-foreground mb-2"),
            ToggleGroup(
                ("option1", "Option 1"),
                ("option2", "Option 2"),
                ("option3", "Option 3"),
                type="single",
                disabled=True,
                variant="outline"
            ),
            cls=""
        ),

        cls="p-4 border rounded-lg"
    )


# ============================================================================
# MODULE-LEVEL DATA (for markdown API)
# ============================================================================

EXAMPLES_DATA = [
    {"title": "Text Formatting Toolbar", "description": "Single-selection toggle group for text formatting options", "fn": text_formatting_toolbar_example},
    {"title": "View Mode Switcher", "description": "Toggle between different content layouts with dynamic content display", "fn": view_mode_switcher_example},
    {"title": "Multi-Select Filters", "description": "Multiple selection toggle group for filtering options", "fn": multi_select_filters_example},
    {"title": "Size Variations", "description": "Toggle groups in different sizes for various use cases", "fn": size_variations_example},
    {"title": "Editor Controls", "description": "Combine single and multiple selection groups for rich text editing", "fn": editor_controls_example},
    {"title": "Variant Styles", "description": "Different visual styles and combinations with icons", "fn": variant_styles_example},
    {"title": "Form Integration", "description": "Complex form scenarios with multiple toggle groups and live feedback", "fn": form_integration_example},
    {"title": "Disabled States", "description": "Toggle groups in disabled states for different scenarios", "fn": disabled_states_example},
]

API_REFERENCE = build_api_reference(
    components=[
        Component(
            name="ToggleGroup",
            description=(
                "A toggle group with single or multiple selection. Pass items as (value, content) tuples. "
                "Selection is exposed as `{signal}_value` (str for single, list[str] for multiple)."
            ),
            props=[
                Prop("type", "Literal['single','multiple']", "Selection mode", "'single'"),
                Prop("signal", "str | None", "Datastar signal prefix; autogenerated when None", "None"),
                Prop("initial_value", "str | list[str] | None", "Initial selection value(s)", "None"),
                Prop("variant", "Literal['default','outline']", "Visual style", "'default'"),
                Prop("size", "Literal['default','sm','lg']", "Button size", "'default'"),
                Prop("disabled", "bool", "Disable all items", "False"),
                Prop("cls", "str", "Additional CSS classes", "''"),
            ],
        ),
    ]
)


def examples():
    """Generate all toggle group examples."""
    yield ComponentPreview(
        text_formatting_toolbar_example(),
        text_formatting_toolbar_example.code,
        title="Text Formatting Toolbar",
        description="Single-selection toggle group for text formatting options"
    )

    yield ComponentPreview(
        view_mode_switcher_example(),
        view_mode_switcher_example.code,
        title="View Mode Switcher",
        description="Toggle between different content layouts with dynamic content display"
    )

    yield ComponentPreview(
        multi_select_filters_example(),
        multi_select_filters_example.code,
        title="Multi-Select Filters",
        description="Multiple selection toggle group for filtering options"
    )

    yield ComponentPreview(
        size_variations_example(),
        size_variations_example.code,
        title="Size Variations",
        description="Toggle groups in different sizes for various use cases"
    )

    yield ComponentPreview(
        editor_controls_example(),
        editor_controls_example.code,
        title="Editor Controls",
        description="Combine single and multiple selection groups for rich text editing"
    )

    yield ComponentPreview(
        variant_styles_example(),
        variant_styles_example.code,
        title="Variant Styles",
        description="Different visual styles and combinations with icons"
    )

    yield ComponentPreview(
        form_integration_example(),
        form_integration_example.code,
        title="Form Integration",
        description="Complex form scenarios with multiple toggle groups and live feedback"
    )

    yield ComponentPreview(
        disabled_states_example(),
        disabled_states_example.code,
        title="Disabled States",
        description="Toggle groups in disabled states for different scenarios"
    )


def create_toggle_group_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)