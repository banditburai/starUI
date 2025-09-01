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

from starhtml import Div, Icon, Span, Img
from starhtml.datastar import ds_signals
from starui.registry.components.typography import (
    Display, H1, H2, H3, H4, H5, H6,
    P, Lead, Large, Small, Muted, Subtitle, Caption,
    Text, InlineCode, Blockquote, List, Prose,
    Kbd, Mark, Strong, Em, Hr, Figure, Figcaption
)
from starui.registry.components.card import Card, CardHeader, CardContent, CardTitle, CardDescription
from starui.registry.components.badge import Badge
from starui.registry.components.separator import Separator
from utils import auto_generate_page
from widgets.component_preview import ComponentPreview


def examples():
    """Generate typography examples using ComponentPreview with tabs."""
    
    # Headings showcase
    yield ComponentPreview(
        Div(
            Display("Display Heading"),
            H1("Heading 1"),
            H2("Heading 2"),
            H3("Heading 3"),
            H4("Heading 4"),
            H5("Heading 5"),
            H6("Heading 6"),
            cls="space-y-4"
        ),
        '''Display("Display Heading")
H1("Heading 1")
H2("Heading 2")
H3("Heading 3")
H4("Heading 4")
H5("Heading 5")
H6("Heading 6")''',
        title="Headings",
        description="All heading levels from Display to H6"
    )
    
    # Text variants
    yield ComponentPreview(
        Div(
            Lead("This is lead text. It stands out with larger font size and muted color, perfect for introductions."),
            P("This is a regular paragraph. It contains the main body text with comfortable spacing and readability. Use it for most of your content."),
            Large("This is large text for emphasis."),
            Text("This is default body text using the Text component."),
            Small("This is small text for secondary information."),
            Muted("This is muted text for less important content."),
            cls="space-y-4 max-w-prose"
        ),
        '''Lead("This is lead text...")
P("This is a regular paragraph...")
Large("This is large text...")
Text("This is default body text...")
Small("This is small text...")
Muted("This is muted text...")''',
        title="Text Variants",
        description="Different text styles for various content types"
    )
    
    # Blog post example
    yield ComponentPreview(
        Card(
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
        ),
        '''Card(
    CardContent(
        Caption("Technology • 5 min read"),
        H1("The Future of Web Development"),
        Subtitle("Exploring emerging trends..."),
        Hr(),
        Lead("The web development landscape..."),
        P("In recent years...", Strong("component-based"), "..."),
        H2("Key Trends to Watch", section=True),
        List(
            "AI-powered tools",
            "WebAssembly",
            "PWAs"
        ),
        Blockquote("The best way to predict...")
    )
)''',
        title="Blog Post",
        description="Complete blog post layout with typography"
    )
    
    # Code documentation
    yield ComponentPreview(
        Card(
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
        ),
        '''Card(
    CardContent(
        H3("Installation"),
        P("Install the package:"),
        InlineCode("npm install @starui/components"),
        
        H3("Props"),
        List(
            Div(InlineCode("variant"), " - Visual style"),
            Div(InlineCode("size"), " - Button size"),
        ),
        
        H3("Keyboard Shortcuts"),
        P(Kbd("⌘"), " + ", Kbd("K"), " - Open command")
    )
)''',
        title="Code Documentation",
        description="API reference with inline code and keyboard shortcuts"
    )
    
    # Article with emphasis
    yield ComponentPreview(
        Card(
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
        ),
        '''H2("Understanding ", Mark("Typography"), " in Design")
P("Typography is ", Em("more than just choosing fonts"), "...")

P("Good typography can ", Mark("make or break"), " a design.")
List(
    Div(Strong("Readability"), " - How easily..."),
    Div(Strong("Hierarchy"), " - How users..."),
    ordered=True
)

Blockquote(
    "Typography is the ", Em("craft"), " of..."
)''',
        title="Text Emphasis",
        description="Using marks, emphasis, and strong text"
    )
    
    # Prose wrapper
    yield ComponentPreview(
        Card(
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
        ),
        '''Prose(
    H2("Using the Prose Component"),
    P("The ", InlineCode("Prose"), " component..."),
    H3("Features"),
    List(
        "Automatic spacing",
        "Beautiful defaults",
        "Dark mode support"
    ),
    Blockquote("Makes content look professional..."),
    size="base"  // or "sm", "lg", "xl"
)''',
        title="Prose Component",
        description="Automatic typography styling for long-form content"
    )
    
    # Figure with caption
    yield ComponentPreview(
        Card(
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
        ),
        '''Figure(
    Div(
        Icon("lucide:image", cls="h-48 w-full"),
        cls="bg-muted rounded-md"
    ),
    Figcaption("Figure 1: Example image with caption")
)''',
        title="Figures & Captions",
        description="Images and content with descriptive captions"
    )
    
    # Complete article example
    yield ComponentPreview(
        Card(
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
        ),
        '''Prose(
    Caption("Tutorial • Advanced • 15 min"),
    Display("Master Typography"),
    Subtitle("A comprehensive guide..."),
    
    Lead("Typography is the foundation..."),
    
    H2("The Basics", section=True),
    P("Every great system starts with..."),
    
    List(
        "Headlines - Large, bold",
        "Body text - Comfortable",
        ordered=True
    ),
    
    Blockquote("Good typography is invisible..."),
    
    Hr(),
    
    size="lg"  // Large prose size
)''',
        title="Complete Article",
        description="Full article layout with all typography elements"
    )


