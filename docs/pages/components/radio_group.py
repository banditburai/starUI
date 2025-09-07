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
from starhtml import Input as HTMLInput, Label as HTMLLabel
from starhtml.datastar import (
    ds_on_click, ds_show, ds_text, ds_signals, value,
    ds_bind, ds_disabled, ds_on_change, ds_effect, ds_class, ds_style, ds_attr, if_, toggle
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
            ds_signals(size_radio=value("md")),
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
    
    # Use RadioGroupItem with custom card styling
    def PlanCard(value, name, price, description, features, badge=None):
        """Create a RadioGroupItem that displays as a card."""
        # Create rich label content with card styling
        label_content = Div(
            Div(
                Div(
                    P(name, cls="font-semibold text-base"),
                    badge and Badge(badge, variant="secondary", cls="ml-2") or None,
                    cls="flex items-center"
                ),
                P(price, cls="text-2xl font-bold mt-1"),
                P(description, cls="text-sm text-muted-foreground mt-2"),
                Div(
                    *[P(f"• {feature}", cls="text-sm") for feature in features],
                    cls="mt-3 space-y-1"
                ),
                cls="flex flex-col"
            ),
            # Use ds_attr to properly set data-selected based on signal
            ds_attr(data_selected=f"$selected_plan === '{value}' ? 'true' : 'false'"),
            cls="p-4 border-2 rounded-lg h-full min-h-[220px] w-full transition-all hover:bg-gray-50 dark:hover:bg-gray-800 border-gray-200 dark:border-gray-700 data-[selected=true]:border-blue-500 data-[selected=true]:ring-2 data-[selected=true]:ring-blue-500/20 data-[selected=true]:bg-blue-50 dark:data-[selected=true]:bg-blue-950/20",
        )
        
        # Return RadioGroupItem - RadioGroupItem handles the layout when hide_indicators=True
        return RadioGroupItem(
            value=value,
            label=label_content,
            class_name="w-full",
        )
    
    # Subscription tier selector with card-styled RadioGroupItems
    yield ComponentPreview(
        Card(
            CardHeader(
                CardTitle("Choose Your Plan"),
                CardDescription("Select the plan that best fits your needs")
            ),
            CardContent(
                Form(
                    P("Subscription Plans", cls="text-sm font-medium mb-4"),
                    RadioGroup(
                        PlanCard(
                            "free",
                            "Free",
                            "$0/month",
                            "Perfect for trying out our service",
                            ["10 projects", "Basic support", "1GB storage"],
                            badge="Most Popular"
                        ),
                        PlanCard(
                            "pro",
                            "Professional", 
                            "$29/month",
                            "For professional developers",
                            ["Unlimited projects", "Priority support", "100GB storage", "Advanced features"]
                        ),
                        PlanCard(
                            "enterprise",
                            "Enterprise",
                            "Custom pricing",
                            "For large teams and organizations",
                            ["Everything in Pro", "Dedicated support", "Unlimited storage", "Custom integrations", "SLA guarantee"]
                        ),
                        initial_value="free",
                        signal="selected_plan",
                        hide_indicators=True,  # Hide radio dots for card-style selection
                        cls="grid grid-cols-1 gap-3 w-full"  # Use grid for truly consistent width
                    ),
                    P(
                        "Selected plan: ",
                        Code(ds_text("$selected_plan || 'none'"), cls="ml-2"),
                        cls="text-sm text-muted-foreground mt-4"
                    ),
                    Button(
                        ds_text("$selected_plan === 'enterprise' ? 'Contact Sales' : 'Get Started'"),
                        ds_on_click("alert(`Selected plan: ${$selected_plan}`)"),
                        cls="w-full mt-4"
                    )
                )
            ),
            cls="max-w-2xl"
        ),
        '''# Custom PlanCard component that works with RadioGroup
def PlanCard(value, name, price, description, features, badge=None):
    def create_plan_card(signal, group_name, default_value=None):
        radio_id = f"plan_{uuid4()[:8]}"
        return Div(
            HTMLInput(
                type="radio", id=radio_id, name=group_name, value=value,
                ds_on_change(f"${signal} = '{value}'"), cls="sr-only peer"
            ),
            HTMLLabel(
                Div(
                    # Plan content with peer-checked: styling
                    cls="p-4 border-2 rounded-lg cursor-pointer transition-all peer-checked:border-primary peer-checked:ring-2 peer-checked:shadow-md"
                ),
                for_=radio_id, cls="block w-full cursor-pointer"
            )
        )
    return create_plan_card

# Use with RadioGroup for semantic structure
RadioGroup(
    PlanCard("free", "Free", "$0/month", "Perfect for trying out", ["10 projects"]),
    PlanCard("pro", "Professional", "$29/month", "For developers", ["Unlimited"]),
    initial_value="free", signal="selected_plan"
)''',
        title="Subscription Plans",
        description="Rich radio options with proper RadioGroup semantics and CSS peer selectors"
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
                            P("Secure payment processing", cls="text-sm"),
                            ds_show("$payment_method === 'card'"),
                            cls="flex items-center p-3 bg-muted rounded-md w-full"
                        ),
                        Div(
                            Icon("lucide:wallet", cls="h-5 w-5 mr-2"),
                            P("Secure payment processing", cls="text-sm"),
                            ds_show("$payment_method === 'paypal'"),
                            cls="flex items-center p-3 bg-muted rounded-md w-full"
                        ),
                        Div(
                            Icon("lucide:building-2", cls="h-5 w-5 mr-2"),
                            P("Secure payment processing", cls="text-sm"),
                            ds_show("$payment_method === 'bank'"),
                            cls="flex items-center p-3 bg-muted rounded-md w-full"
                        ),
                        Div(
                            Icon("lucide:bitcoin", cls="h-5 w-5 mr-2"),
                            P("Secure payment processing", cls="text-sm"),
                            ds_show("$payment_method === 'crypto'"),
                            cls="flex items-center p-3 bg-muted rounded-md w-full"
                        ),
                        cls="mt-4 h-16 flex items-center"
                    ),
                    Button(
                        "Continue to Payment",
                        ds_on_click("event.preventDefault(); alert(`Proceeding with ${$payment_method}`)"),
                        type="submit",
                        cls="w-full mt-4",                        
                    ),
                    ds_signals(
                        payment_method=value("card")
                    )
                )
            ),
            cls="max-w-lg"
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
    ds_show="$payment_method === 'card'"
)''',
        title="Payment Method",
        description="Payment selection with contextual information"
    )
    
    # Interactive 3-question survey
    yield ComponentPreview(
        Card(
            CardHeader(
                CardTitle(
                    ds_text("'Question ' + ($step + 1) + ' of 3'")
                ),
                CardDescription("Web Development Survey")
            ),
            CardContent(
                # Progress bar at the top
                    Div(
                        P(
                            ds_text("`Question ${$step + 1} of 3`"),
                            cls="text-xs text-muted-foreground mb-2"
                        ),
                        Div(
                            Div(
                                ds_style(width="`${([$survey_q1, $survey_q2, $survey_q3].filter(q => q !== '').length / 3) * 100}%`"),
                                cls="h-2 bg-primary rounded-full transition-all duration-300"
                            ),
                            cls="w-full bg-secondary rounded-full h-2 mb-6"
                        ),
                        cls="mb-4"
                    ),
                    
                    
                    # Question 1 - Programming Language
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
                            required=True
                        ),
                        ds_show("$step === 0")
                    ),
                    
                    # Question 2 - Experience Level
                    Div(
                        RadioGroupWithLabel(
                            label="How many years of development experience do you have?",
                            options=[
                                {"value": "0-1", "label": "Less than 1 year"},
                                {"value": "1-3", "label": "1-3 years"},
                                {"value": "3-5", "label": "3-5 years"},
                                {"value": "5-10", "label": "5-10 years"},
                                {"value": "10+", "label": "More than 10 years"}
                            ],
                            signal="survey_q2",
                            required=True
                        ),
                        ds_show("$step === 1")
                    ),
                    
                    # Question 3 - Preferred Framework
                    Div(
                        RadioGroupWithLabel(
                            label="Which frontend framework do you prefer?",
                            options=[
                                {"value": "react", "label": "React"},
                                {"value": "vue", "label": "Vue.js"},
                                {"value": "angular", "label": "Angular"},
                                {"value": "svelte", "label": "Svelte"},
                                {"value": "datastar", "label": "Datastar"},
                                {"value": "vanilla", "label": "Vanilla JS"},
                                {"value": "none", "label": "I'm a backend developer"}
                            ],
                            signal="survey_q3",
                            required=True
                        ),
                        ds_show("$step === 2")
                    ),
                    
                    # Validation message - only show if submitted and no answer
                    P(
                        "Please select an answer to continue",
                        ds_show("$survey_error_visible"),
                        cls="text-sm text-destructive mt-2",                        
                    ),
                    
                    # Navigation buttons
                    Div(
                        Button(
                            ds_disabled("$step === 0"),
                            ds_on_click("if ($step > 0) { $step = $step - 1 }"),
                            "Previous",
                            variant="outline",
                            disabled=True,  # Will be overridden by ds_disabled                            
                        ),
                        Button(
                            "Next",
                            ds_text("$step === 2 ? 'Complete' : 'Next'"),
                            ds_on_click("if ($step < 2) { $step = $step + 1 } else { alert('Survey Complete!') }")
                        ),
                        cls="flex justify-between mt-6"
                    ),
                
                ds_signals(
                    step=0,
                    survey_q1=value(""),
                    survey_q2=value(""),
                    survey_q3=value("")
                )
            ),
            cls="max-w-lg"
        ),
        '''Card(
    CardHeader(
        CardTitle(ds_text("'Question ' + ($step + 1) + ' of 3'")),
        CardDescription("Web Development Survey")
    ),
    CardContent(
        # Progress bar at top
        Div(
            P(ds_text("`Step ${$step + 1} of 3`"), cls="text-xs text-muted-foreground mb-2"),
            Div(
                Div(
                    ds_style(width="`${([$survey_q1, $survey_q2, $survey_q3].filter(q => q !== '').length / 3) * 100}%`"),
                    cls="h-2 bg-primary rounded-full transition-all duration-300"
                ),
                cls="w-full bg-secondary rounded-full h-2 mb-6"
            )
        ),
        
        # Questions with conditional display
        Div(
            ds_show("$step === 0"),
            RadioGroupWithLabel(
                label="What is your primary programming language?",
                options=[
                    {"value": "javascript", "label": "JavaScript/TypeScript"},
                    {"value": "python", "label": "Python"}
                ],
                signal="survey_q1"
            )
        ),
        
        # Navigation buttons  
        Div(
            Button("Previous", variant="outline", ds_disabled("$step === 0")),
            Button(ds_text("$step === 2 ? 'Complete Survey' : 'Next'")),
            cls="flex justify-between mt-6"
        ),
        
        ds_signals(step=0, survey_q1=value(""), survey_q2=value(""), survey_q3=value(""))
    )
)''',
        title="Interactive Survey",
        description="Multi-step survey with progress tracking and validation"
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
                    ),
                    ds_signals(
                        theme_setting=value("system"),
                        font_setting=value("medium"),
                        language_setting=value("en")
                    )
                )
            ),
            cls="max-w-lg"
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
        Button("Apply Settings", ds_on_click("applySettings()"))
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