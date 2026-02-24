TITLE = "Checkbox"
DESCRIPTION = "A control that allows the user to toggle between checked and not checked."
CATEGORY = "form"
ORDER = 15
STATUS = "stable"

from starhtml import Div, P, Input, Label, Icon, Span, H3, Form, Signal, all_, any_, collect, js, evt
from starui.registry.components.checkbox import Checkbox, CheckboxWithLabel
from starui.registry.components.button import Button
from starui.registry.components.card import Card, CardHeader, CardContent, CardTitle, CardDescription
from starui.registry.components.badge import Badge
from starui.registry.components.progress import Progress
from utils import auto_generate_page, with_code, Prop, Component, build_api_reference
from widgets.component_preview import ComponentPreview




@with_code
def hero_checkbox_example():
    dark_mode = Signal("dark_mode", _ref_only=True)
    notifications = Signal("notifications", _ref_only=True)
    auto_save = Signal("auto_save", _ref_only=True)

    preferences = [
        (dark_mode, "Enable dark mode", "Reduce eye strain in low-light conditions", True),
        (notifications, "Show notifications", "Stay updated with real-time alerts", False),
        (auto_save, "Auto-save drafts", "Never lose your work", True),
    ]

    checkboxes = [
        CheckboxWithLabel(label=label, helper_text=helper, signal=sig, checked=checked)
        for sig, label, helper, checked in preferences
    ]

    selected_text = collect([
        (dark_mode, "Dark Mode"),
        (notifications, "Notifications"),
        (auto_save, "Auto-save"),
        ], join_with=" | ")

    preference_summary = Div(
        P("Your preferences: ", cls="text-sm text-muted-foreground mb-1"),
        P(
            Span(
                data_text=selected_text.if_(selected_text, "None selected"),
                cls="font-medium text-sm break-words"
            ),
            cls="min-h-[1.25rem]"
        ),
        cls="mt-4 pt-4 border-t"
    )

    return Card(
        CardHeader(
            CardTitle("Quick Setup"),
            CardDescription("Configure your preferences in seconds")
        ),
        CardContent(
            Div(
                *checkboxes,
                preference_summary,
                cls="space-y-3"
            )
        ),
        cls="max-w-md mx-auto"
    )

@with_code
def terms_conditions_example():
    terms_accepted = Signal("terms_accepted", _ref_only=True)
    privacy_accepted = Signal("privacy_accepted", _ref_only=True)

    return Card(
        CardHeader(
            CardTitle("Complete Registration"),
            CardDescription("Please review and accept our terms")
        ),
        CardContent(
            Form(
                Div(
                    CheckboxWithLabel(
                        label="I accept the Terms of Service",
                        helper_text="You must accept to continue",
                        signal=terms_accepted,
                        required=True
                    ),
                    CheckboxWithLabel(
                        label="I accept the Privacy Policy",
                        helper_text="Learn how we protect your data",
                        signal=privacy_accepted,
                        required=True
                    ),
                    CheckboxWithLabel(
                        label="Send me product updates and offers",
                        helper_text="You can unsubscribe at any time"
                    ),
                    cls="space-y-3"
                ),
                Button(
                    "Create Account",
                    type="submit",
                    cls="w-full mt-4",
                    data_attr_disabled=~all_(terms_accepted, privacy_accepted),
                    data_on_click=evt.preventDefault()
                )
            )
        ),
        cls="max-w-md"
    )


