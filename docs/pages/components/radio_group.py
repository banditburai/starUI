"""
RadioGroup component documentation - Convention-based functional approach.
Clean, minimal, and easy to extend.
"""

# Component metadata for auto-discovery
TITLE = "Radio Group"
DESCRIPTION = "A set of checkable buttons—known as radio buttons—where no more than one of the buttons can be checked at a time."
CATEGORY = "form"
ORDER = 30
STATUS = "stable"

from starhtml import Div, P, Input, Label, Icon, Span, H2, H3, Form, Code
from starhtml.datastar import (
    ds_on_click, ds_show, ds_text, ds_signals, value,
    ds_bind, ds_disabled, ds_on_change, ds_effect, ds_class, toggle
)
from starui.registry.components.radio_group import RadioGroup, RadioGroupItem, RadioGroupWithLabel
from starui.registry.components.button import Button
from starui.registry.components.card import Card, CardHeader, CardContent, CardTitle, CardDescription
from starui.registry.components.badge import Badge
from starui.registry.components.separator import Separator
from utils import auto_generate_page
from widgets.component_preview import ComponentPreview


def examples():
    """Generate radio group examples using ComponentPreview with tabs."""
    
    # Basic usage
    yield ComponentPreview(
        Div(
            RadioGroup(
                RadioGroupItem(value="option1", label="Option 1"),
                RadioGroupItem(value="option2", label="Option 2"),
                RadioGroupItem(value="option3", label="Option 3"),
                signal="basic_radio",
                initial_value="option1"
            ),
            P(
                "Selected: ",
                Code(ds_text("$basic_radio || 'none'"), cls="ml-2"),
                cls="text-sm text-muted-foreground mt-4"
            ),
            cls="space-y-4"
        ),
        '''RadioGroup(
    RadioGroupItem(value="option1", label="Option 1"),
    RadioGroupItem(value="option2", label="Option 2"),
    RadioGroupItem(value="option3", label="Option 3"),
    signal="basic_radio",
    initial_value="option1"
)''',
        title="Basic Radio Group",
        description="Simple radio button group with selection tracking"
    )
    
    # Horizontal layout
    yield ComponentPreview(
        Div(
            RadioGroupWithLabel(
                label="Size",
                options=[
                    {"value": "xs", "label": "Extra Small"},
                    {"value": "sm", "label": "Small"},
                    {"value": "md", "label": "Medium"},
                    {"value": "lg", "label": "Large"},
                    {"value": "xl", "label": "Extra Large"}
                ],
                orientation="horizontal",
                value="md",
                signal="size_radio",
                helper_text="Choose the appropriate size for your needs"
            ),
            cls="max-w-lg"
        ),
        '''RadioGroupWithLabel(
    label="Size",
    options=[
        {"value": "xs", "label": "Extra Small"},
        {"value": "sm", "label": "Small"},
        {"value": "md", "label": "Medium"},
        {"value": "lg", "label": "Large"},
        {"value": "xl", "label": "Extra Large"}
    ],
    orientation="horizontal",
    value="md",
    signal="size_radio",
    helper_text="Choose the appropriate size"
)''',
        title="Horizontal Layout",
        description="Radio buttons arranged horizontally"
    )
    
    # Subscription tier selector
    yield ComponentPreview(
        Card(
            CardHeader(
                CardTitle("Choose Your Plan"),
                CardDescription("Select the plan that best fits your needs")
            ),
            CardContent(
                RadioGroup(
                    Div(
                        RadioGroupItem(value="free", label=""),
                        Div(
                            Div(
                                P("Free", cls="font-semibold"),
                                Badge("Most Popular", variant="secondary", cls="ml-2"),
                                cls="flex items-center"
                            ),
                            P("$0/month", cls="text-2xl font-bold mt-1"),
                            P("Perfect for trying out our service", cls="text-sm text-muted-foreground"),
                            P("• 10 projects", cls="text-sm mt-2"),
                            P("• Basic support", cls="text-sm"),
                            P("• 1GB storage", cls="text-sm"),
                            cls="flex-1 ml-2"
                        ),
                        cls="flex gap-3 p-4 border rounded-lg",
                        ds_class={"border-primary bg-accent": "$plan === 'free'"}
                    ),
                    Div(
                        RadioGroupItem(value="pro", label=""),
                        Div(
                            P("Professional", cls="font-semibold"),
                            P("$29/month", cls="text-2xl font-bold mt-1"),
                            P("For professional developers", cls="text-sm text-muted-foreground"),
                            P("• Unlimited projects", cls="text-sm mt-2"),
                            P("• Priority support", cls="text-sm"),
                            P("• 100GB storage", cls="text-sm"),
                            P("• Advanced features", cls="text-sm"),
                            cls="flex-1 ml-2"
                        ),
                        cls="flex gap-3 p-4 border rounded-lg",
                        ds_class={"border-primary bg-accent": "$plan === 'pro'"}
                    ),
                    Div(
                        RadioGroupItem(value="enterprise", label=""),
                        Div(
                            P("Enterprise", cls="font-semibold"),
                            P("Custom pricing", cls="text-2xl font-bold mt-1"),
                            P("For large teams and organizations", cls="text-sm text-muted-foreground"),
                            P("• Everything in Pro", cls="text-sm mt-2"),
                            P("• Dedicated support", cls="text-sm"),
                            P("• Unlimited storage", cls="text-sm"),
                            P("• Custom integrations", cls="text-sm"),
                            P("• SLA guarantee", cls="text-sm"),
                            cls="flex-1 ml-2"
                        ),
                        cls="flex gap-3 p-4 border rounded-lg",
                        ds_class={"border-primary bg-accent": "$plan === 'enterprise'"}
                    ),
                    signal="plan",
                    initial_value="free",
                    cls="space-y-3"
                ),
                Button(
                    ds_text("$plan === 'enterprise' ? 'Contact Sales' : 'Get Started'"),
                    cls="w-full mt-6",
                    ds_on_click="alert(`Selected plan: ${$plan}`)"
                ),
                ds_signals(plan=value("free"))
            ),
            cls="max-w-lg"
        ),
        '''RadioGroup(
    Div(
        RadioGroupItem(value="free", label=""),
        Div(
            Div(
                P("Free", cls="font-semibold"),
                Badge("Most Popular", variant="secondary")
            ),
            P("$0/month", cls="text-2xl font-bold"),
            P("Perfect for trying out", cls="text-sm text-muted-foreground"),
            P("• 10 projects"),
            P("• Basic support"),
            cls="flex-1 ml-2"
        ),
        cls="flex gap-3 p-4 border rounded-lg",
        ds_class({"border-primary bg-accent": "$plan === 'free'"})
    ),
    // More plan options...
    signal="plan",
    initial_value="free"
)''',
        title="Subscription Plans",
        description="Rich radio options with detailed information"
    )
    
    # Payment method selector
    yield ComponentPreview(
        Card(
            CardHeader(
                CardTitle("Payment Method"),
                CardDescription("How would you like to pay?")
            ),
            CardContent(
                Form(
                    RadioGroupWithLabel(
                        label="Select payment method",
                        options=[
                            {"value": "card", "label": "Credit/Debit Card"},
                            {"value": "paypal", "label": "PayPal"},
                            {"value": "bank", "label": "Bank Transfer"},
                            {"value": "crypto", "label": "Cryptocurrency"}
                        ],
                        value="card",
                        signal="payment_method",
                        required=True
                    ),
                    Div(
                        Div(
                            Icon("lucide:credit-card", cls="h-5 w-5 mr-2"),
                            P("Secure card payment", cls="text-sm"),
                            ds_show("$payment_method === 'card'"),
                            cls="flex items-center p-3 bg-muted rounded-md"
                        ),
                        Div(
                            Icon("lucide:wallet", cls="h-5 w-5 mr-2"),
                            P("Pay with PayPal balance", cls="text-sm"),
                            ds_show("$payment_method === 'paypal'"),
                            cls="flex items-center p-3 bg-muted rounded-md"
                        ),
                        Div(
                            Icon("lucide:building-2", cls="h-5 w-5 mr-2"),
                            P("Direct bank transfer", cls="text-sm"),
                            ds_show("$payment_method === 'bank'"),
                            cls="flex items-center p-3 bg-muted rounded-md"
                        ),
                        Div(
                            Icon("lucide:bitcoin", cls="h-5 w-5 mr-2"),
                            P("Bitcoin or Ethereum", cls="text-sm"),
                            ds_show("$payment_method === 'crypto'"),
                            cls="flex items-center p-3 bg-muted rounded-md"
                        ),
                        cls="mt-4"
                    ),
                    Button(
                        "Continue to Payment",
                        type="submit",
                        cls="w-full mt-4",
                        ds_on_click="event.preventDefault(); alert(`Proceeding with ${$payment_method}`)"
                    )
                )
            ),
            cls="max-w-md"
        ),
        '''RadioGroupWithLabel(
    label="Select payment method",
    options=[
        {"value": "card", "label": "Credit/Debit Card"},
        {"value": "paypal", "label": "PayPal"},
        {"value": "bank", "label": "Bank Transfer"},
        {"value": "crypto", "label": "Cryptocurrency"}
    ],
    value="card",
    signal="payment_method",
    required=True
)
// Show context based on selection
Div(
    Icon("lucide:credit-card"),
    P("Secure card payment"),
    ds_show("$payment_method === 'card'"
)''',
        title="Payment Method",
        description="Payment selection with contextual information"
    )
    
    # Survey/Quiz question
    yield ComponentPreview(
        Card(
            CardHeader(
                CardTitle("Question 1 of 3"),
                CardDescription("Web Development Survey")
            ),
            CardContent(
                Div(
                    RadioGroupWithLabel(
                        label="What is your primary programming language?",
                        options=[
                            {"value": "javascript", "label": "JavaScript/TypeScript"},
                            {"value": "python", "label": "Python"},
                            {"value": "java", "label": "Java"},
                            {"value": "csharp", "label": "C#"},
                            {"value": "go", "label": "Go"},
                            {"value": "rust", "label": "Rust"},
                            {"value": "other", "label": "Other"}
                        ],
                        signal="survey_q1",
                        required=True,
                        error_text=(ds_show("$survey_submitted && !$survey_q1") and "Please select an answer" or None)
                    ),
                    Div(
                        Button(
                            "Previous",
                            variant="outline",
                            disabled=True,
                            cls="mr-2"
                        ),
                        Button(
                            "Next",
                            ds_on_click="""
                                $survey_submitted = true;
                                if ($survey_q1) {
                                    alert('Moving to question 2');
                                    $survey_submitted = false;
                                }
                            """
                        ),
                        cls="flex justify-between mt-6"
                    ),
                    Div(
                        Div(
                            cls="w-1/3 h-2 bg-primary rounded-full"
                        ),
                        cls="w-full bg-secondary rounded-full h-2 mt-4"
                    ),
                    ds_signals(survey_q1=value(""), survey_submitted=False)
                )
            ),
            cls="max-w-md"
        ),
        '''Card(
    CardHeader(
        CardTitle("Question 1 of 3"),
        CardDescription("Web Development Survey")
    ),
    CardContent(
        RadioGroupWithLabel(
            label="What is your primary programming language?",
            options=[
                {"value": "javascript", "label": "JavaScript/TypeScript"},
                {"value": "python", "label": "Python"},
                // ... more options
            ],
            signal="survey_q1",
            required=True,
            error_text=ds_show("$submitted && !$survey_q1") and "Required" or None
        ),
        Div(
            Button("Previous", disabled=True),
            Button("Next", ds_on_click="validateAndNext()")
        ),
        // Progress bar
        Div(cls="w-1/3 h-2 bg-primary rounded-full")
    )
)''',
        title="Survey Question",
        description="Multi-step form with validation"
    )
    
    # Settings panel
    yield ComponentPreview(
        Card(
            CardHeader(
                CardTitle("Display Settings"),
                CardDescription("Customize your viewing experience")
            ),
            CardContent(
                Div(
                    RadioGroupWithLabel(
                        label="Theme",
                        options=[
                            {"value": "light", "label": "Light"},
                            {"value": "dark", "label": "Dark"},
                            {"value": "system", "label": "System"}
                        ],
                        value="system",
                        signal="theme_setting",
                        helper_text="Choose your preferred color scheme"
                    ),
                    Separator(cls="my-4"),
                    RadioGroupWithLabel(
                        label="Font Size",
                        options=[
                            {"value": "small", "label": "Small (14px)"},
                            {"value": "medium", "label": "Medium (16px)"},
                            {"value": "large", "label": "Large (18px)"}
                        ],
                        value="medium",
                        signal="font_setting",
                        helper_text="Adjust text size for better readability"
                    ),
                    Separator(cls="my-4"),
                    RadioGroupWithLabel(
                        label="Language",
                        options=[
                            {"value": "en", "label": "English"},
                            {"value": "es", "label": "Español"},
                            {"value": "fr", "label": "Français"},
                            {"value": "de", "label": "Deutsch"},
                            {"value": "ja", "label": "日本語"}
                        ],
                        value="en",
                        signal="language_setting"
                    ),
                    Button(
                        "Apply Settings",
                        cls="w-full mt-6",
                        ds_on_click="alert(`Settings applied:\\nTheme: ${$theme_setting}\\nFont: ${$font_setting}\\nLanguage: ${$language_setting}`)"
                    )
                )
            ),
            cls="max-w-md"
        ),
        '''Card(
    CardContent(
        RadioGroupWithLabel(
            label="Theme",
            options=[
                {"value": "light", "label": "Light"},
                {"value": "dark", "label": "Dark"},
                {"value": "system", "label": "System"}
            ],
            value="system",
            signal="theme_setting"
        ),
        Separator(),
        RadioGroupWithLabel(
            label="Font Size",
            options=[
                {"value": "small", "label": "Small (14px)"},
                {"value": "medium", "label": "Medium (16px)"},
                {"value": "large", "label": "Large (18px)"}
            ],
            value="medium",
            signal="font_setting"
        ),
        Button("Apply Settings", ds_on_click="applySettings()")
    )
)''',
        title="Settings Panel",
        description="Multiple radio groups for configuration"
    )


