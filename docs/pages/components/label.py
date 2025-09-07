"""
Label component documentation - Form field labels.
"""

# Component metadata for auto-discovery
TITLE = "Label"
DESCRIPTION = "Renders an accessible label associated with form controls."
CATEGORY = "ui"
ORDER = 30
STATUS = "stable"

from starhtml import Div, P, Span, Icon, Button
from starhtml.datastar import ds_signals, ds_on_input, ds_on_click, ds_show, ds_class, value, toggle, ds_text
from starui.registry.components.label import Label
from starui.registry.components.input import Input
from starui.registry.components.checkbox import Checkbox, CheckboxWithLabel
from starui.registry.components.radio_group import RadioGroup, RadioGroupItem
from widgets.component_preview import ComponentPreview


def examples():
    """Generate Label examples using ComponentPreview with tabs."""
    
    # Basic usage - moved to hero example
    # This will be the first example after the hero
    
    # Interactive validation
    yield ComponentPreview(
        Div(
            Div(
                Label(
                    "Project Name",
                    Span(" *", cls="text-destructive"),
                    for_="project-name-val"
                ),
                Input(
                    id="project-name-val", 
                    placeholder="awesome-project",
                    signal="projectName",
                    validation="/^[a-zA-Z0-9-]+$/.test($signal)"
                ),
                Div(
                    P(
                        ds_show("!$projectNameValid && $projectName.length > 0"),
                        "Project names can only contain letters, numbers, and hyphens",
                        cls="text-xs text-destructive"
                    ),
                    P(
                        ds_show("$projectNameValid && $projectName.length > 0"),
                        "✓ Valid project name",
                        cls="text-xs text-green-600"
                    ),
                    cls="mt-1 h-4"
                ),
                cls="space-y-2"
            ),
            # Initialize signals
            ds_signals(
                projectName=value("my-project"), 
                projectNameValid=True
            ),
            cls="w-full max-w-md"
        ),
        '''Label(
    "Project Name",
    Span(" *", cls="text-destructive"),
    for_="project-name"
)
Input(
    id="project-name", 
    placeholder="awesome-project",
    signal="projectName",
    validation="/^[a-zA-Z0-9-]+$/.test($signal)"
)

# Validation messages
P(
    ds_show("!$projectNameValid && $projectName.length > 0"),
    "Project names can only contain letters, numbers, and hyphens", 
    cls="text-xs text-destructive"
)
P(
    ds_show("$projectNameValid && $projectName.length > 0"),
    "✓ Valid project name", 
    cls="text-xs text-green-600"
)

# Initialize signals
ds_signals(projectName=value("my-project"), projectNameValid=True)''',
        title="Interactive Validation",
        description="Labels with real-time validation feedback"
    )
    
    # Interactive label controls
    yield ComponentPreview(
        Div(
            Div(
                Label(
                    Icon("lucide:database", cls="h-4 w-4"),
                    "Database Connection",
                    for_="db-connection-ctx",
                    cls="flex items-center gap-2"
                ),
                Input(id="db-connection-ctx", placeholder="postgresql://user:pass@host:5432/db", cls="font-mono text-sm"),
                cls="space-y-2"
            ),
            Div(
                Div(
                    Label(
                        Icon("lucide:key", cls="h-4 w-4"),
                        "API Secret Key",
                        for_="api-secret-ctx",
                        cls="flex items-center gap-2"
                    ),
                    Button(
                        Span(Icon("lucide:eye-off", cls="h-3 w-3"), ds_show("!$showSecret")),
                        Span(Icon("lucide:eye", cls="h-3 w-3"), ds_show("$showSecret")),
                        ds_on_click("$showSecret = !$showSecret; document.getElementById('api-secret-ctx').type = $showSecret ? 'text' : 'password'"),
                        variant="ghost",
                        size="sm",
                        cls="ml-auto p-0 h-auto text-muted-foreground hover:text-foreground"
                    ),
                    cls="flex items-center justify-between"
                ),
                Input(
                    id="api-secret-ctx", 
                    placeholder="sk_live_...",
                    value="sk_live_abc123xyz789",
                    type="password",
                    cls="font-mono text-sm"
                ),
                ds_signals(showSecret=False),
                cls="space-y-2"
            ),
            cls="grid gap-4 max-w-md"
        ),
        '''Label(
    Icon("lucide:key", cls="h-4 w-4"),
    "API Secret Key",
    Button(
        Icon("lucide:eye-off", cls="h-3 w-3"),
        ds_on_click="$showSecret = !$showSecret",
        ds_show("!$showSecret"),
        cls="ml-auto p-0 h-auto bg-transparent border-0"
    ),
    Button(
        Icon("lucide:eye", cls="h-3 w-3"), 
        ds_on_click="$showSecret = !$showSecret",
        ds_show("$showSecret"),
        cls="ml-auto p-0 h-auto bg-transparent border-0"
    ),
    for_="api-secret",
    cls="flex items-center gap-2"
)
Div(
    Input(
        id="api-secret", 
        placeholder="sk_live_...",
        value="sk_live_abc123xyz789",
        type="password",
        cls="font-mono text-sm w-full",
        ds_show="!$showSecret"
    ),
    Input(
        placeholder="sk_live_...",
        value="sk_live_abc123xyz789", 
        type="text",
        cls="font-mono text-sm w-full",
        ds_show="$showSecret"
    ),
    cls="relative"
)''',
        title="Interactive Label Controls",
        description="Labels with interactive elements like visibility toggles"
    )
    
    # Advanced label patterns
    yield ComponentPreview(
        Div(
            Div(
                Label(
                    "Deployment Region",
                    Span("(affects latency)", cls="text-xs text-muted-foreground font-normal"),
                    for_="region",
                    cls="font-medium"
                ),
                Input(id="region", value="us-east-1", readonly=True, cls="bg-muted font-mono text-sm"),
                P("Contact support to change regions after deployment", cls="text-xs text-muted-foreground mt-1"),
                cls="space-y-2"
            ),
            Div(
                Label(
                    "Custom Domain",
                    Span("Optional", cls="text-xs bg-muted px-2 py-0.5 rounded-full ml-2"),
                    for_="domain",
                    cls="flex items-center font-medium"
                ),
                Input(id="domain", placeholder="app.yourdomain.com"),
                P("Requires DNS configuration and SSL certificate", cls="text-xs text-muted-foreground mt-1"),
                cls="space-y-2"
            ),
            cls="grid gap-4 max-w-md"
        ),
        '''Label(
    "Deployment Region",
    Span("(affects latency)", cls="text-xs text-muted-foreground font-normal"),
    for_="region",
    cls="font-medium"
)

Label(
    "Custom Domain",
    Span("Optional", cls="text-xs bg-muted px-2 py-0.5 rounded-full ml-2"),
    for_="domain",
    cls="flex items-center font-medium"
)''',
        title="Advanced Patterns",
        description="Labels with badges, annotations, and contextual information"
    )
    
    # Radio and checkbox groups  
    yield ComponentPreview(
        Div(
            Div(
                Label("Preferred Contact Method", cls="text-base font-semibold mb-3 block"),
                RadioGroup(
                    RadioGroupItem("email", "Email"),
                    RadioGroupItem("phone", "Phone"), 
                    RadioGroupItem("mail", "Mail"),
                    initial_value="email"
                ),
                cls="p-4 border rounded-lg"
            ),
            Div(
                Label("Notification Preferences", cls="text-base font-semibold mb-3 block"),
                Div(
                    CheckboxWithLabel("Email notifications", name="notify-email"),
                    CheckboxWithLabel("SMS notifications", name="notify-sms"),
                    CheckboxWithLabel("Push notifications", name="notify-push"),
                    cls="space-y-3"
                ),
                cls="p-4 border rounded-lg"
            ),
            cls="grid gap-4 max-w-md"
        ),
        '''Label("Preferred Contact Method", cls="text-base font-semibold mb-3 block")
RadioGroup(
    RadioGroupItem("email", "Email"),
    RadioGroupItem("phone", "Phone"),
    RadioGroupItem("mail", "Mail"),
    initial_value="email"
)

Label("Notification Preferences", cls="text-base font-semibold mb-3 block")
CheckboxWithLabel("Email notifications", name="notify-email")
CheckboxWithLabel("SMS notifications", name="notify-sms")
CheckboxWithLabel("Push notifications", name="notify-push")''',
        title="Radio & Checkbox Groups",
        description="Labels for grouped form controls"
    )
    
    
    # Complete form layout
    yield ComponentPreview(
        Div(
            Div(
                Label("Developer Name", for_="dev-name-form"),
                Input(id="dev-name-form", placeholder="Sarah Chen"),
                cls="space-y-2"
            ),
            Div(
                Label("GitHub Username", for_="github-form"),
                Input(id="github-form", placeholder="sarahc", cls="font-mono text-sm"),
                P("Used for repository access and commit attribution", cls="text-xs text-muted-foreground mt-1"),
                cls="space-y-2"
            ),
            Div(
                Label(
                    "Team Role",
                    Span(" *", cls="text-destructive"),
                    for_="role-form"
                ),
                Input(id="role-form", placeholder="Frontend Engineer"),
                cls="space-y-2"
            ),
            Div(
                Label("Salary Range", for_="salary-form"),
                Input(id="salary-form", placeholder="$120,000 - $150,000", cls="font-mono text-sm"),
                P("Optional - used for budget planning", cls="text-xs text-muted-foreground mt-1"),
                cls="space-y-2"
            ),
            cls="space-y-4 max-w-md border rounded-lg p-4"
        ),
        '''Label("Developer Name", for_="dev-name")
Input(id="dev-name", placeholder="Sarah Chen")

Label("GitHub Username", for_="github")
Input(id="github", placeholder="sarahc", cls="font-mono text-sm")
P("Used for repository access and commit attribution", 
  cls="text-xs text-muted-foreground mt-1")

Label(
    "Team Role",
    Span(" *", cls="text-destructive"),
    for_="role"
)
Input(id="role", placeholder="Frontend Engineer")''',
        title="Complete Form Layout",
        description="Real-world form with various label patterns"
    )


