"""
Input component documentation - Form input fields with styling.
"""

# Component metadata for auto-discovery
TITLE = "Input"
DESCRIPTION = "Displays a form input field or a component that looks like an input field."
CATEGORY = "form"
ORDER = 10
STATUS = "stable"

from starhtml import Div, P, Label, Span, Icon
from starhtml.datastar import ds_signals, ds_show, value
from starui.registry.components.input import Input
from starui.registry.components.button import Button
from starui.registry.components.label import Label as UILabel
from utils import auto_generate_page, with_code, Prop, build_api_reference
from widgets.component_preview import ComponentPreview


def examples():
    
    # Input types
    @with_code
    def input_types_example():
        return Div(
            Div(
                UILabel("Email", for_="email"),
                Input(type="email", id="email", placeholder="you@example.com", cls="w-80"),
                cls="space-y-2"
            ),
            Div(
                UILabel("Password", for_="password"),
                Input(type="password", id="password", placeholder="Enter your password", cls="w-80"),
                cls="space-y-2"
            ),
            Div(
                UILabel("Phone Number", for_="phone"),
                Input(type="tel", id="phone", placeholder="+1 (555) 123-4567", cls="w-80"),
                cls="space-y-2"
            ),
            cls="grid gap-4 max-w-md"
        )

    yield ComponentPreview(
        input_types_example(),
        input_types_example.code,
        title="Input Types",
        description="Different input types for various data"
    )
    
    @with_code
    def reactive_input_validation_example():
        def create_validation_messages(signal_name, invalid_message, valid_message):
            return Div(
                P(
                    ds_show(f"!${signal_name}_valid && ${signal_name}.length > 0"),
                    invalid_message,
                    cls="text-xs text-destructive break-words"
                ),
                P(
                    ds_show(f"${signal_name}_valid && ${signal_name}.length > 0"),
                    valid_message,
                    cls="text-xs text-green-600"
                ),
                cls="mt-1 min-h-[1rem] w-80"
            )
        
        return Div(
            Div(
                UILabel(
                    "Username", 
                    Span(" *", cls="text-destructive"),
                    for_="username-reactive"
                ),
                Input(
                    id="username-reactive",
                    placeholder="Enter username",
                    signal="username",
                    validation="/^[a-zA-Z0-9_]{3,}$/.test($signal)",
                    cls="w-80"
                ),
                create_validation_messages(
                    "username",
                    "Username must be at least 3 characters, letters/numbers/underscores only",
                    "✓ Username is available"
                ),
                cls="space-y-2"
            ),
            Div(
                UILabel("Email", for_="email-reactive"),
                Input(
                    type="email",
                    id="email-reactive", 
                    placeholder="you@example.com",
                    signal="user_email",
                    validation="/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test($signal)",
                    cls="w-80"
                ),
                create_validation_messages(
                    "user_email",
                    "Please enter a valid email address",
                    "✓ Valid email format"
                ),
                cls="space-y-2"
            ),
            ds_signals(username=value(""), username_valid=False, user_email=value(""), user_email_valid=False),
            cls="grid gap-4 max-w-md"
        )

    yield ComponentPreview(
        reactive_input_validation_example(),
        reactive_input_validation_example.code,
        title="Reactive Input with Validation",
        description="Real-time input validation using signals"
    )
    
    # Input with button
    @with_code
    def input_with_buttons_example():
        return Div(
            Div(
                UILabel("Subscribe to Newsletter", for_="newsletter"),
                Div(
                    Input(type="email", id="newsletter", placeholder="Enter your email", cls="w-80"),
                    Button("Subscribe"),
                    cls="flex gap-2 items-center"
                ),
                cls="space-y-2"
            ),
            Div(
                UILabel("Search", for_="search"),
                Div(
                    Input(type="search", id="search", placeholder="Search products...", cls="w-80"),
                    Button("Search", variant="outline"),
                    cls="flex gap-2 items-center"
                ),
                cls="space-y-2"
            ),
            cls="grid gap-4 max-w-md"
        )

    yield ComponentPreview(
        input_with_buttons_example(),
        input_with_buttons_example.code,
        title="Input with Buttons",
        description="Combine inputs with action buttons"
    )
    
    @with_code
    def inputs_with_icons_example():
        inputs_with_icons = [
            ("quantity", "Quantity", "lucide:hash", "number", "Enter quantity", {"min": 1, "max": 99, "step": 1}),
            ("dob", "Date of Birth", "lucide:calendar", "text", "MM/DD/YYYY", {}),
            ("time", "Appointment Time", "lucide:clock", "text", "HH:MM", {}),
            ("website", "Website", "lucide:globe", "url", "https://example.com", {})
        ]
        
        def create_input_with_icon(field_id, label, icon, input_type, placeholder, extra_props):
            return Div(
                UILabel(label, for_=field_id),
                Div(
                    Icon(icon, width="16", height="16", cls="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground pointer-events-none"),
                    Input(type=input_type, id=field_id, placeholder=placeholder, cls="pl-10 w-80", **extra_props),
                    cls="relative"
                ),
                cls="space-y-2"
            )
        
        return Div(
            *[create_input_with_icon(field_id, label, icon, input_type, placeholder, extra_props)
              for field_id, label, icon, input_type, placeholder, extra_props in inputs_with_icons],
            cls="grid gap-4 max-w-md"
        )

    yield ComponentPreview(
        inputs_with_icons_example(),
        inputs_with_icons_example.code,
        title="Input with Icons",
        description="Inputs with custom icons that adapt to dark mode"
    )
    
    # Input states
    @with_code
    def input_states_example():
        return Div(
            Div(
                UILabel("Disabled Input", for_="disabled", cls="opacity-50"),
                Input(id="disabled", placeholder="This field is disabled", disabled=True, cls="w-80"),
                cls="space-y-2"
            ),
            Div(
                UILabel("Read-only Input", for_="readonly"),
                Input(id="readonly", value="This value cannot be changed", readonly=True, cls="w-80"),
                cls="space-y-2"
            ),
            Div(
                UILabel(
                    "Required Field",
                    Span(" *", cls="text-destructive"),
                    for_="required"
                ),
                Input(id="required", placeholder="This field is required", required=True, cls="w-80"),
                P("This field is required", cls="text-xs text-muted-foreground"),
                cls="space-y-2"
            ),
            cls="grid gap-4 max-w-md"
        )

    yield ComponentPreview(
        input_states_example(),
        input_states_example.code,
        title="Input States",
        description="Disabled, read-only, and required inputs"
    )
    
    # File upload
    @with_code
    def file_upload_inputs_example():
        return Div(
            Div(
                UILabel("Profile Picture", for_="avatar"),
                Input(type="file", id="avatar", accept="image/*", cls="w-80"),
                P("PNG, JPG up to 2MB", cls="text-xs text-muted-foreground"),
                cls="space-y-2"
            ),
            Div(
                UILabel("Document Upload", for_="docs"),
                Input(type="file", id="docs", accept=".pdf,.doc,.docx", multiple=True, cls="w-80"),
                P("PDF, DOC, DOCX files", cls="text-xs text-muted-foreground"),
                cls="space-y-2"
            ),
            cls="grid gap-4 max-w-md"
        )

    yield ComponentPreview(
        file_upload_inputs_example(),
        file_upload_inputs_example.code,
        title="File Upload",
        description="File input fields with accept filters"
    )
    
    # Form layout
    @with_code
    def complete_form_example():
        return Div(
            Div(
                UILabel("First Name", for_="first"),
                Input(id="first", placeholder="John", cls="w-80"),
                cls="space-y-2"
            ),
            Div(
                UILabel("Last Name", for_="last"),
                Input(id="last", placeholder="Doe", cls="w-80"),
                cls="space-y-2"
            ),
            Div(
                UILabel("Email Address", for_="email-form"),
                Input(type="email", id="email-form", placeholder="john.doe@example.com", cls="w-80"),
                cls="space-y-2"
            ),
            Div(
                UILabel("Message", for_="message"),
                Input(id="message", placeholder="Tell us about your project...", cls="w-80"),
                cls="space-y-2"
            ),
            Div(
                Button("Submit Form", cls="w-full"),
                cls="pt-2"
            ),
            cls="space-y-4 max-w-md"
        )

    yield ComponentPreview(
        complete_form_example(),
        complete_form_example.code,
        title="Complete Form",
        description="Multiple inputs in a form layout"
    )