def create_radio_group_docs():
    """Create radio group documentation page using convention-based approach."""
    
    api_reference = {
        "props": [
            {
                "name": "initial_value",
                "type": "str | None",
                "default": "None",
                "description": "Initially selected radio value"
            },
            {
                "name": "signal",
                "type": "str",
                "default": "auto-generated",
                "description": "Datastar signal name for state management"
            },
            {
                "name": "disabled",
                "type": "bool",
                "default": "False",
                "description": "Whether entire group is disabled"
            },
            {
                "name": "required",
                "type": "bool",
                "default": "False",
                "description": "Whether selection is required"
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
                "name": "RadioGroupItem",
                "description": "Individual radio button option",
                "props": [
                    {
                        "name": "value",
                        "type": "str",
                        "description": "Value when this option is selected"
                    },
                    {
                        "name": "label",
                        "type": "str | None",
                        "description": "Display label for the radio button"
                    },
                    {
                        "name": "disabled",
                        "type": "bool",
                        "default": "False",
                        "description": "Whether this specific option is disabled"
                    },
                    {
                        "name": "indicator_cls",
                        "type": "str",
                        "default": "''",
                        "description": "Additional CSS classes for the indicator"
                    }
                ]
            },
            {
                "name": "RadioGroupWithLabel",
                "description": "Complete radio group with label and helper text",
                "props": [
                    {
                        "name": "label",
                        "type": "str",
                        "description": "Label text for the radio group"
                    },
                    {
                        "name": "options",
                        "type": "list[dict[str, Any]]",
                        "description": "List of option dictionaries with 'value', 'label', and optional 'disabled' keys"
                    },
                    {
                        "name": "value",
                        "type": "str | None",
                        "description": "Initially selected value"
                    },
                    {
                        "name": "signal",
                        "type": "str | None",
                        "description": "Datastar signal name"
                    },
                    {
                        "name": "helper_text",
                        "type": "str | None",
                        "description": "Helper text below the radio group"
                    },
                    {
                        "name": "error_text",
                        "type": "str | None",
                        "description": "Error message"
                    },
                    {
                        "name": "orientation",
                        "type": "str",
                        "default": "'vertical'",
                        "description": "Layout orientation ('vertical' or 'horizontal')"
                    }
                ]
            }
        ]
    }
    
    # Hero example
    hero_example = ComponentPreview(
        Div(
            RadioGroup(
                RadioGroupItem(value="email", label="Email notifications"),
                RadioGroupItem(value="sms", label="SMS notifications"),
                RadioGroupItem(value="push", label="Push notifications"),
                RadioGroupItem(value="none", label="No notifications"),
                signal="notification_pref",
                initial_value="email"
            ),
            cls="max-w-md mx-auto"
        ),
        '''RadioGroup(
    RadioGroupItem(value="email", label="Email notifications"),
    RadioGroupItem(value="sms", label="SMS notifications"),
    RadioGroupItem(value="push", label="Push notifications"),
    RadioGroupItem(value="none", label="No notifications"),
    signal="notification_pref",
    initial_value="email"
)''',
        copy_button=True
    )
    
    return auto_generate_page(
        TITLE,
        DESCRIPTION,
        list(examples()),
        cli_command="star add radio-group",
        api_reference=api_reference,
        hero_example=hero_example,
        component_slug="radio-group"
    )