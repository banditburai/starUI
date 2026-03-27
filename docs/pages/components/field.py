"""
Field component documentation - Accessible form field composition.
"""

TITLE = "Field"
DESCRIPTION = "Composable primitives for accessible form fields with orientation, error state, and description wiring."
CATEGORY = "form"
ORDER = 5
STATUS = "stable"

from starhtml import A, Div, Form
from starhtml.forms import email, form_submit, min_length, matches
from components.button import Button
from components.field import (
    Field, FieldSet, FieldLegend, FieldGroup,
    FieldLabel, FieldDescription, FieldSeparator, FieldError,
)
from components.input import Input
from utils import auto_generate_page, Prop, Component, build_api_reference, with_code


@with_code
def hero_field_example():
    return FieldGroup(
        Field(
            FieldLabel("Workspace"),
            Input(placeholder="Acme Corp"),
            FieldDescription("At least 3 characters."),
            FieldError(),
            validate=(min_length, 3, "Workspace"),
            name="hero-ws",
        ),
        Field(
            FieldLabel("Admin email"),
            Input(type="email", placeholder="ops@acme.co"),
            FieldError(),
            validate=email,
            name="hero-email",
        ),
        cls="max-w-sm",
    )


@with_code
def orientation_example():
    return FieldGroup(
        Field(
            FieldLabel("Display name"),
            Input(placeholder="Jane Doe", cls="flex-1"),
            orientation="responsive",
            name="ori-name",
        ),
        Field(
            FieldLabel("Username"),
            Input(placeholder="janedoe", cls="flex-1"),
            orientation="responsive",
            name="ori-user",
        ),
        cls="max-w-lg",
    )


@with_code
def states_example():
    return FieldGroup(
        Field(
            FieldLabel("Account ID"),
            Input(value="acct_7x9k2m", disabled=True),
            FieldDescription("Contact support to change your account ID."),
            data_disabled="true",
            name="st-id",
        ),
        Field(
            FieldLabel("Plan"),
            Input(value="Professional", readonly=True),
            name="st-plan",
        ),
        Field(
            FieldLabel("Subdomain"),
            Input(value="admin"),
            FieldError(errors=["Already taken"]),
            invalid=True,
            name="st-sub",
        ),
        cls="max-w-sm",
    )


@with_code
def form_example():
    email_f = Field(
        FieldLabel("Email"),
        Input(type="email", autocomplete="email", placeholder="you@company.com"),
        FieldError(),
        validate=email,
        name="reg-email",
    )
    pw_f = Field(
        FieldLabel("Password"),
        Input(type="password", autocomplete="new-password"),
        FieldDescription("At least 8 characters."),
        FieldError(),
        validate=(min_length, 8, "Password"),
        name="reg-pw",
    )
    pw2_f = Field(
        FieldLabel("Confirm password"),
        Input(type="password", autocomplete="new-password"),
        FieldError(),
        validate=(matches, pw_f.signal, "Passwords must match", {"label": "Confirmation"}),
        name="reg-pw2",
    )
    return Form(
        (fs := form_submit("/api/register", email_f, pw_f, pw2_f, name="reg")),
        FieldGroup(email_f, pw_f, pw2_f),
        Div(
            data_text=fs.error, data_show=fs.error,
            role="status", aria_live="polite",
            cls="text-sm text-destructive",
        ),
        Button(
            "Create account", type="submit",
            data_text=fs.submitting.if_("Creating account...", "Create account"),
            data_attr_disabled=fs.submitting,
            cls="w-full",
        ),
        cls="flex w-full max-w-lg flex-col gap-6",
    )


@with_code
def fieldset_example():
    return FieldSet(
        FieldLegend("Billing contact"),
        FieldDescription(
            "Used for invoices and ",
            A("payment receipts", href="#"),
            ".",
        ),
        FieldGroup(
            Field(
                FieldLabel("Company"),
                Input(placeholder="Acme Corp"),
                name="fs-company",
            ),
            Div(
                Field(
                    FieldLabel("Tax ID"),
                    Input(placeholder="12-3456789"),
                    name="fs-tax",
                ),
                Field(
                    FieldLabel("PO number"),
                    Input(placeholder="PO-2026-041"),
                    name="fs-po",
                ),
                cls="grid grid-cols-2 gap-4",
            ),
            cls="max-w-md",
        ),
    )


