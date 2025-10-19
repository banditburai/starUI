TITLE = "Select"
DESCRIPTION = "Displays a list of options for the user to pick from—triggered by a button."
CATEGORY = "form"
ORDER = 20
STATUS = "stable"

from starhtml import Div, P, Label, Icon, Span, Form, Signal
from starui.registry.components.select import (
    Select, SelectTrigger, SelectValue, SelectContent, SelectItem,
    SelectGroup, SelectLabel, SelectWithLabel
)
from starui.registry.components.button import Button
from starui.registry.components.card import Card, CardHeader, CardContent, CardTitle, CardDescription
from starui.registry.components.badge import Badge
from utils import auto_generate_page, with_code, Component, build_api_reference


@with_code
def grouped_options_select_example():
    return SelectWithLabel(
        label="Timezone",
        options=[
            {"group": "North America", "items": [
                ("est", "Eastern Time (EST)"),
                ("cst", "Central Time (CST)"),
                ("mst", "Mountain Time (MST)"),
                ("pst", "Pacific Time (PST)")
            ]},
            {"group": "Europe", "items": [
                ("gmt", "Greenwich Mean Time (GMT)"),
                ("cet", "Central European Time (CET)"),
                ("eet", "Eastern European Time (EET)")
            ]},
            {"group": "Asia", "items": [
                ("jst", "Japan Standard Time (JST)"),
                ("cst_china", "China Standard Time (CST)"),
                ("ist", "India Standard Time (IST)")
            ]}
        ],
        value="pst",
        placeholder="Select a timezone",
        select_cls="w-[240px]"
    )


@with_code
def form_integration_select_example():
    return Card(
        CardContent(
            Form(
                SelectWithLabel(
                    label="Country",
                    options=[
                        ("us", "United States"),
                        ("uk", "United Kingdom"),
                        ("ca", "Canada"),
                        ("au", "Australia"),
                        ("de", "Germany"),
                        ("fr", "France"),
                        ("jp", "Japan")
                    ],
                    placeholder="Choose your country",
                    helper_text="Select your country of residence",
                    required=True,
                    signal="country_form",
                    select_cls="w-full"
                ),
                SelectWithLabel(
                    label="Preferred Language",
                    options=[
                        {"group": "Popular", "items": [("en", "English"), ("es", "Spanish"), ("zh", "Chinese")]},
                        {"group": "European", "items": [("fr", "French"), ("de", "German"), ("it", "Italian")]},
                        {"group": "Other", "items": [("ja", "Japanese"), ("ko", "Korean"), ("ar", "Arabic")]}
                    ],
                    value="en",
                    helper_text="We'll use this for communication",
                    signal="language_form",
                    select_cls="w-full"
                ),
                Button(
                    "Save Preferences",
                    type="submit",
                    cls="w-full mt-4",
                    data_on_click="evt.preventDefault(); alert(`Country: ${$country_form_value}, Language: ${$language_form_value}`)"
                ),
                cls="space-y-4"
            )
        ),
        cls="max-w-md"
    )