def create_typography_docs():
    """Create typography documentation page using convention-based approach."""
    
    api_reference = {
        "components": [
            {
                "name": "Headings",
                "description": "Heading components from Display to H6",
                "items": [
                    {"name": "Display", "description": "Extra large display heading (6xl)"},
                    {"name": "H1", "description": "Primary heading (4xl)"},
                    {"name": "H2", "description": "Secondary heading (3xl) with optional section border"},
                    {"name": "H3", "description": "Tertiary heading (2xl)"},
                    {"name": "H4", "description": "Quaternary heading (xl)"},
                    {"name": "H5", "description": "Quinary heading (lg)"},
                    {"name": "H6", "description": "Senary heading (base)"}
                ]
            },
            {
                "name": "Text Components",
                "description": "Various text styles and components",
                "items": [
                    {"name": "P", "description": "Standard paragraph with comfortable spacing"},
                    {"name": "Lead", "description": "Larger, muted text for introductions"},
                    {"name": "Large", "description": "Large emphasized text"},
                    {"name": "Small", "description": "Small text for secondary information"},
                    {"name": "Muted", "description": "Muted color text"},
                    {"name": "Subtitle", "description": "Subtitle text for headings"},
                    {"name": "Caption", "description": "Small uppercase caption text"},
                    {"name": "Text", "description": "Generic text with variant prop"}
                ]
            },
            {
                "name": "Inline Elements",
                "description": "Inline text formatting components",
                "items": [
                    {"name": "InlineCode", "description": "Inline code snippets"},
                    {"name": "Kbd", "description": "Keyboard key representation"},
                    {"name": "Mark", "description": "Highlighted/marked text"},
                    {"name": "Strong", "description": "Bold/strong emphasis"},
                    {"name": "Em", "description": "Italic/emphasis"}
                ]
            },
            {
                "name": "Block Elements",
                "description": "Block-level typography components",
                "items": [
                    {"name": "Blockquote", "description": "Quoted text blocks"},
                    {"name": "List", "description": "Ordered or unordered lists"},
                    {"name": "Hr", "description": "Horizontal rule/separator"},
                    {"name": "Figure", "description": "Figure container"},
                    {"name": "Figcaption", "description": "Figure caption"}
                ]
            },
            {
                "name": "Prose",
                "description": "Automatic typography styling wrapper",
                "props": [
                    {
                        "name": "size",
                        "type": "Literal['sm', 'base', 'lg', 'xl']",
                        "default": "'base'",
                        "description": "Prose content size"
                    }
                ]
            }
        ]
    }
    
    # Hero example
    hero_example = ComponentPreview(
        Div(
            H1("Beautiful Typography"),
            Lead("Create stunning text layouts with our comprehensive typography system."),
            P("From headings to paragraphs, ", Strong("bold text"), " to ", Em("italics"), ", and everything in between. Our typography components provide ", Mark("consistent styling"), " across your entire application."),
            cls="space-y-4 max-w-prose"
        ),
        '''H1("Beautiful Typography")
Lead("Create stunning text layouts...")
P(
    "From headings to paragraphs, ",
    Strong("bold text"),
    " to ",
    Em("italics"),
    ", and everything in between."
)''',
        copy_button=True
    )
    
    return auto_generate_page(
        TITLE,
        DESCRIPTION,
        list(examples()),
        cli_command="star add typography",
        api_reference=api_reference,
        hero_example=hero_example,
        component_slug="typography"
    )