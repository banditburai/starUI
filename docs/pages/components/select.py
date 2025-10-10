"""
Select component documentation - Convention-based functional approach.
Clean, minimal, and easy to extend.
"""

# Component metadata for auto-discovery
TITLE = "Select"
DESCRIPTION = "Displays a list of options for the user to pick from—triggered by a button."
CATEGORY = "form"
ORDER = 20
STATUS = "stable"

from starhtml import Div, P, Input, Label, Icon, Span, H2, H3, Form, Code, Signal, js
from starui.registry.components.select import (
    Select, SelectTrigger, SelectValue, SelectContent, SelectItem,
    SelectGroup, SelectLabel, SelectWithLabel
)
from starui.registry.components.button import Button
from starui.registry.components.card import Card, CardHeader, CardContent, CardTitle, CardDescription
from starui.registry.components.badge import Badge
from starui.registry.components.input import Input as UIInput
from utils import auto_generate_page, with_code, Component, build_api_reference
from widgets.component_preview import ComponentPreview


# ============================================================================
# EXAMPLE FUNCTIONS (decorated with @with_code for markdown generation)
# ============================================================================

# Grouped options
@with_code
def grouped_options_select_example():
    return Select(
        SelectTrigger(
            SelectValue(placeholder="Select a timezone"),
            cls="w-[240px]"
        ),
        SelectContent(
            SelectGroup(
                SelectLabel("North America"),
                SelectItem("est", "Eastern Time (EST)"),
                SelectItem("cst", "Central Time (CST)"),
                SelectItem("mst", "Mountain Time (MST)"),
                SelectItem("pst", "Pacific Time (PST)")
            ),
            SelectGroup(
                SelectLabel("Europe"),
                SelectItem("gmt", "Greenwich Mean Time (GMT)"),
                SelectItem("cet", "Central European Time (CET)"),
                SelectItem("eet", "Eastern European Time (EET)")
            ),
            SelectGroup(
                SelectLabel("Asia"),
                SelectItem("jst", "Japan Standard Time (JST)"),
                SelectItem("cst_china", "China Standard Time (CST)"),
                SelectItem("ist", "India Standard Time (IST)")
            )
        ),
        default_value="pst"
    )


# With label and validation
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
                    data_on_click=js("evt.preventDefault(); alert(`Country: ${$country_form_value}, Language: ${$language_form_value}`)")
                ),
                cls="space-y-4"
            )
        ),
        cls="max-w-md"
    )


# Dynamic filtering example
@with_code
def product_filtering_select_example():
    price_filter_value = Signal("price_filter_value", "all")
    price_filter_label = Signal("price_filter_label", "All Prices")
    sort_filter_value = Signal("sort_filter_value", "relevance")
    sort_filter_label = Signal("sort_filter_label", "Relevance")
    category_filter_value = Signal("category_filter_value", "All Categories")

    return Card(
        CardHeader(
            CardTitle("Product Filter"),
            CardDescription("Find the perfect product for your needs")
        ),
        CardContent(
            Div(
                price_filter_value, price_filter_label, sort_filter_value, sort_filter_label, category_filter_value,
                SelectWithLabel(
                    label="Category",
                    options=[
                        "All Categories",
                        "Electronics",
                        "Clothing",
                        "Books",
                        "Home & Garden",
                        "Sports"
                    ],
                    value="All Categories",
                    signal="category_filter",
                    select_cls="w-full"
                ),
                SelectWithLabel(
                    label="Price Range",
                    options=[
                        ("all", "All Prices"),
                        ("0-25", "Under $25"),
                        ("25-50", "$25 - $50"),
                        ("50-100", "$50 - $100"),
                        ("100-250", "$100 - $250"),
                        ("250+", "Over $250")
                    ],
                    value="all",
                    signal="price_filter",
                    select_cls="w-full"
                ),
                SelectWithLabel(
                    label="Sort By",
                    options=[
                        ("relevance", "Relevance"),
                        ("price-low", "Price: Low to High"),
                        ("price-high", "Price: High to Low"),
                        ("rating", "Customer Rating"),
                        ("newest", "Newest First")
                    ],
                    value="relevance",
                    signal="sort_filter",
                    select_cls="w-full"
                ),
                Button(
                    Icon("lucide:search", cls="h-4 w-4 mr-2"),
                    "Apply Filters",
                    cls="w-full mt-4",
                    data_on_click=js("alert(`Searching: Category=${$category_filter_value || 'All Categories'}, Price=${$price_filter_label || 'All Prices'}, Sort=${$sort_filter_label || 'Relevance'}`)")
                ),
                Div(
                    Div(
                        Badge(
                            data_text=js("$category_filter_value"),
                            variant="secondary"
                        ),
                        data_show=js("$category_filter_value !== 'All Categories'")
                    ),
                    Div(
                        Badge(
                            data_text=js("$price_filter_label || 'All Prices'"),
                            variant="secondary"
                        ),
                        data_show=js("$price_filter_value !== 'all'")
                    ),
                    Div(
                        Badge(
                            data_text=js("'Sort: ' + ($sort_filter_label || 'Relevance')"),
                            variant="secondary"
                        ),
                        data_show=js("$sort_filter_value !== 'relevance'")
                    ),
                    cls="flex flex-col gap-1 mt-4",
                    data_show=js("$category_filter_value !== 'All Categories' || $price_filter_value !== 'all' || $sort_filter_value !== 'relevance'")
                ),
                cls="space-y-3"
            )
        ),
        cls="w-full max-w-md"
    )


