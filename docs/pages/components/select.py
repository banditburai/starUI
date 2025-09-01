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
    ds_bind, ds_disabled, ds_on_change, ds_effect, ds_class, toggle
)
from starui.registry.components.select import (
    Select, SelectTrigger, SelectValue, SelectContent, SelectItem,
    SelectGroup, SelectLabel, SelectWithLabel
)
from starui.registry.components.button import Button
from starui.registry.components.card import Card, CardHeader, CardContent, CardTitle, CardDescription
from starui.registry.components.badge import Badge
from starui.registry.components.input import Input as UIInput
from utils import auto_generate_page
from widgets.component_preview import ComponentPreview


def examples():
    """Generate select examples using ComponentPreview with tabs."""
    
    # Basic usage
    yield ComponentPreview(
        Div(
            Select(
                SelectTrigger(
                    SelectValue(placeholder="Select a fruit", signal="fruit"),
                    signal="fruit",
                    width="w-[200px]"
                ),
                SelectContent(
                    SelectItem("apple", "Apple", signal="fruit"),
                    SelectItem("banana", "Banana", signal="fruit"),
                    SelectItem("orange", "Orange", signal="fruit"),
                    SelectItem("grape", "Grape", signal="fruit"),
                    SelectItem("strawberry", "Strawberry", signal="fruit"),
                    signal="fruit"
                ),
                signal="fruit"
            ),
            P(
                "Selected: ",
                Code(ds_text("$fruit_value || 'none'"), cls="ml-2"),
                ds_show("$fruit_value"),
                cls="text-sm text-muted-foreground mt-4"
            ),
            cls="flex flex-col items-center"
        ),
        '''Select(
    SelectTrigger(
        SelectValue(placeholder="Select a fruit", signal="fruit"),
        signal="fruit",
        width="w-[200px]"
    ),
    SelectContent(
        SelectItem("apple", "Apple", signal="fruit"),
        SelectItem("banana", "Banana", signal="fruit"),
        SelectItem("orange", "Orange", signal="fruit"),
        SelectItem("grape", "Grape", signal="fruit"),
        SelectItem("strawberry", "Strawberry", signal="fruit"),
        signal="fruit"
    ),
    signal="fruit"
)''',
        title="Basic Select",
        description="Simple dropdown with options"
    )
    
    # Grouped options
    yield ComponentPreview(
        Select(
            SelectTrigger(
                SelectValue(placeholder="Select a timezone", signal="timezone"),
                signal="timezone",
                width="w-[240px]"
            ),
            SelectContent(
                SelectGroup(
                    SelectLabel("North America"),
                    SelectItem("est", "Eastern Time (EST)", signal="timezone"),
                    SelectItem("cst", "Central Time (CST)", signal="timezone"),
                    SelectItem("mst", "Mountain Time (MST)", signal="timezone"),
                    SelectItem("pst", "Pacific Time (PST)", signal="timezone")
                ),
                SelectGroup(
                    SelectLabel("Europe"),
                    SelectItem("gmt", "Greenwich Mean Time (GMT)", signal="timezone"),
                    SelectItem("cet", "Central European Time (CET)", signal="timezone"),
                    SelectItem("eet", "Eastern European Time (EET)", signal="timezone")
                ),
                SelectGroup(
                    SelectLabel("Asia"),
                    SelectItem("jst", "Japan Standard Time (JST)", signal="timezone"),
                    SelectItem("cst_china", "China Standard Time (CST)", signal="timezone"),
                    SelectItem("ist", "India Standard Time (IST)", signal="timezone")
                ),
                signal="timezone"
            ),
            initial_value="pst",
            signal="timezone"
        ),
        '''Select(
    SelectTrigger(
        SelectValue(placeholder="Select a timezone", signal="timezone"),
        signal="timezone"
    ),
    SelectContent(
        SelectGroup(
            SelectLabel("North America"),
            SelectItem("est", "Eastern Time (EST)", signal="timezone"),
            SelectItem("cst", "Central Time (CST)", signal="timezone"),
            # ... more items
        ),
        SelectGroup(
            SelectLabel("Europe"),
            SelectItem("gmt", "Greenwich Mean Time (GMT)", signal="timezone"),
            # ... more items
        ),
        signal="timezone"
    ),
    initial_value="pst",
    signal="timezone"
)''',
        title="Grouped Options",
        description="Organize options into logical groups"
    )
    
    # With label and validation
    yield ComponentPreview(
        Card(
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
                        ds_on_click="event.preventDefault(); alert(`Country: ${$country_form_value}, Language: ${$language_form_value}`)"
                    ),
                    cls="space-y-4"
                )
            ),
            cls="max-w-md"
        ),
        '''SelectWithLabel(
    label="Country",
    options=[
        ("us", "United States"),
        ("uk", "United Kingdom"),
        ("ca", "Canada"),
        # ... more countries
    ],
    placeholder="Choose your country",
    helper_text="Select your country of residence",
    required=True,
    signal="country_form"
)

SelectWithLabel(
    label="Preferred Language",
    options=[
        {"group": "Popular", "items": [("en", "English"), ("es", "Spanish")]},
        {"group": "European", "items": [("fr", "French"), ("de", "German")]},
    ],
    value="en",
    helper_text="We'll use this for communication",
    signal="language_form"
)''',
        title="Form Integration",
        description="Select with labels, helper text, and form submission"
    )
    
    # Dynamic filtering example
    yield ComponentPreview(
        Card(
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
                        ds_on_click="alert(`Searching: Category=${$category_filter_value}, Price=${$price_filter_label}, Sort=${$sort_filter_label}`)"
                    ),
                    Div(
                        Badge(
                            ds_text("$category_filter_value"),
                            ds_show("$category_filter_value !== 'All Categories'"),
                            variant="secondary"
                        ),
                        Badge(
                            ds_text("$price_filter_label"),
                            ds_show("$price_filter_value !== 'all'"),
                            variant="secondary"
                        ),
                        Badge(
                            ds_text("'Sort: ' + $sort_filter_label"),
                            ds_show("$sort_filter_value !== 'relevance'"),
                            variant="secondary"
                        ),
                        cls="flex gap-2 mt-4 flex-wrap",
                        ds_show="$category_filter_value !== 'All Categories' || $price_filter_value !== 'all' || $sort_filter_value !== 'relevance'"
                    ),
                    cls="space-y-3"
                )
            ),
            cls="max-w-md"
        ),
        '''Card(
    CardContent(
        SelectWithLabel(
            label="Category",
            options=["All Categories", "Electronics", "Clothing", "Books"],
            signal="category_filter"
        ),
        SelectWithLabel(
            label="Price Range",
            options=[
                ("all", "All Prices"),
                ("0-25", "Under $25"),
                ("25-50", "$25 - $50"),
            ],
            signal="price_filter"
        ),
        SelectWithLabel(
            label="Sort By",
            options=[
                ("relevance", "Relevance"),
                ("price-low", "Price: Low to High"),
            ],
            signal="sort_filter"
        ),
        Button("Apply Filters", ds_on_click="applyFilters()"),
        Div(  # Active filters badges
            Badge(ds_text("$category_filter_value"), ds_show="..."),
            Badge(ds_text("$price_filter_label"), ds_show="...")
        )
    )
)''',
        title="Product Filtering",
        description="Multi-select filtering system with active filter display"
    )
    
    # Dependent selects
    yield ComponentPreview(
        Card(
            CardHeader(
                CardTitle("Location Selection"),
                CardDescription("Choose your location details")
            ),
            CardContent(
                Form(
                    SelectWithLabel(
                        label="Country",
                        options=[
                            "United States",
                            "Canada",
                            "Mexico"
                        ],
                        placeholder="Select country first",
                        signal="location_country",
                        select_cls="w-full"
                    ),
                    SelectWithLabel(
                        label="State/Province",
                        options=[],
                        placeholder="Select a country first",
                        signal="location_state",
                        select_cls="w-full",
                        disabled=True
                    ),
                    SelectWithLabel(
                        label="City",
                        options=[],
                        placeholder="Select a state first",
                        signal="location_city",
                        select_cls="w-full",
                        disabled=True
                    ),
                    Div(
                        P(
                            Icon("lucide:map-pin", cls="h-4 w-4 inline mr-1"),
                            "Location: ",
                            Span(
                                ds_text("[$location_city_label, $location_state_label, $location_country_value].filter(Boolean).join(', ') || 'Not selected'"),
                                cls="font-medium"
                            ),
                            cls="text-sm"
                        ),
                        cls="mt-4 p-3 bg-muted rounded-md"
                    ),
                    ds_effect("""
                        // Enable state select when country is selected
                        const stateSelect = document.querySelector('[data-bind*="location_state"]');
                        const citySelect = document.querySelector('[data-bind*="location_city"]');
                        
                        if ($location_country_value) {
                            // In real app, fetch states based on country
                            if (stateSelect) {
                                stateSelect.closest('button').disabled = false;
                            }
                        }
                        
                        if ($location_state_value) {
                            // In real app, fetch cities based on state
                            if (citySelect) {
                                citySelect.closest('button').disabled = false;
                            }
                        }
                    """),
                    cls="space-y-4"
                )
            ),
            cls="max-w-md"
        ),
        '''// Dependent selects that update based on parent selection
Form(
    SelectWithLabel(
        label="Country",
        options=["United States", "Canada", "Mexico"],
        signal="location_country"
    ),
    SelectWithLabel(
        label="State/Province",
        options=[],  // Populated based on country
        signal="location_state",
        disabled=True  // Enabled when country selected
    ),
    SelectWithLabel(
        label="City",
        options=[],  // Populated based on state
        signal="location_city",
        disabled=True  // Enabled when state selected
    ),
    ds_effect("""
        // Enable/disable and populate dependent selects
        if ($location_country_value) {
            // Fetch and populate states
        }
        if ($location_state_value) {
            // Fetch and populate cities
        }
    """)
)''',
        title="Dependent Selects",
        description="Cascading selects that update based on parent selection"
    )
    
    # Multi-action select
    yield ComponentPreview(
        Card(
            CardHeader(
                CardTitle("User Management"),
                CardDescription("Manage user roles and permissions")
            ),
            CardContent(
                Div(
                    Div(
                        Div(
                            P("John Doe", cls="font-medium"),
                            P("john@example.com", cls="text-sm text-muted-foreground"),
                            cls="flex-1"
                        ),
                        Select(
                            SelectTrigger(
                                SelectValue(placeholder="Select role", signal="user1_role"),
                                signal="user1_role",
                                width="w-[140px]"
                            ),
                            SelectContent(
                                SelectItem("viewer", "Viewer", signal="user1_role"),
                                SelectItem("editor", "Editor", signal="user1_role"),
                                SelectItem("admin", "Admin", signal="user1_role"),
                                SelectItem("owner", "Owner", signal="user1_role", disabled=True),
                                signal="user1_role"
                            ),
                            initial_value="editor",
                            signal="user1_role"
                        ),
                        cls="flex items-center justify-between p-3 border rounded-md"
                    ),
                    Div(
                        Div(
                            P("Jane Smith", cls="font-medium"),
                            P("jane@example.com", cls="text-sm text-muted-foreground"),
                            cls="flex-1"
                        ),
                        Select(
                            SelectTrigger(
                                SelectValue(placeholder="Select role", signal="user2_role"),
                                signal="user2_role",
                                width="w-[140px]"
                            ),
                            SelectContent(
                                SelectItem("viewer", "Viewer", signal="user2_role"),
                                SelectItem("editor", "Editor", signal="user2_role"),
                                SelectItem("admin", "Admin", signal="user2_role"),
                                SelectItem("owner", "Owner", signal="user2_role", disabled=True),
                                signal="user2_role"
                            ),
                            initial_value="viewer",
                            signal="user2_role"
                        ),
                        cls="flex items-center justify-between p-3 border rounded-md"
                    ),
                    Div(
                        Div(
                            P("Bob Wilson", cls="font-medium"),
                            P("bob@example.com", cls="text-sm text-muted-foreground"),
                            cls="flex-1"
                        ),
                        Select(
                            SelectTrigger(
                                SelectValue(placeholder="Select role", signal="user3_role"),
                                signal="user3_role",
                                width="w-[140px]"
                            ),
                            SelectContent(
                                SelectItem("viewer", "Viewer", signal="user3_role"),
                                SelectItem("editor", "Editor", signal="user3_role"),
                                SelectItem("admin", "Admin", signal="user3_role"),
                                SelectItem("owner", "Owner", signal="user3_role", disabled=True),
                                signal="user3_role"
                            ),
                            initial_value="admin",
                            signal="user3_role"
                        ),
                        cls="flex items-center justify-between p-3 border rounded-md"
                    ),
                    Button(
                        "Save Changes",
                        cls="w-full mt-4",
                        ds_on_click="alert(`Roles updated:\\nJohn: ${$user1_role_label}\\nJane: ${$user2_role_label}\\nBob: ${$user3_role_label}`)"
                    ),
                    cls="space-y-2"
                )
            ),
            cls="max-w-lg"
        ),
        '''// User role management with multiple selects
Div(
    // User row
    Div(
        Div(
            P("John Doe", cls="font-medium"),
            P("john@example.com", cls="text-sm text-muted-foreground")
        ),
        Select(
            SelectTrigger(SelectValue(signal="user1_role")),
            SelectContent(
                SelectItem("viewer", "Viewer", signal="user1_role"),
                SelectItem("editor", "Editor", signal="user1_role"),
                SelectItem("admin", "Admin", signal="user1_role"),
                SelectItem("owner", "Owner", signal="user1_role", disabled=True)
            ),
            initial_value="editor"
        ),
        cls="flex items-center justify-between"
    ),
    // More user rows...
    Button("Save Changes", ds_on_click="saveRoles()")
)''',
        title="Role Management",
        description="Manage multiple user roles with inline selects"
    )


