TITLE = "Accordion"
DESCRIPTION = "A vertically stacked set of interactive headings that each reveal a section of content."
CATEGORY = "ui"
ORDER = 60
STATUS = "stable"

from starhtml import Div, P, Icon, Span, Code, Ul, Li, Strong, Signal
from starui.registry.components.accordion import (
    Accordion, AccordionItem, AccordionTrigger, AccordionContent
)
from starui.registry.components.button import Button
from starui.registry.components.badge import Badge
from starui.registry.components.card import Card, CardHeader, CardContent, CardTitle, CardDescription
from starui.registry.components.input import InputWithLabel
from starui.registry.components.checkbox import CheckboxWithLabel
from starui.registry.components.utils import cn
from utils import auto_generate_page, Prop, build_api_reference, with_code
from widgets.component_preview import ComponentPreview



@with_code
def hero_accordion_example():
    faqs = [
        ("What is StarUI?",
         "StarUI is a modern component library built with StarHTML and Datastar, providing beautiful, accessible, and interactive UI components."),
        ("How do I get started?",
         P("Install StarUI using the CLI command ", Code("star add [component]"),
           " and start building your application with our pre-built components.")),
        ("Is it production ready?",
         "Yes! StarUI components are thoroughly tested, accessible, and used in production by many applications.")
    ]

    accordion_items = [
        AccordionItem(
            AccordionTrigger(q),
            AccordionContent(P(a) if isinstance(a, str) else a)
        ) for q, a in faqs
    ]

    return Div(
        Accordion(
            *accordion_items,
            type="single",
            collapsible=True
        ),
        cls="w-full max-w-2xl"
    )

@with_code
def basic_accordion_example():
    return Div(
        Accordion(
            AccordionItem(
                AccordionTrigger("Is it accessible?"),
                AccordionContent(P("Yes. It adheres to the WAI-ARIA design pattern..."))
            ),
            AccordionItem(
                AccordionTrigger("Is it styled?"),
                AccordionContent(P("Yes. It comes with default styles..."))
            ),
            AccordionItem(
                AccordionTrigger("Is it animated?"),
                AccordionContent(P("Yes. It's animated by default..."))
            ),
            type="single",
            collapsible=True,
            value=1
        ),
        cls="w-full max-w-2xl"
    )


@with_code
def faq_accordion_example():
    def faq_item(question, answer, icon="lucide:help-circle", *, items=None, badges=None):
        content = [
            P(answer, cls="mb-2" if (items or badges) else ""),
            badges and Div(*[Badge(b, variant="secondary", cls="mr-2") for b in badges], cls="mb-3"),
            items and Ul(*[Li(item) for item in items],
                         cls="list-disc list-inside space-y-1 text-sm text-muted-foreground")
        ]

        return AccordionItem(
            AccordionTrigger(
                Div(Icon(icon, cls="h-4 w-4 mr-2"),
                    Span(question),
                    cls="flex items-center flex-1")
            ),
            AccordionContent(*content),            
        )

    faq_items = [
        faq_item(
            "What payment methods do you accept?",
            "We accept all major credit cards, PayPal, and bank transfers.",
            icon="lucide:credit-card",
            items=["Visa, Mastercard, American Express",
                   "PayPal and PayPal Credit",
                   "ACH bank transfers (US only)",
                   "Wire transfers for enterprise accounts"]
        ),
        faq_item(
            "How secure is my data?",
            "Your data security is our top priority. We use industry-standard encryption and comply with all major data protection regulations.",
            icon="lucide:shield-check",
            badges=["256-bit SSL", "GDPR Compliant", "SOC 2 Type II"]
        ),
        faq_item(
            "What is your refund policy?",
            "We offer a 30-day money-back guarantee. If you're not satisfied with our service within the first 30 days, you can request a full refund with no questions asked.",
            icon="lucide:rotate-ccw"
        ),
        faq_item(
            "How can I contact support?",
            "Our support team is available 24/7 through multiple channels:",
            icon="lucide:headphones",
            items=["Live chat on our website",
                   "Email: support@example.com",
                   "Phone: 1-800-EXAMPLE",
                   "Support ticket system"]
        )
    ]

    return Card(
        CardHeader(
            CardTitle("Frequently Asked Questions"),
            CardDescription("Find answers to common questions about our service")
        ),
        CardContent(
            Accordion(
                *faq_items,
                type="single",
                collapsible=True,
                value=0
            )
        ),
        cls="max-w-2xl"
    )


