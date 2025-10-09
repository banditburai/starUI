"""
Typography component documentation - Convention-based functional approach.
Clean, minimal, and easy to extend.
"""

# Component metadata for auto-discovery
TITLE = "Typography"
DESCRIPTION = "Beautifully styled typographic elements for consistent text presentation."
CATEGORY = "ui"
ORDER = 85
STATUS = "stable"

from starhtml import Div, Icon, Span, Img, Signal, js
from starui.registry.components.typography import (
    Display, H1, H2, H3, H4, H5, H6,
    P, Lead, Large, Small, Muted, Subtitle, Caption,
    Text, InlineCode, Blockquote, List, Prose,
    Kbd, Mark, Strong, Em, Hr, Figure, Figcaption
)
from starui.registry.components.card import Card, CardHeader, CardContent, CardTitle, CardDescription
from starui.registry.components.badge import Badge
from starui.registry.components.separator import Separator
from utils import auto_generate_page, with_code, Component, Prop, build_api_reference
from widgets.component_preview import ComponentPreview


# ============================================================================
# EXAMPLE FUNCTIONS (decorated with @with_code for markdown generation)
# ============================================================================

# Headings showcase
@with_code
def headings_showcase_example():
    return Div(
        Display("Display Heading"),
        H1("Heading 1"),
        H2("Heading 2"),
        H3("Heading 3"),
        H4("Heading 4"),
        H5("Heading 5"),
        H6("Heading 6"),
        cls="space-y-4"
    )


# Text variants
@with_code
def text_variants_example():
    return Div(
        Lead("This is lead text. It stands out with larger font size and muted color, perfect for introductions."),
        P("This is a regular paragraph. It contains the main body text with comfortable spacing and readability. Use it for most of your content."),
        Large("This is large text for emphasis."),
        Text("This is default body text using the Text component."),
        Small("This is small text for secondary information."),
        Muted("This is muted text for less important content."),
        cls="space-y-4 max-w-prose"
    )


# Blog post example
@with_code
def blog_post_example():
    return Card(
        CardContent(
            Div(
                Caption("Technology • 5 min read"),
                H1("The Future of Web Development"),
                Subtitle("Exploring emerging trends and technologies shaping the web"),
                Hr(),
                Lead("The web development landscape is evolving rapidly, with new frameworks, tools, and methodologies emerging constantly."),
                P("In recent years, we've witnessed a significant shift in how we build web applications. The rise of ",
                  Strong("component-based architectures"), ", ",
                  Strong("server-side rendering"), ", and ",
                  Strong("edge computing"), " has fundamentally changed our approach to web development."),
                H2("Key Trends to Watch", section=True),
                P("Several important trends are shaping the future of web development:"),
                List(
                    "AI-powered development tools",
                    "WebAssembly adoption",
                    "Progressive Web Apps (PWAs)",
                    "Serverless architectures",
                    "Micro-frontends"
                ),
                Blockquote("The best way to predict the future is to invent it. — Alan Kay"),
                P("As developers, we must stay adaptable and continue learning to remain relevant in this rapidly changing field."),
                cls="prose max-w-none"
            ),
            cls="py-8"
        ),
        cls="max-w-3xl"
    )


# Code documentation
@with_code
def code_documentation_example():
    return Card(
        CardHeader(
            CardTitle("API Reference"),
            CardDescription("Component usage documentation")
        ),
        CardContent(
            Div(
                H3("Installation"),
                P("Install the package using your preferred package manager:"),
                InlineCode("npm install @starui/components"),

                H3("Usage", cls="mt-6"),
                P("Import the ", InlineCode("Button"), " component and use it in your application:"),
                Div(
                    InlineCode("import { Button } from '@starui/components'"),
                    cls="p-3 bg-muted rounded-md font-mono text-sm"
                ),

                H3("Props", cls="mt-6"),
                P("The component accepts the following props:"),
                List(
                    Div(InlineCode("variant"), " - Visual style variant (default: 'default')"),
                    Div(InlineCode("size"), " - Button size (default: 'default')"),
                    Div(InlineCode("disabled"), " - Whether button is disabled (default: false)"),
                    ordered=False
                ),

                H3("Keyboard Shortcuts", cls="mt-6"),
                P("The following keyboard shortcuts are available:"),
                Div(
                    P(Kbd("⌘"), " + ", Kbd("K"), " - Open command palette"),
                    P(Kbd("⌘"), " + ", Kbd("Shift"), " + ", Kbd("P"), " - Open preferences"),
                    P(Kbd("Esc"), " - Close dialog"),
                    cls="space-y-2"
                ),
                cls="space-y-4"
            )
        ),
        cls="max-w-2xl"
    )


