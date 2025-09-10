"""
Checkbox component documentation - Convention-based functional approach.
Clean, minimal, and easy to extend.
"""

# Component metadata for auto-discovery
TITLE = "Checkbox"
DESCRIPTION = "A control that allows the user to toggle between checked and not checked."
CATEGORY = "form"
ORDER = 15
STATUS = "stable"

from starhtml import Div, P, Input, Label, Icon, Span, H2, H3, Button as HTMLButton, Form
from starhtml.datastar import (
    ds_on_click, ds_show, ds_text, ds_signals, value,
    ds_bind, ds_disabled, ds_on_change, ds_effect, ds_class, ds_style, ds_computed, toggle_class
)
from starui.registry.components.checkbox import Checkbox, CheckboxWithLabel
from starui.registry.components.button import Button
from starui.registry.components.card import Card, CardHeader, CardContent, CardTitle, CardDescription
from starui.registry.components.badge import Badge
from starui.registry.components.progress import Progress
from utils import auto_generate_page
from widgets.component_preview import ComponentPreview


def examples():
    """Generate checkbox examples using ComponentPreview with tabs."""
    
    # Terms and conditions example
    yield ComponentPreview(
        Card(
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
                        ds_disabled="!$terms_accepted || !$privacy_accepted",
                        ds_on_click="event.preventDefault(); alert('Account created!')"
                    ),
                    ds_signals(terms_accepted=False, privacy_accepted=False, marketing_emails=True)
                )
            ),
            cls="max-w-md"
        ),
        '''Card(
    CardContent(
        Form(
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
                ds_disabled="!$terms_accepted || !$privacy_accepted"
            ),
            ds_signals(terms_accepted=False, privacy_accepted=False, marketing_emails=True)
        )
    )
)''',
        title="Terms & Conditions",
        description="Registration form with required checkboxes"
    )
    
    # Feature permissions
    yield ComponentPreview(
        Card(
            CardHeader(
                CardTitle("App Permissions"),
                CardDescription("Control what this app can access")
            ),
            CardContent(
                Div(
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
                            ds_text("[$camera && 'Camera', $location && 'Location', $contacts && 'Contacts', $notify && 'Notifications'].filter(Boolean).length + ' optional permissions'"),
                            variant="secondary"
                        ),
                        cls="mt-4 flex justify-center"
                    ),
                    ds_signals(storage=True, network=True, camera=False, location=True, contacts=False, notify=True)
                )
            ),
            cls="max-w-md"
        ),
        '''Card(
    CardHeader(
        CardTitle("App Permissions"),
        CardDescription("Control what this app can access")
    ),
    CardContent(
        Div(
            Div(
                H3("Essential", cls="text-sm font-semibold"),
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
                )
            ),
            Div(
                H3("Optional", cls="text-sm font-semibold"),
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
                # ... more permissions
            ),
            ds_signals(camera=False, location=True, contacts=False, notify=True)
        )
    )
)''',
        title="Feature Permissions",
        description="Grouped checkboxes with disabled states"
    )
    
    # Todo list example
    yield ComponentPreview(
        Card(
            CardHeader(
                CardTitle("✓ Todo List"),
                CardDescription("Track your daily tasks")
            ),
            CardContent(
                Div(
                    CheckboxWithLabel(
                        label="Write documentation",
                        signal="todo1",
                        slot_attrs={
                            "label": toggle_class("todo1", "line-through text-muted-foreground", "")
                        }
                    ),
                    CheckboxWithLabel(
                        label="Review pull requests",
                        signal="todo2",
                        slot_attrs={
                            "label": toggle_class("todo2", "line-through text-muted-foreground", "")
                        }
                    ),
                    CheckboxWithLabel(
                        label="Update dependencies",
                        signal="todo3",
                        slot_attrs={
                            "label": toggle_class("todo3", "line-through text-muted-foreground", "")
                        }
                    ),
                    CheckboxWithLabel(
                        label="Deploy to production",
                        signal="todo4",
                        slot_attrs={
                            "label": toggle_class("todo4", "line-through text-muted-foreground", "")
                        }
                    ),
                    cls="space-y-3"
                ),
                Div(
                    P(
                        "Completed: ",
                        Span(
                            ds_text("[$todo1, $todo2, $todo3, $todo4].filter(Boolean).length"),
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
                ),
                ds_signals(
                    todo1=True, 
                    todo2=True, 
                    todo3=False, 
                    todo4=False
                ),
                ds_computed("todo_progress", "([$todo1, $todo2, $todo3, $todo4].filter(Boolean).length / 4) * 100")
            ),
            cls="max-w-md"
        ),
        '''Card(
    CardHeader(
        CardTitle("✓ Todo List"),
        CardDescription("Track your daily tasks")
    ),
    CardContent(
        Div(
            CheckboxWithLabel(
                label="Write documentation",
                signal="todo1",
                label_cls=ds_class(**{"line-through text-muted-foreground": "$todo1"})
            ),
            # ... more todos
            cls="space-y-3"
        ),
        Div(
            P("Completed: ", Span(ds_text("[$todo1, $todo2, $todo3, $todo4].filter(Boolean).length")), " of 4"),
            Progress(signal="todo_progress", cls="w-full h-2")
        ),
        ds_signals(
            todo1=True, todo2=True, todo3=False, todo4=False
        ),
        ds_computed("todo_progress", "([$todo1, $todo2, $todo3, $todo4].filter(Boolean).length / 4) * 100")
    )
)''',
        title="Interactive Todo List",
        description="Task tracking with progress visualization"
    )
    
    # Select all pattern
    yield ComponentPreview(
        Card(
            CardHeader(
                CardTitle("Bulk Actions"),
                CardDescription("Select items for batch operations")
            ),
            CardContent(
                Div(
                    Div(
                        CheckboxWithLabel(
                            label="Select All",
                            signal="selectAll",
                            checkbox_cls="border-2"
                        ),
                        cls="border-b pb-2 mb-3"
                    ),
                    Div(
                        Div(
                            CheckboxWithLabel(
                                label="invoice-2024-001.pdf",
                                signal="file1",
                                helper_text="2.4 MB"
                            ),
                            ds_show("$file1_exists")
                        ),
                        Div(
                            CheckboxWithLabel(
                                label="report-q3.xlsx",
                                signal="file2",
                                helper_text="1.8 MB"
                            ),
                            ds_show("$file2_exists")
                        ),
                        Div(
                            CheckboxWithLabel(
                                label="presentation.pptx",
                                signal="file3",
                                helper_text="5.2 MB"
                            ),
                            ds_show("$file3_exists")
                        ),
                        Div(
                            CheckboxWithLabel(
                                label="contracts.zip",
                                signal="file4",
                                helper_text="12.1 MB"
                            ),
                            ds_show("$file4_exists")
                        ),
                        cls="space-y-2 pl-6"
                    ),
                    Div(
                        Button(
                            Icon("lucide:trash-2", cls="h-4 w-4 mr-2"),
                            Span(ds_text("`Delete ${[$file1, $file2, $file3, $file4].filter(Boolean).length} Selected`")),
                            ds_on_click("""
                                if ($file1) $file1_exists = false;
                                if ($file2) $file2_exists = false;
                                if ($file3) $file3_exists = false;
                                if ($file4) $file4_exists = false;
                                $file1 = false;
                                $file2 = false;
                                $file3 = false;
                                $file4 = false;
                                $selectAll = false;
                            """),
                            variant="destructive",
                            size="sm",
                            ds_disabled="!$file1 && !$file2 && !$file3 && !$file4",                            
                        ),
                        cls="flex items-center justify-start mt-4 pt-4 border-t"
                    ),
                    P(
                        "All files deleted!",
                        ds_show("!$file1_exists && !$file2_exists && !$file3_exists && !$file4_exists"),
                        cls="text-sm text-center text-muted-foreground mt-4",                        
                    ),
                    ds_signals(
                        selectAll=False, 
                        file1=False, file2=False, file3=False, file4=False,
                        file1_exists=True, file2_exists=True, file3_exists=True, file4_exists=True
                    ),
                    ds_effect("$selectAll = $file1 && $file2 && $file3 && $file4 && ($file1 || $file2 || $file3 || $file4)"),
                    ds_on_change("""
                        if (event.target.matches('[data-bind="selectAll"]')) {
                            if ($file1_exists) $file1 = $selectAll;
                            if ($file2_exists) $file2 = $selectAll;
                            if ($file3_exists) $file3 = $selectAll;
                            if ($file4_exists) $file4 = $selectAll;
                        }
                    """)
                )
            ),
            cls="max-w-md"
        ),
        '''Card(
    CardContent(
        Div(
            CheckboxWithLabel(label="Select All", signal="selectAll"),
            Div(
                Div(CheckboxWithLabel(label="invoice.pdf", signal="file1"), ds_show("$file1_exists")),
                Div(CheckboxWithLabel(label="report.xlsx", signal="file2"), ds_show("$file2_exists")),
                # ... more files with ds_show
            ),
            Button(
                Span(ds_text("`Delete ${count} Selected`")),
                ds_disabled("!$file1 && !$file2 && !$file3 && !$file4"),
                ds_on_click("""
                    if ($file1) $file1_exists = false;
                    if ($file2) $file2_exists = false;
                    // Remove selected files and uncheck
                """)
            ),
            P(ds_text("`${count} item${count !== 1 ? 's' : ''} selected`")),
            ds_signals(
                selectAll=False, file1=False, file2=False,
                file1_exists=True, file2_exists=True
            ),
            ds_effect("$selectAll = $file1 && $file2 && ($file1 || $file2)"),
            ds_on_change("if (event.target.matches('[data-bind=\\"selectAll\\"]')) { /* sync */ }")
        )
    )
)''',
        title="Select All Pattern",
        description="Bulk selection with parent-child checkbox relationship"
    )
    
    # Filter/preferences form
    yield ComponentPreview(
        Card(
            CardHeader(
                CardTitle("Filter Options"),
                CardDescription("Customize your search results")
            ),
            CardContent(
                Form(
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
                            ds_on_click="event.preventDefault(); applyFilters()"
                        ),
                        Button(
                            "Reset",
                            variant="outline",
                            cls="w-full mt-2",
                            ds_on_click="""
                                event.preventDefault();
                                $cat_electronics = false; $cat_clothing = false; 
                                $cat_books = false; $cat_home = false;
                                $price_1 = false; $price_2 = false;
                                $price_3 = false; $price_4 = false;
                                $free_shipping = false; $express = false;
                            """
                        ),
                        cls="mt-6"
                    ),
                    ds_signals(
                        cat_electronics=True, cat_clothing=False, cat_books=True, cat_home=False,
                        price_1=False, price_2=True, price_3=True, price_4=False,
                        free_shipping=True, express=False
                    )
                )
            ),
            cls="max-w-sm"
        ),
        '''Card(
    CardHeader(CardTitle("Filter Options")),
    CardContent(
        Form(
            # Categories section
            Div(
                H3("Categories"),
                CheckboxWithLabel(label="Electronics", signal="cat_electronics"),
                # ... more categories
            ),
            # Price range section
            Div(
                H3("Price Range"),
                CheckboxWithLabel(label="Under $25", signal="price_1"),
                # ... more price ranges
            ),
            # Action buttons
            Button("Apply Filters", type="submit"),
            Button("Reset", variant="outline", ds_on_click="resetFilters()"),
            ds_signals(/* initial filter states */)
        )
    )
)''',
        title="Filter Form",
        description="Multi-category filtering interface"
    )
    
    # Settings panel with validation
    yield ComponentPreview(
        Card(
            CardHeader(
                CardTitle("Notification Settings"),
                CardDescription("Choose how you want to be notified")
            ),
            CardContent(
                Form(
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
                            checkbox_cls=ds_class(**{"border-blue-500": "$marketing"})
                        ),
                        cls="mt-6 pt-6 border-t"
                    ),
                    Div(
                        P(
                            Icon("lucide:alert-circle", cls="h-4 w-4 mr-1 flex-shrink-0"),
                            "At least one notification method must be enabled",
                            ds_show("!$email_notif && !$push_notif && !$sms_notif"),
                            cls="text-sm text-destructive flex items-start"
                        ),
                        cls="mt-4 min-h-[1.5rem] w-full max-w-full overflow-hidden"
                    ),
                    Button(
                        "Save Settings",
                        type="submit",
                        ds_disabled="!$email_notif && !$push_notif && !$sms_notif",
                        ds_on_click="event.preventDefault(); alert('Settings saved!')",
                        cls="w-full mt-4"
                    ),
                    Div(
                        Div(
                            Badge(
                                ds_text("'Active: ' + [$email_notif && 'Email', $push_notif && 'Push', $sms_notif && 'SMS'].filter(Boolean).join(', ')"),
                                ds_show("$email_notif || $push_notif || $sms_notif"),
                                variant="secondary",                            
                            ),
                            cls="flex justify-center"
                        ),
                        Div(
                            Badge(
                                "Marketing enabled",
                                ds_show("$marketing"),
                                variant="outline"
                            ),
                            cls="flex justify-center mt-2"
                        ),
                        cls="mt-4"
                    ),
                    ds_signals(email_notif=True, push_notif=False, sms_notif=False, marketing=False)
                )
            ),
            cls="w-80"
        ),
        '''Card(
    CardContent(
        Form(
            Div(
                CheckboxWithLabel(
                    label="Email Notifications",
                    helper_text="Receive important updates via email",
                    signal="email_notif"
                ),
                # ... more notification options
            ),
            P(
                "At least one notification method must be enabled",
                ds_show("!$email_notif && !$push_notif && !$sms_notif"),
                cls="text-destructive"
            ),
            Button(
                "Save Settings",
                ds_disabled("!$email_notif && !$push_notif && !$sms_notif")
            ),
            ds_signals(email_notif=True, push_notif=False, sms_notif=False)
        )
    )
)''',
        title="Settings with Validation",
        description="Form validation based on checkbox selections"
    )


