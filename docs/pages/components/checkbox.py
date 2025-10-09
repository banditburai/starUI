TITLE = "Checkbox"
DESCRIPTION = "A control that allows the user to toggle between checked and not checked."
CATEGORY = "form"
ORDER = 15
STATUS = "stable"

from starhtml import Div, P, Input, Label, Icon, Span, H3, Form, Signal
from starhtml.datastar import js
from starui.registry.components.checkbox import Checkbox, CheckboxWithLabel
from starui.registry.components.button import Button
from starui.registry.components.card import Card, CardHeader, CardContent, CardTitle, CardDescription
from starui.registry.components.badge import Badge
from starui.registry.components.progress import Progress
from utils import auto_generate_page, with_code, Prop, Component, build_api_reference
from widgets.component_preview import ComponentPreview


# ============================================================================
# EXAMPLE FUNCTIONS (decorated with @with_code for markdown generation)
# ============================================================================

@with_code
def terms_conditions_example():
    terms_accepted = Signal("terms_accepted", False)
    privacy_accepted = Signal("privacy_accepted", False)
    marketing_emails = Signal("marketing_emails", True)

    return Card(
        CardHeader(
            CardTitle("Complete Registration"),
            CardDescription("Please review and accept our terms")
        ),
        CardContent(
            Form(
                terms_accepted,
                privacy_accepted,
                marketing_emails,
                Div(
                    CheckboxWithLabel(
                        label="I accept the Terms of Service",
                        helper_text="You must accept to continue",
                        signal="terms_accepted",
                        required=True
                    ),
                    CheckboxWithLabel(
                        label="I accept the Privacy Policy",
                        helper_text="Learn how we protect your data",
                        signal="privacy_accepted",
                        required=True
                    ),
                    CheckboxWithLabel(
                        label="Send me product updates and offers",
                        helper_text="You can unsubscribe at any time",
                        signal="marketing_emails"
                    ),
                    cls="space-y-3"
                ),
                Button(
                    "Create Account",
                    type="submit",
                    cls="w-full mt-4",
                    data_attr_disabled=js("!$terms_accepted || !$privacy_accepted"),
                    data_on_click="evt.preventDefault(); alert('Account created!')"
                )
            )
        ),
        cls="max-w-md"
    )


@with_code
def feature_permissions_example():
    storage = Signal("storage", True)
    network = Signal("network", True)
    camera = Signal("camera", False)
    location = Signal("location", True)
    contacts = Signal("contacts", False)
    notify = Signal("notify", True)

    return Card(
        CardHeader(
            CardTitle("App Permissions"),
            CardDescription("Control what this app can access")
        ),
        CardContent(
            Div(
                storage, network, camera, location, contacts, notify,
                Div(
                    H3("Essential", cls="text-sm font-semibold mb-2 text-muted-foreground"),
                    CheckboxWithLabel(
                        label="Storage",
                        helper_text="Save files and preferences",
                        signal="storage",
                        checked=True,
                        disabled=True
                    ),
                    CheckboxWithLabel(
                        label="Network",
                        helper_text="Connect to the internet",
                        signal="network",
                        checked=True,
                        disabled=True
                    ),
                    cls="space-y-2 mb-4"
                ),
                Div(
                    H3("Optional", cls="text-sm font-semibold mb-2 text-muted-foreground"),
                    CheckboxWithLabel(
                        label="Camera",
                        helper_text="Take photos and videos",
                        signal="camera"
                    ),
                    CheckboxWithLabel(
                        label="Location",
                        helper_text="Access your location for maps",
                        signal="location",
                        checked=True
                    ),
                    CheckboxWithLabel(
                        label="Contacts",
                        helper_text="Find friends using this app",
                        signal="contacts"
                    ),
                    CheckboxWithLabel(
                        label="Notifications",
                        helper_text="Show alerts and reminders",
                        signal="notify",
                        checked=True
                    ),
                    cls="space-y-2"
                ),
                Div(
                    Badge(
                        data_text=js("[$camera && 'Camera', $location && 'Location', $contacts && 'Contacts', $notify && 'Notifications'].filter(Boolean).length + ' optional permissions'"),
                        variant="secondary"
                    ),
                    cls="mt-4 flex justify-center"
                )
            )
        ),
        cls="max-w-md"
    )