@with_code
def product_filtering_select_example():
    category_value = Signal("category_filter_value", "")
    category_label = Signal("category_filter_label", "")
    price_value = Signal("price_filter_value", "")
    sort_value = Signal("sort_filter_value", "")
    sort_label = Signal("sort_filter_label", "")

    has_filters = category_value | price_value | sort_value

    price_formatted = price_value.if_(
        (price_value == "0-25").if_(
            "Under " + "$" + price_value.split("-")[1],
            (price_value == "250+").if_(
                "Over " + "$" + price_value.replace("+", ""),
                "$" + price_value.split("-")[0] + " - " + "$" + price_value.split("-")[1]
            )
        ),
        ""
    )

    return Card(
        CardHeader(
            CardTitle("Product Filter"),
            CardDescription("Find the perfect product for your needs")
        ),
        CardContent(
            Div(
                category_value, category_label, price_value, sort_value, sort_label,
                SelectWithLabel(
                    label="Category",
                    options=[
                        "Electronics",
                        "Clothing",
                        "Books",
                        "Home & Garden",
                        "Sports"
                    ],
                    placeholder="All Categories",
                    signal="category_filter",
                    select_cls="w-full"
                ),
                Div(
                    Label("Price Range", cls="block text-sm font-medium mb-1.5"),
                    Select(
                        SelectTrigger(
                            SelectValue(
                                placeholder="All Prices",
                                data_text=price_formatted.or_("All Prices")
                            ),
                            cls="w-full"
                        ),
                        SelectContent(
                            SelectItem("Under $25", value="0-25"),
                            SelectItem("$25 - $50", value="25-50"),
                            SelectItem("$50 - $100", value="50-100"),
                            SelectItem("$100 - $250", value="100-250"),
                            SelectItem("Over $250", value="250+"),
                        ),
                        signal="price_filter"
                    ),
                    cls="space-y-1.5"
                ),
                SelectWithLabel(
                    label="Sort By",
                    options=[
                        ("price-low", "Price: Low to High"),
                        ("price-high", "Price: High to Low"),
                        ("rating", "Customer Rating"),
                        ("newest", "Newest First")
                    ],
                    placeholder="Relevance",
                    signal="sort_filter",
                    select_cls="w-full"
                ),
                Button(
                    Icon("lucide:search", cls="h-4 w-4 mr-2"),
                    "Apply Filters",
                    cls="w-full mt-4",
                    data_on_click="alert(`Searching: Category=${$category_filter_value || 'All'}, Price=${$price_filter_value || 'All'}, Sort=${$sort_filter_label || 'Relevance'}`)"
                ),
                Div(
                    Div(
                        Badge(data_text=category_label, variant="secondary"),
                        data_show=category_value
                    ),
                    Div(
                        Badge(data_text=price_formatted, variant="secondary"),
                        data_show=price_value
                    ),
                    Div(
                        Badge(data_text="Sort: " + sort_label, variant="secondary"),
                        data_show=sort_value
                    ),
                    cls="flex flex-col gap-1 mt-4",
                    data_show=has_filters
                ),
                cls="space-y-3"
            )
        ),
        cls="w-full max-w-md"
    )


@with_code
def dependent_selects_example():
    country_value = Signal("location_country_value", "")
    country_label = Signal("location_country_label", "")
    state_value = Signal("location_state_value", "")
    state_label = Signal("location_state_label", "")

    location_text = (state_label & country_label).if_(
        state_label + ", " + country_label,
        country_label.or_("Not selected")
    )

    invalid_us_state = (country_value == "us") & ~((state_value == "ca") | (state_value == "tx") | (state_value == "ny") | (state_value == "fl"))
    invalid_ca_province = (country_value == "ca") & ~((state_value == "on") | (state_value == "qc") | (state_value == "bc") | (state_value == "ab"))
    invalid_mx_state = (country_value == "mx") & ~((state_value == "mx_city") | (state_value == "jal") | (state_value == "nl") | (state_value == "ver"))

    should_clear_state = ~country_value | invalid_us_state | invalid_ca_province | invalid_mx_state

    return Card(
        CardHeader(
            CardTitle("Location Selection"),
            CardDescription("Choose your location details")
        ),
        CardContent(
            Form(
                country_value, country_label, state_value, state_label,
                Div(
                    Label("Country", cls="text-sm font-medium"),
                    Select(
                        SelectTrigger(
                            SelectValue(placeholder="Select country"),
                            cls="w-full"
                        ),
                        SelectContent(
                            SelectItem("United States", value="us"),
                            SelectItem("Canada", value="ca"),
                            SelectItem("Mexico", value="mx")
                        ),
                        signal="location_country"
                    ),
                    cls="space-y-2"
                ),
                Div(
                    Label("State/Province", cls="text-sm font-medium"),
                    Select(
                        SelectTrigger(
                            SelectValue(placeholder="Select state"),
                            data_attr_disabled=~country_value,
                            cls="w-full"
                        ),
                        SelectContent(
                            Div(
                                SelectItem("California", value="ca"),
                                SelectItem("Texas", value="tx"),
                                SelectItem("New York", value="ny"),
                                SelectItem("Florida", value="fl"),
                                data_show=country_value == "us"
                            ),
                            Div(
                                SelectItem("Ontario", value="on"),
                                SelectItem("Quebec", value="qc"),
                                SelectItem("British Columbia", value="bc"),
                                SelectItem("Alberta", value="ab"),
                                data_show=country_value == "ca"
                            ),
                            Div(
                                SelectItem("Mexico City", value="mx_city"),
                                SelectItem("Jalisco", value="jal"),
                                SelectItem("Nuevo León", value="nl"),
                                SelectItem("Veracruz", value="ver"),
                                data_show=country_value == "mx"
                            )
                        ),
                        signal="location_state"
                    ),
                    cls="space-y-2"
                ),
                Div(
                    Div(
                        Icon("lucide:map-pin", cls="h-4 w-4 text-muted-foreground mt-0.5 flex-shrink-0"),
                        Div(
                            P("Location", cls="text-xs text-muted-foreground mb-0.5"),
                            P(data_text=location_text, cls="text-sm font-medium"),
                            cls="flex-1"
                        ),
                        cls="flex gap-2 items-start"
                    ),
                    cls="mt-4 p-3 bg-muted/50 rounded-md border"
                ),
                data_effect=[
                    state_value.set(should_clear_state.if_("", state_value)),
                    state_label.set(should_clear_state.if_("", state_label))
                ],
                cls="space-y-4"
            )
        ),
        cls="w-full max-w-md"
    )


