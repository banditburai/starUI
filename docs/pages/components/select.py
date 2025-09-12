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

from starhtml import Div, P, Input, Label, Icon, Span, H2, H3, Form, Code
from starhtml.datastar import (
    ds_on_click, ds_show, ds_text, ds_signals, value,
    ds_bind, ds_disabled, ds_on_change, ds_effect, ds_class
)
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


def examples():
    
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
            initial_value="pst"
        )

    yield ComponentPreview(
        grouped_options_select_example(),
        grouped_options_select_example.code,
        title="Grouped Options",
        description="Organize options into logical groups"
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
                        ds_on_click="evt.preventDefault(); alert(`Country: ${$country_form_value}, Language: ${$language_form_value}`)"
                    ),
                    cls="space-y-4"
                )
            ),
            cls="max-w-md"
        )

    yield ComponentPreview(
        form_integration_select_example(),
        form_integration_select_example.code,
        title="Form Integration",
        description="Select with labels, helper text, and form submission"
    )
    
    # Dynamic filtering example
    @with_code
    def product_filtering_select_example():
        return Card(
            CardHeader(
                CardTitle("Product Filter"),
                CardDescription("Find the perfect product for your needs")
            ),
            CardContent(
                Div(
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
                        ds_on_click="alert(`Searching: Category=${$category_filter_value || 'All Categories'}, Price=${$price_filter_label || 'All Prices'}, Sort=${$sort_filter_label || 'Relevance'}`)"
                    ),
                    Div(
                        Div(
                            Badge(
                                ds_text("$category_filter_value"),
                                variant="secondary"
                            ),
                            ds_show("$category_filter_value !== 'All Categories'")
                        ),
                        Div(
                            Badge(
                                ds_text("$price_filter_label || 'All Prices'"),
                                variant="secondary"
                            ),
                            ds_show("$price_filter_value !== 'all'")
                        ),
                        Div(
                            Badge(
                                ds_text("'Sort: ' + ($sort_filter_label || 'Relevance')"),
                                variant="secondary"
                            ),
                            ds_show("$sort_filter_value !== 'relevance'")
                        ),
                        cls="flex flex-col gap-1 mt-4",
                        ds_show="$category_filter_value !== 'All Categories' || $price_filter_value !== 'all' || $sort_filter_value !== 'relevance'"
                    ),
                    ds_signals(
                        price_filter_value=value("all"),
                        price_filter_label=value("All Prices"),
                        sort_filter_value=value("relevance"),
                        sort_filter_label=value("Relevance"),
                        category_filter_value=value("All Categories")
                    ),
                    cls="space-y-3"
                )
            ),
            cls="w-full max-w-md"
        )

    yield ComponentPreview(
        product_filtering_select_example(),
        product_filtering_select_example.code,
        title="Product Filtering",
        description="Multi-select filtering system with active filter display"
    )
    
    # Dependent selects
    @with_code
    def dependent_selects_example():
        return Card(
            CardHeader(
                CardTitle("Location Selection"),
                CardDescription("Choose your location details")
            ),
            CardContent(
                Form(
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
                                ds_disabled("!$location_country_value"),
                                cls="w-full"
                            ),
                            SelectContent(
                                # US States
                                Div(
                                    SelectItem("ca", "California"),
                                    SelectItem("tx", "Texas"),
                                    SelectItem("ny", "New York"),
                                    SelectItem("fl", "Florida"),
                                    ds_show("$location_country_value === 'us'")
                                ),
                                # Canadian Provinces
                                Div(
                                    SelectItem("on", "Ontario"),
                                    SelectItem("qc", "Quebec"),
                                    SelectItem("bc", "British Columbia"),
                                    SelectItem("ab", "Alberta"),
                                    ds_show("$location_country_value === 'ca'")
                                ),
                                # Mexican States
                                Div(
                                    SelectItem("mx_city", "Mexico City"),
                                    SelectItem("jal", "Jalisco"),
                                    SelectItem("nl", "Nuevo León"),
                                    SelectItem("ver", "Veracruz"),
                                    ds_show("$location_country_value === 'mx'")
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
                                    ds_text("($location_state_label && $location_country_label ? $location_state_label + ', ' + $location_country_label : $location_country_label) || 'Not selected'"),
                                    cls="text-sm font-medium"
                                ),
                                cls="flex-1"
                            ),
                            cls="flex gap-2 items-start"
                        ),
                        cls="mt-4 p-3 bg-muted/50 rounded-md border"
                    ),
                    ds_signals(
                        location_country_value=value(""),
                        location_country_label=value(""),
                        location_state_value=value(""),
                        location_state_label=value("")
                    ),
                    ds_effect("""
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

    yield ComponentPreview(
        dependent_selects_example(),
        dependent_selects_example.code,
        title="Dependent Selects",
        description="Cascading selects that update based on parent selection"
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
                    initial_value=initial_value,
                    initial_label=initial_label,
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
                    ds_on_click="alert(`Roles updated:\\nJohn: ${$user1_role_label}\\nJane: ${$user2_role_label}\\nBob: ${$user3_role_label}`)"
                )
            ),
            cls="max-w-2xl"
        )

    yield ComponentPreview(
        role_management_select_example(),
        role_management_select_example.code,
        title="Role Management",
        description="Manage multiple user roles with inline selects"
    )


def create_select_docs():
    
    # For Select, users benefit most from understanding the building blocks
    # and composition rather than container props, so we show components.
    api_reference = build_api_reference(
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
    
    # Hero example - Interactive preferences panel
    @with_code
    def hero_select_example():
        return Card(
            CardHeader(
                CardTitle("Quick Settings"),
                CardDescription("Configure your preferences")
            ),
            CardContent(
                Div(
                    Div(
                        SelectWithLabel(
                            label="Theme",
                            options=[
                                ("light", "Light"),
                                ("dark", "Dark"),
                                ("auto", "System")
                            ],
                            value="auto",
                            signal="theme",
                            select_cls="w-full"
                        ),
                        SelectWithLabel(
                            label="Language",
                            options=[
                                ("en", "English"),
                                ("es", "Español"),
                                ("fr", "Français"),
                                ("de", "Deutsch"),
                                ("zh", "中文"),
                                ("ja", "日本語")
                            ],
                            value="en",
                            signal="language",
                            select_cls="w-full"
                        ),
                        SelectWithLabel(
                            label="Timezone",
                            options=[
                                {"group": "Americas", "items": [
                                    ("est", "Eastern Time"),
                                    ("cst", "Central Time"),
                                    ("pst", "Pacific Time")
                                ]},
                                {"group": "Europe", "items": [
                                    ("gmt", "GMT"),
                                    ("cet", "Central European")
                                ]}
                            ],
                            value="pst",
                            signal="timezone_hero",
                            select_cls="w-full"
                        ),
                        cls="grid grid-cols-1 md:grid-cols-3 gap-4"
                    ),
                    Div(
                        P(
                            "Your settings: ",
                            cls="text-sm text-muted-foreground mb-2"
                        ),
                        Div(
                            Badge(
                                Icon("lucide:palette", cls="h-3 w-3 mr-1"),
                                ds_text("$theme_label || 'System'"),
                                variant="outline"
                            ),
                            Badge(
                                Icon("lucide:globe", cls="h-3 w-3 mr-1"),
                                ds_text("$language_label || 'English'"),
                                variant="outline"
                            ),
                            Badge(
                                Icon("lucide:clock", cls="h-3 w-3 mr-1"),
                                ds_text("$timezone_hero_label || 'Pacific Time'"),
                                variant="outline"
                            ),
                            cls="flex flex-wrap gap-2"
                        ),
                        cls="mt-6 pt-6 border-t"
                    ),
                    ds_signals(
                        theme_value=value("auto"),
                        theme_label=value("System"),
                        language_value=value("en"),
                        language_label=value("English"),
                        timezone_hero_value=value("pst"),
                        timezone_hero_label=value("Pacific Time")
                    )
                )
            ),
            cls="w-full max-w-2xl mx-auto"
        )

    hero_example = ComponentPreview(
        hero_select_example(),
        hero_select_example.code,
        copy_button=True
    )
    
    return auto_generate_page(
        TITLE,
        DESCRIPTION,
        list(examples()),
        cli_command="star add select",
        api_reference=api_reference,
        hero_example=hero_example,
        component_slug="select"
    )