def create_select_docs():
    """Create select documentation page using convention-based approach."""
    
    api_reference = {
        "props": [
            {
                "name": "initial_value",
                "type": "str | None",
                "default": "None",
                "description": "Initial selected value"
            },
            {
                "name": "signal",
                "type": "str | None",
                "default": "auto-generated",
                "description": "Datastar signal name for state management"
            },
            {
                "name": "cls",
                "type": "str",
                "default": "''",
                "description": "Additional CSS classes"
            }
        ],
        "sub_components": [
            {
                "name": "SelectTrigger",
                "description": "Button that triggers the dropdown",
                "props": [
                    {
                        "name": "signal",
                        "type": "str",
                        "description": "Signal name (must match parent Select)"
                    },
                    {
                        "name": "width",
                        "type": "str",
                        "default": "'w-[180px]'",
                        "description": "Width class for the trigger button"
                    },
                    {
                        "name": "disabled",
                        "type": "bool",
                        "default": "False",
                        "description": "Whether the select is disabled"
                    }
                ]
            },
            {
                "name": "SelectValue",
                "description": "Displays the selected value or placeholder",
                "props": [
                    {
                        "name": "placeholder",
                        "type": "str",
                        "default": "'Select an option'",
                        "description": "Placeholder text when no value selected"
                    },
                    {
                        "name": "signal",
                        "type": "str",
                        "description": "Signal name (must match parent Select)"
                    }
                ]
            },
            {
                "name": "SelectContent",
                "description": "Container for select options",
                "props": [
                    {
                        "name": "signal",
                        "type": "str",
                        "description": "Signal name (must match parent Select)"
                    }
                ]
            },
            {
                "name": "SelectItem",
                "description": "Individual select option",
                "props": [
                    {
                        "name": "value",
                        "type": "str",
                        "description": "Value when this option is selected"
                    },
                    {
                        "name": "label",
                        "type": "str | None",
                        "description": "Display text (defaults to value)"
                    },
                    {
                        "name": "signal",
                        "type": "str",
                        "description": "Signal name (must match parent Select)"
                    },
                    {
                        "name": "disabled",
                        "type": "bool",
                        "default": "False",
                        "description": "Whether this option is disabled"
                    }
                ]
            },
            {
                "name": "SelectGroup",
                "description": "Groups related options together",
                "props": [
                    {
                        "name": "label",
                        "type": "str | None",
                        "description": "Group label text"
                    }
                ]
            },
            {
                "name": "SelectWithLabel",
                "description": "Complete select with label and helper text",
                "props": [
                    {
                        "name": "label",
                        "type": "str",
                        "description": "Label text"
                    },
                    {
                        "name": "options",
                        "type": "list[str | tuple | dict]",
                        "description": "List of options (strings, (value, label) tuples, or group dicts)"
                    },
                    {
                        "name": "value",
                        "type": "str | None",
                        "description": "Initial selected value"
                    },
                    {
                        "name": "placeholder",
                        "type": "str",
                        "default": "'Select an option'",
                        "description": "Placeholder text"
                    },
                    {
                        "name": "helper_text",
                        "type": "str | None",
                        "description": "Helper text below the select"
                    },
                    {
                        "name": "error_text",
                        "type": "str | None",
                        "description": "Error message"
                    },
                    {
                        "name": "required",
                        "type": "bool",
                        "default": "False",
                        "description": "Whether field is required"
                    },
                    {
                        "name": "disabled",
                        "type": "bool",
                        "default": "False",
                        "description": "Whether select is disabled"
                    }
                ]
            }
        ]
    }
    
    # Hero example
    hero_example = ComponentPreview(
        Div(
            Select(
                SelectTrigger(
                    SelectValue(placeholder="Select framework", signal="framework"),
                    signal="framework",
                    width="w-[200px]"
                ),
                SelectContent(
                    SelectGroup(
                        SelectLabel("Frontend"),
                        SelectItem("react", "React", signal="framework"),
                        SelectItem("vue", "Vue", signal="framework"),
                        SelectItem("angular", "Angular", signal="framework"),
                        SelectItem("svelte", "Svelte", signal="framework")
                    ),
                    SelectGroup(
                        SelectLabel("Backend"),
                        SelectItem("django", "Django", signal="framework"),
                        SelectItem("fastapi", "FastAPI", signal="framework"),
                        SelectItem("flask", "Flask", signal="framework"),
                        SelectItem("rails", "Ruby on Rails", signal="framework")
                    ),
                    signal="framework"
                ),
                initial_value="react",
                signal="framework"
            ),
            cls="flex justify-center"
        ),
        '''Select(
    SelectTrigger(
        SelectValue(placeholder="Select framework", signal="framework"),
        signal="framework"
    ),
    SelectContent(
        SelectGroup(
            SelectLabel("Frontend"),
            SelectItem("react", "React", signal="framework"),
            SelectItem("vue", "Vue", signal="framework"),
            // ... more items
        ),
        SelectGroup(
            SelectLabel("Backend"),
            SelectItem("django", "Django", signal="framework"),
            // ... more items
        ),
        signal="framework"
    ),
    initial_value="react",
    signal="framework"
)''',
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