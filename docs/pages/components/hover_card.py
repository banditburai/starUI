"""
HoverCard component documentation - Convention-based functional approach.
Clean, minimal, and easy to extend.
"""

# Component metadata for auto-discovery
TITLE = "Hover Card"
DESCRIPTION = "For sighted users to preview content available behind a link or element on hover. Unlike popovers, hover cards are triggered by mouse hover and are ideal for supplemental information."
CATEGORY = "overlay"
ORDER = 120
STATUS = "stable"

from starhtml import Div, P, Input, Label, Icon, Span, H2, H3, H4, Code, Ul, Li, A, Img, Strong, Hr, Button as HtmlButton, Signal, js
from starui.registry.components.hover_card import (
    HoverCard, HoverCardTrigger, HoverCardContent
)
from starui.registry.components.button import Button
from starui.registry.components.input import Input as UIInput, InputWithLabel
from starui.registry.components.textarea import TextareaWithLabel
from starui.registry.components.card import Card, CardHeader, CardContent, CardTitle, CardDescription
from starui.registry.components.badge import Badge
from starui.registry.components.separator import Separator
from starui.registry.components.avatar import Avatar
from utils import auto_generate_page, with_code, Component, build_api_reference
from widgets.component_preview import ComponentPreview



@with_code
def basic_hover_card_example():
    return Div(
        P("Hover over the link below to see a preview:", cls="text-sm text-muted-foreground mb-6"),
        HoverCard(
            HoverCardTrigger(
                Div(
                    Icon("lucide:external-link", cls="h-4 w-4 mr-2 text-blue-500"),
                    Span("StarUI Documentation", cls="text-blue-600 hover:underline font-medium"),
                    cls="inline-flex items-center cursor-pointer"
                )
            ),
            HoverCardContent(
                Div(
                    Div(
                        Icon("lucide:star", cls="h-6 w-6 mr-2 text-blue-600"),
                        Div(
                            H4("StarUI Component Library", cls="font-semibold text-sm"),
                            P("Modern, accessible React components", cls="text-xs text-muted-foreground"),
                            cls="space-y-0.5"
                        ),
                        cls="flex items-center mb-3"
                    ),
                    P("Build beautiful interfaces with our comprehensive collection of customizable UI components.", cls="text-sm text-muted-foreground mb-3"),
                    Div(
                        *[Div(
                            Div(value, cls="font-semibold text-sm"),
                            Div(label, cls="text-xs text-muted-foreground"),
                            cls="text-center space-y-1"
                        ) for value, label in [("50+", "Components"), ("TypeScript", "Support"), ("Dark", "Mode")]],
                        cls="flex justify-between py-3 px-3 bg-muted/30 rounded-md"
                    ),
                    cls="space-y-2"
                )
            )
        ),
        cls="text-center"
    )


@with_code
def user_profile_hover_card_example():
    return Div(
        P("Hover over the user avatar to see their profile:", cls="text-sm text-muted-foreground mb-4 text-center"),
        Div(
            HoverCard(
                HoverCardTrigger(
                    Div(
                        Avatar(
                            Img(src="https://github.com/shadcn.png", alt="@shadcn"),
                            size="sm",
                            cls="mr-3"
                        ),
                        Span("@shadcn", cls="text-sm font-medium"),
                        cls="flex items-center cursor-pointer hover:bg-muted/50 p-2 rounded-md transition-colors"
                    )
                ),
                HoverCardContent(
                    Div(
                        Div(
                            Avatar(
                                Img(src="https://github.com/shadcn.png", alt="@shadcn"),
                                size="md",
                                cls="mr-3"
                            ),
                            Div(
                                H4("shadcn", cls="text-sm font-semibold"),
                                P("@shadcn", cls="text-xs text-muted-foreground"),
                                Badge("Pro", variant="secondary", cls="mt-1"),
                                cls="space-y-1"
                            ),
                            cls="flex items-start mb-4"
                        ),
                        P("Building beautiful and accessible UI components. Creator of ui/shadcn.", cls="text-sm text-muted-foreground mb-4"),
                        Div(
                            *[Div(
                                Strong(value, cls="text-sm"),
                                P(label, cls="text-xs text-muted-foreground"),
                                cls="text-center"
                            ) for value, label in [("1.2k", "Following"), ("12.5k", "Followers"), ("342", "Repos")]],
                            cls="flex justify-around py-3 border-t border-b border-border my-4"
                        ),
                        Div(
                            Button("Follow", size="sm", cls="flex-1 mr-2"),
                            Button("Message", size="sm", variant="outline", cls="flex-1"),
                            cls="flex gap-2"
                        ),
                        cls="space-y-2"
                    ),
                    cls="w-80"
                )
            ),
            cls="flex justify-center"
        )
    )


