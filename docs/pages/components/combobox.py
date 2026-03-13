TITLE = "Combobox"
DESCRIPTION = "Autocomplete input with a searchable dropdown list of options."
CATEGORY = "form"
ORDER = 22
STATUS = "stable"

from starhtml import Div, P, Code, Form, Signal, Icon
from components.combobox import (
    Combobox, ComboboxTrigger, ComboboxContent, ComboboxItem,
    ComboboxEmpty, ComboboxGroup, ComboboxSeparator, ComboboxWithLabel
)
from components.button import Button
from components.card import Card, CardHeader, CardContent, CardTitle, CardDescription
from utils import auto_generate_page, with_code, Component, build_api_reference


@with_code
def default_example():
    cb = Combobox(  #: hide
        ComboboxTrigger(placeholder="Select currency...", cls="w-[200px]"),
        ComboboxContent(
            ComboboxEmpty("No currency found."),
            ComboboxItem("US Dollar (USD)", value="usd"),
            ComboboxItem("Euro (EUR)", value="eur"),
            ComboboxItem("British Pound (GBP)", value="gbp"),
            ComboboxItem("Japanese Yen (JPY)", value="jpy"),
            ComboboxItem("Swiss Franc (CHF)", value="chf"),
            ComboboxItem("Canadian Dollar (CAD)", value="cad"),
        ),
        signal="cb_currency",
        value="eur",
        label="Euro (EUR)",
    )  #: hide
    return Div(
        cb,
        P(
            "Selected: ",
            Code(data_text=cb.selected.or_("none")),  #: hide
            cls="text-sm text-muted-foreground mt-3"
        ),
        cls="max-w-sm"
    )


@with_code
def with_icons_example():
    return Combobox(
        ComboboxTrigger(placeholder="Set status...", cls="w-[200px]"),
        ComboboxContent(
            ComboboxEmpty("No status found."),
            ComboboxItem(
                Icon("lucide:circle", cls="!size-3.5 text-muted-foreground fill-muted-foreground/30"),
                "Backlog", value="backlog",
            ),
            ComboboxItem(
                Icon("lucide:circle-dashed", cls="!size-3.5 text-blue-500"),
                "Todo", value="todo",
            ),
            ComboboxItem(
                Icon("lucide:timer", cls="!size-3.5 text-yellow-500"),
                "In Progress", value="in-progress",
            ),
            ComboboxItem(
                Icon("lucide:check-circle-2", cls="!size-3.5 text-green-500"),
                "Done", value="done",
            ),
            ComboboxItem(
                Icon("lucide:x-circle", cls="!size-3.5 text-red-500"),
                "Cancelled", value="cancelled",
            ),
        ),
        signal="cb_status",
    )


@with_code
def multiselect_example():
    cb = Combobox(  #: hide
        ComboboxTrigger(placeholder="Add genres...", cls="w-[300px]"),
        ComboboxContent(
            ComboboxEmpty("No genres found."),
            ComboboxItem("Jazz", value="jazz"),
            ComboboxItem("Electronic", value="electronic"),
            ComboboxItem("Classical", value="classical"),
            ComboboxItem("Hip Hop", value="hiphop"),
            ComboboxItem("Rock", value="rock"),
            ComboboxItem("Folk", value="folk"),
        ),
        signal="cb_genres",
        multiple=True,
        value=["jazz", "electronic"],
        label=["Jazz", "Electronic"],
    )  #: hide
    return Div(
        cb,
        P(
            "Selected: ",
            Code(data_text=cb.selected.join(", ").or_("none")),  #: hide
            cls="text-sm text-muted-foreground mt-3"
        ),
        cls="max-w-sm"
    )


@with_code
def grouped_example():
    return Combobox(
        ComboboxTrigger(placeholder="Search timezone...", cls="w-[280px]"),
        ComboboxContent(
            ComboboxEmpty("No timezone found."),
            ComboboxGroup(
                "North America",
                ComboboxItem("Eastern Time (EST)", value="est"),
                ComboboxItem("Central Time (CST)", value="cst"),
                ComboboxItem("Mountain Time (MST)", value="mst"),
                ComboboxItem("Pacific Time (PST)", value="pst"),
            ),
            ComboboxSeparator(),
            ComboboxGroup(
                "Europe",
                ComboboxItem("Greenwich Mean Time (GMT)", value="gmt"),
                ComboboxItem("Central European Time (CET)", value="cet"),
                ComboboxItem("Eastern European Time (EET)", value="eet"),
            ),
            ComboboxSeparator(),
            ComboboxGroup(
                "Asia",
                ComboboxItem("Japan Standard Time (JST)", value="jst"),
                ComboboxItem("China Standard Time (CST)", value="cst_cn"),
                ComboboxItem("India Standard Time (IST)", value="ist"),
            ),
        ),
        signal="cb_tz",
    )