@with_code
def interactive_todo_list_example():
    todo1 = Signal("todo1", True)
    todo2 = Signal("todo2", True)
    todo3 = Signal("todo3", False)
    todo4 = Signal("todo4", False)
    todo_progress = Signal("todo_progress", js("([$todo1, $todo2, $todo3, $todo4].filter(Boolean).length / 4) * 100"))

    return Card(
        CardHeader(
            CardTitle("✓ Todo List"),
            CardDescription("Track your daily tasks")
        ),
        CardContent(
            Div(
                todo1, todo2, todo3, todo4, todo_progress,
                Div(
                    CheckboxWithLabel(
                        label="Write documentation",
                        signal="todo1",
                        label_cls=todo1.if_("line-through text-muted-foreground", "")
                    ),
                    CheckboxWithLabel(
                        label="Review pull requests",
                        signal="todo2",
                        label_cls=todo2.if_("line-through text-muted-foreground", "")
                    ),
                    CheckboxWithLabel(
                        label="Update dependencies",
                        signal="todo3",
                        label_cls=todo3.if_("line-through text-muted-foreground", "")
                    ),
                    CheckboxWithLabel(
                        label="Deploy to production",
                        signal="todo4",
                        label_cls=todo4.if_("line-through text-muted-foreground", "")
                    ),
                    cls="space-y-3"
                ),
                Div(
                    P(
                        "Completed: ",
                        Span(
                            data_text=js("[$todo1, $todo2, $todo3, $todo4].filter(Boolean).length"),
                            cls="font-bold"
                        ),
                        " of 4",
                        cls="text-sm text-muted-foreground"
                    ),
                    Progress(
                        signal="todo_progress",
                        cls="w-full h-2 mt-2"
                    ),
                    cls="mt-4"
                )
            )
        ),
        cls="max-w-md"
    )


@with_code
def select_all_pattern_example():
    # Define file data server-side (this could come from a database, API, etc.)
    files = [
        {"id": "file1", "name": "invoice-2024-001.pdf", "size": "2.4 MB"},
        {"id": "file2", "name": "report-q3.xlsx", "size": "1.8 MB"},
        {"id": "file3", "name": "presentation.pptx", "size": "5.2 MB"},
        {"id": "file4", "name": "contracts.zip", "size": "12.1 MB"}
    ]

    # Create Signal objects dynamically
    select_all = Signal("select_all", False)
    file_signals = {}
    exists_signals = {}

    for file in files:
        file_signals[file["id"]] = Signal(file["id"], False)
        exists_signals[file["id"]] = Signal(f"{file['id']}_exists", True)

    # Generate selected count computation dynamically
    selected_conditions = " + ".join([
        f"(${file['id']} && ${file['id']}_exists ? 1 : 0)"
        for file in files
    ])

    # Generate existing count computation dynamically
    existing_conditions = " + ".join([
        f"(${file['id']}_exists ? 1 : 0)"
        for file in files
    ])

    # Create computed signals
    selected_count = Signal("selected_count", js(selected_conditions))
    existing_count = Signal("existing_count", js(existing_conditions))

    # Generate select all change handler dynamically
    select_all_logic = "; ".join([
        f"if (${file['id']}_exists) ${file['id']} = $select_all"
        for file in files
    ])

    # Generate delete logic dynamically
    delete_logic = "; ".join([
        f"if (${file['id']}) {{ ${file['id']}_exists = false; ${file['id']} = false; }}"
        for file in files
    ])

    # Collect all signals for rendering
    all_signals = [select_all, selected_count, existing_count]
    for file in files:
        all_signals.append(file_signals[file["id"]])
        all_signals.append(exists_signals[file["id"]])

    return Card(
        CardHeader(
            CardTitle("Bulk Actions"),
            CardDescription("Select items for batch operations")
        ),
        CardContent(
            Div(
                *all_signals,
                Div(
                    CheckboxWithLabel(
                        label="Select All",
                        signal="select_all",
                        checkbox_cls="border-2"
                    ),
                    cls="border-b pb-2 mb-3"
                ),
                Div(
                    # Generate checkboxes dynamically server-side
                    *[
                        Div(
                            CheckboxWithLabel(
                                label=file["name"],
                                signal=file["id"],
                                helper_text=file["size"]
                            ),
                            data_show=js(f"${file['id']}_exists")
                        )
                        for file in files
                    ],
                    cls="space-y-2 pl-6"
                ),
                Div(
                    Button(
                        Icon("lucide:trash-2", cls="h-4 w-4 mr-2"),
                        Span(data_text=js("$selected_count > 0 ? `Delete ${$selected_count} Selected` : 'Delete Selected'")),
                        data_on_click=js(f"{delete_logic}; $select_all = false;"),
                        variant="destructive",
                        size="sm",
                        data_attr_disabled=js("$selected_count === 0")
                    ),
                    cls="flex items-center justify-start mt-4 pt-4 border-t"
                ),
                P(
                    "All files deleted!",
                    data_show=js("$existing_count === 0"),
                    cls="text-sm text-center text-muted-foreground mt-4"
                ),
                data_on_input=js(f"""
                    $select_all = $existing_count > 0 && $selected_count === $existing_count;
                    if (evt.target.matches('[data-bind="select_all"]')) {{
                        {select_all_logic};
                    }}
                """)
            )
        ),
        cls="max-w-md"
    )


