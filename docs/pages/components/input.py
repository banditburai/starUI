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
from widgets.component_preview import ComponentPreview


def examples():
    """Generate Input examples using ComponentPreview with tabs."""
    
    # Note: Basic input moved to hero example
    # This will be the first example after the hero
    
    # Input types
    yield ComponentPreview(
        Div(
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
        ),
        '''Input(type="email", placeholder="you@example.com")
Input(type="password", placeholder="Enter your password")
Input(type="tel", placeholder="+1 (555) 123-4567")''',
        title="Input Types",
        description="Different input types for various data"
    )
    
    # Reactive Input with validation
    yield ComponentPreview(
        Div(
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
                Div(
                    P(
                        ds_show("!$username_valid && $username.length > 0"),
                        "Username must be at least 3 characters, letters/numbers/underscores only",
                        cls="text-xs text-destructive break-words"
                    ),
                    P(
                        ds_show("$username_valid && $username.length > 0"),
                        "✓ Username is available",
                        cls="text-xs text-green-600"
                    ),
                    cls="mt-1 min-h-[1rem] w-80"
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
                Div(
                    P(
                        ds_show("!$user_email_valid && $user_email.length > 0"),
                        "Please enter a valid email address",
                        cls="text-xs text-destructive break-words"
                    ),
                    P(
                        ds_show("$user_email_valid && $user_email.length > 0"),
                        "✓ Valid email format",
                        cls="text-xs text-green-600"
                    ),
                    cls="mt-1 min-h-[1rem] w-80"
                ),
                cls="space-y-2"
            ),
            ds_signals(username=value(""), username_valid=False, user_email=value(""), user_email_valid=False),
            cls="grid gap-4 max-w-md"
        ),
        '''Input(
    placeholder="Enter username",
    signal="username", 
    validation="/^[a-zA-Z0-9_]{3,}$/.test($signal)"
)

Input(
    type="email",
    placeholder="you@example.com", 
    signal="user_email",
    validation="/^[^\\\\s@]+@[^\\\\s@]+\\\\.[^\\\\s@]+$/.test($signal)"
)

P("Username must be at least 3 characters...", 
  ds_show="!$username_valid && $username.length > 0",
  cls="text-xs text-destructive")''',
        title="Reactive Input with Validation",
        description="Real-time input validation using signals"
    )
    
    # Input with button
    yield ComponentPreview(
        Div(
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
        ),
        '''Div(
    Input(type="email", placeholder="Enter your email", cls="flex-1"),
    Button("Subscribe"),
    cls="flex gap-2"
)

Div(
    Input(type="search", placeholder="Search products...", cls="flex-1"),
    Button("Search", variant="outline"),
    cls="flex gap-2"
)''',
        title="Input with Buttons",
        description="Combine inputs with action buttons"
    )
    
    # Number and date inputs with icon styling
    yield ComponentPreview(
        Div(
            Div(
                UILabel("Quantity", for_="quantity"),
                Div(
                    Icon("lucide:hash", width="16", height="16", cls="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground"),
                    Input(type="number", id="quantity", placeholder="Enter quantity", min=1, max=99, step=1, cls="pl-10 w-80"),
                    cls="relative"
                ),
                cls="space-y-2"
            ),
            Div(
                UILabel("Date of Birth", for_="dob"),
                Div(
                    Icon("lucide:calendar", width="16", height="16", cls="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground pointer-events-none"),
                    Input(type="text", id="dob", placeholder="MM/DD/YYYY", cls="pl-10 w-80"),
                    cls="relative"
                ),
                cls="space-y-2"
            ),
            Div(
                UILabel("Appointment Time", for_="time"),
                Div(
                    Icon("lucide:clock", width="16", height="16", cls="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground pointer-events-none"),
                    Input(type="text", id="time", placeholder="HH:MM", cls="pl-10 w-80"),
                    cls="relative"
                ),
                cls="space-y-2"
            ),
            Div(
                UILabel("Website", for_="website"),
                Div(
                    Icon("lucide:globe", width="16", height="16", cls="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground pointer-events-none"),
                    Input(type="url", id="website", placeholder="https://example.com", cls="pl-10 w-80"),
                    cls="relative"
                ),
                cls="space-y-2"
            ),
            cls="grid gap-4 max-w-md"
        ),
        '''# Input with custom icons
Div(
    Icon("lucide:hash", width="16", height="16", cls="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground"),
    Input(type="number", placeholder="Enter quantity", cls="pl-10"),
    cls="relative"
)

Div(
    Icon("lucide:calendar", width="16", height="16", cls="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground pointer-events-none"),
    Input(type="text", placeholder="MM/DD/YYYY", cls="pl-10"),
    cls="relative"
)

Div(
    Icon("lucide:clock", width="16", height="16", cls="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground pointer-events-none"),
    Input(type="text", placeholder="HH:MM", cls="pl-10"),
    cls="relative"
)

Div(
    Icon("lucide:globe", width="16", height="16", cls="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground pointer-events-none"),
    Input(type="url", placeholder="https://example.com", cls="pl-10"),
    cls="relative"
)''',
        title="Input with Icons",
        description="Inputs with custom icons that adapt to dark mode"
    )
    
    # Input states
    yield ComponentPreview(
        Div(
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
        ),
        '''Input(placeholder="This field is disabled", disabled=True)
Input(value="This value cannot be changed", readonly=True)
Input(placeholder="This field is required", required=True)''',
        title="Input States",
        description="Disabled, read-only, and required inputs"
    )
    
    # File upload
    yield ComponentPreview(
        Div(
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
        ),
        '''Input(type="file", accept="image/*")
Input(type="file", accept=".pdf,.doc,.docx", multiple=True)''',
        title="File Upload",
        description="File input fields with accept filters"
    )
    
    # Form layout
    yield ComponentPreview(
        Div(
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
        ),
        '''Div(
    Div(
        Label("First Name", for_="first"),
        Input(id="first", placeholder="John"),
        cls="space-y-2"
    ),
    Div(
        Label("Last Name", for_="last"),
        Input(id="last", placeholder="Doe"),
        cls="space-y-2"
    ),
    Div(
        Label("Email Address", for_="email"),
        Input(type="email", id="email", placeholder="john.doe@example.com"),
        cls="space-y-2"
    ),
    Button("Submit Form", cls="w-full"),
    cls="space-y-4"
)''',
        title="Complete Form",
        description="Multiple inputs in a form layout"
    )


