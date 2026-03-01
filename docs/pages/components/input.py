"""
Input component documentation - Form input fields with styling.
"""

# Component metadata for auto-discovery
TITLE = "Input"
DESCRIPTION = "Displays a form input field or a component that looks like an input field."
CATEGORY = "form"
ORDER = 10
STATUS = "stable"

from starhtml import Div, P, Span, Icon, Signal, regex, js
from starui.registry.components.input import Input
from starui.registry.components.button import Button
from starui.registry.components.label import Label as UILabel
from utils import auto_generate_page, with_code, Prop, build_api_reference



@with_code
def default_example():
    return Div(
        UILabel("Email", fr="email"),
        Input(type="email", id="email", placeholder="you@example.com"),
        P("Enter your email address.", cls="text-xs text-muted-foreground"),
        cls="grid w-full max-w-sm gap-1.5"
    )


@with_code
def input_with_icon_example():
    icon_cls = "size-4 absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground pointer-events-none"
    return Div(
        Div(
            Icon("lucide:mail", cls=icon_cls),
            Input(type="email", placeholder="you@example.com", cls="pl-9"),
            cls="relative"
        ),
        Div(
            Icon("lucide:search", cls=icon_cls),
            Input(placeholder="Search...", cls="pl-9"),
            cls="relative"
        ),
        cls="grid w-full max-w-sm gap-3"
    )


@with_code
def input_with_button_example():
    return Div(
        (email := Signal("sub_email", "")),
        Input(type="email", placeholder="Enter your email", signal=email),
        Button("Subscribe", data_attr_disabled=~email),
        cls="flex w-full max-w-sm gap-2"
    )


@with_code
def reactive_validation_example():
    return Div(
        (username := Signal("username", "")),
        (username_valid := Signal("username_valid", False)),
        UILabel(
            "Username",
            Span(" *", cls="text-destructive"),
            fr="username-reactive"
        ),
        Input(
            id="username-reactive",
            placeholder="Enter username",
            signal=username,
            data_on_input=username_valid.set(username.match(regex(r"^[a-zA-Z0-9_]{3,}$"))),
        ),
        P(
            "Must be at least 3 characters, letters/numbers/underscores only",
            data_show=~username_valid & (username.length > 0),
            cls="text-xs text-destructive"
        ),
        P(
            "Username is available",
            data_show=username_valid & (username.length > 0),
            cls="text-xs text-muted-foreground"
        ),
        cls="grid w-full max-w-sm gap-1.5"
    )


@with_code
def input_states_example():
    return Div(
        Div(
            UILabel("Disabled", fr="disabled"),
            Input(id="disabled", placeholder="This field is disabled", disabled=True),
            cls="grid gap-1.5"
        ),
        Div(
            UILabel("Read-only", fr="readonly"),
            Input(id="readonly", value="This value cannot be changed", readonly=True),
            cls="grid gap-1.5"
        ),
        Div(
            UILabel(
                "Required",
                Span(" *", cls="text-destructive"),
                fr="required"
            ),
            Input(id="required", placeholder="This field is required", required=True),
            P("This field is required", cls="text-xs text-muted-foreground"),
            cls="grid gap-1.5"
        ),
        cls="grid w-full max-w-sm gap-4"
    )


@with_code
def file_upload_example():
    return Div(
        (avatar_input := Signal("avatar_input", _ref_only=True)),
        (file_name := Signal("file_name", "")),
        UILabel("Profile Picture"),
        Div(
            Input(
                type="file",
                accept=".png,.jpg,.jpeg",
                data_ref=avatar_input,
                data_on_change=file_name.set(js("evt.target.files[0]?.name || ''")),
                cls="hidden"
            ),
            Button(
                Icon("lucide:upload"),
                "Choose File",
                variant="outline",
                data_on_click=avatar_input.click(),
                type="button"
            ),
            Span(
                data_text=file_name | "No file chosen",
                cls="text-sm text-muted-foreground"
            ),
            cls="flex items-center gap-3"
        ),
        P("PNG, JPG up to 2MB", cls="text-xs text-muted-foreground"),
        cls="grid w-full max-w-sm gap-1.5"
    )



EXAMPLES_DATA = [
    {"title": "Default", "description": "A simple labeled input with helper text", "fn": default_example},
    {"title": "With Icon", "description": "Inputs with leading icons using absolute positioning", "fn": input_with_icon_example},
    {"title": "With Button", "description": "Combine an input with an action button", "fn": input_with_button_example},
    {"title": "Reactive Validation", "description": "Real-time input validation using signals and regex", "fn": reactive_validation_example},
    {"title": "States", "description": "Disabled, read-only, and required inputs", "fn": input_states_example},
    {"title": "File Upload", "description": "Custom file input with a styled trigger button", "fn": file_upload_example},
]

API_REFERENCE = build_api_reference(
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


def create_input_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)