@with_code
def filter_form_example():
    cat_electronics = Signal("cat_electronics", True)
    cat_clothing = Signal("cat_clothing", False)
    cat_books = Signal("cat_books", True)
    cat_home = Signal("cat_home", False)
    price_1 = Signal("price_1", False)
    price_2 = Signal("price_2", True)
    price_3 = Signal("price_3", True)
    price_4 = Signal("price_4", False)
    free_shipping = Signal("free_shipping", True)
    express = Signal("express", False)

    return Card(
        CardHeader(
            CardTitle("Filter Options"),
            CardDescription("Customize your search results")
        ),
        CardContent(
            Form(
                cat_electronics, cat_clothing, cat_books, cat_home,
                price_1, price_2, price_3, price_4,
                free_shipping, express,
                Div(
                    H3("Categories", cls="text-sm font-semibold mb-3"),
                    Div(
                        CheckboxWithLabel(label="Electronics", signal="cat_electronics", checked=True),
                        CheckboxWithLabel(label="Clothing", signal="cat_clothing"),
                        CheckboxWithLabel(label="Books", signal="cat_books", checked=True),
                        CheckboxWithLabel(label="Home & Garden", signal="cat_home"),
                        cls="space-y-2"
                    ),
                    cls="mb-6"
                ),
                Div(
                    H3("Price Range", cls="text-sm font-semibold mb-3"),
                    Div(
                        CheckboxWithLabel(label="Under $25", signal="price_1"),
                        CheckboxWithLabel(label="$25 - $50", signal="price_2", checked=True),
                        CheckboxWithLabel(label="$50 - $100", signal="price_3", checked=True),
                        CheckboxWithLabel(label="Over $100", signal="price_4"),
                        cls="space-y-2"
                    ),
                    cls="mb-6"
                ),
                Div(
                    H3("Shipping", cls="text-sm font-semibold mb-3"),
                    Div(
                        CheckboxWithLabel(label="Free Shipping", signal="free_shipping", checked=True),
                        CheckboxWithLabel(label="Express Available", signal="express"),
                        cls="space-y-2"
                    )
                ),
                Div(
                    Button(
                        "Apply Filters",
                        type="submit",
                        cls="w-full",
                        data_on_click="evt.preventDefault(); applyFilters()"
                    ),
                    Button(
                        "Reset",
                        variant="outline",
                        cls="w-full mt-2",
                        data_on_click=js("evt.preventDefault(); $cat_electronics=false; $cat_clothing=false; $cat_books=false; $cat_home=false; $price_1=false; $price_2=false; $price_3=false; $price_4=false; $free_shipping=false; $express=false;")
                    ),
                    cls="mt-6"
                )
            )
        ),
        cls="max-w-sm"
    )