@with_code
def keyword_search_example():
    return Combobox(
        ComboboxTrigger(placeholder="Search countries...", cls="w-[240px]"),
        ComboboxContent(
            ComboboxEmpty("No country found."),
            ComboboxItem("United States", value="us", keywords="america usa"),
            ComboboxItem("United Kingdom", value="uk", keywords="britain england gb"),
            ComboboxItem("Deutschland", value="de", keywords="germany"),
            ComboboxItem("Nihon", value="jp", keywords="japan nippon"),
            ComboboxItem("Brasil", value="br", keywords="brazil"),
            ComboboxItem("Schweiz", value="ch", keywords="switzerland suisse"),
        ),
        signal="cb_country",
    )


@with_code
def disabled_items_example():
    return Combobox(
        ComboboxTrigger(placeholder="Select plan...", cls="w-[220px]"),
        ComboboxContent(
            ComboboxEmpty("No plan found."),
            ComboboxItem("Free", value="free"),
            ComboboxItem("Starter", value="starter"),
            ComboboxItem("Pro", value="pro"),
            ComboboxItem("Enterprise", value="enterprise", disabled=True),
        ),
        signal="cb_plan",
    )


@with_code
def states_example():
    return Div(
        ComboboxWithLabel(
            label="Placeholder",
            options=["Email", "Slack", "Webhook", "SMS"],
            placeholder="Select channel...",
        ),
        ComboboxWithLabel(
            label="Disabled",
            options=["Email", "Slack", "Webhook", "SMS"],
            value="Slack",
            disabled=True,
        ),
        ComboboxWithLabel(
            label="Required",
            options=["Email", "Slack", "Webhook", "SMS"],
            placeholder="Select channel...",
            required=True,
        ),
        ComboboxWithLabel(
            label="Error",
            options=["Email", "Slack", "Webhook", "SMS"],
            placeholder="Select channel...",
            error_text="A notification channel is required",
        ),
        cls="grid w-full max-w-sm gap-6"
    )


@with_code
def form_example():
    role_value = Signal("cb_role_value", "")  #: hide
    return Card(
        CardHeader(
            CardTitle("Invite Member"),
            CardDescription("Add someone to the project")
        ),
        CardContent(
            Form(
                role_value,  #: hide
                ComboboxWithLabel(
                    label="Role",
                    options=[
                        ("viewer", "Viewer"),
                        ("editor", "Editor"),
                        ("admin", "Admin"),
                        ("owner", "Owner"),
                    ],
                    placeholder="Search roles...",
                    required=True,
                    signal="cb_role",
                    helper_text="Select the permission level for the new member",
                    trigger_cls="w-full",
                ),
                Button(
                    "Send Invite",
                    type="submit",
                    cls="w-full mt-4",
                    data_attr_disabled=~role_value,
                ),
                cls="space-y-4"
            )
        ),
        cls="max-w-md"
    )


EXAMPLES_DATA = [
    {"fn": default_example, "title": "Default", "description": "Searchable currency selector with pre-selected value"},
    {"fn": with_icons_example, "title": "With Icons", "description": "Status selector with colored icons per option"},
    {"fn": multiselect_example, "title": "Multiple Selection", "description": "Multi-select with chips and pre-selected values"},
    {"fn": grouped_example, "title": "Grouped", "description": "Timezone selector with group headings and separators that auto-hide when filtered"},
    {"fn": keyword_search_example, "title": "Keyword Search", "description": "Country selector that matches on hidden keywords like alternate names"},
    {"fn": disabled_items_example, "title": "Disabled Items", "description": "Individual items can be disabled while others remain selectable"},
    {"fn": states_example, "title": "States", "description": "Placeholder, disabled, required, and error states"},
    {"fn": form_example, "title": "Form Integration", "description": "ComboboxWithLabel in a card form with required validation and helper text"},
]

API_REFERENCE = build_api_reference(
    components=[
        Component("Combobox", "Root container managing selection state via Datastar signals"),
        Component("ComboboxTrigger", "Search input with chevron button that opens the dropdown"),
        Component("ComboboxContent", "Popover panel listing filterable options"),
        Component("ComboboxItem", "Individual selectable option with value, label, and check indicator"),
        Component("ComboboxEmpty", "Shown when no items match the search query"),
        Component("ComboboxGroup", "Group related options under a heading"),
        Component("ComboboxSeparator", "Visual divider between items or groups"),
        Component("ComboboxWithLabel", "Convenience wrapper with label, helper text, and error text"),
    ]
)


def create_combobox_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)