# Dependent selects
@with_code
def dependent_selects_example():
    location_country_value = Signal("location_country_value", "")
    location_country_label = Signal("location_country_label", "")
    location_state_value = Signal("location_state_value", "")
    location_state_label = Signal("location_state_label", "")

    return Card(
        CardHeader(
            CardTitle("Location Selection"),
            CardDescription("Choose your location details")
        ),
        CardContent(
            Form(
                location_country_value, location_country_label, location_state_value, location_state_label,
                Div(
                    Label("Country", cls="text-sm font-medium"),
                    Select(
                        SelectTrigger(
                            SelectValue(placeholder="Select country"),
                            cls="w-full"
                        ),
                        SelectContent(
                            SelectItem("us", "United States"),
                            SelectItem("ca", "Canada"),
                            SelectItem("mx", "Mexico")
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
                            data_attr_disabled=js("!$location_country_value"),
                            cls="w-full"
                        ),
                        SelectContent(
                            # US States
                            Div(
                                SelectItem("ca", "California"),
                                SelectItem("tx", "Texas"),
                                SelectItem("ny", "New York"),
                                SelectItem("fl", "Florida"),
                                data_show=js("$location_country_value === 'us'")
                            ),
                            # Canadian Provinces
                            Div(
                                SelectItem("on", "Ontario"),
                                SelectItem("qc", "Quebec"),
                                SelectItem("bc", "British Columbia"),
                                SelectItem("ab", "Alberta"),
                                data_show=js("$location_country_value === 'ca'")
                            ),
                            # Mexican States
                            Div(
                                SelectItem("mx_city", "Mexico City"),
                                SelectItem("jal", "Jalisco"),
                                SelectItem("nl", "Nuevo León"),
                                SelectItem("ver", "Veracruz"),
                                data_show=js("$location_country_value === 'mx'")
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
                            P(
                                data_text=js("($location_state_label && $location_country_label ? $location_state_label + ', ' + $location_country_label : $location_country_label) || 'Not selected'"),
                                cls="text-sm font-medium"
                            ),
                            cls="flex-1"
                        ),
                        cls="flex gap-2 items-start"
                    ),
                    cls="mt-4 p-3 bg-muted/50 rounded-md border"
                ),
                data_effect=js("""
                    // Reset state when country changes or is cleared
                    if (!$location_country_value ||
                        ($location_country_value && $location_state_value &&
                         (($location_country_value === 'us' && !['ca', 'tx', 'ny', 'fl'].includes($location_state_value)) ||
                          ($location_country_value === 'ca' && !['on', 'qc', 'bc', 'ab'].includes($location_state_value)) ||
                          ($location_country_value === 'mx' && !['mx_city', 'jal', 'nl', 'ver'].includes($location_state_value))))) {
                        $location_state_value = '';
                        $location_state_label = '';
                    }
                """),
                cls="space-y-4"
            )
        ),
        cls="w-full max-w-md"
    )


@with_code
def role_management_select_example():
    users = [
        ("John Doe", "john@example.com", "editor", "Editor", "user1_role"),
        ("Jane Smith", "jane@example.com", "viewer", "Viewer", "user2_role"),
        ("Bob Wilson", "bob@example.com", "admin", "Admin", "user3_role")
    ]

    def create_user_role_row(name, email, initial_value, initial_label, signal):
        return Div(
            Div(
                P(name, cls="font-medium"),
                P(email, cls="text-sm text-muted-foreground"),
                cls="flex-1"
            ),
            Select(
                SelectTrigger(
                    SelectValue(placeholder="Select role"),
                    cls="w-[160px]"
                ),
                SelectContent(
                    SelectItem("viewer", "Viewer"),
                    SelectItem("editor", "Editor"),
                    SelectItem("admin", "Admin"),
                    SelectItem("owner", "Owner", disabled=True)
                ),
                default_value=initial_value,
                default_label=initial_label,
                signal=signal
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
                *[create_user_role_row(name, email, initial_value, initial_label, signal)
                  for name, email, initial_value, initial_label, signal in users],
                cls="divide-y border rounded-lg"
            ),
            Button(
                "Save Changes",
                cls="w-full mt-4",
                data_on_click=js("alert(`Roles updated:\\nJohn: ${$user1_role_label}\\nJane: ${$user2_role_label}\\nBob: ${$user3_role_label}`)")
            )
        ),
        cls="max-w-2xl"
    )


# ============================================================================
# MODULE-LEVEL DATA (for markdown API)
# ============================================================================

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


def examples():
    """Generate all select examples."""
    yield ComponentPreview(
        grouped_options_select_example(),
        grouped_options_select_example.code,
        title="Grouped Options",
        description="Organize options into logical groups"
    )

    yield ComponentPreview(
        form_integration_select_example(),
        form_integration_select_example.code,
        title="Form Integration",
        description="Select with labels, helper text, and form submission"
    )

    yield ComponentPreview(
        product_filtering_select_example(),
        product_filtering_select_example.code,
        title="Product Filtering",
        description="Multi-select filtering system with active filter display"
    )

    yield ComponentPreview(
        dependent_selects_example(),
        dependent_selects_example.code,
        title="Dependent Selects",
        description="Cascading selects that update based on parent selection"
    )

    yield ComponentPreview(
        role_management_select_example(),
        role_management_select_example.code,
        title="Role Management",
        description="Manage multiple user roles with inline selects"
    )


# ============================================================================
# DOCUMENTATION PAGE GENERATION
# ============================================================================


def create_select_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)