@with_code
def settings_with_validation_example():
    email_notif = Signal("email_notif", True)
    push_notif = Signal("push_notif", False)
    sms_notif = Signal("sms_notif", False)
    marketing = Signal("marketing", False)

    return Card(
        CardHeader(
            CardTitle("Notification Settings"),
            CardDescription("Choose how you want to be notified")
        ),
        CardContent(
            Form(
                email_notif, push_notif, sms_notif, marketing,
                Div(
                    CheckboxWithLabel(
                        label="Email Notifications",
                        helper_text="Receive important updates via email",
                        signal="email_notif",
                        checked=True
                    ),
                    CheckboxWithLabel(
                        label="Push Notifications",
                        helper_text="Get instant updates on your device",
                        signal="push_notif"
                    ),
                    CheckboxWithLabel(
                        label="SMS Alerts",
                        helper_text="Critical alerts sent to your phone",
                        signal="sms_notif"
                    ),
                    cls="space-y-4"
                ),
                Div(
                    H3("Optional", cls="text-sm font-semibold mb-3"),
                    CheckboxWithLabel(
                        label="Marketing Communications",
                        helper_text="Product updates and special offers",
                        signal="marketing",
                        checkbox_cls=marketing.if_("border-blue-500", "")
                    ),
                    cls="mt-6 pt-6 border-t"
                ),
                Div(
                    P(
                        Icon("lucide:alert-circle", cls="h-4 w-4 mr-1 flex-shrink-0"),
                        "At least one notification method must be enabled",
                        data_show=js("!$email_notif && !$push_notif && !$sms_notif"),
                        cls="text-sm text-destructive flex items-start"
                    ),
                    cls="mt-4 min-h-[1.5rem] w-full max-w-full overflow-hidden"
                ),
                Button(
                    "Save Settings",
                    type="submit",
                    data_attr_disabled=js("!$email_notif && !$push_notif && !$sms_notif"),
                    data_on_click="evt.preventDefault(); alert('Settings saved!')",
                    cls="w-full mt-4"
                ),
                Div(
                    Div(
                        Badge(
                            data_text=js("'Active: ' + [$email_notif && 'Email', $push_notif && 'Push', $sms_notif && 'SMS'].filter(Boolean).join(', ')"),
                            data_show=js("$email_notif || $push_notif || $sms_notif"),
                            variant="secondary"
                        ),
                        cls="flex justify-center"
                    ),
                    Div(
                        Badge(
                            "Marketing enabled",
                            data_show=marketing,
                            variant="outline"
                        ),
                        cls="flex justify-center mt-2"
                    ),
                    cls="mt-4"
                )
            )
        ),
        cls="w-80"
    )


# ============================================================================
# EXAMPLES GENERATOR (for rendering on the page)
# ============================================================================

def examples():
    yield ComponentPreview(
        terms_conditions_example(),
        terms_conditions_example.code,
        title="Terms & Conditions",
        description="Registration form with required checkboxes"
    )

    yield ComponentPreview(
        feature_permissions_example(),
        feature_permissions_example.code,
        title="Feature Permissions",
        description="Grouped checkboxes with disabled states"
    )

    yield ComponentPreview(
        interactive_todo_list_example(),
        interactive_todo_list_example.code,
        title="Interactive Todo List",
        description="Task tracking with progress visualization"
    )

    yield ComponentPreview(
        select_all_pattern_example(),
        select_all_pattern_example.code,
        title="Select All Pattern",
        description="Bulk selection with parent-child checkbox relationship"
    )

    yield ComponentPreview(
        filter_form_example(),
        filter_form_example.code,
        title="Filter Form",
        description="Multi-category filtering interface"
    )

    yield ComponentPreview(
        settings_with_validation_example(),
        settings_with_validation_example.code,
        title="Settings with Validation",
        description="Form validation based on checkbox selections"
    )