def create_input_docs():
    """Create input documentation page using convention-based approach."""
    from utils import auto_generate_page
    
    # Hero example - basic input showcase
    hero_example = ComponentPreview(
        Div(
            Input(placeholder="Enter text...", cls="mb-3 w-80"),
            Input(type="email", placeholder="you@example.com", cls="mb-3 w-80"),
            Input(type="password", placeholder="Enter your password", cls="w-80"),
            cls="grid gap-3 max-w-sm"
        ),
        '''Input(placeholder="Enter text...")
Input(type="email", placeholder="you@example.com")
Input(type="password", placeholder="Enter your password")'''
    )
    
    return auto_generate_page(
        TITLE,
        DESCRIPTION,
        list(examples()),
        cli_command="star add input",
        hero_example=hero_example,
        component_slug="input",
        api_reference={
            "props": [
                {
                    "name": "type",
                    "type": "InputType",
                    "default": "text",
                    "description": "The type of input (text, email, password, etc.)"
                },
                {
                    "name": "placeholder",
                    "type": "str | None",
                    "default": "None",
                    "description": "Placeholder text when input is empty"
                },
                {
                    "name": "value",
                    "type": "str | None",
                    "default": "None",
                    "description": "Initial value (for non-reactive inputs)"
                },
                {
                    "name": "signal",
                    "type": "str | None",
                    "default": "None",
                    "description": "Signal name for reactive binding (enables reactivity)"
                },
                {
                    "name": "validation",
                    "type": "str | None",
                    "default": "None",
                    "description": "JavaScript validation expression (e.g., '/^[a-zA-Z0-9-]+$/.test($signal)')"
                },
                {
                    "name": "disabled",
                    "type": "bool",
                    "default": "False",
                    "description": "Whether the input is disabled"
                },
                {
                    "name": "required",
                    "type": "bool",
                    "default": "False",
                    "description": "Whether the input is required"
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