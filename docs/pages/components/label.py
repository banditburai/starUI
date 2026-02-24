"""
Label component documentation - Form field labels.
"""

TITLE = "Label"
DESCRIPTION = "Renders an accessible label associated with form controls."
CATEGORY = "ui"
ORDER = 30
STATUS = "stable"

from starhtml import Div, P, Span, Icon, Button, Signal, regex
from starui.registry.components.label import Label
from starui.registry.components.input import Input
from starui.registry.components.checkbox import CheckboxWithLabel
from starui.registry.components.radio_group import RadioGroup, RadioGroupItem
from utils import with_code, Prop, build_api_reference, auto_generate_page


@with_code
def interactive_validation_example():
    return Div(
        (project_name := Signal("project_name", "my-project")),
        (project_name_valid := Signal("project_name_valid", True)),
        Div(
            Label(
                "Project Name",
                Span(" *", cls="text-destructive"),
                fr="project-name-val"
            ),
            Input(
                id="project-name-val",
                placeholder="awesome-project",
                signal=project_name,
                data_on_input=project_name_valid.set(project_name.match(regex(r"^[a-zA-Z0-9-]+$"))),
                cls="w-80"
            ),
            Div(
                P(
                    "Project names can only contain letters, numbers, and hyphens",
                    data_show=~project_name_valid & (project_name.length > 0),
                    cls="text-xs text-destructive"
                ),
                P(
                    "✓ Valid project name",
                    data_show=project_name_valid & (project_name.length > 0),
                    cls="text-xs text-green-600"
                ),
                cls="mt-1 h-4"
            ),
            cls="space-y-2"
        ),
        cls="w-full max-w-md"
    )


@with_code
def interactive_label_controls_example():
    return Div(
        (show_secret := Signal("show_secret", False)),
        (secret_input := Signal("secret_input", _ref_only=True)),
        Div(
            Label(
                Icon("lucide:database", cls="h-4 w-4"),
                "Database Connection",
                fr="db-connection-ctx",
                cls="flex items-center gap-2"
            ),
            Input(id="db-connection-ctx", placeholder="postgresql://user:pass@host:5432/db", cls="font-mono text-sm w-80"),
            cls="space-y-2"
        ),
        Div(
            Div(
                Label(
                    Icon("lucide:key", cls="h-4 w-4"),
                    "API Secret Key",
                    fr="api-secret-ctx",
                    cls="flex items-center gap-2"
                ),
                Button(
                    Icon("lucide:eye-off", cls="h-3 w-3", data_show=~show_secret),
                    Icon("lucide:eye", cls="h-3 w-3", data_show=show_secret),
                    data_on_click=[
                        show_secret.set(~show_secret),
                        secret_input.setAttribute("type", show_secret.if_("text", "password"))
                    ],
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
                data_ref=secret_input,
                cls="font-mono text-sm w-80"
            ),
            cls="space-y-2"
        ),
        cls="grid gap-4 max-w-md"
    )


@with_code
def advanced_label_patterns_example():
    return Div(
        Div(
            Label(
                "Deployment Region",
                Span("(affects latency)", cls="text-xs text-muted-foreground font-normal"),
                fr="region",
                cls="font-medium"
            ),
            Input(id="region", value="us-east-1", readonly=True, cls="bg-muted font-mono text-sm w-80"),
            P("Contact support to change regions after deployment", cls="text-xs text-muted-foreground mt-1"),
            cls="space-y-2"
        ),
        Div(
            Label(
                "Custom Domain",
                Span("Optional", cls="text-xs bg-muted px-2 py-0.5 rounded-full ml-2"),
                fr="domain",
                cls="flex items-center font-medium"
            ),
            Input(id="domain", placeholder="app.yourdomain.com", cls="w-80"),
            P("Requires DNS configuration and SSL certificate", cls="text-xs text-muted-foreground mt-1"),
            cls="space-y-2"
        ),
        cls="grid gap-4 max-w-md"
    )


@with_code
def radio_checkbox_groups_example():
    return Div(
        Div(
            Label("Preferred Contact Method", cls="text-base font-semibold mb-3 block"),
            RadioGroup(
                RadioGroupItem("email", "Email"),
                RadioGroupItem("phone", "Phone"),
                RadioGroupItem("mail", "Mail"),
                value="email"
            ),
            cls="p-4 border rounded-lg"
        ),
        Div(
            Label("Notification Preferences", cls="text-base font-semibold mb-3 block"),
            Div(
                CheckboxWithLabel(label="Email notifications", name="notify-email"),
                CheckboxWithLabel(label="SMS notifications", name="notify-sms"),
                CheckboxWithLabel(label="Push notifications", name="notify-push"),
                cls="space-y-3"
            ),
            cls="p-4 border rounded-lg"
        ),
        cls="grid gap-4 max-w-md"
    )


@with_code
def complete_form_layout_example():
    return Div(
        Div(
            Label("Developer Name", fr="dev-name-form"),
            Input(id="dev-name-form", placeholder="Sarah Chen", cls="w-80"),
            cls="space-y-2"
        ),
        Div(
            Label("GitHub Username", fr="github-form"),
            Input(id="github-form", placeholder="sarahc", cls="font-mono text-sm w-80"),
            P("Used for repository access and commit attribution", cls="text-xs text-muted-foreground mt-1"),
            cls="space-y-2"
        ),
        Div(
            Label(
                "Team Role",
                Span(" *", cls="text-destructive"),
                fr="role-form"
            ),
            Input(id="role-form", placeholder="Frontend Engineer", cls="w-80"),
            cls="space-y-2"
        ),
        Div(
            Label("Salary Range", fr="salary-form"),
            Input(id="salary-form", placeholder="$120,000 - $150,000", cls="font-mono text-sm w-80"),
            P("Optional - used for budget planning", cls="text-xs text-muted-foreground mt-1"),
            cls="space-y-2"
        ),
        cls="space-y-4 max-w-md border rounded-lg p-4"
    )


EXAMPLES_DATA = [
    {"title": "Interactive Validation", "description": "Labels with real-time validation feedback", "fn": interactive_validation_example},
    {"title": "Interactive Label Controls", "description": "Labels with interactive elements like visibility toggles", "fn": interactive_label_controls_example},
    {"title": "Advanced Patterns", "description": "Labels with badges, annotations, and contextual information", "fn": advanced_label_patterns_example},
    {"title": "Radio & Checkbox Groups", "description": "Labels for grouped form controls", "fn": radio_checkbox_groups_example},
    {"title": "Complete Form Layout", "description": "Real-world form with various label patterns", "fn": complete_form_layout_example},
]

API_REFERENCE = build_api_reference(
    main_props=[
        Prop("fr", "str | None", "ID of the associated form control (sets 'for' attribute)", "None"),
        Prop("cls", "str", "Additional CSS classes for spacing/layout", "''"),
    ]
)


def create_label_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)