# ============================================================================
# API REFERENCE
# ============================================================================

API_REFERENCE = build_api_reference(
    main_props=[
        Prop("checked", "bool | None", "Initial checked state of the checkbox", "None"),
        Prop("signal", "str | None", "Datastar signal name for state management and reactive updates", "auto-generated"),
        Prop("label", "str", "Label text for the checkbox (CheckboxWithLabel only)"),
        Prop("helper_text", "str | None", "Helper text displayed below the label", "None"),
        Prop("disabled", "bool", "Whether checkbox is disabled", "False"),
        Prop("required", "bool", "Whether checkbox is required for form validation", "False"),
        Prop("name", "str | None", "Name attribute for form submission", "None"),
        Prop("cls", "str", "Additional CSS classes for styling", "''"),
    ]
)


# ============================================================================
# EXAMPLES DATA (for markdown generation with code)
# ============================================================================

EXAMPLES_DATA = [
    {"title": "Terms & Conditions", "description": "Registration form with required checkboxes", "code": terms_conditions_example.code},
    {"title": "Feature Permissions", "description": "Grouped checkboxes with disabled states", "code": feature_permissions_example.code},
    {"title": "Interactive Todo List", "description": "Task tracking with progress visualization", "code": interactive_todo_list_example.code},
    {"title": "Select All Pattern", "description": "Bulk selection with parent-child checkbox relationship", "code": select_all_pattern_example.code},
    {"title": "Filter Form", "description": "Multi-category filtering interface", "code": filter_form_example.code},
    {"title": "Settings with Validation", "description": "Form validation based on checkbox selections", "code": settings_with_validation_example.code},
]


# ============================================================================
# DOCS PAGE
# ============================================================================

@with_code
def hero_checkbox_example():
    dark_mode = Signal("dark_mode", True)
    notifications = Signal("notifications", False)
    auto_save = Signal("auto_save", True)

    return Card(
        CardHeader(
            CardTitle("Quick Setup"),
            CardDescription("Configure your preferences in seconds")
        ),
        CardContent(
            Div(
                dark_mode, notifications, auto_save,
                CheckboxWithLabel(
                    label="Enable dark mode",
                    helper_text="Reduce eye strain in low-light conditions",
                    signal="dark_mode",
                    checked=True
                ),
                CheckboxWithLabel(
                    label="Show notifications",
                    helper_text="Stay updated with real-time alerts",
                    signal="notifications"
                ),
                CheckboxWithLabel(
                    label="Auto-save drafts",
                    helper_text="Never lose your work",
                    signal="auto_save",
                    checked=True
                ),
                Div(
                    P(
                        "Your preferences: ",
                        cls="text-sm text-muted-foreground mb-1"
                    ),
                    P(
                        Span(
                            data_text=js("[$dark_mode && 'Dark Mode', $notifications && 'Notifications', $auto_save && 'Auto-save'].filter(Boolean).join(', ') || 'None selected'"),
                            cls="font-medium text-sm break-words"
                        ),
                        cls="min-h-[1.25rem]"
                    ),
                    cls="mt-4 pt-4 border-t"
                ),
                cls="space-y-3"
            )
        ),
        cls="max-w-md mx-auto"
    )


def create_checkbox_docs():
    hero_example = ComponentPreview(
        hero_checkbox_example(),
        hero_checkbox_example.code,
        copy_button=True
    )

    return auto_generate_page(
        TITLE,
        DESCRIPTION,
        list(examples()),
        cli_command="star add checkbox",
        api_reference=API_REFERENCE,
        hero_example=hero_example,
        component_slug="checkbox"
    )