# Article with emphasis
@with_code
def text_emphasis_example():
    return Card(
        CardContent(
            Div(
                H2("Understanding ", Mark("Typography"), " in Design"),
                P("Typography is ", Em("more than just choosing fonts"), ". It's about creating ",
                  Strong("hierarchy"), ", improving ", Strong("readability"), ", and establishing ",
                  Strong("visual rhythm"), " in your designs."),

                H3("Why Typography Matters"),
                P("Good typography can ", Mark("make or break"), " a design. It affects:"),
                List(
                    Div(Strong("Readability"), " - How easily users can read your content"),
                    Div(Strong("Hierarchy"), " - How users navigate through information"),
                    Div(Strong("Mood"), " - The emotional response to your design"),
                    Div(Strong("Brand Identity"), " - How users perceive your brand"),
                    ordered=True
                ),

                Blockquote(
                    "Typography is the ", Em("craft"), " of endowing human language with a ",
                    Strong("durable visual form"), "."
                ),

                P("When choosing typography for your project, consider the ",
                  Mark("context"), ", ", Mark("audience"), ", and ", Mark("purpose"),
                  " of your content."),
                cls="prose max-w-none space-y-4"
            )
        ),
        cls="max-w-2xl"
    )


# Prose wrapper
@with_code
def prose_component_example():
    return Card(
        CardContent(
            Prose(
                H2("Using the Prose Component"),
                P("The ", InlineCode("Prose"), " component automatically styles its children with beautiful typography defaults. It's perfect for rendering markdown content or long-form articles."),
                H3("Features"),
                List(
                    "Automatic spacing between elements",
                    "Beautiful default styles",
                    "Dark mode support",
                    "Responsive font sizes"
                ),
                P("You can also control the size of the prose content:"),
                Div(
                    Badge("prose-sm", variant="outline", cls="mr-2"),
                    Badge("prose", variant="outline", cls="mr-2"),
                    Badge("prose-lg", variant="outline", cls="mr-2"),
                    Badge("prose-xl", variant="outline"),
                    cls="flex items-center"
                ),
                Blockquote("The Prose component makes your content look professional with minimal effort."),
                size="base"
            ),
            cls="py-4"
        ),
        cls="max-w-3xl"
    )


# Figure with caption
@with_code
def figures_captions_example():
    return Card(
        CardContent(
            Div(
                H2("Visual Content"),
                P("Images and figures can be enhanced with proper captions:"),
                Figure(
                    Div(
                        Icon("lucide:image", cls="h-48 w-full text-muted-foreground/20"),
                        cls="bg-muted rounded-md flex items-center justify-center"
                    ),
                    Figcaption("Figure 1: Example image with descriptive caption explaining the visual content")
                ),
                P("Captions provide context and improve accessibility for visual content."),
                Hr(),
                P("You can also use figures for code blocks, charts, or any content that benefits from a caption."),
                cls="space-y-4"
            )
        ),
        cls="max-w-2xl"
    )


# Complete article example
@with_code
def complete_article_example():
    return Card(
        CardContent(
            Prose(
                Caption("Tutorial • Advanced • 15 min read"),
                Display("Master Typography"),
                Subtitle("A comprehensive guide to beautiful text on the web"),

                Div(
                    Badge("Design", variant="secondary", cls="mr-2"),
                    Badge("Typography", variant="secondary", cls="mr-2"),
                    Badge("UI/UX", variant="secondary"),
                    cls="flex items-center my-4"
                ),

                Hr(),

                Lead("Typography is the foundation of great design. This guide will teach you everything you need to know about creating beautiful, readable text for the web."),

                H2("The Basics", section=True),
                P("Every great typographic system starts with a ", Strong("solid foundation"), ". This includes choosing the right ", Mark("typeface"), ", establishing a ", Mark("type scale"), ", and defining ", Mark("spacing rules"), "."),

                H3("1. Choose Your Typeface"),
                P("Select fonts that complement each other. A common approach is pairing a ", Em("serif"), " font for headings with a ", Em("sans-serif"), " for body text."),

                H3("2. Establish Hierarchy"),
                P("Use different sizes, weights, and styles to create visual hierarchy:"),
                List(
                    Div(Strong("Headlines"), " - Large, bold, attention-grabbing"),
                    Div(Strong("Subheadings"), " - Medium size, clear structure"),
                    Div(Strong("Body text"), " - Comfortable reading size"),
                    Div(Strong("Captions"), " - Small, supplementary information"),
                    ordered=True
                ),

                Blockquote("Good typography is invisible. Great typography is unforgettable."),

                H2("Advanced Techniques", section=True),
                P("Once you've mastered the basics, explore advanced techniques like ", InlineCode("variable fonts"), ", ", InlineCode("fluid typography"), ", and ", InlineCode("optical sizing"), "."),

                H3("Pro Tips"),
                List(
                    "Use a modular scale for consistent sizing",
                    "Maintain 45-75 characters per line for optimal readability",
                    "Adjust line-height based on font size and line length",
                    "Use proper kerning and letter-spacing",
                    "Test your typography on different devices"
                ),

                Hr(),

                P(Small("Last updated: December 2024 • Written by the StarUI Team")),

                size="lg"
            ),
            cls="py-8"
        ),
        cls="max-w-4xl"
    )