@with_code
def separator_example():
    return FieldGroup(
        Field(
            FieldLabel("Work email"),
            Input(type="email", placeholder="you@company.com"),
            FieldDescription("Sign in with your organization's SSO."),
            name="sep-sso",
        ),
        FieldSeparator("or"),
        Field(
            FieldLabel("Personal email"),
            Input(type="email", placeholder="hey@pm.me"),
            FieldDescription("We'll send a magic link."),
            name="sep-magic",
        ),
        cls="max-w-sm",
    )


EXAMPLES_DATA = [
    {"fn": hero_field_example, "title": "Field", "description": "Validated fields with auto-wired IDs, FieldError, and FieldDescription via name= and validate="},
    {"fn": orientation_example, "title": "Orientation", "description": "Responsive orientation \u2014 stacks vertically in narrow containers, goes horizontal at wider breakpoints"},
    {"fn": states_example, "title": "States", "description": "Disabled, readonly, and error states with data_disabled, invalid, and server-side FieldError"},
    {"fn": form_example, "title": "Form Submission", "description": "Complete form with form_submit \u2014 auto-creates submitting/error signals, validates all fields, and disables submit while in flight"},
    {"fn": fieldset_example, "title": "FieldSet", "description": "Semantic fieldset with legend, inline-link description, and grid layout"},
    {"fn": separator_example, "title": "With Separator", "description": "Visual divider between alternative sign-in methods"},
]

API_REFERENCE = build_api_reference(
    components=[
        Component("Field", "Accessible wrapper with orientation, validation, and error-state propagation via data-invalid", [
            Prop("name", "str | None", "Auto-wires coordinated IDs across label, input, description, and error", "None"),
            Prop("orientation", "Literal['vertical', 'horizontal', 'responsive']", "Layout direction", "'vertical'"),
            Prop("invalid", "bool | Signal | None", "Error state \u2014 True for static, Signal for reactive (auto-set when validate= is used)", "None"),
            Prop("validate", "callable | tuple | None", "Validation rule \u2014 email, (min_length, 8, 'Label'), or (matches, other_sig, 'msg'). Auto-creates signal, wires Input, FieldError, and invalid.", "None"),
            Prop("signal", "Signal | None", "Explicit signal override for validation (otherwise auto-created from name=)", "None"),
            Prop("cls", "str", "Additional CSS classes", "''"),
        ]),
        Component("FieldSet", "Semantic <fieldset> container \u2014 FieldLegend must be the first child", [
            Prop("cls", "str", "Additional CSS classes", "''"),
        ]),
        Component("FieldLegend", "Legend element for FieldSet with size variants", [
            Prop("variant", "Literal['legend', 'label']", "Text size variant", "'legend'"),
            Prop("cls", "str", "Additional CSS classes", "''"),
        ]),
        Component("FieldGroup", "Layout wrapper enabling @container queries for responsive Field orientation", [
            Prop("cls", "str", "Additional CSS classes", "''"),
        ]),
        Component("FieldContent", "Groups control and descriptions beside the label in horizontal layouts"),
        Component("FieldLabel", "Accessible <label> \u2014 auto-wired via Field(name=) or explicit fr=", [
            Prop("fr", "str | None", "Explicit ID override for the associated form control", "None"),
            Prop("cls", "str", "Additional CSS classes", "''"),
        ]),
        Component("FieldTitle", "Title inside FieldContent \u2014 shares field-label slot for CSS selector parity"),
        Component("FieldDescription", "Helper text with auto-wired id via Field(name=) and inline link support"),
        Component("FieldSeparator", "Visual divider with optional inline content (e.g. 'or')"),
        Component("FieldError", "Error display \u2014 auto-wired from Field(validate=), or use explicit signal= / errors=[...]", [
            Prop("signal", "Signal | None", "Explicit signal override \u2014 auto-wired from Field context when validate= is used", "None"),
            Prop("errors", "list | None", "Server-side error messages (deduped, renders as list if multiple)", "None"),
        ]),
    ]
)


def create_field_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)
