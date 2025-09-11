"""
Accordion component documentation - Convention-based functional approach.
Clean, minimal, and easy to extend.
"""

# Component metadata for auto-discovery
TITLE = "Accordion"
DESCRIPTION = "A vertically stacked set of interactive headings that each reveal a section of content."
CATEGORY = "ui"
ORDER = 60
STATUS = "stable"

from starhtml import Div, P, Icon, Span, H3, Code, Ul, Li, Strong
from starhtml.datastar import (
    ds_on_click, ds_show, ds_text, ds_signals, value,
    ds_bind, ds_disabled, ds_on_change, ds_effect, ds_class
)
from starui.registry.components.accordion import (
    Accordion, AccordionItem, AccordionTrigger, AccordionContent
)
from starui.registry.components.button import Button
from starui.registry.components.badge import Badge
from starui.registry.components.card import Card, CardHeader, CardContent, CardTitle, CardDescription
from starui.registry.components.input import InputWithLabel
from starui.registry.components.checkbox import CheckboxWithLabel
from utils import auto_generate_page, Prop, build_api_reference, with_code
from widgets.component_preview import ComponentPreview


def examples():
    """Generate accordion examples using ComponentPreview with tabs."""
    
    # Basic accordion
    @with_code
    def basic_accordion_example():
        return Div(
            Accordion(
                AccordionItem(
                    AccordionTrigger("Is it accessible?"),
                    AccordionContent(
                        P("Yes. It adheres to the WAI-ARIA design pattern and uses semantic HTML.")
                    ),
                    value="item-1"
                ),
                AccordionItem(
                    AccordionTrigger("Is it styled?"),
                    AccordionContent(
                        P("Yes. It comes with default styles that match the other components' aesthetic.")
                    ),
                    value="item-2"
                ),
                AccordionItem(
                    AccordionTrigger("Is it animated?"),
                    AccordionContent(
                        P("Yes. It's animated by default with smooth transitions.")
                    ),
                    value="item-3"
                ),
                type="single",
                collapsible=True,
                default_value="item-1",
                signal="basic_accordion"
            ),
            cls="w-full max-w-2xl"
        )
    
    yield ComponentPreview(
        basic_accordion_example(),
        basic_accordion_example.code,
        title="Basic Accordion",
        description="Single selection accordion with collapsible behavior"
    )
    
    # FAQ section
    @with_code
    def faq_accordion_example():
        return Card(
            CardHeader(
                CardTitle("Frequently Asked Questions"),
                CardDescription("Find answers to common questions about our service")
            ),
            CardContent(
                Accordion(
                    AccordionItem(
                        AccordionTrigger(
                            Div(
                                Icon("lucide:credit-card", cls="h-4 w-4 mr-2"),
                                Span("What payment methods do you accept?"),
                                cls="flex items-center flex-1"
                            )
                        ),
                        AccordionContent(
                            P("We accept all major credit cards, PayPal, and bank transfers.", cls="mb-2"),
                            Ul(
                                Li("Visa, Mastercard, American Express"),
                                Li("PayPal and PayPal Credit"),
                                Li("ACH bank transfers (US only)"),
                                Li("Wire transfers for enterprise accounts"),
                                cls="list-disc list-inside space-y-1 text-sm text-muted-foreground"
                            )
                        ),
                        value="payment"
                    ),
                    AccordionItem(
                        AccordionTrigger(
                            Div(
                                Icon("lucide:shield-check", cls="h-4 w-4 mr-2"),
                                Span("How secure is my data?"),
                                cls="flex items-center flex-1"
                            )
                        ),
                        AccordionContent(
                            P("Your data security is our top priority.", cls="mb-2"),
                            Div(
                                Badge("256-bit SSL", variant="secondary", cls="mr-2"),
                                Badge("GDPR Compliant", variant="secondary", cls="mr-2"),
                                Badge("SOC 2 Type II", variant="secondary"),
                                cls="mb-3"
                            ),
                            P("We use industry-standard encryption and comply with all major data protection regulations.",
                              cls="text-sm text-muted-foreground")
                        ),
                        value="security"
                    ),
                    AccordionItem(
                        AccordionTrigger(
                            Div(
                                Icon("lucide:rotate-ccw", cls="h-4 w-4 mr-2"),
                                Span("What is your refund policy?"),
                                cls="flex items-center flex-1"
                            )
                        ),
                        AccordionContent(
                            P("We offer a 30-day money-back guarantee.", cls="mb-2"),
                            P("If you're not satisfied with our service within the first 30 days, "
                              "you can request a full refund with no questions asked.",
                              cls="text-sm text-muted-foreground")
                        ),
                        value="refund"
                    ),
                    AccordionItem(
                        AccordionTrigger(
                            Div(
                                Icon("lucide:headphones", cls="h-4 w-4 mr-2"),
                                Span("How can I contact support?"),
                                cls="flex items-center flex-1"
                            )
                        ),
                        AccordionContent(
                            P("Our support team is available 24/7 through multiple channels:", cls="mb-2"),
                            Ul(
                                Li("Live chat on our website"),
                                Li("Email: support@example.com"),
                                Li("Phone: 1-800-EXAMPLE"),
                                Li("Support ticket system"),
                                cls="list-disc list-inside space-y-1 text-sm text-muted-foreground"
                            )
                        ),
                        value="support"
                    ),
                    type="single",
                    collapsible=True,
                    signal="faq_accordion"
                )
            ),
            cls="max-w-2xl"
        )
    
    yield ComponentPreview(
        faq_accordion_example(),
        faq_accordion_example.code,
        title="FAQ Section",
        description="Frequently asked questions with icons and rich content"
    )
    
    # Multiple selection accordion
    @with_code
    def multiple_selection_accordion_example():
        return Card(
            CardHeader(
                CardTitle("API Documentation"),
                CardDescription("Explore available endpoints and methods")
            ),
            CardContent(
                Accordion(
                    AccordionItem(
                        AccordionTrigger("Authentication"),
                        AccordionContent(
                            Code("POST /api/auth/login", cls="block p-2 bg-muted rounded mb-2"),
                            P("Authenticate a user and receive a JWT token.", cls="mb-2"),
                            P("Required fields:", cls="text-sm font-medium"),
                            Ul(
                                Li(Code("email"), " - User's email address"),
                                Li(Code("password"), " - User's password"),
                                cls="list-disc list-inside text-sm text-muted-foreground"
                            )
                        ),
                        value="auth"
                    ),
                    AccordionItem(
                        AccordionTrigger("Users"),
                        AccordionContent(
                            Code("GET /api/users", cls="block p-2 bg-muted rounded mb-2"),
                            P("Retrieve a list of users.", cls="mb-2"),
                            Code("GET /api/users/:id", cls="block p-2 bg-muted rounded mb-2"),
                            P("Retrieve a specific user by ID.", cls="mb-2"),
                            Code("POST /api/users", cls="block p-2 bg-muted rounded mb-2"),
                            P("Create a new user account.")
                        ),
                        value="users"
                    ),
                    AccordionItem(
                        AccordionTrigger("Projects"),
                        AccordionContent(
                            Code("GET /api/projects", cls="block p-2 bg-muted rounded mb-2"),
                            P("List all projects for the authenticated user.", cls="mb-2"),
                            Code("POST /api/projects", cls="block p-2 bg-muted rounded mb-2"),
                            P("Create a new project.", cls="mb-2"),
                            Code("DELETE /api/projects/:id", cls="block p-2 bg-muted rounded mb-2"),
                            P("Delete a project (requires admin permissions).")
                        ),
                        value="projects"
                    ),
                    type="multiple",
                    default_value=["auth", "users"],
                    signal="api_accordion"
                )
            ),
            cls="max-w-2xl"
        )
    
    yield ComponentPreview(
        multiple_selection_accordion_example(),
        multiple_selection_accordion_example.code,
        title="Multiple Selection",
        description="API documentation with multiple sections open simultaneously"
    )
    
    # Settings accordion with forms
    @with_code
    def settings_accordion_example():
        return Card(
            CardHeader(
                CardTitle("Account Settings"),
                CardDescription("Manage your account preferences")
            ),
            CardContent(
                Accordion(
                    AccordionItem(
                        AccordionTrigger(
                            Div(
                                Badge("3 fields", variant="secondary", cls="mr-2"),
                                Span("Personal Information"),
                                cls="flex items-center"
                            )
                        ),
                        AccordionContent(
                            Div(
                                InputWithLabel(
                                    label="Full Name",
                                    value="John Doe",
                                    signal="user_name"
                                ),
                                InputWithLabel(
                                    label="Email",
                                    type="email",
                                    value="john@example.com",
                                    signal="user_email"
                                ),
                                InputWithLabel(
                                    label="Phone",
                                    type="tel",
                                    value="+1 234 567 8900",
                                    signal="user_phone"
                                ),
                                Button("Save Changes", cls="mt-4"),
                                ds_signals(
                                    user_name=value("John Doe"),
                                    user_email=value("john@example.com"),
                                    user_phone=value("+1 234 567 8900")
                                ),
                                cls="space-y-4"
                            )
                        ),
                        value="personal"
                    ),
                    AccordionItem(
                        AccordionTrigger(
                            Div(
                                Badge("Security", variant="destructive", cls="mr-2"),
                                Span("Password & Security"),
                                cls="flex items-center"
                            )
                        ),
                        AccordionContent(
                            Div(
                                InputWithLabel(
                                    label="Current Password",
                                    type="password",
                                    signal="current_password"
                                ),
                                InputWithLabel(
                                    label="New Password",
                                    type="password",
                                    signal="new_password"
                                ),
                                InputWithLabel(
                                    label="Confirm New Password",
                                    type="password",
                                    signal="confirm_password"
                                ),
                                CheckboxWithLabel(
                                    label="Enable two-factor authentication",
                                    signal="two_factor",
                                    helper_text="Adds an extra layer of security to your account"
                                ),
                                Button("Update Security Settings", variant="destructive", cls="mt-4"),
                                ds_signals(
                                    current_password=value(""),
                                    new_password=value(""),
                                    confirm_password=value(""),
                                    two_factor=False
                                ),
                                cls="space-y-4"
                            )
                        ),
                        value="security"
                    ),
                    AccordionItem(
                        AccordionTrigger(
                            Div(
                                Icon("lucide:bell", cls="h-4 w-4 mr-2"),
                                Span("Notifications"),
                                cls="flex items-center"
                            )
                        ),
                        AccordionContent(
                            Div(
                                CheckboxWithLabel(
                                    label="Email notifications",
                                    checked=True,
                                    signal="email_notif",
                                    helper_text="Receive updates via email"
                                ),
                                CheckboxWithLabel(
                                    label="Push notifications",
                                    signal="push_notif",
                                    helper_text="Browser notifications for important updates"
                                ),
                                CheckboxWithLabel(
                                    label="Marketing emails",
                                    signal="marketing",
                                    helper_text="Product updates and special offers"
                                ),
                                Button("Save Preferences", cls="mt-4"),
                                ds_signals(
                                    email_notif=True,
                                    push_notif=False,
                                    marketing=False
                                ),
                                cls="space-y-3"
                            )
                        ),
                        value="notifications"
                    ),
                    type="single",
                    collapsible=True,
                    signal="settings_accordion"
                )
            ),
            cls="max-w-2xl"
        )
    
    yield ComponentPreview(
        settings_accordion_example(),
        settings_accordion_example.code,
        title="Settings Panel",
        description="Account settings organized in collapsible sections with forms"
    )
    
    # File explorer accordion
    @with_code
    def file_explorer_accordion_example():
        return Card(
            CardHeader(
                CardTitle("Project Structure"),
                CardDescription("Browse project files and folders")
            ),
            CardContent(
                Accordion(
                    AccordionItem(
                        AccordionTrigger(
                            Div(
                                Icon("lucide:folder", cls="h-4 w-4 mr-2 text-blue-500"),
                                Span("src/"),
                                Badge("12 files", variant="outline", cls="ml-auto mr-2"),
                                cls="flex items-center w-full"
                            )
                        ),
                        AccordionContent(
                            Div(
                                # Visual hierarchy with border and indentation
                                Div(
                                    Accordion(
                                        AccordionItem(
                                            AccordionTrigger(
                                                Div(
                                                    Icon("lucide:folder", cls="h-4 w-4 mr-2 text-blue-500"),
                                                    Span("components/"),
                                                    Badge("8", variant="outline", cls="ml-auto mr-2"),
                                                    cls="flex items-center w-full"
                                                )
                                            ),
                                            AccordionContent(
                                                Div(
                                                    Div(Icon("lucide:file", cls="h-4 w-4 mr-2"), "Button.tsx", cls="flex items-center py-1 pl-8"),
                                                    Div(Icon("lucide:file", cls="h-4 w-4 mr-2"), "Card.tsx", cls="flex items-center py-1 pl-8"),
                                                    Div(Icon("lucide:file", cls="h-4 w-4 mr-2"), "Dialog.tsx", cls="flex items-center py-1 pl-8"),
                                                    Div(Icon("lucide:file", cls="h-4 w-4 mr-2"), "Input.tsx", cls="flex items-center py-1 pl-8"),
                                                    cls="text-sm text-muted-foreground"
                                                )
                                            ),
                                            value="components"
                                        ),
                                        AccordionItem(
                                            AccordionTrigger(
                                                Div(
                                                    Icon("lucide:folder", cls="h-4 w-4 mr-2 text-blue-500"),
                                                    Span("utils/"),
                                                    Badge("4", variant="outline", cls="ml-auto mr-2"),
                                                    cls="flex items-center w-full"
                                                )
                                            ),
                                            AccordionContent(
                                                Div(
                                                    Div(Icon("lucide:file", cls="h-4 w-4 mr-2"), "cn.ts", cls="flex items-center py-1 pl-8"),
                                                    Div(Icon("lucide:file", cls="h-4 w-4 mr-2"), "helpers.ts", cls="flex items-center py-1 pl-8"),
                                                    cls="text-sm text-muted-foreground"
                                                )
                                            ),
                                            value="utils"
                                        ),
                                        type="multiple",
                                        signal="src_accordion"
                                    ),
                                    cls="ml-2 pl-3 border-l-2 border-muted"
                                )
                            )
                        ),
                        value="src"
                    ),
                    AccordionItem(
                        AccordionTrigger(
                            Div(
                                Icon("lucide:folder", cls="h-4 w-4 mr-2 text-blue-500"),
                                Span("docs/"),
                                Badge("5 files", variant="outline", cls="ml-auto mr-2"),
                                cls="flex items-center w-full"
                            )
                        ),
                        AccordionContent(
                            Div(
                                Div(Icon("lucide:file", cls="h-4 w-4 mr-2"), "README.md", cls="flex items-center py-1"),
                                Div(Icon("lucide:file", cls="h-4 w-4 mr-2"), "CONTRIBUTING.md", cls="flex items-center py-1"),
                                Div(Icon("lucide:file", cls="h-4 w-4 mr-2"), "API.md", cls="flex items-center py-1"),
                                cls="text-sm text-muted-foreground"
                            )
                        ),
                        value="docs"
                    ),
                    AccordionItem(
                        AccordionTrigger(
                            Div(
                                Icon("lucide:folder", cls="h-4 w-4 mr-2 text-blue-500"),
                                Span("tests/"),
                                Badge("8 files", variant="outline", cls="ml-auto mr-2"),
                                cls="flex items-center w-full"
                            )
                        ),
                        AccordionContent(
                            Div(
                                Div(Icon("lucide:file", cls="h-4 w-4 mr-2"), "Button.test.tsx", cls="flex items-center py-1"),
                                Div(Icon("lucide:file", cls="h-4 w-4 mr-2"), "utils.test.ts", cls="flex items-center py-1"),
                                cls="text-sm text-muted-foreground"
                            )
                        ),
                        value="tests"
                    ),
                    type="multiple",
                    signal="file_accordion"
                )
            ),
            cls="max-w-xl"
        )
    
    yield ComponentPreview(
        file_explorer_accordion_example(),
        file_explorer_accordion_example.code,
        title="File Explorer",
        description="Nested accordions for file tree navigation"
    )
    
    # Course curriculum accordion
    @with_code
    def course_curriculum_accordion_example():
        return Card(
            CardHeader(
                CardTitle("Course Curriculum"),
                CardDescription("Web Development Bootcamp")
            ),
            CardContent(
                Accordion(
                    AccordionItem(
                        AccordionTrigger(
                            Div(
                                Badge("5 lessons", variant="secondary", cls="mr-2"),
                                Strong("Module 1: HTML & CSS Fundamentals"),
                                Badge("2.5 hours", variant="outline", cls="ml-auto mr-2"),
                                cls="flex items-center w-full"
                            )
                        ),
                        AccordionContent(
                            Ul(
                                Li(
                                    Div(
                                        Icon("lucide:play-circle", cls="h-4 w-4 mr-2"),
                                        "Introduction to HTML",
                                        Span("15:30", cls="ml-auto text-muted-foreground"),
                                        cls="flex items-center"
                                    )
                                ),
                                Li(
                                    Div(
                                        Icon("lucide:play-circle", cls="h-4 w-4 mr-2"),
                                        "CSS Basics",
                                        Span("22:15", cls="ml-auto text-muted-foreground"),
                                        cls="flex items-center"
                                    )
                                ),
                                Li(
                                    Div(
                                        Icon("lucide:file-text", cls="h-4 w-4 mr-2"),
                                        "Practice Exercise: Build a Landing Page",
                                        Badge("Exercise", variant="outline", cls="ml-auto"),
                                        cls="flex items-center"
                                    )
                                ),
                                Li(
                                    Div(
                                        Icon("lucide:check-circle", cls="h-4 w-4 mr-2 text-green-500"),
                                        "Quiz: HTML & CSS",
                                        Badge("Completed", variant="secondary", cls="ml-auto"),
                                        cls="flex items-center"
                                    )
                                ),
                                cls="space-y-3"
                            )
                        ),
                        value="module1"
                    ),
                    AccordionItem(
                        AccordionTrigger(
                            Div(
                                Badge("7 lessons", variant="secondary", cls="mr-2"),
                                Strong("Module 2: JavaScript Essentials"),
                                Badge("4 hours", variant="outline", cls="ml-auto mr-2"),
                                cls="flex items-center w-full"
                            )
                        ),
                        AccordionContent(
                            Ul(
                                Li(
                                    Div(
                                        Icon("lucide:play-circle", cls="h-4 w-4 mr-2"),
                                        "Variables and Data Types",
                                        Span("18:45", cls="ml-auto text-muted-foreground"),
                                        cls="flex items-center"
                                    )
                                ),
                                Li(
                                    Div(
                                        Icon("lucide:play-circle", cls="h-4 w-4 mr-2"),
                                        "Functions and Scope",
                                        Span("25:00", cls="ml-auto text-muted-foreground"),
                                        cls="flex items-center"
                                    )
                                ),
                                Li(
                                    Div(
                                        Icon("lucide:lock", cls="h-4 w-4 mr-2 text-muted-foreground"),
                                        "Arrays and Objects",
                                        Badge("Locked", variant="outline", cls="ml-auto"),
                                        cls="flex items-center opacity-50"
                                    )
                                ),
                                cls="space-y-3"
                            )
                        ),
                        value="module2"
                    ),
                    AccordionItem(
                        AccordionTrigger(
                            Div(
                                Badge("Coming Soon", variant="outline", cls="mr-2"),
                                Strong("Module 3: React Framework"),
                                Icon("lucide:lock", cls="h-4 w-4 ml-auto mr-2 text-muted-foreground"),
                                cls="flex items-center w-full"
                            )
                        ),
                        AccordionContent(
                            P("This module will be available after completing Module 2.",
                              cls="text-muted-foreground italic")
                        ),
                        value="module3"
                    ),
                    type="single",
                    default_value="module1",
                    signal="course_accordion"
                )
            ),
            cls="max-w-3xl"
        )
    
    yield ComponentPreview(
        course_curriculum_accordion_example(),
        course_curriculum_accordion_example.code,
        title="Course Curriculum",
        description="Educational content with progress tracking and lesson details"
    )


