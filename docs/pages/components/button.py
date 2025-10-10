TITLE = "Button"
DESCRIPTION = "Displays a button or a component that looks like a button."
CATEGORY = "ui"
ORDER = 10
STATUS = "stable"

from starhtml import Div, P, Input, Label, Icon, Span, Signal
from starui.registry.components.button import Button
from utils import auto_generate_page, Prop, build_api_reference, with_code
from widgets.component_preview import ComponentPreview


# ============================================================================
# EXAMPLE FUNCTIONS (decorated with @with_code for markdown generation)
# ============================================================================

@with_code
def button_sizes_example():
    return Div(
        Button("Small", size="sm"),
        Button("Default"),
        Button("Large", size="lg"),
        Button(Icon("lucide:chevron-right", cls="h-4 w-4"), variant="outline", size="icon"),
        cls="flex items-center gap-2"
    )


@with_code
def buttons_with_icons_example():
    return Div(
        Button(Icon("lucide:mail", cls="mr-2 h-4 w-4"), "Login with Email"),
        Button(Icon("lucide:loader-2", cls="mr-2 h-4 w-4 animate-spin"), "Please wait", disabled=True),
        cls="flex gap-2"
    )


@with_code
def interactive_counter_example():
    return Div(
        (count := Signal("count", 0)),
        Button("Click me!", data_on_click=count.add(1)),
        P("Clicked: ", Span(data_text=count, cls="font-bold text-blue-600")),
        cls="flex flex-col items-center gap-4"
    )


@with_code
def toggle_visibility_example():
    return Div(
        (expanded := Signal("expanded", False)),
        Button(
            data_text=expanded.if_("Hide Details", "Show Details"),
            data_on_click=expanded.toggle(),
            variant="outline"
        ),
        Div(
            Div(
                P("✨ Here are some additional details!", cls="font-medium"),
                P("This content smoothly fades in and out.", cls="text-sm text-muted-foreground"),
                data_show=expanded,
                cls="transition-all duration-300 ease-in-out"
            ),
            cls="mt-4 min-h-[60px] flex items-center justify-center"
        ),
        cls="w-full max-w-sm mx-auto text-center"
    )


@with_code
def form_integration_example():
    return Div(
        (name := Signal("name", "")),
        Div(
            Label("Name:", cls="block text-sm font-medium mb-1"),
            Input(
                data_bind=name,
                type="text",
                placeholder="Enter your name",
                cls="w-full px-3 py-2 border rounded-md"
            ),
            cls="mb-4"
        ),
        Button(
            "Submit",
            data_attr_disabled=name.eq(""),
            data_on_click="alert(`Hello ${$name}!`)"
        ),
        P("Button is disabled until you enter a name", cls="text-sm text-gray-600 mt-2"),
        cls="w-full max-w-sm mx-auto"
    )


# ============================================================================
# EXAMPLES GENERATOR (for rendering on the page)
# ============================================================================

# ============================================================================
# API REFERENCE
# ============================================================================

API_REFERENCE = build_api_reference(
    main_props=[
        Prop("variant", "Literal['default', 'secondary', 'destructive', 'outline', 'ghost', 'link']",
             "Button visual variant", "'default'"),
        Prop("size", "Literal['default', 'sm', 'lg', 'icon']",
             "Button size", "'default'"),
        Prop("disabled", "bool",
             "Whether button is disabled", "False"),
        Prop("cls", "str",
             "Additional CSS classes", "''"),
    ]
)


# ============================================================================
# EXAMPLES DATA (for markdown generation with code)
# ============================================================================

EXAMPLES_DATA = [
    {"title": "Button Sizes", "description": "Different sizes including icon-only buttons", "fn": button_sizes_example},
    {"title": "Buttons with Icons", "description": "Buttons enhanced with icons for better UX", "fn": buttons_with_icons_example},
    {"title": "Interactive Counter", "description": "Button that updates state on click", "fn": interactive_counter_example},
    {"title": "Toggle Visibility", "description": "Show/hide content with smooth transitions and dynamic button text", "fn": toggle_visibility_example},
    {"title": "Form Integration", "description": "Button state controlled by form input", "fn": form_integration_example},
]


# ============================================================================
# DOCS PAGE
# ============================================================================


@with_code
def hero_button_example():
    return Div(
        Button("Default"),
        Button("Secondary", variant="secondary"),
        Button("Destructive", variant="destructive"),
        Button("Outline", variant="outline"),
        Button("Ghost", variant="ghost"),
        Button("Link", variant="link"),
        cls="flex flex-wrap gap-2 justify-center"
    )


def create_button_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)