TITLE = "Radio Group"
DESCRIPTION = "A set of checkable buttons—known as radio buttons—where no more than one of the buttons can be checked at a time."
CATEGORY = "form"
ORDER = 30
STATUS = "stable"

from starhtml import Div, P, Span, Icon, Form, Code, Signal, js, match
from starui.registry.components.radio_group import RadioGroup, RadioGroupItem, RadioGroupWithLabel
from starui.registry.components.button import Button
from starui.registry.components.card import Card, CardHeader, CardContent, CardTitle, CardDescription
from utils import auto_generate_page, with_code, Component, build_api_reference


@with_code
def default_example():
    return Div(
        (notify := Signal("notify", "all")),
        P("Notify me about...", cls="text-sm font-medium mb-3"),
        RadioGroup(
            RadioGroupItem(value="all", label="All new messages"),
            RadioGroupItem(value="mentions", label="Direct messages and mentions"),
            RadioGroupItem(value="nothing", label="Nothing"),
            value="all",
            signal=notify,
        ),
        P(
            "Current: ",
            Code(data_text=notify),
            cls="text-sm text-muted-foreground mt-3"
        ),
        cls="max-w-sm"
    )


@with_code
def horizontal_layout_example():
    return Div(
        RadioGroupWithLabel(
            label="Size",
            options=[
                {"value": "sm", "label": "Small"},
                {"value": "md", "label": "Medium"},
                {"value": "lg", "label": "Large"},
            ],
            orientation="horizontal",
            value="md",
            helper_text="Choose the appropriate size"
        ),
        cls="max-w-lg"
    )


@with_code
def states_example():
    return Div(
        RadioGroupWithLabel(
            label="Per-item disabled",
            options=[
                {"value": "active", "label": "Active"},
                {"value": "inactive", "label": "Inactive", "disabled": True},
                {"value": "pending", "label": "Pending"},
            ],
            value="active",
        ),
        RadioGroupWithLabel(
            label="Fully disabled",
            options=[
                {"value": "on", "label": "On"},
                {"value": "off", "label": "Off"},
            ],
            value="on",
            disabled=True,
        ),
        RadioGroupWithLabel(
            label="Required field",
            options=[
                {"value": "yes", "label": "Yes"},
                {"value": "no", "label": "No"},
            ],
            required=True,
        ),
        RadioGroupWithLabel(
            label="With error",
            options=[
                {"value": "a", "label": "Option A"},
                {"value": "b", "label": "Option B"},
            ],
            error_text="Please select an option to continue",
            disabled=True,
        ),
        cls="grid w-full max-w-sm gap-6"
    )


@with_code
def form_integration_example():
    return Card(
        CardHeader(
            CardTitle("Contact Preference"),
            CardDescription("How should we reach you?")
        ),
        CardContent(
            Form(
                (contact := Signal("contact", "")),
                RadioGroupWithLabel(
                    label="Preferred method",
                    options=[
                        {"value": "email", "label": "Email"},
                        {"value": "phone", "label": "Phone"},
                        {"value": "post", "label": "Postal mail"},
                    ],
                    signal=contact,
                    required=True,
                ),
                Button(
                    "Submit",
                    type="submit",
                    data_attr_disabled=~contact,
                    data_on_click=(js("alert(`Preference: ${$contact}`)"), dict(prevent=True)),
                    cls="w-full mt-4"
                ),
            )
        ),
        cls="max-w-sm"
    )


@with_code
def custom_cards_example():
    deploy = Signal("deploy_region", "us-east")

    def RegionCard(value, name, location):
        is_initial = deploy.default == value
        return RadioGroupItem(
            value=value,
            label=Div(
                Icon("lucide:server", cls="size-5 mb-1 text-muted-foreground"),
                P(name, cls="font-semibold text-sm"),
                P(location, cls="text-xs text-muted-foreground"),
                data_selected="true" if is_initial else "false",
                data_attr_data_selected=deploy.eq(value).if_("true", "false"),
                cls="flex flex-col items-center p-4 border-2 rounded-lg text-center transition-all hover:bg-accent border-border data-[selected=true]:border-primary data-[selected=true]:ring-2 data-[selected=true]:ring-ring/20",
            ),
        )

    return Div(
        deploy,
        P("Deploy to", cls="text-sm font-medium mb-3"),
        RadioGroup(
            RegionCard("us-east", "US East", "Virginia"),
            RegionCard("eu-west", "EU West", "Ireland"),
            RegionCard("ap-south", "Asia Pacific", "Singapore"),
            value="us-east",
            signal=deploy,
            hide_indicators=True,
            cls="grid grid-cols-3 gap-3",
        ),
        P(
            "Region: ",
            Code(data_text=deploy),
            cls="text-sm text-muted-foreground mt-3"
        ),
        cls="max-w-md"
    )


@with_code
def plan_selector_example():
    plan = Signal("hosting_plan", "starter")

    price = match(plan, starter="$9/mo", pro="$29/mo", business="$99/mo")
    desc = match(plan, starter="1 project, 1GB storage, community support",
                 pro="10 projects, 50GB storage, priority support",
                 business="Unlimited projects, 500GB, dedicated support")

    return Div(
        plan,
        RadioGroup(
            RadioGroupItem(value="starter", label="Starter"),
            RadioGroupItem(value="pro", label="Pro"),
            RadioGroupItem(value="business", label="Business"),
            value="starter",
            signal=plan,
            cls="flex gap-4",
        ),
        Div(
            Span(data_text=price, cls="text-sm font-semibold"),
            Span(" — "),
            Span(data_text=desc, cls="text-sm text-muted-foreground"),
            cls="mt-1",
        ),
        cls="grid gap-2 w-full max-w-md",
    )


API_REFERENCE = build_api_reference(
    components=[
        Component("RadioGroup", "Container that manages a single selection across contained items"),
        Component("RadioGroupItem", "Individual option; provide a unique value and label content"),
        Component("RadioGroupWithLabel", "Convenience wrapper that renders a labelled group from an options list"),
    ]
)


EXAMPLES_DATA = [
    {"fn": default_example, "title": "Default", "description": "Bare RadioGroup with RadioGroupItem and reactive signal display"},
    {"fn": horizontal_layout_example, "title": "Horizontal Layout", "description": "Radio buttons arranged in a row with helper text"},
    {"fn": states_example, "title": "States", "description": "Disabled, required, and error states"},
    {"fn": form_integration_example, "title": "Form Integration", "description": "Contact preference form with conditional submit button"},
    {"fn": custom_cards_example, "title": "Custom Cards", "description": "Hidden indicators with custom card labels and selection styling"},
    {"fn": plan_selector_example, "title": "Plan Selector", "description": "Detail panel updates with price and features per selection [match(), data_text]"},
]


def create_radio_group_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)
