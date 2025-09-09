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

from starhtml import Div, P, Input, Label, Icon, Span, H2, H3, H4, Code, Ul, Li, A, Img, Strong, Hr, Button as HtmlButton
from starhtml.datastar import (
    ds_on_click, ds_show, ds_text, ds_signals, value,
    ds_bind, ds_disabled, ds_on_change, ds_effect, ds_class, ds_style
)
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
from utils import auto_generate_page
from widgets.component_preview import ComponentPreview


def examples():
    """Generate hover card examples using ComponentPreview with tabs."""
    
    # Basic hover card
    yield ComponentPreview(
        Div(
            P("Hover over the link below to see a preview:", cls="text-sm text-muted-foreground mb-6"),
            HoverCard(
                HoverCardTrigger(
                    Div(
                        Icon("lucide:external-link", cls="h-4 w-4 mr-2 text-blue-500"),
                        Span("StarUI Documentation", cls="text-blue-600 hover:underline font-medium"),
                        cls="inline-flex items-center cursor-pointer"
                    ),
                    signal="basic_hover"
                ),
                HoverCardContent(
                    Div(
                        # Header with icon
                        Div(
                            Icon("lucide:star", width="24", height="24", cls="mr-2 text-blue-600 text-xl"),
                            Div(
                                H4("StarUI Component Library", cls="font-semibold text-sm"),
                                P("Modern, accessible React components", cls="text-xs text-muted-foreground"),
                                cls="space-y-0.5"
                            ),
                            cls="flex items-center mb-3"
                        ),
                        # Description
                        P("Build beautiful interfaces with our comprehensive collection of customizable UI components.", 
                          cls="text-sm text-muted-foreground mb-3"),
                        # Quick stats
                        Div(
                            Div(
                                Div("50+", cls="font-semibold text-sm"),
                                Div("Components", cls="text-xs text-muted-foreground"),
                                cls="text-center space-y-1"
                            ),
                            Div(
                                Div("TypeScript", cls="font-semibold text-sm"),
                                Div("Support", cls="text-xs text-muted-foreground"),
                                cls="text-center space-y-1"
                            ),
                            Div(
                                Div("Dark", cls="font-semibold text-sm"),
                                Div("Mode", cls="text-xs text-muted-foreground"),
                                cls="text-center space-y-1"
                            ),
                            cls="flex justify-between py-3 px-3 bg-muted/30 rounded-md"
                        ),
                        cls="space-y-2"
                    ),
                    signal="basic_hover"
                ),
                signal="basic_hover"
            ),
            cls="text-center"
        ),
        '''HoverCard(
    HoverCardTrigger(
        Div(
            Icon("lucide:external-link", cls="h-4 w-4 mr-2 text-blue-500"),
            Span("StarUI Documentation", cls="text-blue-600 hover:underline font-medium"),
            cls="inline-flex items-center cursor-pointer"
        ),
        signal="basic_hover"
    ),
    HoverCardContent(
        Div(
            # Header with icon
            Div(
                Icon("lucide:star", width="24", height="24", cls="mr-2 text-blue-600 text-xl"),
                Div(
                    H4("StarUI Component Library", cls="font-semibold text-sm"),
                    P("Modern, accessible React components", cls="text-xs text-muted-foreground")
                ),
                cls="flex items-center mb-3"
            ),
            # Description  
            P("Build beautiful interfaces with our comprehensive collection of customizable UI components.", 
              cls="text-sm text-muted-foreground mb-3"),
            # Quick stats with better spacing
            Div(
                Div(
                    Div("50+", cls="font-semibold text-sm"),
                    Div("Components", cls="text-xs text-muted-foreground"),
                    cls="text-center space-y-1"
                ),
                Div(
                    Div("TypeScript", cls="font-semibold text-sm"),
                    Div("Support", cls="text-xs text-muted-foreground"),
                    cls="text-center space-y-1"
                ),
                Div(
                    Div("Dark", cls="font-semibold text-sm"),
                    Div("Mode", cls="text-xs text-muted-foreground"),
                    cls="text-center space-y-1"
                ),
                cls="flex justify-between py-3 px-3 bg-muted/30 rounded-md"
            )
        ),
        signal="basic_hover"
    ),
    signal="basic_hover"
)''',
        title="Basic Hover Card",
        description="Simple hover card with text content that appears on hover"
    )
    
    # User profile hover card
    yield ComponentPreview(
        Div(
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
                        ),
                        signal="profile_hover"
                    ),
                HoverCardContent(
                    Div(
                        # Header with avatar and basic info
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
                        # Bio
                        P("Building beautiful and accessible UI components. Creator of ui/shadcn.", 
                          cls="text-sm text-muted-foreground mb-4"),
                        # Stats
                        Div(
                            Div(
                                Strong("1.2k", cls="text-sm"),
                                P("Following", cls="text-xs text-muted-foreground"),
                                cls="text-center"
                            ),
                            Div(
                                Strong("12.5k", cls="text-sm"),
                                P("Followers", cls="text-xs text-muted-foreground"),
                                cls="text-center"
                            ),
                            Div(
                                Strong("342", cls="text-sm"),
                                P("Repos", cls="text-xs text-muted-foreground"),
                                cls="text-center"
                            ),
                            cls="flex justify-around py-3 border-t border-b border-border my-4"
                        ),
                        # Actions
                        Div(
                            Button("Follow", size="sm", cls="flex-1 mr-2"),
                            Button("Message", size="sm", variant="outline", cls="flex-1"),
                            cls="flex gap-2"
                        ),
                        cls="space-y-2"
                    ),
                    signal="profile_hover",
                    cls="w-80"
                ),
                signal="profile_hover"
            ),
                cls="flex justify-center"
            )
        ),
        '''HoverCard(
    HoverCardTrigger(
        Div(
            Avatar(Img(src="https://github.com/shadcn.png", alt="@shadcn"), size="sm"),
            Span("@shadcn", cls="text-sm font-medium"),
            cls="flex items-center cursor-pointer hover:bg-muted/50 p-2 rounded-md"
        ),
        signal="profile_hover"
    ),
    HoverCardContent(
        Div(
            # Profile header
            Div(
                Avatar(Img(src="https://github.com/shadcn.png"), size="md"),
                Div(
                    H4("shadcn", cls="text-sm font-semibold"),
                    P("@shadcn", cls="text-xs text-muted-foreground"),
                    Badge("Pro", variant="secondary")
                ),
                cls="flex items-start mb-4"
            ),
            # Bio
            P("Building beautiful and accessible UI components...", 
              cls="text-sm text-muted-foreground mb-4"),
            # Stats section
            Div(/* following, followers, repos stats */),
            # Action buttons
            Div(
                Button("Follow", size="sm"),
                Button("Message", size="sm", variant="outline")
            )
        ),
        signal="profile_hover",
        cls="w-80"
    ),
    signal="profile_hover"
)''',
        title="User Profile Hover Card",
        description="Rich profile card with avatar, bio, stats, and action buttons"
    )
    
    # Repository preview hover card
    yield ComponentPreview(
        Div(
            P("Hover over the repository link:", cls="text-sm text-muted-foreground mb-4"),
            HoverCard(
                HoverCardTrigger(
                    Div(
                        Icon("lucide:star", width="16", height="16", cls="mr-2 text-blue-500"),
                        A("starui/components", href="#", cls="text-blue-600 hover:underline font-medium"),
                        cls="inline-flex items-center cursor-pointer"
                    ),
                    signal="repo_hover"
                ),
                HoverCardContent(
                    Div(
                        # Repo header
                        Div(
                            Icon("lucide:repo", width="16", height="16", cls="mr-2 text-muted-foreground"),
                            H4("starui/components", cls="text-sm font-semibold text-blue-600"),
                            Badge("Public", variant="secondary", cls="ml-auto text-xs"),
                            cls="flex items-center mb-3"
                        ),
                        # Description
                        P("Beautifully designed components that make building interfaces with StarHTML a breeze.", 
                          cls="text-sm text-muted-foreground mb-3"),
                        # Repository stats - GitHub style with better indent
                        Div(
                            Div(
                                Icon("lucide:star", width="14", height="14", cls="mr-1 text-yellow-500"),
                                Span("2.1k", cls="text-sm font-medium mr-4"),
                                Icon("lucide:git-fork", width="14", height="14", cls="mr-1 text-muted-foreground"),
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
                    signal="repo_hover",
                    side="top"
                ),
                signal="repo_hover"
            ),
            cls="text-center"
        ),
        '''HoverCard(
    HoverCardTrigger(
        Div(
            Icon("lucide:star", width="16", height="16", cls="mr-2 text-blue-500"),
            A("starui/components", href="#", cls="text-blue-600 hover:underline font-medium"),
            cls="inline-flex items-center cursor-pointer"
        ),
        signal="repo_hover"
    ),
    HoverCardContent(
        Div(
            # Repository header with icon and badge
            Div(
                Icon("lucide:repo", width="16", height="16", cls="mr-2 text-muted-foreground"),
                H4("starui/components", cls="text-sm font-semibold text-blue-600"),
                Badge("Public", variant="secondary", cls="ml-auto text-xs"),
                cls="flex items-center mb-3"
            ),
            # Description
            P("Beautifully designed components that make building interfaces with StarHTML a breeze.", 
              cls="text-sm text-muted-foreground mb-3"),
            # GitHub-style stats
            Div(
                Div(
                    Icon("lucide:star", width="14", height="14", cls="mr-1 text-yellow-500"),
                    Span("2.1k", cls="text-sm font-medium mr-4"),
                    Icon("lucide:git-fork", width="14", height="14", cls="mr-1 text-muted-foreground"),
                    Span("184", cls="text-sm text-muted-foreground"),
                    cls="flex items-center mb-2"
                ),
                Div(
                    Div(cls="w-3 h-3 bg-blue-500 rounded-full mr-1"),  # Language dot
                    Span("Python", cls="text-xs text-muted-foreground mr-3"),
                    Span("Updated 2 days ago", cls="text-xs text-muted-foreground"),
                    cls="flex items-center"
                ),
                cls="space-y-1 pl-6"  # Add indent to stats section
            )
        ),
        signal="repo_hover",
        side="top"
    ),
    signal="repo_hover"
)''',
        title="Repository Hover Card",
        description="GitHub repository preview with stats and language info"
    )
    
    # Product preview hover card
    yield ComponentPreview(
        Div(
            P("Hover over the product name to see details:", cls="text-sm text-muted-foreground mb-4"),
            HoverCard(
                HoverCardTrigger(
                    Div(
                        Div("📱", cls="text-xl mr-2"),
                        Span("iPhone 15 Pro", cls="text-sm font-medium text-blue-600"),
                        cls="flex items-center cursor-pointer hover:underline"
                    ),
                    signal="product_hover"
                ),
                HoverCardContent(
                    Div(
                        # Product header
                        Div(
                            Div("📱", cls="text-3xl mb-2"),
                            H4("iPhone 15 Pro", cls="font-semibold text-lg"),
                            P("Titanium. So strong. So light. So Pro.", cls="text-sm text-muted-foreground mb-3"),
                            cls="text-center"
                        ),
                        # Pricing and rating
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
                        # Features list
                        Div(
                            Ul(
                                Li("A17 Pro chip with 6-core GPU", cls="text-xs"),
                                Li("ProRAW and ProRes recording", cls="text-xs"),
                                Li("Up to 29 hours video playback", cls="text-xs"),
                                cls="list-disc list-inside space-y-1 text-muted-foreground mb-4"
                            )
                        ),
                        # CTA
                        Button("Learn More", size="sm", cls="w-full"),
                        cls="space-y-3"
                    ),
                    signal="product_hover",
                    side="top",
                    cls="w-72"
                ),
                signal="product_hover"
            ),
            cls="text-center"
        ),
        '''HoverCard(
    HoverCardTrigger(
        Div(
            Div("📱", cls="text-xl mr-2"),
            Span("iPhone 15 Pro", cls="text-sm font-medium text-blue-600"),
            cls="flex items-center cursor-pointer hover:underline"
        ),
        signal="product_hover"
    ),
    HoverCardContent(
        Div(
            # Product header
            Div(
                Div("📱", cls="text-3xl mb-2"),
                H4("iPhone 15 Pro", cls="font-semibold text-lg"),
                P("Titanium. So strong. So light. So Pro.", cls="text-sm text-muted-foreground")
            ),
            # Pricing and rating  
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
                )
            ),
            # Features
            Ul(
                Li("A17 Pro chip with 6-core GPU"),
                Li("ProRAW and ProRes recording"),
                Li("Up to 29 hours video playback"),
                cls="list-disc list-inside space-y-1 text-muted-foreground"
            ),
            # CTA button
            Button("Learn More", size="sm", cls="w-full")
        ),
        signal="product_hover",
        side="top",
        cls="w-72"
    ),
    signal="product_hover"
)''',
        title="Product Preview Hover Card",
        description="E-commerce product preview with pricing, features, and call-to-action"
    )
    
    # Multiple positioning demonstration
    yield ComponentPreview(
        Div(
            P("Hover over the buttons to see different positioning options:", cls="text-sm text-muted-foreground mb-4"),
            Div(
                # Top
                HoverCard(
                    HoverCardTrigger(
                        Button("Top", variant="outline", size="sm"),
                        signal="top_hover"
                    ),
                    HoverCardContent(
                        Div(
                            H4("Top Position", cls="font-semibold mb-2"),
                            P("This hover card appears above the trigger", cls="text-sm text-muted-foreground"),
                            cls="text-center"
                        ),
                        signal="top_hover",
                        side="top"
                    ),
                    signal="top_hover"
                ),
                # Bottom  
                HoverCard(
                    HoverCardTrigger(
                        Button("Bottom", variant="outline", size="sm"),
                        signal="bottom_hover"
                    ),
                    HoverCardContent(
                        Div(
                            H4("Bottom Position", cls="font-semibold mb-2"),
                            P("This hover card appears below the trigger", cls="text-sm text-muted-foreground"),
                            cls="text-center"
                        ),
                        signal="bottom_hover",
                        side="bottom"
                    ),
                    signal="bottom_hover"
                ),
                # Left
                HoverCard(
                    HoverCardTrigger(
                        Button("Left", variant="outline", size="sm"),
                        signal="left_hover"
                    ),
                    HoverCardContent(
                        Div(
                            H4("Left Position", cls="font-semibold mb-2"),
                            P("This hover card appears to the left", cls="text-sm text-muted-foreground"),
                            cls="text-center"
                        ),
                        signal="left_hover",
                        side="left"
                    ),
                    signal="left_hover"
                ),
                # Right
                HoverCard(
                    HoverCardTrigger(
                        Button("Right", variant="outline", size="sm"),
                        signal="right_hover"
                    ),
                    HoverCardContent(
                        Div(
                            H4("Right Position", cls="font-semibold mb-2"),
                            P("This hover card appears to the right", cls="text-sm text-muted-foreground"),
                            cls="text-center"
                        ),
                        signal="right_hover",
                        side="right",
                        align="start"
                    ),
                    signal="right_hover"
                ),
                cls="flex gap-4 items-center justify-center py-8 flex-wrap"
            ),
            cls="space-y-4 overflow-visible"
        ),
        '''# Different positioning options
HoverCard(
    HoverCardTrigger(Button("Top", variant="outline", size="sm"), signal="top_hover"),
    HoverCardContent(
        Div(
            H4("Top Position", cls="font-semibold mb-2"),
            P("This hover card appears above the trigger", cls="text-sm text-muted-foreground")
        ),
        signal="top_hover",
        side="top"  # Positions above the trigger
    ),
    signal="top_hover"
)

HoverCard(
    HoverCardTrigger(Button("Right", variant="outline", size="sm"), signal="right_hover"),
    HoverCardContent(
        Div(
            H4("Right Position", cls="font-semibold mb-2"),
            P("This hover card appears to the right", cls="text-sm text-muted-foreground")
        ),
        signal="right_hover",
        side="right",    # Positions to the right
        align="start"    # Aligns with start of trigger
    ),
    signal="right_hover"
)''',
        title="Positioning Options",
        description="Hover cards can be positioned on any side with flexible alignment"
    )
    
    # Link preview with rich content
    yield ComponentPreview(
        Div(
            P("Rich content hover cards for documentation links:", cls="text-sm text-muted-foreground mb-4"),
            Div(
                P("Learn more about ", 
                  HoverCard(
                      HoverCardTrigger(
                          A("StarHTML", href="#", cls="text-blue-600 hover:underline font-semibold"),
                          signal="docs_hover"
                      ),
                      HoverCardContent(
                          Div(
                              # Header with icon and title
                              Div(
                                  Icon("lucide:book-open", width="20", height="20", cls="mr-3 text-blue-600"),
                                  Div(
                                      H4("StarHTML Framework", cls="font-semibold text-sm mb-1"),
                                      P("Modern Python web framework", cls="text-xs text-muted-foreground"),
                                  ),
                                  cls="flex items-start mb-4"
                              ),
                              # Description
                              P("A Python framework for building modern web applications with server-side rendering and reactive components.", 
                                cls="text-sm text-muted-foreground mb-4"),
                              # Features - simplified
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
                              # Action links
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
                          signal="docs_hover",
                          side="top",
                          cls="w-80"
                      ),
                      signal="docs_hover"
                  ),
                  " and its component system.", cls="text-sm")
            )
        ),
        '''P("Learn more about ", 
  HoverCard(
      HoverCardTrigger(
          A("StarHTML", href="#", cls="text-blue-600 hover:underline font-semibold"),
          signal="docs_hover"
      ),
      HoverCardContent(
          Div(
              # Header with icon and title
              Div(
                  Icon("lucide:book-open", width="20", height="20", cls="mr-3 text-blue-600"),
                  Div(
                      H4("StarHTML Framework", cls="font-semibold text-sm mb-1"),
                      P("Modern Python web framework", cls="text-xs text-muted-foreground")
                  ),
                  cls="flex items-start mb-4"
              ),
              # Description
              P("A Python framework for building modern web applications with server-side rendering and reactive components.", 
                cls="text-sm text-muted-foreground mb-4"),
              # Features - simplified and left-aligned
              Div(
                  H4("Key Features", cls="text-sm font-semibold mb-2"),
                  Div(
                      Div("• Server-side rendering", cls="text-sm text-muted-foreground mb-1"),
                      Div("• Reactive components", cls="text-sm text-muted-foreground mb-1"),
                      Div("• Modern Python syntax", cls="text-sm text-muted-foreground mb-1"),
                      Div("• TypeScript-like development", cls="text-sm text-muted-foreground")
                  ),
                  cls="mb-4"
              ),
              # Action links - stacked vertically
              Div(
                  A("View Documentation →", href="#", cls="text-sm text-blue-600 hover:text-blue-800 block mb-2"),
                  A("View on GitHub →", href="#", cls="text-sm text-blue-600 hover:text-blue-800 block")
              )
          ),
          signal="docs_hover",
          side="top",
          cls="w-80"
      ),
      signal="docs_hover"
  ),
  " and its component system.")''',
        title="Link Preview Hover Card",
        description="Rich documentation previews with features, links, and detailed content"
    )
    
    # Interactive hover card with form
    yield ComponentPreview(
        Div(
            P("Hover over the contact button to see an interactive form:", cls="text-sm text-muted-foreground mb-4 text-center"),
            Div(
                HoverCard(
                HoverCardTrigger(
                    Div(
                        Icon("lucide:mail", cls="h-4 w-4 mr-2"),
                        Span("Quick Contact", cls="text-sm font-medium"),
                        cls="flex items-center p-2 rounded-md border hover:bg-accent cursor-pointer"
                    ),
                    signal="contact_hover"
                ),
                HoverCardContent(
                    Div(
                        H4("Send Quick Message", cls="font-semibold text-sm mb-4"),
                        Div(
                            # Name input
                            Div(
                                Label("Name", cls="text-xs font-medium mb-1 block"),
                                UIInput(
                                    placeholder="Your name",
                                    cls="text-sm",
                                    signal="contact_name"
                                ),
                                cls="mb-3"
                            ),
                            # Email input
                            Div(
                                Label("Email", cls="text-xs font-medium mb-1 block"),
                                UIInput(
                                    type="email",
                                    placeholder="your@email.com",
                                    signal="contact_email",
                                    cls="text-sm"
                                ),
                                cls="mb-3"
                            ),
                            # Message textarea
                            TextareaWithLabel(
                                label="Message",
                                placeholder="Your message...",
                                signal="contact_message",
                                rows=3,
                                cls="text-sm resize-none",
                                class_name="mb-4"
                            ),
                            # Submit button
                            Button(
                                "Send Message",
                                size="sm",
                                cls="w-full",
                                ds_disabled="!$contact_name || !$contact_email || !$contact_message",
                                ds_on_click="""
                                    if ($contact_name && $contact_email && $contact_message) {
                                        alert(`Thank you ${$contact_name}! Your message has been sent.`);
                                        $contact_name = '';
                                        $contact_email = '';
                                        $contact_message = '';
                                    }
                                """
                            ),
                            ds_signals(
                                contact_name=value(""),
                                contact_email=value(""),
                                contact_message=value("")
                            )
                        ),
                        cls="space-y-2"
                    ),
                    signal="contact_hover",
                    side="left",
                    cls="w-72"
                ),
                signal="contact_hover"
            ),
                cls="flex justify-center"
            )
        ),
        '''HoverCard(
    HoverCardTrigger(
        Div(
            Icon("lucide:mail", cls="h-4 w-4 mr-2"),
            Span("Quick Contact", cls="text-sm font-medium"),
            cls="flex items-center p-2 rounded-md border hover:bg-accent cursor-pointer"
        ),
        signal="contact_hover"
    ),
    HoverCardContent(
        Div(
            H4("Send Quick Message", cls="font-semibold text-sm mb-4"),
            Div(
                # Form fields
                Div(
                    Label("Name", cls="text-xs font-medium mb-1 block"),
                    UIInput(placeholder="Your name", signal="contact_name")
                ),
                Div(
                    Label("Email", cls="text-xs font-medium mb-1 block"),
                    UIInput(type="email", placeholder="your@email.com", signal="contact_email")
                ),
                TextareaWithLabel(
                    label="Message",
                    placeholder="Your message...",
                    signal="contact_message",
                    rows=3,
                    cls="text-sm resize-none"
                ),
                # Submit button with validation
                Button(
                    "Send Message",
                    size="sm",
                    cls="w-full",
                    ds_disabled="!$contact_name || !$contact_email || !$contact_message",
                    ds_on_click="sendContactForm()"
                ),
                ds_signals(contact_name="", contact_email="", contact_message="")
            )
        ),
        signal="contact_hover",
        side="left",
        cls="w-72"
    ),
    signal="contact_hover"
)''',
        title="Interactive Form Hover Card",
        description="Hover card with interactive form fields and validation"
    )


def create_hover_card_docs():
    """Create hover card documentation page using convention-based approach."""
    
    api_reference = {
        "props": [
            {
                "name": "children",
                "type": "tuple[FT, ...]",
                "description": "HoverCardTrigger and HoverCardContent components"
            },
            {
                "name": "signal",
                "type": "str | None",
                "default": "None",
                "description": "Custom signal name for the hover state. Auto-generated if not provided."
            },
            {
                "name": "default_open",
                "type": "bool",
                "default": "False",
                "description": "Whether the hover card is initially visible"
            },
            {
                "name": "cls",
                "type": "str",
                "default": "'relative inline-block'",
                "description": "Additional CSS classes for the container"
            }
        ],
        "sub_components": [
            {
                "name": "HoverCardTrigger",
                "description": "Element that triggers the hover card on mouse enter/leave",
                "props": [
                    {
                        "name": "signal",
                        "type": "str | None",
                        "default": "None",
                        "description": "Signal name matching the parent HoverCard"
                    },
                    {
                        "name": "hover_delay",
                        "type": "int",
                        "default": "700",
                        "description": "Delay in milliseconds before showing the hover card"
                    },
                    {
                        "name": "hide_delay",
                        "type": "int",
                        "default": "300",
                        "description": "Delay in milliseconds before hiding the hover card"
                    },
                    {
                        "name": "cls",
                        "type": "str",
                        "default": "'inline-block cursor-pointer'",
                        "description": "Additional CSS classes for the trigger element"
                    }
                ]
            },
            {
                "name": "HoverCardContent",
                "description": "Container for hover card content with positioning",
                "props": [
                    {
                        "name": "signal",
                        "type": "str | None",
                        "default": "None",
                        "description": "Signal name matching the parent HoverCard"
                    },
                    {
                        "name": "side",
                        "type": "Literal['top', 'right', 'bottom', 'left']",
                        "default": "'bottom'",
                        "description": "Preferred side for hover card placement"
                    },
                    {
                        "name": "align",
                        "type": "Literal['start', 'center', 'end']",
                        "default": "'center'",
                        "description": "Alignment relative to the trigger element"
                    },
                    {
                        "name": "hide_delay",
                        "type": "int",
                        "default": "300",
                        "description": "Delay in milliseconds before hiding when mouse leaves content"
                    },
                    {
                        "name": "cls",
                        "type": "str",
                        "default": "'fixed z-50 w-72 max-w-[90vw] pointer-events-auto rounded-md border bg-popover p-4 text-popover-foreground shadow-md outline-none'",
                        "description": "CSS classes for content styling and positioning"
                    }
                ]
            }
        ]
    }
    
    # Hero example
    hero_example = ComponentPreview(
        Div(
            HoverCard(
                HoverCardTrigger(
                    A("@starui", href="#", cls="text-blue-600 hover:underline font-semibold"),
                    signal="hero_hover"
                ),
                HoverCardContent(
                    Div(
                        H3("StarUI Components", cls="font-semibold text-sm mb-2"),
                        P("Beautiful, accessible components built with StarHTML. Perfect for displaying rich content on hover without disrupting the user experience.", 
                          cls="text-sm text-muted-foreground mb-4"),
                        Div(
                            Button("Explore Components", size="sm", cls="w-full"),
                            Button("Documentation", size="sm", variant="outline", cls="w-full"),
                            cls="space-y-2"
                        )
                    ),
                    signal="hero_hover"
                ),
                signal="hero_hover"
            ),
            cls="flex justify-center py-8"
        ),
        '''HoverCard(
    HoverCardTrigger(
        A("@starui", href="#", cls="text-blue-600 hover:underline font-semibold"),
        signal="hero_hover"
    ),
    HoverCardContent(
        Div(
            H3("StarUI Components", cls="font-semibold text-sm mb-2"),
            P("Beautiful, accessible components built with StarHTML...", 
              cls="text-sm text-muted-foreground mb-4"),
            Div(
                Button("Explore Components", size="sm", cls="w-full"),
                Button("Documentation", size="sm", variant="outline", cls="w-full"),
                cls="space-y-2"
            )
        ),
        signal="hero_hover"
    ),
    signal="hero_hover"
)''',
        copy_button=True
    )
    
    return auto_generate_page(
        TITLE,
        DESCRIPTION,
        list(examples()),
        cli_command="star add hover-card",
        api_reference=api_reference,
        hero_example=hero_example,
        component_slug="hover-card"
    )