@with_code
def multiple_selection_accordion_example():
    def api_endpoint(method, path, description, params=None):
        return Div(
            Code(f"{method} {path}", cls="block p-2 bg-muted rounded mb-2"),
            P(description, cls="mb-2" if params else ""),
            Ul(
                *[Li(Code(p[0]), f" - {p[1]}") for p in params],
                cls="list-disc list-inside text-sm text-muted-foreground"
            ) if params else None
        )

    api_sections = {
        "auth": {
            "title": "Authentication",
            "endpoints": [
                api_endpoint("POST", "/api/auth/login",
                            "Authenticate a user and receive a JWT token.",
                            [("email", "User's email address"),
                             ("password", "User's password")])
            ]
        },
        "users": {
            "title": "Users",
            "endpoints": [
                api_endpoint("GET", "/api/users", "Retrieve a list of users."),
                api_endpoint("GET", "/api/users/:id", "Retrieve a specific user by ID."),
                api_endpoint("POST", "/api/users", "Create a new user account.")
            ]
        },
        "projects": {
            "title": "Projects",
            "endpoints": [
                api_endpoint("GET", "/api/projects", "List all projects for the authenticated user."),
                api_endpoint("POST", "/api/projects", "Create a new project."),
                api_endpoint("DELETE", "/api/projects/:id", "Delete a project (requires admin permissions).")
            ]
        }
    }

    accordion_sections = [
        AccordionItem(
            AccordionTrigger(section["title"]),
            AccordionContent(*section["endpoints"]),
            value=key
        ) for key, section in api_sections.items()
    ]

    return Card(
        CardHeader(
            CardTitle("API Documentation"),
            CardDescription("Explore available endpoints and methods")
        ),
        CardContent(
            Accordion(
                *accordion_sections,
                type="multiple",
                value=["auth", "users"]
            )
        ),
        cls="max-w-2xl"
    )


@with_code
def settings_accordion_example():
    def settings_trigger(title, *, badge_text=None, badge_variant="secondary", icon=None):
        return Div(
            badge_text and Badge(badge_text, variant=badge_variant, cls="mr-2"),
            icon and Icon(icon, cls="h-4 w-4 mr-2"),
            Span(title),
            cls="flex items-center"
        )

    personal_form = Div(
        InputWithLabel(label="Full Name", value="John Doe"),
        InputWithLabel(label="Email", type="email", value="john@example.com"),
        InputWithLabel(label="Phone", type="tel", value="+1 234 567 8900"),
        Button("Save Changes", cls="mt-4"),
        cls="space-y-4 px-1"
    )

    security_form = Div(
        InputWithLabel(label="Current Password", type="password"),
        InputWithLabel(label="New Password", type="password"),
        InputWithLabel(label="Confirm New Password", type="password"),
        CheckboxWithLabel(
            label="Enable two-factor authentication",
            helper_text="Adds an extra layer of security to your account"
        ),
        Button("Update Security Settings", variant="destructive", cls="mt-4"),
        cls="space-y-4 px-1"
    )

    notification_form = Div(
        CheckboxWithLabel(
            label="Email notifications",
            checked=True,
            helper_text="Receive updates via email"
        ),
        CheckboxWithLabel(
            label="Push notifications",
            helper_text="Browser notifications for important updates"
        ),
        CheckboxWithLabel(
            label="Marketing emails",
            helper_text="Product updates and special offers"
        ),
        Button("Save Preferences", cls="mt-4"),
        cls="space-y-3 px-1"
    )

    settings_sections = [
        AccordionItem(
            AccordionTrigger(settings_trigger("Personal Information", badge_text="3 fields")),
            AccordionContent(personal_form),            
        ),
        AccordionItem(
            AccordionTrigger(settings_trigger("Password & Security", badge_text="Security", badge_variant="destructive")),
            AccordionContent(security_form),            
        ),
        AccordionItem(
            AccordionTrigger(settings_trigger("Notifications", icon="lucide:bell")),
            AccordionContent(notification_form),            
        )
    ]

    return Card(
        CardHeader(
            CardTitle("Account Settings"),
            CardDescription("Manage your account preferences")
        ),
        CardContent(
            Accordion(
                *settings_sections,
                type="single",
                collapsible=True
            )
        ),
        cls="max-w-2xl"
    )


@with_code
def file_explorer_accordion_example():
    def folder_item(name, count, files):
        return AccordionItem(
            AccordionTrigger(
                Div(
                    Icon("lucide:folder", cls="h-4 w-4 mr-2 text-blue-500"),
                    Span(name),
                    Badge(f"{count} files", variant="outline", cls="ml-auto mr-2"),
                    cls="flex items-center w-full"
                )
            ),
            AccordionContent(
                Div(
                    *[Div(Icon("lucide:file", cls="h-4 w-4 mr-2"), f, cls="flex items-center py-1")
                      for f in files],
                    cls="text-sm text-muted-foreground"
                )
            )            
        )

    src_content = Div(
        Accordion(
            folder_item("components/", 4, ["Button.tsx", "Card.tsx", "Dialog.tsx", "Input.tsx"]),
            folder_item("utils/", 2, ["cn.ts", "helpers.ts"]),
            type="multiple"
        ),
        cls="ml-2 pl-3 border-l-2 border-muted"
    )

    src_trigger = Div(
        Icon("lucide:folder", cls="h-4 w-4 mr-2 text-blue-500"),
        Span("src/"),
        Badge("12 files", variant="outline", cls="ml-auto mr-2"),
        cls="flex items-center w-full"
    )

    file_items = [
        AccordionItem(
            AccordionTrigger(src_trigger),
            AccordionContent(src_content),            
        ),
        folder_item("docs/", 3, ["README.md", "CONTRIBUTING.md", "API.md"]),
        folder_item("tests/", 2, ["Button.test.tsx", "utils.test.ts"])
    ]

    return Card(
        CardHeader(
            CardTitle("Project Structure"),
            CardDescription("Browse project files and folders")
        ),
        CardContent(
            Accordion(
                *file_items,
                type="multiple"
            )
        ),
        cls="max-w-xl"
    )