def create_checkbox_docs():
    """Create checkbox documentation page using convention-based approach."""
    
    api_reference = {
        "props": [
            {
                "name": "checked",
                "type": "bool | None",
                "default": "None",
                "description": "Initial checked state of the checkbox"
            },
            {
                "name": "name",
                "type": "str | None",
                "default": "None",
                "description": "Name attribute for form submission"
            },
            {
                "name": "value",
                "type": "str | None",
                "default": "'on'",
                "description": "Value when checkbox is checked"
            },
            {
                "name": "signal",
                "type": "str | None",
                "default": "auto-generated",
                "description": "Datastar signal name for state management"
            },
            {
                "name": "disabled",
                "type": "bool",
                "default": "False",
                "description": "Whether checkbox is disabled"
            },
            {
                "name": "required",
                "type": "bool",
                "default": "False",
                "description": "Whether checkbox is required"
            },
            {
                "name": "cls",
                "type": "str",
                "default": "''",
                "description": "Additional CSS classes for checkbox"
            },
            {
                "name": "indicator_cls",
                "type": "str",
                "default": "''",
                "description": "Additional CSS classes for check indicator"
            }
        ],
        "helper_components": [
            {
                "name": "CheckboxWithLabel",
                "description": "Checkbox with integrated label and helper/error text",
                "props": [
                    {
                        "name": "label",
                        "type": "str",
                        "description": "Label text for the checkbox"
                    },
                    {
                        "name": "helper_text",
                        "type": "str | None",
                        "description": "Helper text displayed below the label"
                    },
                    {
                        "name": "error_text",
                        "type": "str | None",
                        "description": "Error message displayed below the checkbox"
                    },
                    {
                        "name": "label_cls",
                        "type": "str",
                        "description": "Additional CSS classes for the label"
                    },
                    {
                        "name": "checkbox_cls",
                        "type": "str",
                        "description": "Additional CSS classes for the checkbox itself"
                    }
                ]
            }
        ]
    }
    
    # Hero example - Interactive settings panel
    hero_example = ComponentPreview(
        Card(
            CardHeader(
                CardTitle("Quick Setup"),
                CardDescription("Configure your preferences in seconds")
            ),
            CardContent(
                Div(
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
                                ds_text("[$dark_mode && 'Dark Mode', $notifications && 'Notifications', $auto_save && 'Auto-save'].filter(Boolean).join(', ') || 'None selected'"),
                                cls="font-medium text-sm break-words"
                            ),
                            cls="min-h-[1.25rem]"
                        ),
                        cls="mt-4 pt-4 border-t"
                    ),
                    ds_signals(dark_mode=True, notifications=False, auto_save=True),
                    cls="space-y-3"
                )
            ),
            cls="max-w-md mx-auto"
        ),
        '''Card(
    CardHeader(
        CardTitle("Quick Setup"),
        CardDescription("Configure your preferences in seconds")
    ),
    CardContent(
        Div(
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
                P("Your preferences: ", cls="text-sm text-muted-foreground mb-1"),
                P(
                    Span(
                        ds_text("[$dark_mode && 'Dark Mode', $notifications && 'Notifications', $auto_save && 'Auto-save'].filter(Boolean).join(', ') || 'None selected'"),
                        cls="font-medium text-sm break-words"
                    ),
                    cls="min-h-[1.25rem]"
                ),
                cls="mt-4 pt-4 border-t"
            ),
            ds_signals(dark_mode=True, notifications=False, auto_save=True)
        )
    )
)''',
        copy_button=True
    )
    
    return auto_generate_page(
        TITLE,
        DESCRIPTION,
        list(examples()),
        cli_command="star add checkbox",
        api_reference=api_reference,
        hero_example=hero_example,
        component_slug="checkbox"
    )