# ============================================================================
# MODULE-LEVEL DATA (for markdown API)
# ============================================================================

EXAMPLES_DATA = [
    {"title": "Headings", "description": "All heading levels from Display to H6", "code": headings_showcase_example.code},
    {"title": "Text Variants", "description": "Different text styles for various content types", "code": text_variants_example.code},
    {"title": "Blog Post", "description": "Complete blog post layout with typography", "code": blog_post_example.code},
    {"title": "Code Documentation", "description": "API reference with inline code and keyboard shortcuts", "code": code_documentation_example.code},
    {"title": "Text Emphasis", "description": "Using marks, emphasis, and strong text", "code": text_emphasis_example.code},
    {"title": "Prose Component", "description": "Automatic typography styling for long-form content", "code": prose_component_example.code},
    {"title": "Figures & Captions", "description": "Images and content with descriptive captions", "code": figures_captions_example.code},
    {"title": "Complete Article", "description": "Full article layout with all typography elements", "code": complete_article_example.code},
]

API_REFERENCE = build_api_reference(
    components=[
        Component("Headings", "Headings Display → H6. `H2(section=True)` draws a section divider."),
        Component("Text Components", "`P`, `Lead`, `Large`, `Small`, `Muted`, `Subtitle`, `Caption`, and `Text(variant='body'|'lead'|'large'|'small'|'muted')"),
        Component("Inline Elements", "`InlineCode`, `Kbd`, `Mark`, `Strong`, `Em` for inline emphasis and notation."),
        Component("Block Elements", "`Blockquote`, `List(ordered=True|False)`, `Hr`, `Figure`, `Figcaption`."),
        Component("Prose", "Typography wrapper to style content; supports sizes.",
            [Prop("size", "Literal['sm','base','lg','xl']", "Typography scale for prose content", "'base'")]),
    ]
)


def examples():
    """Generate all typography examples."""
    yield ComponentPreview(
        headings_showcase_example(),
        headings_showcase_example.code,
        title="Headings",
        description="All heading levels from Display to H6"
    )

    yield ComponentPreview(
        text_variants_example(),
        text_variants_example.code,
        title="Text Variants",
        description="Different text styles for various content types"
    )

    yield ComponentPreview(
        blog_post_example(),
        blog_post_example.code,
        title="Blog Post",
        description="Complete blog post layout with typography"
    )

    yield ComponentPreview(
        code_documentation_example(),
        code_documentation_example.code,
        title="Code Documentation",
        description="API reference with inline code and keyboard shortcuts"
    )

    yield ComponentPreview(
        text_emphasis_example(),
        text_emphasis_example.code,
        title="Text Emphasis",
        description="Using marks, emphasis, and strong text"
    )

    yield ComponentPreview(
        prose_component_example(),
        prose_component_example.code,
        title="Prose Component",
        description="Automatic typography styling for long-form content"
    )

    yield ComponentPreview(
        figures_captions_example(),
        figures_captions_example.code,
        title="Figures & Captions",
        description="Images and content with descriptive captions"
    )

    yield ComponentPreview(
        complete_article_example(),
        complete_article_example.code,
        title="Complete Article",
        description="Full article layout with all typography elements"
    )


def create_typography_docs():
    """Create typography documentation page using convention-based approach."""

    # Hero example
    @with_code
    def hero_typography_example():
        return Div(
            H1("Beautiful Typography"),
            Lead("Create stunning text layouts with our comprehensive typography system."),
            P("From headings to paragraphs, ", Strong("bold text"), " to ", Em("italics"), ", and everything in between. Our typography components provide ", Mark("consistent styling"), " across your entire application."),
            cls="space-y-4 max-w-prose"
        )

    hero_example = ComponentPreview(
        hero_typography_example(),
        hero_typography_example.code,
        copy_button=True
    )

    return auto_generate_page(
        TITLE,
        DESCRIPTION,
        list(examples()),
        cli_command="star add typography",
        api_reference=API_REFERENCE,
        hero_example=hero_example,
        component_slug="typography"
    )