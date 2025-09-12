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
    
    @with_code
    def basic_accordion_example():
        items = [
            ("Is it accessible?", 
             "Yes. It adheres to the WAI-ARIA design pattern and uses semantic HTML."),
            ("Is it styled?", 
             "Yes. It comes with default styles that match the other components' aesthetic."),
            ("Is it animated?", 
             "Yes. It's animated by default with smooth transitions.")
        ]
        
        accordion_items = [
            AccordionItem(
                AccordionTrigger(question),
                AccordionContent(P(answer)),
                value=f"item-{i+1}"
            ) for i, (question, answer) in enumerate(items)
        ]
        
        return Div(
            Accordion(
                *accordion_items,
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
    
    @with_code
    def faq_accordion_example():
        def faq_item(question, answer, icon="lucide:help-circle", *, items=None, badges=None):
            content = [P(answer, cls="mb-2" if (items or badges) else "")]
            
            if badges:
                content.append(
                    Div(*[Badge(b, variant="secondary", cls="mr-2") for b in badges], cls="mb-3")
                )
            
            if items:
                content.append(
                    Ul(*[Li(item) for item in items],
                       cls="list-disc list-inside space-y-1 text-sm text-muted-foreground")
                )
            
            return AccordionItem(
                AccordionTrigger(
                    Div(Icon(icon, cls="h-4 w-4 mr-2"), 
                        Span(question),
                        cls="flex items-center flex-1")
                ),
                AccordionContent(*content),
                value=question.lower().replace(" ", "_")[:20]
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
    
    @with_code
    def settings_accordion_example():
        def settings_trigger(title, *, badge_text=None, badge_variant="secondary", icon=None):
            elements = [
                Badge(badge_text, variant=badge_variant, cls="mr-2") if badge_text else None,
                Icon(icon, cls="h-4 w-4 mr-2") if icon else None,
                Span(title)
            ]
            return Div(*filter(None, elements), cls="flex items-center")
        
        personal_form = Div(
            InputWithLabel(label="Full Name", value="John Doe", signal="user_name"),
            InputWithLabel(label="Email", type="email", value="john@example.com", signal="user_email"),
            InputWithLabel(label="Phone", type="tel", value="+1 234 567 8900", signal="user_phone"),
            Button("Save Changes", cls="mt-4"),
            ds_signals(
                user_name=value("John Doe"),
                user_email=value("john@example.com"),
                user_phone=value("+1 234 567 8900")
            ),
            cls="space-y-4 px-1"
        )
        
        security_form = Div(
            InputWithLabel(label="Current Password", type="password", signal="current_password"),
            InputWithLabel(label="New Password", type="password", signal="new_password"),
            InputWithLabel(label="Confirm New Password", type="password", signal="confirm_password"),
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
            cls="space-y-4 px-1"
        )
        
        notification_form = Div(
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
            ds_signals(email_notif=True, push_notif=False, marketing=False),
            cls="space-y-3 px-1"
        )
        
        settings_sections = [
            AccordionItem(
                AccordionTrigger(settings_trigger("Personal Information", badge_text="3 fields")),
                AccordionContent(personal_form),
                value="personal"
            ),
            AccordionItem(
                AccordionTrigger(settings_trigger("Password & Security", badge_text="Security", badge_variant="destructive")),
                AccordionContent(security_form),
                value="security"
            ),
            AccordionItem(
                AccordionTrigger(settings_trigger("Notifications", icon="lucide:bell")),
                AccordionContent(notification_form),
                value="notifications"
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
                ),
                value=name.replace("/", "")
            )
        
        src_content = Div(
            Accordion(
                folder_item("components/", 4, ["Button.tsx", "Card.tsx", "Dialog.tsx", "Input.tsx"]),
                folder_item("utils/", 2, ["cn.ts", "helpers.ts"]),
                type="multiple",
                signal="src_nested"
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
                value="src"
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
    
    @with_code
    def course_curriculum_accordion_example():
        def lesson_item(title, duration=None, type="video", completed=False, locked=False):
            icons = {
                "video": "lucide:play-circle",
                "exercise": "lucide:file-text",
                "quiz": "lucide:check-circle" if completed else "lucide:help-circle",
            }
            
            icon = "lucide:lock" if locked else icons.get(type, "lucide:file")
            icon_cls = "h-4 w-4 mr-2" + (
                " text-green-500" if completed else 
                " text-muted-foreground" if locked else ""
            )
            
            right_element = (
                Span(duration, cls="ml-auto text-muted-foreground") if duration else
                Badge("Exercise", variant="outline", cls="ml-auto") if type == "exercise" else
                Badge("Completed", variant="secondary", cls="ml-auto") if completed else
                Badge("Locked", variant="outline", cls="ml-auto") if locked else
                None
            )
            
            return Li(
                Div(
                    Icon(icon, cls=icon_cls),
                    title,
                    right_element,
                    cls=f"flex items-center{' opacity-50' if locked else ''}"
                )
            )
        
        def course_module(title, lesson_count, duration, lessons, value, locked=False):
            left_badge = Badge(
                "Coming Soon" if locked else f"{lesson_count} lessons",
                variant="outline" if locked else "secondary",
                cls="mr-2"
            )
            
            right_element = (
                Icon("lucide:lock", cls="h-4 w-4 ml-auto mr-2 text-muted-foreground") if locked else
                Badge(duration, variant="outline", cls="ml-auto mr-2")
            )
            
            content = (
                P("This module will be available after completing previous modules.",
                  cls="text-muted-foreground italic") if locked else 
                Ul(*lessons, cls="space-y-3")
            )
            
            return AccordionItem(
                AccordionTrigger(
                    Div(left_badge, Strong(title), right_element, cls="flex items-center w-full")
                ),
                AccordionContent(content),
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
                AccordionContent(P(a) if isinstance(a, str) else a),
                value=f"item-{i+1}"
            ) for i, (q, a) in enumerate(faqs)
        ]
        
        return Div(
            Accordion(
                *accordion_items,
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