TITLE = "Radio Group"
DESCRIPTION = "A set of checkable buttons—known as radio buttons—where no more than one of the buttons can be checked at a time."
CATEGORY = "form"
ORDER = 30
STATUS = "stable"

from starhtml import Div, P, Icon, Span, H3, Form, Code, Signal, js
from starui.registry.components.radio_group import RadioGroup, RadioGroupItem, RadioGroupWithLabel
from starui.registry.components.button import Button
from starui.registry.components.card import Card, CardHeader, CardContent, CardTitle, CardDescription
from starui.registry.components.badge import Badge
from starui.registry.components.separator import Separator
from utils import auto_generate_page, with_code, Component, build_api_reference



@with_code
def horizontal_layout_example():
    return Div(
        (size_radio := Signal("size_radio", "md")),
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
            signal=size_radio,
            helper_text="Choose the appropriate size for your needs"
        ),
        cls="max-w-lg"
    )


@with_code
def subscription_plans_example():
    selected_plan = Signal("selected_plan", "free")

    def PlanCard(value, name, price, description, features, badge=None):
        is_initial = selected_plan.default == value
        return RadioGroupItem(
            value=value,
            label=Div(
                Div(
                    Div(
                        P(name, cls="font-semibold text-base"),
                        Badge(badge, variant="secondary", cls="ml-2") if badge else None,
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
                data_selected="true" if is_initial else "false",
                data_attr_data_selected=selected_plan.eq(value).if_("true", "false"),
                cls="p-4 border-2 rounded-lg h-full min-h-[220px] w-full transition-all hover:bg-gray-50 dark:hover:bg-gray-800 border-gray-200 dark:border-gray-700 data-[selected=true]:border-blue-500 data-[selected=true]:ring-2 data-[selected=true]:ring-blue-500/20 data-[selected=true]:bg-blue-50 dark:data-[selected=true]:bg-blue-950/20",
            ),
            cls="w-full"
        )

    return Card(
        CardHeader(
            CardTitle("Choose Your Plan"),
            CardDescription("Select the plan that best fits your needs")
        ),
        CardContent(
            Form(
                selected_plan,
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
                    value="free",
                    signal=selected_plan,
                    hide_indicators=True,
                    cls="grid grid-cols-1 gap-3 w-full"
                ),
                P(
                    "Selected plan: ",
                    Code(data_text=selected_plan, cls="ml-2"),
                    cls="text-sm text-muted-foreground mt-4"
                ),
                Button(
                    data_text=selected_plan.eq("enterprise").if_("Contact Sales", "Get Started"),
                    data_on_click=js("alert(`Selected plan: ${$selected_plan}`)"),
                    cls="w-full mt-4"
                )
            )
        ),
        cls="max-w-2xl"
    )


@with_code
def payment_method_example():
    payment_method = Signal("payment_method", "card")

    def PaymentInfo(method, icon):
        is_initial = payment_method.default == method
        return Div(
            Icon(icon, cls="h-5 w-5 mr-2"),
            P("Secure payment processing", cls="text-sm"),
            style="" if is_initial else "display: none",
            data_show=payment_method.eq(method),
            cls="flex items-center p-3 bg-muted rounded-md w-full"
        )

    return Card(
        CardHeader(
            CardTitle("Payment Method"),
            CardDescription("How would you like to pay?")
        ),
        CardContent(
            Form(
                payment_method,
                RadioGroupWithLabel(
                    label="Select payment method",
                    options=[
                        {"value": "card", "label": "Credit/Debit Card"},
                        {"value": "paypal", "label": "PayPal"},
                        {"value": "bank", "label": "Bank Transfer"},
                        {"value": "crypto", "label": "Cryptocurrency"}
                    ],
                    value="card",
                    signal=payment_method,
                    required=True
                ),
                Div(
                    PaymentInfo("card", "lucide:credit-card"),
                    PaymentInfo("paypal", "lucide:wallet"),
                    PaymentInfo("bank", "lucide:building-2"),
                    PaymentInfo("crypto", "lucide:bitcoin"),
                    cls="mt-4 h-16 flex items-center"
                ),
                Button(
                    "Continue to Payment",
                    data_on_click=js("evt.preventDefault(); alert(`Proceeding with ${$payment_method}`)"),
                    type="submit",
                    cls="w-full mt-4"
                )
            )
        ),
        cls="max-w-lg"
    )


@with_code
def interactive_survey_example():
    step = Signal("step", 0)

    # Data-driven: define questions once
    questions = [
        {
            "signal_name": "survey_q1",
            "label": "What is your primary programming language?",
            "options": [
                {"value": "javascript", "label": "JavaScript/TypeScript"},
                {"value": "python", "label": "Python"},
                {"value": "java", "label": "Java"},
                {"value": "csharp", "label": "C#"},
                {"value": "go", "label": "Go"},
                {"value": "rust", "label": "Rust"},
                {"value": "other", "label": "Other"}
            ]
        },
        {
            "signal_name": "survey_q2",
            "label": "How many years of development experience do you have?",
            "options": [
                {"value": "0-1", "label": "Less than 1 year"},
                {"value": "1-3", "label": "1-3 years"},
                {"value": "3-5", "label": "3-5 years"},
                {"value": "5-10", "label": "5-10 years"},
                {"value": "10+", "label": "More than 10 years"}
            ]
        },
        {
            "signal_name": "survey_q3",
            "label": "Which frontend framework do you prefer?",
            "options": [
                {"value": "react", "label": "React"},
                {"value": "vue", "label": "Vue.js"},
                {"value": "angular", "label": "Angular"},
                {"value": "svelte", "label": "Svelte"},
                {"value": "datastar", "label": "Datastar"},
                {"value": "vanilla", "label": "Vanilla JS"},
                {"value": "none", "label": "I'm a backend developer"}
            ]
        }
    ]

    # Create signals from questions data
    signals = {q["signal_name"]: Signal(q["signal_name"], "") for q in questions}

    # Compute answered count from signals
    answered_count = Signal("answered_count", sum(signals[q["signal_name"]] != "" for q in questions))
    total_questions = len(questions)

    return Card(
        CardHeader(
            CardTitle(data_text="Question " + (step + 1) + " of " + total_questions),
            CardDescription("Web Development Survey")
        ),
        CardContent(
            Div(
                step,
                *signals.values(),
                answered_count,
                Div(
                    P(
                        data_text="Question " + (step + 1) + " of " + total_questions,
                        cls="text-xs text-muted-foreground mb-2"
                    ),
                    Div(
                        Div(
                            data_style_width=(answered_count / total_questions * 100) + "%",
                            cls="h-2 bg-primary rounded-full transition-all duration-300"
                        ),
                        cls="w-full bg-secondary rounded-full h-2 mb-6"
                    ),
                    cls="mb-4"
                ),
                Div(
                    *[Div(
                        RadioGroupWithLabel(
                            label=q["label"],
                            options=q["options"],
                            signal=signals[q["signal_name"]],
                            required=True
                        ),
                        style="display: none" if i > 0 else "",
                        data_show=step.eq(i)
                    ) for i, q in enumerate(questions)],
                ),
                Div(
                    Button(
                        "Previous",
                        data_attr_disabled=step.eq(0),
                        data_on_click=step.add(-1),
                        variant="outline",
                        disabled=True
                    ),
                    Button(
                        data_text=step.eq(total_questions - 1).if_("Complete", "Next"),
                        data_on_click=js(f"if ($step === {total_questions - 1}) {{ $step = 0; {'; '.join(f'${q["signal_name"]} = \"\"' for q in questions)}; }} else {{ $step++; }}"),
                        variant="default"
                    ),
                    cls="flex justify-between mt-6"
                )
            )
        ),
        cls="w-full max-w-lg"
    )


@with_code
def settings_panel_example():
    return Card(
        CardHeader(
            CardTitle("Display Settings"),
            CardDescription("Customize your viewing experience")
        ),
        CardContent(
            Div(
                (theme_setting := Signal("theme_setting", "system")),
                (font_setting := Signal("font_setting", "medium")),
                (language_setting := Signal("language_setting", "en")),
                RadioGroupWithLabel(
                    label="Theme",
                    options=[
                        {"value": "light", "label": "Light"},
                        {"value": "dark", "label": "Dark"},
                        {"value": "system", "label": "System"}
                    ],
                    value="system",
                    signal=theme_setting,
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
                    signal=font_setting,
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
                    signal=language_setting
                ),
                Button(
                    "Apply Settings",
                    data_on_click=js("alert('Settings applied!\\nTheme: ' + $theme_setting + '\\nFont: ' + $font_setting + '\\nLanguage: ' + $language_setting)"),
                    cls="w-full mt-6"
                )
            )
        ),
        cls="max-w-lg"
    )



API_REFERENCE = build_api_reference(
    components=[
        Component("RadioGroup", "Container that manages a single selection across contained items"),
        Component("RadioGroupItem", "Individual option; provide a unique value and label content"),
        Component("RadioGroupWithLabel", "Convenience wrapper that renders a labelled group from an options list"),
    ]
)



EXAMPLES_DATA = [
    {"fn": horizontal_layout_example, "title": "Horizontal Layout", "description": "Radio buttons arranged horizontally"},
    {"fn": subscription_plans_example, "title": "Subscription Plans", "description": "Rich radio options with proper RadioGroup semantics and CSS peer selectors"},
    {"fn": payment_method_example, "title": "Payment Method", "description": "Payment selection with contextual information"},
    {"fn": interactive_survey_example, "title": "Interactive Survey", "description": "Multi-step survey with progress tracking and validation"},
    {"fn": settings_panel_example, "title": "Settings Panel", "description": "Multiple radio groups for configuration"},
]



def create_radio_group_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)