def create_label_docs():
    """Create label documentation page using convention-based approach."""
    from utils import auto_generate_page
    
    # Hero example - showcase different label patterns
    hero_example = ComponentPreview(
        Div(
            # Basic form fields
            Div(
                Label("Email", for_="email"),
                Input(type="email", id="email", placeholder="Enter your email"),
                cls="space-y-2"
            ),
            # Required field
            Div(
                Label(
                    "Password",
                    Span(" *", cls="text-destructive"),
                    for_="password"
                ),
                Input(type="password", id="password", placeholder="Enter your password"),
                cls="space-y-2"
            ),
            # Label with icon
            Div(
                Label(
                    Icon("lucide:user", width="16", height="16"),
                    "Username",
                    for_="username",
                    cls="flex items-center gap-2"
                ),
                Input(id="username", placeholder="Enter your username"),
                cls="space-y-2"
            ),
            cls="grid gap-6 max-w-sm"
        ),
        '''Label("Email", for_="email")
Input(type="email", id="email", placeholder="Enter your email")

Label(
    "Password",
    Span(" *", cls="text-destructive"),
    for_="password"
)

Label(
    Icon("lucide:user", width="16", height="16"),
    "Username", 
    for_="username",
    cls="flex items-center gap-2"
)'''
    )
    
    return auto_generate_page(
        TITLE,
        DESCRIPTION,
        list(examples()),
        cli_command="star add label",
        hero_example=hero_example,
        component_slug="label",
        api_reference={
            "props": [
                {
                    "name": "for_",
                    "type": "str | None",
                    "default": "None",
                    "description": "ID of the form control this label is for"
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