@with_code
def feature_permissions_example():
    camera = Signal("camera", _ref_only=True)
    location = Signal("location", _ref_only=True)
    contacts = Signal("contacts", _ref_only=True)
    notify = Signal("notify", _ref_only=True)
    optional_count = Signal("optional_count", camera + location + contacts + notify)

    return Card(
        CardHeader(
            CardTitle("App Permissions"),
            CardDescription("Control what this app can access")
        ),
        CardContent(
            Div(
                optional_count,
                Div(
                    H3("Essential", cls="text-sm font-semibold mb-2 text-muted-foreground"),
                    CheckboxWithLabel(
                        label="Storage",
                        helper_text="Save files and preferences",
                        checked=True,
                        disabled=True
                    ),
                    CheckboxWithLabel(
                        label="Network",
                        helper_text="Connect to the internet",
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
                        signal=camera
                    ),
                    CheckboxWithLabel(
                        label="Location",
                        helper_text="Access your location for maps",
                        signal=location,
                        checked=True
                    ),
                    CheckboxWithLabel(
                        label="Contacts",
                        helper_text="Find friends using this app",
                        signal=contacts
                    ),
                    CheckboxWithLabel(
                        label="Notifications",
                        helper_text="Show alerts and reminders",
                        signal=notify,
                        checked=True
                    ),
                    cls="space-y-2"
                ),
                Div(
                    Badge(
                        data_text=optional_count + " optional permissions",
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
    todo1 = Signal("todo1", _ref_only=True)
    todo2 = Signal("todo2", _ref_only=True)
    todo3 = Signal("todo3", _ref_only=True)
    todo4 = Signal("todo4", _ref_only=True)
    completed_count = Signal("completed_count", todo1 + todo2 + todo3 + todo4)
    todo_progress = Signal("todo_progress", completed_count / 4 * 100)

    def todo_item(label, signal, checked=False):
        return CheckboxWithLabel(
            label=label,
            signal=signal,
            checked=checked,
            label_cls=signal.if_("line-through text-muted-foreground")
        )

    return Card(
        CardHeader(
            CardTitle("✓ Todo List"),
            CardDescription("Track your daily tasks")
        ),
        CardContent(
            Div(
                completed_count, todo_progress,
                Div(
                    todo_item("Write documentation", todo1, checked=True),
                    todo_item("Review pull requests", todo2, checked=True),
                    todo_item("Update dependencies", todo3),
                    todo_item("Deploy to production", todo4),
                    cls="space-y-3"
                ),
                Div(
                    P(
                        "Completed: ",
                        Span(data_text=completed_count, cls="font-bold"),
                        " of 4",
                        cls="text-sm text-muted-foreground"
                    ),
                    Progress(
                        signal=todo_progress,
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
    files = [
        {"id": "file1", "name": "invoice-2024-001.pdf", "size": "2.4 MB"},
        {"id": "file2", "name": "report-q3.xlsx", "size": "1.8 MB"},
        {"id": "file3", "name": "presentation.pptx", "size": "5.2 MB"},
        {"id": "file4", "name": "contracts.zip", "size": "12.1 MB"}
    ]

    file_signals = {file["id"]: Signal(file["id"], _ref_only=True) for file in files}
    deleted_signals = {file["id"]: Signal(file["id"] + "_deleted", False) for file in files}
    select_all = Signal("select_all", False)

    selected_count = Signal("selected_count",
        sum([file_signals[file["id"]] & ~deleted_signals[file["id"]] for file in files])
    )

    delete_actions = [
        file_signals[file["id"]].then(deleted_signals[file["id"]].set(True))
        for file in files
    ] + [select_all.set(False)]

    select_actions = [
        (~deleted_signals[file["id"]]).then(file_signals[file["id"]].set(select_all))
        for file in files
    ]

    return Card(
        CardHeader(
            CardTitle("Bulk Delete"),
            CardDescription("Select-all pattern with bulk delete functionality")
        ),
        CardContent(
            Div(
                select_all, *deleted_signals.values(), selected_count,
                Div(
                    CheckboxWithLabel(
                        label="Select All",
                        signal=select_all,
                        checkbox_cls="border-2",
                        data_on_change=select_actions
                    ),
                    cls="border-b pb-2 mb-3"
                ),
                Div(
                    *[
                        Div(
                            CheckboxWithLabel(
                                label=file["name"],
                                signal=file_signals[file["id"]],
                                helper_text=file["size"]
                            ),
                            data_show=~deleted_signals[file["id"]]
                        )
                        for file in files
                    ],
                    cls="space-y-2 pl-6"
                ),
                Div(
                    Button(
                        Icon("lucide:trash-2", cls="h-4 w-4 mr-2"),
                        Span(data_text=(selected_count > 0).if_("Delete " + selected_count + " Selected", "Delete Selected")),
                        data_on_click=delete_actions,
                        variant="destructive",
                        size="sm",
                        data_attr_disabled=selected_count == 0
                    ),
                    cls="mt-4 pt-4 border-t"
                )
            )
        ),
        cls="max-w-md"
    )


@with_code
def filter_form_example():
    # (signal_name, label, collect_label, checked)
    categories = [
        ("cat_electronics", "Electronics", "Electronics", True),
        ("cat_clothing", "Clothing", "Clothing", False),
        ("cat_books", "Books", "Books", True),
        ("cat_home", "Home & Garden", "Home & Garden", False),
    ]

    # Dollar signs in collect expressions are interpreted as signal references
    prices = [
        ("price_1", "Under $25", "Under 25", False),
        ("price_2", "$25 - $50", "25-50", True),
        ("price_3", "$50 - $100", "50-100", True),
        ("price_4", "Over $100", "Over 100", False),
    ]

    shipping = [
        ("free_shipping", "Free Shipping", "Free Shipping", True),
        ("express", "Express Available", "Express", False),
    ]

    all_filters = categories + prices + shipping
    filter_signals = {name: Signal(name, _ref_only=True) for name, _, _, _ in all_filters}
    reset_actions = [filter_signals[name].set(False) for name, _, _, _ in all_filters]

    active_filters = collect([
        (filter_signals[name], collect_label)
        for name, _, collect_label, _ in all_filters
    ], join_with=", ")

    filter_message = Signal("filter_message",
        active_filters.if_("Filters: " + active_filters, "No filters selected")
    )

    def filter_group(title, options, mb_class="mb-6"):
        return Div(
            H3(title, cls="text-sm font-semibold mb-3"),
            Div(
                *[CheckboxWithLabel(label=label, signal=filter_signals[name], checked=checked)
                  for name, label, _, checked in options],
                cls="space-y-2"
            ),
            cls=mb_class
        )

    return Card(
        CardHeader(
            CardTitle("Filter Options"),
            CardDescription("Customize your search results")
        ),
        CardContent(
            Form(
                filter_message,
                filter_group("Categories", categories),
                filter_group("Price Range", prices),
                filter_group("Shipping", shipping, mb_class=""),
                Div(
                    Button(
                        "Apply Filters",
                        type="submit",
                        cls="w-full",
                        data_on_click=(js("alert($filter_message)"), dict(prevent=True))
                    ),
                    Button(
                        "Reset",
                        variant="outline",
                        cls="w-full mt-2",
                        data_on_click=(reset_actions, dict(prevent=True))
                    ),
                    cls="mt-6"
                )
            )
        ),
        cls="max-w-sm"
    )


@with_code
def settings_with_validation_example():
    email_notif = Signal("email_notif", _ref_only=True)
    push_notif = Signal("push_notif", _ref_only=True)
    sms_notif = Signal("sms_notif", _ref_only=True)
    marketing = Signal("marketing", _ref_only=True)

    active_notifs_text = collect([
        (email_notif, "Email"),
        (push_notif, "Push"),
        (sms_notif, "SMS")
    ], join_with=" | ")

    # (label, helper_text, signal, checked)
    notifications = [
        ("Email Notifications", "Receive important updates via email", email_notif, True),
        ("Push Notifications", "Get instant updates on your device", push_notif, False),
        ("SMS Alerts", "Critical alerts sent to your phone", sms_notif, False),
    ]

    return Card(
        CardHeader(
            CardTitle("Notification Settings"),
            CardDescription("Choose how you want to be notified")
        ),
        CardContent(
            Form(
                Div(
                    *[CheckboxWithLabel(
                        label=label,
                        helper_text=helper,
                        signal=signal,
                        checked=checked
                    ) for label, helper, signal, checked in notifications],
                    cls="space-y-4"
                ),
                Div(
                    H3("Optional", cls="text-sm font-semibold mb-3"),
                    CheckboxWithLabel(
                        label="Marketing Communications",
                        helper_text="Product updates and special offers",
                        signal=marketing
                    ),
                    cls="mt-6 pt-6 border-t"
                ),
                Div(
                    P(
                        Icon("lucide:alert-circle", cls="h-4 w-4 mr-1 flex-shrink-0"),
                        "At least one notification method must be enabled",
                        data_show=~any_(email_notif, push_notif, sms_notif),
                        cls="text-sm text-destructive flex items-start"
                    ),
                    cls="mt-4 min-h-[1.5rem] w-full max-w-full overflow-hidden"
                ),
                Button(
                    "Save Settings",
                    type="submit",
                    data_attr_disabled=~any_(email_notif, push_notif, sms_notif),
                    data_on_click=evt.preventDefault(),
                    cls="w-full mt-4"
                ),
                Div(
                    Div(
                        Badge(
                            data_text="Active: " + active_notifs_text,
                            data_show=any_(email_notif, push_notif, sms_notif),
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


EXAMPLES_DATA = [
    {"title": "Quick Setup", "description": "Basic checkbox usage with dynamic preference summary", "fn": hero_checkbox_example},
    {"title": "Terms & Conditions", "description": "Registration form with required checkboxes", "fn": terms_conditions_example},
    {"title": "Feature Permissions", "description": "Grouped checkboxes with disabled states", "fn": feature_permissions_example},
    {"title": "Interactive Todo List", "description": "Task tracking with progress visualization", "fn": interactive_todo_list_example},
    {"title": "Bulk Delete", "description": "Select-all pattern with bulk delete - selected items are removed from view", "fn": select_all_pattern_example},
    {"title": "Filter Form", "description": "Multi-category filtering interface", "fn": filter_form_example},
    {"title": "Settings with Validation", "description": "Form validation based on checkbox selections", "fn": settings_with_validation_example},
]


def create_checkbox_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)