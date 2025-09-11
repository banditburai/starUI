"""
Button component documentation - Convention-based functional approach.
Clean, minimal, and easy to extend.
"""

# Component metadata for auto-discovery
TITLE = "Button"
DESCRIPTION = "Displays a button or a component that looks like a button."
CATEGORY = "ui"
ORDER = 10
STATUS = "stable"

from starhtml import Div, P, Input, Label, Icon, Span, H2, H3
from starhtml.datastar import (
    ds_on_click, ds_show, ds_text, ds_signals, value,
    ds_bind, ds_disabled, ds_on_mouseenter, ds_on_mouseleave, ds_style, toggle_signal
)
from starui.registry.components.button import Button
from utils import auto_generate_page, Prop, build_api_reference, with_code
from widgets.component_preview import ComponentPreview


def examples():
    """Generate button examples using ComponentPreview with tabs."""
    
    # Sizes
    @with_code
    def button_sizes_example():
        return Div(
            Button("Small", size="sm", cls="mr-2"),
            Button("Default", cls="mr-2"),
            Button("Large", size="lg", cls="mr-2"),
            Button(Icon("lucide:chevron-right", cls="h-4 w-4"), variant="outline", size="icon"),
            cls="flex items-center gap-2"
        )
    
    yield ComponentPreview(
        button_sizes_example(),
        button_sizes_example.code,
        title="Button Sizes",
        description="Different sizes including icon-only buttons"
    )
    
    # With icons
    @with_code
    def buttons_with_icons_example():
        return Div(
            Button(Icon("lucide:mail", cls="mr-2 h-4 w-4"), "Login with Email", cls="mr-2"),
            Button(Icon("lucide:loader-2", cls="mr-2 h-4 w-4 animate-spin"), "Please wait", disabled=True),
            cls="flex gap-2"
        )
    
    yield ComponentPreview(
        buttons_with_icons_example(),
        buttons_with_icons_example.code,
        title="Buttons with Icons",
        description="Buttons enhanced with icons for better UX"
    )
    
    # Interactive examples with Datastar
    @with_code
    def interactive_counter_example():
        return Div(
            Button("Click me!", ds_on_click("$count++")),
            P("Clicked: ", Span(ds_text("$count"), cls="font-bold text-blue-600")),
            ds_signals(count=0),
            cls="flex flex-col items-center gap-4"
        )
    
    yield ComponentPreview(
        interactive_counter_example(),
        interactive_counter_example.code,
        title="Interactive Counter",
        description="Button that updates state on click"
    )
    
    @with_code
    def toggle_visibility_example():
        return Div(
            Button(
                ds_text("$expanded ? 'Hide Details' : 'Show Details'"),
                ds_on_click(toggle_signal("expanded")),
                variant="outline"
            ),
            Div(
                Div(
                    P("✨ Here are some additional details!", cls="font-medium"),
                    P("This content smoothly fades in and out.", cls="text-sm text-muted-foreground"),
                    ds_show("$expanded"),
                    cls="transition-all duration-300 ease-in-out"
                ),
                cls="mt-4 min-h-[60px] flex items-center justify-center"
            ),
            ds_signals(expanded=False),
            cls="w-full max-w-sm mx-auto text-center"
        )
    
    yield ComponentPreview(
        toggle_visibility_example(),
        toggle_visibility_example.code,
        title="Toggle Visibility",
        description="Show/hide content with smooth transitions and dynamic button text"
    )
    
    @with_code
    def form_integration_example():
        return Div(
            Div(
                Label("Name:", cls="block text-sm font-medium mb-1"),
                Input(
                    signal="name",
                    type="text",
                    placeholder="Enter your name",                
                    cls="w-full px-3 py-2 border rounded-md"
                ),
                cls="mb-4"
            ),
            Button(
                "Submit",
                ds_disabled("$name == ''"),
                ds_on_click("alert(`Hello ${$name}!`)"),
            ),
            P("Button is disabled until you enter a name", cls="text-sm text-gray-600 mt-2"),
            ds_signals(name=value("")),
            cls="w-full max-w-sm mx-auto"
        )
    
    yield ComponentPreview(
        form_integration_example(),
        form_integration_example.code,
        title="Form Integration",
        description="Button state controlled by form input"
    )


def create_button_docs():
    """Create button documentation page using convention-based approach."""
    from utils import auto_generate_page
    
    api_reference = build_api_reference(
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
    
    # Hero example to show at the top
    @with_code
    def hero_button_example():
        return Div(
            Button("Default", cls="mr-2"),
            Button("Secondary", variant="secondary", cls="mr-2"),
            Button("Destructive", variant="destructive", cls="mr-2"),
            Button("Outline", variant="outline", cls="mr-2"),
            Button("Ghost", variant="ghost", cls="mr-2"),
            Button("Link", variant="link"),
            cls="flex flex-wrap gap-2 justify-center"
        )
    
    hero_example = ComponentPreview(
        hero_button_example(),
        hero_button_example.code,
        copy_button=True
    )
    
    return auto_generate_page(
        TITLE,
        DESCRIPTION,
        list(examples()),
        cli_command="star add button", 
        api_reference=api_reference,
        hero_example=hero_example,
        component_slug="button"
    )