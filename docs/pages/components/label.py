"""
Label component documentation - Form field labels.
"""

# Component metadata for auto-discovery
TITLE = "Label"
DESCRIPTION = "Renders an accessible label associated with form controls."
CATEGORY = "ui"
ORDER = 30
STATUS = "stable"

from starhtml import Div, P, Span, Icon
from starui.registry.components.label import Label
from starui.registry.components.input import Input
from starui.registry.components.checkbox import CheckboxWithLabel
from utils import with_code, Prop, build_api_reference, auto_generate_page


@with_code
def default_example():
    return Div(
        CheckboxWithLabel(label="Accept terms and conditions", name="terms"),
        cls="flex items-center"
    )


@with_code
def with_input_example():
    return Div(
        Label("Email", fr="label-email"),
        Input(type="email", id="label-email", placeholder="you@example.com"),
        P("Enter your email address.", cls="text-xs text-muted-foreground"),
        cls="grid w-full max-w-sm gap-1.5"
    )


@with_code
def composed_content_example():
    return Div(
        Div(
            Label(
                Icon("lucide:globe", cls="size-4"),
                "Custom Domain",
                Span("Optional", cls="text-xs bg-muted px-2 py-0.5 rounded-full font-normal"),
                fr="domain",
            ),
            Input(id="domain", placeholder="app.yourdomain.com"),
            cls="grid gap-1.5"
        ),
        Div(
            Label(
                Icon("lucide:key", cls="size-4"),
                "API Secret Key",
                Span(" *", cls="text-destructive"),
                fr="api-secret",
            ),
            Input(id="api-secret", placeholder="sk_live_...", type="password", cls="font-mono text-sm"),
            cls="grid gap-1.5"
        ),
        cls="grid w-full max-w-sm gap-4"
    )


@with_code
def disabled_state_example():
    return Div(
        Div(
            Label("Active Field", fr="active-field"),
            Input(id="active-field", placeholder="This input is enabled"),
            cls="grid gap-1.5"
        ),
        Div(
            Label("Disabled Field", fr="disabled-field"),
            Input(id="disabled-field", placeholder="This input is disabled", disabled=True),
            cls="grid gap-1.5"
        ),
        cls="grid w-full max-w-sm gap-4"
    )


EXAMPLES_DATA = [
    {"title": "Default", "description": "A label paired with a checkbox — clicking the label toggles the control", "fn": default_example},
    {"title": "With Input", "description": "Label associated with a text input via the for attribute", "fn": with_input_example},
    {"title": "Composed Content", "description": "Labels with icons, badges, and required indicators as children", "fn": composed_content_example},
    {"title": "Disabled State", "description": "Label automatically dims when its associated input is disabled", "fn": disabled_state_example},
]

API_REFERENCE = build_api_reference(
    main_props=[
        Prop("fr", "str | None", "ID of the associated form control (sets 'for' attribute)", "None"),
        Prop("cls", "str", "Additional CSS classes for spacing/layout", "''"),
    ]
)


def create_label_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)