@with_code
def repository_hover_card_example():
    return Div(
        P("Hover over the repository link:", cls="text-sm text-muted-foreground mb-4"),
        HoverCard(
            HoverCardTrigger(
                Div(
                    Icon("lucide:star", cls="h-4 w-4 mr-2 text-blue-500"),
                    A("starui/components", href="#", cls="text-blue-600 hover:underline font-medium"),
                    cls="inline-flex items-center cursor-pointer"
                )
            ),
            HoverCardContent(
                Div(
                    Div(
                        Icon("lucide:folder-git-2", cls="h-4 w-4 mr-2 text-muted-foreground"),
                        H4("starui/components", cls="text-sm font-semibold text-blue-600"),
                        Badge("Public", variant="secondary", cls="ml-auto text-xs"),
                        cls="flex items-center mb-3"
                    ),
                    P("Beautifully designed components that make building interfaces with StarHTML a breeze.", cls="text-sm text-muted-foreground mb-3"),
                    Div(
                        Div(
                            Icon("lucide:star", cls="h-3.5 w-3.5 mr-1 text-yellow-500"),
                            Span("2.1k", cls="text-sm font-medium mr-4"),
                            Icon("lucide:git-fork", cls="h-3.5 w-3.5 mr-1 text-muted-foreground"),
                            Span("184", cls="text-sm text-muted-foreground"),
                            cls="flex items-center mb-2"
                        ),
                        Div(
                            Div(cls="w-3 h-3 bg-blue-500 rounded-full mr-1"),
                            Span("Python", cls="text-xs text-muted-foreground mr-3"),
                            Span("Updated 2 days ago", cls="text-xs text-muted-foreground"),
                            cls="flex items-center"
                        ),
                        cls="space-y-1 pl-6"
                    ),
                    cls="space-y-1"
                ),
                side="top"
            )
        ),
        cls="text-center"
    )


@with_code
def product_preview_hover_card_example():
    return Div(
        P("Hover over the product name to see details:", cls="text-sm text-muted-foreground mb-4"),
        HoverCard(
            HoverCardTrigger(
                Div(
                    Div("📱", cls="text-xl mr-2"),
                    Span("iPhone 15 Pro", cls="text-sm font-medium text-blue-600"),
                    cls="flex items-center cursor-pointer hover:underline"
                )
            ),
            HoverCardContent(
                Div(
                    Div(
                        Div("📱", cls="text-3xl mb-2"),
                        H4("iPhone 15 Pro", cls="font-semibold text-lg"),
                        P("Titanium. So strong. So light. So Pro.", cls="text-sm text-muted-foreground mb-3"),
                        cls="text-center"
                    ),
                    Div(
                        Div(
                            Span("Starting at", cls="text-xs text-muted-foreground block mb-1"),
                            Span("$999", cls="text-xl font-bold text-foreground"),
                            cls="text-center mb-3"
                        ),
                        Div(
                            Span("⭐ 4.8", cls="text-sm font-medium mr-2"),
                            Span("(2.1k reviews)", cls="text-xs text-muted-foreground"),
                            cls="flex items-center justify-center"
                        ),
                        cls="mb-4"
                    ),
                    Div(
                        Ul(
                            Li("A17 Pro chip with 6-core GPU", cls="text-xs"),
                            Li("ProRAW and ProRes recording", cls="text-xs"),
                            Li("Up to 29 hours video playback", cls="text-xs"),
                            cls="list-disc list-inside space-y-1 text-muted-foreground mb-4"
                        )
                    ),
                    Button("Learn More", size="sm", cls="w-full"),
                    cls="space-y-3"
                ),
                side="top",
                cls="w-72"
            )
        ),
        cls="text-center"
    )


@with_code
def positioning_hover_card_examples():
    positions = [
        ("Top", "top", "This hover card appears above the trigger", {}),
        ("Bottom", "bottom", "This hover card appears below the trigger", {}),
        ("Left", "left", "This hover card appears to the left", {}),
        ("Right", "right", "This hover card appears to the right", {"align": "start"})
    ]

    def create_positioned_hover_card(label, side, description, extra_props):
        return HoverCard(
            HoverCardTrigger(Button(label, variant="outline", size="sm")),
            HoverCardContent(
                Div(
                    H4(f"{label} Position", cls="font-semibold mb-2"),
                    P(description, cls="text-sm text-muted-foreground"),
                    cls="text-center"
                ),
                side=side,
                **extra_props
            )
        )

    return Div(
        P("Hover over the buttons to see different positioning options:", cls="text-sm text-muted-foreground mb-4"),
        Div(
            *[create_positioned_hover_card(label, side, description, extra_props)
              for label, side, description, extra_props in positions],
            cls="flex gap-4 items-center justify-center py-8 flex-wrap"
        ),
        cls="space-y-4 overflow-visible"
    )