def create_input_docs():
    
    # Intentional API: focus on the props users set most when adding inputs
    api_reference = build_api_reference(
        main_props=[
            Prop("type", "InputType", "Input type (text, email, password, number, etc.)", "text"),
            Prop("placeholder", "str | None", "Placeholder text shown when empty", "None"),
            Prop("signal", "str | None", "Datastar signal for reactive binding", "None"),
            Prop("validation", "str | None", "JS expression to set <signal>_valid on input", "None"),
            Prop("value", "str | None", "Initial value for non-reactive usage", "None"),
            Prop("disabled", "bool", "Disable the input and style accordingly", "False"),
            Prop("readonly", "bool", "Make input read-only without disabling", "False"),
            Prop("required", "bool", "Mark the input as required", "False"),
            Prop("cls", "str", "Additional CSS classes for layout/styling", "''"),
        ]
    )

    # Hero example - basic input showcase
    @with_code
    def hero_input_example():
        return Div(
            Input(placeholder="Enter text...", cls="mb-3 w-80"),
            Input(type="email", placeholder="you@example.com", cls="mb-3 w-80"),
            Input(type="password", placeholder="Enter your password", cls="w-80"),
            cls="grid gap-3 max-w-sm"
        )

    hero_example = ComponentPreview(
        hero_input_example(),
        hero_input_example.code,
        copy_button=True
    )
    
    return auto_generate_page(
        TITLE,
        DESCRIPTION,
        list(examples()),
        cli_command="star add input",
        hero_example=hero_example,
        component_slug="input",
        api_reference=api_reference
    )