@with_code
def course_curriculum_accordion_example():
    def lesson_item(title, duration=None, type="video", completed=False, locked=False):
        icons = {
            "video": "lucide:play-circle",
            "exercise": "lucide:file-text",
            "quiz": "lucide:check-circle" if completed else "lucide:help-circle"
        }
        icon = "lucide:lock" if locked else icons.get(type, "lucide:file")
        icon_cls = cn("h-4 w-4 mr-2", completed and "text-green-500", locked and "text-muted-foreground")

        right_element = (
            Span(duration, cls="ml-auto text-muted-foreground") if duration
            else Badge("Exercise", variant="outline", cls="ml-auto") if type == "exercise"
            else Badge("Completed", variant="secondary", cls="ml-auto") if completed
            else Badge("Locked", variant="outline", cls="ml-auto") if locked
            else None
        )

        return Li(Div(Icon(icon, cls=icon_cls), title, right_element,
                      cls=cn("flex items-center", locked and "opacity-50")))

    def course_module(title, lesson_count, duration, lessons, value, locked=False):
        return AccordionItem(
            AccordionTrigger(
                Div(
                    Badge("Coming Soon" if locked else f"{lesson_count} lessons",
                          variant="outline" if locked else "secondary", cls="mr-2"),
                    Strong(title),
                    Icon("lucide:lock", cls="h-4 w-4 ml-auto mr-2 text-muted-foreground") if locked
                    else Badge(duration, variant="outline", cls="ml-auto mr-2"),
                    cls="flex items-center w-full"
                )
            ),
            AccordionContent(
                P("This module will be available after completing previous modules.",
                  cls="text-muted-foreground italic") if locked
                else Ul(*lessons, cls="space-y-3")
            ),
            value=value
        )

    course_modules = [
        course_module(
            "Module 1: HTML & CSS Fundamentals", 5, "2.5 hours",
            [
                lesson_item("Introduction to HTML", "15:30"),
                lesson_item("CSS Basics", "22:15"),
                lesson_item("Practice Exercise: Build a Landing Page", type="exercise"),
                lesson_item("Quiz: HTML & CSS", type="quiz", completed=True)
            ],
            "module1"
        ),
        course_module(
            "Module 2: JavaScript Essentials", 7, "4 hours",
            [
                lesson_item("Variables and Data Types", "18:45"),
                lesson_item("Functions and Scope", "25:00"),
                lesson_item("Arrays and Objects", locked=True)
            ],
            "module2"
        ),
        course_module(
            "Module 3: React Framework", 0, "",
            [],
            "module3",
            locked=True
        )
    ]

    return Card(
        CardHeader(
            CardTitle("Course Curriculum"),
            CardDescription("Web Development Bootcamp")
        ),
        CardContent(
            Accordion(
                *course_modules,
                type="single",
                value="module1"
            )
        ),
        cls="max-w-3xl"
    )




API_REFERENCE = build_api_reference(
    main_props=[
        Prop("type", "Literal['single', 'multiple']", "Whether one or multiple items can be open", "'single'"),
        Prop("collapsible", "bool", "When type='single', allows closing all items", "False"),
        Prop("value", "str | int | list[str | int] | None", "Initially open item(s). Can be index (int) or custom value (str)", "None"),
        Prop("signal", "str", "Datastar signal name for state management", "auto-generated"),
        Prop("cls", "str", "Additional CSS classes", "''"),
    ]
)



EXAMPLES_DATA = [
    {"fn": hero_accordion_example, "title": "Basic Usage", "description": "Single selection accordion with collapsible items"},
    {"fn": basic_accordion_example, "title": "Collapsible Single", "description": "Single item open at a time, all items can be closed"},
    {"fn": faq_accordion_example, "title": "Rich Content", "description": "Single selection with icons, badges, and formatted content"},
    {"fn": multiple_selection_accordion_example, "title": "Multiple Selection", "description": "Multiple items can be open simultaneously"},
    {"fn": settings_accordion_example, "title": "With Forms", "description": "Single selection accordion containing interactive form elements"},
    {"fn": file_explorer_accordion_example, "title": "Nested Accordions", "description": "Accordions nested within accordion items for hierarchical content"},
    {"fn": course_curriculum_accordion_example, "title": "Always One Open", "description": "Non-collapsible single selection - exactly one item must always be open"},
]



def create_accordion_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)