@with_code
def role_management_select_example():
    users = [
        {"name": "John Doe", "email": "john@example.com", "role": "editor", "role_label": "Editor", "signal": "user1_role"},
        {"name": "Jane Smith", "email": "jane@example.com", "role": "viewer", "role_label": "Viewer", "signal": "user2_role"},
        {"name": "Bob Wilson", "email": "bob@example.com", "role": "admin", "role_label": "Admin", "signal": "user3_role"}
    ]

    signals = []
    for user in users:
        signals.extend([
            Signal(f"{user['signal']}_value", user['role']),
            Signal(f"{user['signal']}_label", user['role_label'])
        ])

    def create_user_row(user):
        return Div(
            Div(
                P(user['name'], cls="font-medium"),
                P(user['email'], cls="text-sm text-muted-foreground"),
                cls="flex-1"
            ),
            Select(
                SelectTrigger(
                    SelectValue(placeholder="Select role"),
                    cls="w-[160px]"
                ),
                SelectContent(
                    SelectItem("Viewer", value="viewer"),
                    SelectItem("Editor", value="editor"),
                    SelectItem("Admin", value="admin"),
                    SelectItem("Owner", value="owner", disabled=True)
                ),
                value=user['role'],
                label=user['role_label'],
                signal=user['signal']
            ),
            cls="flex items-center justify-between gap-6 px-4 py-3 first:pt-4 last:pb-4"
        )

    return Card(
        CardHeader(
            CardTitle("User Management"),
            CardDescription("Manage user roles and permissions")
        ),
        CardContent(
            Div(
                *signals,
                *[create_user_row(user) for user in users],
                cls="divide-y border rounded-lg"
            ),
            Button(
                "Save Changes",
                cls="w-full mt-4",
                data_on_click="alert(`Roles updated:\\nJohn: ${$user1_role_label}\\nJane: ${$user2_role_label}\\nBob: ${$user3_role_label}`)"
            )
        ),
        cls="max-w-2xl"
    )


EXAMPLES_DATA = [
    {"title": "Grouped Options", "description": "Organize options into logical groups", "fn": grouped_options_select_example},
    {"title": "Form Integration", "description": "Select with labels, helper text, and form submission", "fn": form_integration_select_example},
    {"title": "Product Filtering", "description": "Multi-select filtering system with active filter display", "fn": product_filtering_select_example},
    {"title": "Dependent Selects", "description": "Cascading selects that update based on parent selection", "fn": dependent_selects_example},
    {"title": "Role Management", "description": "Manage multiple user roles with inline selects", "fn": role_management_select_example},
]

API_REFERENCE = build_api_reference(
    components=[
        Component("Select", "Main container managing selected state via Datastar signals"),
        Component("SelectTrigger", "Button that opens the dropdown menu"),
        Component("SelectValue", "Displays current selection or placeholder"),
        Component("SelectContent", "Dropdown panel listing available items"),
        Component("SelectItem", "Individual selectable option with value and label"),
        Component("SelectGroup", "Group related options for easier scanning"),
        Component("SelectLabel", "Label heading for a group of options"),
        Component("SelectWithLabel", "Convenience wrapper with label, helper, and error text")
    ]
)


def create_select_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)