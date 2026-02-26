"""
Input component documentation - Form input fields with styling.
"""

# Component metadata for auto-discovery
TITLE = "Input"
DESCRIPTION = "Displays a form input field or a component that looks like an input field."
CATEGORY = "form"
ORDER = 10
STATUS = "stable"

from starhtml import Div, P, Label, Span, Icon, Signal, regex, set_timeout, js
from starui.registry.components.input import Input
from starui.registry.components.button import Button
from starui.registry.components.label import Label as UILabel
from utils import auto_generate_page, with_code, Prop, build_api_reference



@with_code
def input_types_example():
    return Div(
        Div(
            UILabel("First Name", fr="first"),
            Input(id="first", placeholder="John", cls="w-80"),
            cls="space-y-2"
        ),
        Div(
            UILabel("Last Name", fr="last"),
            Input(id="last", placeholder="Doe", cls="w-80"),
            cls="space-y-2"
        ),
        Div(
            UILabel("Email", fr="email"),
            Input(type="email", id="email", placeholder="you@example.com", cls="w-80"),
            cls="space-y-2"
        ),
        Div(
            UILabel("Password", fr="password"),
            Input(type="password", id="password", placeholder="Enter your password", cls="w-80"),
            cls="space-y-2"
        ),
        Div(
            UILabel("Phone Number", fr="phone"),
            Input(type="tel", id="phone", placeholder="+1 (555) 123-4567", cls="w-80"),
            cls="space-y-2"
        ),
        Div(
            Button("Submit Form", cls="w-full"),
            cls="pt-2"
        ),
        cls="space-y-4 max-w-md"
    )


@with_code
def reactive_input_validation_example():
    return Div(
        (username := Signal("username", "")),
        (username_valid := Signal("username_valid", False)),
        (user_email := Signal("user_email", "")),
        (user_email_valid := Signal("user_email_valid", False)),
        Div(
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
                cls="w-80"
            ),
            Div(
                P(
                    "Username must be at least 3 characters, letters/numbers/underscores only",
                    data_show=~username_valid & (username.length > 0),
                    cls="text-xs text-destructive break-words"
                ),
                P(
                    "✓ Username is available",
                    data_show=username_valid & (username.length > 0),
                    cls="text-xs text-green-600"
                ),
                cls="mt-1 min-h-[1rem] w-80"
            ),
            cls="space-y-2"
        ),
        Div(
            UILabel("Email", fr="email-reactive"),
            Input(
                type="email",
                id="email-reactive",
                placeholder="you@example.com",
                signal=user_email,
                data_on_input=user_email_valid.set(user_email.match(regex(r"^[^\s@]+@[^\s@]+\.[^\s@]+$"))),
                cls="w-80"
            ),
            Div(
                P(
                    "Please enter a valid email address",
                    data_show=~user_email_valid & (user_email.length > 0),
                    cls="text-xs text-destructive break-words"
                ),
                P(
                    "✓ Valid email format",
                    data_show=user_email_valid & (user_email.length > 0),
                    cls="text-xs text-green-600"
                ),
                cls="mt-1 min-h-[1rem] w-80"
            ),
            cls="space-y-2"
        ),
        cls="grid gap-4 max-w-md"
    )


@with_code
def input_with_buttons_example():
    return Div(
        (email := Signal("newsletter_email", "")),
        (subscribed := Signal("subscribed", False)),
        (search_query := Signal("search_query", "")),
        Div(
            UILabel("Subscribe to Newsletter", fr="newsletter"),
            Div(
                Input(
                    type="email",
                    id="newsletter",
                    placeholder="Enter your email",
                    signal=email,
                    cls="w-80"
                ),
                Button(
                    "Subscribe",
                    data_attr_disabled=~email,
                    data_on_click=[
                        subscribed.set(True),
                        email.set(""),
                        set_timeout(subscribed.set(False), 3000)
                    ]
                ),
                cls="flex gap-2 items-center"
            ),
            P(
                "✓ Successfully subscribed!",
                data_show=subscribed,
                cls="text-sm text-green-600"
            ),
            cls="space-y-2"
        ),
        Div(
            UILabel("Search Products", fr="search"),
            Div(
                Input(
                    type="text",
                    id="search",
                    placeholder="Search products...",
                    signal=search_query,
                    cls="w-80"
                ),
                Button(
                    "Clear",
                    variant="outline",
                    data_attr_disabled=~search_query,
                    data_on_click=search_query.set("")
                ),
                cls="flex gap-2 items-center"
            ),
            P(
                "Searching for: ",
                Span(data_text=search_query, cls="font-medium"),
                data_show=search_query,
                cls="text-sm text-muted-foreground"
            ),
            cls="space-y-2"
        ),
        cls="grid gap-4 max-w-md"
    )