def create_accordion_docs():
    """Create accordion documentation page using convention-based approach."""
    
    # For Accordion, users need to understand the main behavioral props
    # (single vs multiple, collapsible, default values) more than sub-component structure
    api_reference = build_api_reference(
        main_props=[
            Prop("type", "Literal['single', 'multiple']", "Whether one or multiple items can be open", "'single'"),
            Prop("collapsible", "bool", "When type='single', allows closing all items", "False"),
            Prop("default_value", "str | list[str] | None", "Initially open item(s)", "None"),
            Prop("signal", "str", "Datastar signal name for state management", "auto-generated"),
            Prop("cls", "str", "Additional CSS classes", "''"),
        ]
    )
    
    # Hero example
    @with_code
    def hero_accordion_example():
        return Div(
            Accordion(
                AccordionItem(
                    AccordionTrigger("What is StarUI?"),
                    AccordionContent(
                        P("StarUI is a modern component library built with StarHTML and Datastar, "
                          "providing beautiful, accessible, and interactive UI components.")
                    ),
                    value="item-1"
                ),
                AccordionItem(
                    AccordionTrigger("How do I get started?"),
                    AccordionContent(
                        P("Install StarUI using the CLI command ", Code("star add [component]"), 
                          " and start building your application with our pre-built components.")
                    ),
                    value="item-2"
                ),
                AccordionItem(
                    AccordionTrigger("Is it production ready?"),
                    AccordionContent(
                        P("Yes! StarUI components are thoroughly tested, accessible, "
                          "and used in production by many applications.")
                    ),
                    value="item-3"
                ),
                type="single",
                collapsible=True,
                default_value="item-1"
            ),
            cls="w-full max-w-2xl"
        )
    
    hero_example = ComponentPreview(
        hero_accordion_example(),
        hero_accordion_example.code,
        copy_button=True
    )
    
    return auto_generate_page(
        TITLE,
        DESCRIPTION,
        list(examples()),
        cli_command="star add accordion",
        api_reference=api_reference,
        hero_example=hero_example,
        component_slug="accordion"
    )