@with_code
def link_preview_hover_card_example():
    return Div(
        P("Rich content hover cards for documentation links:", cls="text-sm text-muted-foreground mb-4"),
        Div(
            P("Learn more about ",
              HoverCard(
                  HoverCardTrigger(
                      A("StarHTML", href="#", cls="text-blue-600 hover:underline font-semibold")
                  ),
                  HoverCardContent(
                      Div(
                          Div(
                              Icon("lucide:book-open", cls="h-5 w-5 mr-3 text-blue-600"),
                              Div(
                                  H4("StarHTML Framework", cls="font-semibold text-sm mb-1"),
                                  P("Modern Python web framework", cls="text-xs text-muted-foreground"),
                              ),
                              cls="flex items-start mb-4"
                          ),
                          P("A Python framework for building modern web applications with server-side rendering and reactive components.",
                            cls="text-sm text-muted-foreground mb-4"),
                          Div(
                              H4("Key Features", cls="text-sm font-semibold mb-2"),
                              Div(
                                  Div("• Server-side rendering", cls="text-sm text-muted-foreground mb-1"),
                                  Div("• Reactive components", cls="text-sm text-muted-foreground mb-1"),
                                  Div("• Modern Python syntax", cls="text-sm text-muted-foreground mb-1"),
                                  Div("• TypeScript-like development", cls="text-sm text-muted-foreground"),
                              ),
                              cls="mb-4"
                          ),
                          Div(
                              A(
                                  "View Documentation →",
                                  href="#",
                                  cls="text-sm text-blue-600 hover:text-blue-800 block mb-2"
                              ),
                              A(
                                  "View on GitHub →",
                                  href="#",
                                  cls="text-sm text-blue-600 hover:text-blue-800 block"
                              ),
                          ),
                      ),
                      side="top",
                      cls="w-80"
                  )
              ),
              " and its component system.", cls="text-sm")
        )
    )


@with_code
def interactive_form_hover_card_example():
    contact_name = Signal("contact_name", "")
    contact_email = Signal("contact_email", "")
    contact_message = Signal("contact_message", "")

    return Div(
        P("Hover over the contact button to see an interactive form:", cls="text-sm text-muted-foreground mb-4 text-center"),
        Div(
            HoverCard(
                HoverCardTrigger(
                    Div(
                        Icon("lucide:mail", cls="h-4 w-4 mr-2"),
                        Span("Quick Contact", cls="text-sm font-medium"),
                        cls="flex items-center p-2 rounded-md border hover:bg-accent cursor-pointer"
                    )
                ),
                HoverCardContent(
                    Div(
                        contact_name,
                        contact_email,
                        contact_message,
                        H4("Send Quick Message", cls="font-semibold text-sm mb-4"),
                        Div(
                            Div(
                                Label("Name", cls="text-xs font-medium mb-1 block"),
                                UIInput(
                                    placeholder="Your name",
                                    cls="text-sm",
                                    signal=contact_name
                                ),
                                cls="mb-3"
                            ),
                            Div(
                                Label("Email", cls="text-xs font-medium mb-1 block"),
                                UIInput(
                                    type="email",
                                    placeholder="your@email.com",
                                    signal=contact_email,
                                    cls="text-sm"
                                ),
                                cls="mb-3"
                            ),
                            Div(
                                TextareaWithLabel(
                                    label="Message",
                                    placeholder="Your message...",
                                    signal=contact_message,
                                    rows=3,
                                    cls="text-sm resize-none"
                                ),
                                cls="mb-4"
                            ),
                            Button(
                                "Send Message",
                                size="sm",
                                cls="w-full",
                                data_attr_disabled=~contact_name | ~contact_email | ~contact_message,
                                data_on_click=[
                                    f"alert('Thank you ' + {contact_name} + '! Your message has been sent.')",
                                    contact_name.set(''),
                                    contact_email.set(''),
                                    contact_message.set('')
                                ]
                            ),
                        ),
                        cls="space-y-2"
                    ),
                    side="left",
                    cls="w-72"
                )
            ),
            cls="flex justify-center"
        )
    )



EXAMPLES_DATA = [
    {"title": "Basic Hover Card", "description": "Simple hover card with text content that appears on hover", "fn": basic_hover_card_example},
    {"title": "User Profile Hover Card", "description": "Rich profile card with avatar, bio, stats, and action buttons", "fn": user_profile_hover_card_example},
    {"title": "Repository Hover Card", "description": "GitHub repository preview with stats and language info", "fn": repository_hover_card_example},
    {"title": "Product Preview Hover Card", "description": "E-commerce product preview with pricing, features, and call-to-action", "fn": product_preview_hover_card_example},
    {"title": "Positioning Options", "description": "Hover cards can be positioned on any side with flexible alignment", "fn": positioning_hover_card_examples},
    {"title": "Link Preview Hover Card", "description": "Rich documentation previews with features, links, and detailed content", "fn": link_preview_hover_card_example},
    {"title": "Interactive Form Hover Card", "description": "Hover card with interactive form fields and validation", "fn": interactive_form_hover_card_example},
]

API_REFERENCE = build_api_reference(
    components=[
        Component("HoverCard", "Container that manages open state for trigger and content on hover"),
        Component("HoverCardTrigger", "Element that opens/closes the hover card based on mouse enter/leave, with delays"),
        Component("HoverCardContent", "The floating content positioned relative to its trigger with side and alignment controls"),
    ]
)




def create_hover_card_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)