@with_code
def inputs_with_icons_example():
    return Div(
        Div(
            UILabel("Quantity", fr="quantity"),
            Div(
                Icon("lucide:hash", cls="h-4 w-4 absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground pointer-events-none"),
                Input(type="number", id="quantity", placeholder="Enter quantity", min=1, max=99, step=1, cls="pl-10 w-80"),
                cls="relative"
            ),
            cls="space-y-2"
        ),
        Div(
            UILabel("Email Address", fr="email-icon"),
            Div(
                Icon("lucide:mail", cls="h-4 w-4 absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground pointer-events-none"),
                Input(type="email", id="email-icon", placeholder="you@example.com", cls="pl-10 w-80"),
                cls="relative"
            ),
            cls="space-y-2"
        ),
        Div(
            UILabel("Phone Number", fr="phone-icon"),
            Div(
                Icon("lucide:phone", cls="h-4 w-4 absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground pointer-events-none"),
                Input(type="tel", id="phone-icon", placeholder="+1 (555) 123-4567", cls="pl-10 w-80"),
                cls="relative"
            ),
            cls="space-y-2"
        ),
        Div(
            UILabel("Website", fr="website"),
            Div(
                Icon("lucide:globe", cls="h-4 w-4 absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground pointer-events-none"),
                Input(type="url", id="website", placeholder="https://example.com", cls="pl-10 w-80"),
                cls="relative"
            ),
            cls="space-y-2"
        ),
        cls="grid gap-4 max-w-md"
    )


@with_code
def input_states_example():
    return Div(
        Div(
            UILabel("Disabled Input", fr="disabled", cls="opacity-50"),
            Input(id="disabled", placeholder="This field is disabled", disabled=True, cls="w-80"),
            cls="space-y-2"
        ),
        Div(
            UILabel("Read-only Input", fr="readonly"),
            Input(id="readonly", value="This value cannot be changed", readonly=True, cls="w-80"),
            cls="space-y-2"
        ),
        Div(
            UILabel(
                "Required Field",
                Span(" *", cls="text-destructive"),
                fr="required"
            ),
            Input(id="required", placeholder="This field is required", required=True, cls="w-80"),
            P("This field is required", cls="text-xs text-muted-foreground"),
            cls="space-y-2"
        ),
        cls="grid gap-4 max-w-md"
    )


@with_code
def file_upload_inputs_example():
    return Div(
        (file_error := Signal("file_error", "")),
        (file_name := Signal("file_name", "")),
        (doc_count := Signal("doc_count", 0)),
        (avatar_input := Signal("avatar_input", _ref_only=True)),
        (docs_input := Signal("docs_input", _ref_only=True)),
        Div(
            UILabel("Profile Picture"),
            Div(
                Input(
                    type="file",
                    accept=".png,.jpg,.jpeg",
                    data_ref=avatar_input,
                    data_on_change=[
                        file_name.set("evt.target.files[0]?.name || ''"),
                        file_error.set(
                            "(evt.target.files[0]?.size || 0) > 2097152 ? 'File size must be under 2MB' : ''"
                        )
                    ],
                    cls="hidden"
                ),
                Button(
                    Icon("lucide:upload", cls="h-4 w-4 mr-2"),
                    "Choose File",
                    variant="outline",
                    data_on_click=avatar_input.click(),
                    type="button"
                ),
                Span(
                    data_text=file_name | "No file chosen",
                    cls="ml-3 text-sm text-muted-foreground"
                ),
                cls="flex items-center"
            ),
            P("PNG, JPG up to 2MB", data_show=~file_error & ~file_name, cls="text-xs text-muted-foreground mt-1.5"),
            P(data_text=file_error, data_show=file_error, cls="text-xs text-destructive mt-1.5"),
            P(
                "✓ File ready to upload",
                data_show=file_name & ~file_error,
                cls="text-xs text-green-600 mt-1.5"
            ),
            cls="space-y-2"
        ),
        Div(
            UILabel("Document Upload"),
            Div(
                Input(
                    type="file",
                    accept=".pdf,.doc,.docx",
                    multiple=True,
                    data_ref=docs_input,
                    data_on_change=doc_count.set("evt.target.files.length"),
                    cls="hidden"
                ),
                Button(
                    Icon("lucide:paperclip", cls="h-4 w-4 mr-2"),
                    "Choose Files",
                    variant="outline",
                    data_on_click=docs_input.click(),
                    type="button"
                ),
                Span(
                    data_text=(doc_count > 0).if_(doc_count + " file(s) selected", "No files chosen"),
                    cls="ml-3 text-sm text-muted-foreground"
                ),
                cls="flex items-center"
            ),
            P("PDF, DOC, DOCX files (multiple allowed)", cls="text-xs text-muted-foreground mt-1.5"),
            cls="space-y-2"
        ),
        cls="grid gap-4 max-w-md"
    )



EXAMPLES_DATA = [
    {"title": "Input Types", "description": "Complete form with different input types", "fn": input_types_example},
    {"title": "Reactive Input with Validation", "description": "Real-time input validation using signals", "fn": reactive_input_validation_example},
    {"title": "Input with Buttons", "description": "Combine inputs with action buttons", "fn": input_with_buttons_example},
    {"title": "Input with Icons", "description": "Inputs with custom icons that adapt to dark mode", "fn": inputs_with_icons_example},
    {"title": "Input States", "description": "Disabled, read-only, and required inputs", "fn": input_states_example},
    {"title": "File Upload", "description": "File input fields with accept filters", "fn": file_upload_inputs_example},
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