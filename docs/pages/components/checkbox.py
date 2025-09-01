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
    ds_bind, ds_disabled, ds_on_change, ds_effect, ds_class, toggle, ds_style
)
from starui.registry.components.checkbox import Checkbox, CheckboxWithLabel
from starui.registry.components.button import Button
from starui.registry.components.card import Card, CardHeader, CardContent, CardTitle, CardDescription
from starui.registry.components.badge import Badge
from utils import auto_generate_page
from widgets.component_preview import ComponentPreview


def examples():
    """Generate checkbox examples using ComponentPreview with tabs."""
    
    # Basic usage
    yield ComponentPreview(
        Div(
            Checkbox(),
            Checkbox(checked=True, cls="ml-4"),
            Checkbox(disabled=True, cls="ml-4"),
            Checkbox(checked=True, disabled=True, cls="ml-4"),
            cls="flex items-center gap-4"
        ),
        '''Checkbox()
Checkbox(checked=True)
Checkbox(disabled=True)
Checkbox(checked=True, disabled=True)''',
        title="Basic Checkboxes",
        description="Default, checked, and disabled states"
    )
    
    # With labels and helper text
    yield ComponentPreview(
        Div(
            CheckboxWithLabel(
                label="Accept terms and conditions",
                signal="terms"
            ),
            CheckboxWithLabel(
                label="Subscribe to newsletter",
                helper_text="Get weekly updates about new features",
                checked=True,
                signal="newsletter"
            ),
            CheckboxWithLabel(
                label="Required field",
                required=True,
                helper_text="This field must be checked to continue",
                signal="required_field"
            ),
            cls="space-y-4"
        ),
        '''CheckboxWithLabel(
    label="Accept terms and conditions",
    signal="terms"
)
CheckboxWithLabel(
    label="Subscribe to newsletter",
    helper_text="Get weekly updates about new features",
    checked=True,
    signal="newsletter"
)
CheckboxWithLabel(
    label="Required field",
    required=True,
    helper_text="This field must be checked to continue",
    signal="required_field"
)''',
        title="Checkbox with Labels",
        description="Labels, helper text, and required indicators"
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
                        label_cls=ds_class(**{"line-through text-muted-foreground": "$todo1"})
                    ),
                    CheckboxWithLabel(
                        label="Review pull requests",
                        signal="todo2",
                        label_cls=ds_class(**{"line-through text-muted-foreground": "$todo2"})
                    ),
                    CheckboxWithLabel(
                        label="Update dependencies",
                        signal="todo3",
                        label_cls=ds_class(**{"line-through text-muted-foreground": "$todo3"})
                    ),
                    CheckboxWithLabel(
                        label="Deploy to production",
                        signal="todo4",
                        label_cls=ds_class(**{"line-through text-muted-foreground": "$todo4"})
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
                    Div(
                        cls="w-full bg-secondary rounded-full h-2 mt-2",
                        children=[
                            Div(
                                ds_style(width="`${[$todo1, $todo2, $todo3, $todo4].filter(Boolean).length * 25}%`"),
                                cls="bg-primary h-2 rounded-full transition-all duration-300"
                            )
                        ]
                    ),
                    cls="mt-4"
                ),
                ds_signals(todo1=True, todo2=True, todo3=False, todo4=False)
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
            Div(  # Progress bar
                Div(ds_style(width="`${[$todo1, $todo2, $todo3, $todo4].filter(Boolean).length * 25}%`")),
            )
        ),
        ds_signals(todo1=True, todo2=True, todo3=False, todo4=False)
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
                        CheckboxWithLabel(
                            label="invoice-2024-001.pdf",
                            signal="file1",
                            helper_text="2.4 MB"
                        ),
                        CheckboxWithLabel(
                            label="report-q3.xlsx",
                            signal="file2",
                            helper_text="1.8 MB"
                        ),
                        CheckboxWithLabel(
                            label="presentation.pptx",
                            signal="file3",
                            helper_text="5.2 MB"
                        ),
                        CheckboxWithLabel(
                            label="contracts.zip",
                            signal="file4",
                            helper_text="12.1 MB"
                        ),
                        cls="space-y-2 pl-6"
                    ),
                    Div(
                        Button(
                            Icon("lucide:trash-2", cls="h-4 w-4 mr-2"),
                            "Delete Selected",
                            variant="destructive",
                            size="sm",
                            ds_disabled="!$file1 && !$file2 && !$file3 && !$file4",
                            ds_on_click="alert(`Deleting ${[$file1 && 'invoice-2024-001.pdf', $file2 && 'report-q3.xlsx', $file3 && 'presentation.pptx', $file4 && 'contracts.zip'].filter(Boolean).length} files`)"
                        ),
                        P(
                            ds_text("[$file1, $file2, $file3, $file4].filter(Boolean).length"),
                            " items selected",
                            cls="text-sm text-muted-foreground ml-auto",
                            ds_show="[$file1, $file2, $file3, $file4].some(Boolean)"
                        ),
                        cls="flex items-center justify-between mt-4 pt-4 border-t"
                    ),
                    ds_signals(selectAll=False, file1=False, file2=False, file3=False, file4=False),
                    ds_effect("$selectAll = $file1 && $file2 && $file3 && $file4 && ($file1 || $file2 || $file3 || $file4)"),
                    ds_on_change("""
                        if (event.target.matches('[data-bind="selectAll"]')) {
                            $file1 = $selectAll;
                            $file2 = $selectAll;
                            $file3 = $selectAll;
                            $file4 = $selectAll;
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
                CheckboxWithLabel(label="file1.pdf", signal="file1"),
                CheckboxWithLabel(label="file2.xlsx", signal="file2"),
                # ... more files
            ),
            Button(
                "Delete Selected",
                ds_disabled("!$file1 && !$file2 && !$file3 && !$file4"),
                ds_on_click("deleteSelected()")
            ),
            ds_signals(selectAll=False, file1=False, file2=False, file3=False, file4=False),
            ds_effect("$selectAll = $file1 && $file2 && $file3 && $file4"),
            ds_on_change("if (event.target.matches('[data-bind=\\"selectAll\\"]')) { /* sync all */ }")
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
                        CheckboxWithLabel(
                            label="Marketing Communications",
                            helper_text="Product updates and special offers",
                            signal="marketing",
                            checkbox_cls=ds_class(**{"border-blue-500": "$marketing"})
                        ),
                        cls="space-y-4"
                    ),
                    Div(
                        P(
                            Icon("lucide:alert-circle", cls="h-4 w-4 inline mr-1"),
                            "At least one notification method must be enabled",
                            ds_show("!$email_notif && !$push_notif && !$sms_notif"),
                            cls="text-sm text-destructive"
                        ),
                        cls="mt-4"
                    ),
                    Button(
                        "Save Settings",
                        type="submit",
                        ds_disabled="!$email_notif && !$push_notif && !$sms_notif",
                        ds_on_click="event.preventDefault(); alert('Settings saved!')",
                        cls="w-full mt-4"
                    ),
                    Div(
                        Badge(
                            ds_text("'Active: ' + [$email_notif && 'Email', $push_notif && 'Push', $sms_notif && 'SMS'].filter(Boolean).join(', ')"),
                            variant="secondary",
                            ds_show="$email_notif || $push_notif || $sms_notif"
                        ),
                        cls="mt-4 text-center"
                    ),
                    ds_signals(email_notif=True, push_notif=False, sms_notif=False, marketing=False)
                )
            ),
            cls="max-w-md"
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
    
    # Hero example
    hero_example = ComponentPreview(
        Div(
            Div(
                Checkbox(cls="mr-4"),
                CheckboxWithLabel(label="I agree to the terms", signal="terms_hero", cls="mr-4"),
                CheckboxWithLabel(
                    label="Subscribe to updates",
                    helper_text="Get notified about new features",
                    checked=True,
                    signal="updates_hero"
                ),
                cls="flex flex-col sm:flex-row gap-4 items-start sm:items-center"
            ),
            cls="flex justify-center"
        ),
        '''Checkbox()
CheckboxWithLabel(label="I agree to the terms", signal="terms")
CheckboxWithLabel(
    label="Subscribe to updates",
    helper_text="Get notified about new features", 
    checked=True,
    signal="updates"
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