"""
Typography component documentation — semantic text elements with consistent sizing and spacing.
"""

# Component metadata for auto-discovery
TITLE = "Typography"
DESCRIPTION = "Semantic heading, text, and inline elements with consistent sizing and spacing."
CATEGORY = "ui"
ORDER = 85
STATUS = "stable"

from starhtml import Div, Li
from starui.registry.components.typography import (
    Display, H1, H2, H3, H4,
    P, Lead, Large, Small, Muted, Caption,
    InlineCode, Blockquote, List, Prose,
    Kbd, Mark, Hr
)
from starui.registry.components.card import Card, CardContent
from starui.registry.components.badge import Badge
from utils import auto_generate_page, with_code, Component, Prop, build_api_reference


@with_code
def headings_scale_example():
    return Div(
        Div(Caption("Display"), Display("Sourdough", cls="mt-0"), cls="space-y-1"),
        Div(Caption("H1"), H1("The Beginner's Loaf", cls="mt-0"), cls="space-y-1"),
        Div(Caption("H2"), H2("Ingredients", cls="border-0 pb-0 mt-0"), cls="space-y-1"),
        Div(Caption("H3"), H3("Bulk Ferment", cls="mt-0"), cls="space-y-1"),
        Div(Caption("H4"), H4("Shaping Notes", cls="mt-0"), cls="space-y-1"),
        cls="space-y-6"
    )


@with_code
def text_variants_example():
    return Div(
        Div(Caption("Lead"), Lead("The longest-running experiment in physics began in 1927, when Professor Parnell heated a lump of pitch and poured it into a funnel."), cls="space-y-1"),
        Div(Caption("P"), P("Nine drops have fallen since then. The eighth drop fell in November 2000, but nobody saw it happen — the webcam installed to catch it had suffered an outage twenty minutes earlier."), cls="space-y-1"),
        Div(Caption("Large"), Large("One drop per decade."), cls="space-y-1"),
        Div(Caption("Small"), Small("University of Queensland · Est. 1927"), cls="space-y-1"),
        Div(Caption("Muted"), Muted("The ninth drop fell on 24 April 2014."), cls="space-y-1"),
        Div(Caption("Caption"), Caption("Fluid Dynamics"), cls="space-y-1"),
        cls="space-y-6 max-w-prose [&_p]:mt-0"
    )


@with_code
def inline_elements_example():
    return Div(
        P("Install the package with ", InlineCode("pip install starui"), " and import what you need."),
        P("Press ", Kbd("⌘"), " + ", Kbd("K"), " to open the command palette, or ", Kbd("Esc"), " to close it."),
        P("The search index will ", Mark("highlight matching terms"), " across all results so you can scan quickly."),
        cls="space-y-2 max-w-prose"
    )


@with_code
def blockquote_list_example():
    return Div(
        Blockquote(
            P("After all, all he did was string together a bunch of alien quotations and was that any way to write a story?"),
            Small("— James Michener", cls="not-italic block mt-2"),
        ),
        List(
            "Preheat the oven to 260\u00b0C with the Dutch oven inside",
            "Score the dough with a razor blade or lame",
            "Bake covered for 20 minutes, then remove the lid",
            "Continue baking until the crust is deep brown, about 25 more minutes",
            ordered=True,
        ),
        List(
            "Bread flour (12–13% protein)",
            "Fine sea salt",
            "Filtered water at 30\u00b0C",
        ),
        cls="max-w-prose"
    )


@with_code
def changelog_example():
    return Card(
        CardContent(
            Div(
                Caption("December 15, 2025"),
                H2("v2.4.0", cls="border-0 pb-0"),
                Lead("New calendar component and date picker improvements."),
                H3("Added", cls="mt-4"),
                List(
                    Li(InlineCode("Calendar"), " — standalone month-view date picker"),
                    Li(InlineCode("DatePicker"), " now supports range selection"),
                    Li("Keyboard navigation for all date components"),
                    cls="my-0",
                ),
                H3("Fixed", cls="mt-4"),
                List(
                    Li("Popover positioning on scroll (", InlineCode("#412"), ")"),
                    Li("Select dropdown closing on outside click"),
                    cls="my-0",
                ),
                Hr(cls="my-4"),
                Muted("Full changelog on GitHub"),
                cls="max-w-2xl space-y-2"
            ),
            cls="pt-6"
        ),
    )


@with_code
def settings_section_example():
    return Div(
        Div(
            H3("Notifications"),
            Muted("Choose which events trigger email or push notifications."),
            cls="space-y-1"
        ),
        Hr(cls="my-4"),
        Div(
            H4("Email Digest"),
            Muted("Receive a daily summary of activity in your workspace."),
            cls="space-y-1"
        ),
        Div(
            H4("Mentions"),
            Muted("Get notified when someone mentions you in a comment."),
            cls="space-y-1"
        ),
        Div(
            H4("Security Alerts"),
            Muted("Immediate notification for login attempts and permission changes."),
            cls="space-y-1"
        ),
        cls="max-w-lg space-y-6"
    )


@with_code
def prose_sizes_example():
    return Div(
        Div(
            Badge("prose-sm", variant="outline"),
            Prose(
                H3("Tartine Method"),
                P("Mix 200g leaven with 700g water. Add 900g bread flour and 100g whole wheat. Autolyse 25\u201340 minutes, then add 20g salt with 50g warm water."),
                size="sm",
            ),
            cls="space-y-2"
        ),
        Div(
            Badge("prose (default)", variant="outline"),
            Prose(
                H3("Why Autolyse Matters"),
                P("During autolyse, flour absorbs water and enzymes begin breaking down starch into sugar. Gluten strands start forming on their own, which means less kneading later and a more extensible dough."),
                P("The window is 25\u201340 minutes. Shorter and you miss the benefit; longer and the dough starts to degrade."),
                size="base",
            ),
            cls="space-y-2"
        ),
        Div(
            Badge("prose-lg", variant="outline"),
            Prose(
                H3("The Crumb"),
                P("An open, irregular crumb comes from high hydration, gentle handling, and a strong starter. If your crumb is tight and even, try increasing hydration by 5% and using coil folds instead of stretch-and-folds."),
                size="lg",
            ),
            cls="space-y-2"
        ),
        cls="space-y-8 max-w-2xl"
    )


@with_code
def article_opening_example():
    return Div(
        Caption("Field Notes \u00b7 March 2026"),
        H2("Scoring Patterns and Oven Spring", cls="border-0 pb-0"),
        Lead("How blade angle, depth, and steam timing affect the final shape of your loaf."),
        Hr(cls="my-4"),
        P("The score is not decorative. It controls where steam escapes during the first ten minutes of baking, and that escape path determines the shape of the ear and the overall rise. A shallow score at 30\u00b0 produces a wide, flat ear. A deep score at 90\u00b0 splits the loaf open symmetrically."),
        P("Most bakers score too timidly. The blade should pass through the skin of the dough in a single, confident stroke \u2014 hesitation creates drag, which tears rather than cuts."),
        Small("8 min read"),
        cls="max-w-2xl"
    )


EXAMPLES_DATA = [
    {"fn": headings_scale_example, "title": "Heading Scale", "description": "Display through H4 — each level uses the heading_variants CVA with responsive sizing"},
    {"fn": text_variants_example, "title": "Text Variants", "description": "Lead, P, Large, Small, Muted, and Caption — each maps to a text_variants CVA variant"},
    {"fn": inline_elements_example, "title": "Inline Elements", "description": "InlineCode, Kbd, and Mark for code references, keyboard shortcuts, and highlights"},
    {"fn": blockquote_list_example, "title": "Blockquote & Lists", "description": "Blockquote for callouts — List auto-wraps children in li elements and supports ordered mode"},
    {"fn": changelog_example, "title": "Changelog", "description": "Real-world composition — Caption, headings, InlineCode, and List for release notes in a Card"},
    {"fn": settings_section_example, "title": "Settings Section", "description": "H3/H4 with Muted descriptions and Hr dividers — typical app settings layout"},
    {"fn": prose_sizes_example, "title": "Prose Sizes", "description": "Prose wraps content with @tailwindcss/typography — sm, base, and lg for comparison"},
    {"fn": article_opening_example, "title": "Article Opening", "description": "Caption, H2, Lead, Hr, P, and Small composed as a natural article header with body text"},
]

API_REFERENCE = build_api_reference(
    main_props=[
        Prop("cls", "str", "Additional CSS classes merged via cn()", "''"),
    ],
    components=[
        Component("Display", "Renders <h1> with responsive text-4xl/5xl/6xl. For hero headings and page titles."),
        Component("H1", "Renders <h1> with text-3xl/4xl/5xl font-extrabold. Primary page heading."),
        Component("H2", "Renders <h2> with border-b by default. Section headings.",
            [Prop("cls", "str", "Override with cls='border-0 pb-0' to remove border", "''")]),
        Component("H3", "Renders <h3> with text-2xl font-semibold."),
        Component("H4", "Renders <h4> with text-xl font-semibold."),
        Component("P", "Renders <p> with leading-7 and [&:not(:first-child)]:mt-6 spacing."),
        Component("Lead", "Renders <p> with text-xl text-muted-foreground. For introductory paragraphs."),
        Component("Large", "Renders <div> with text-lg font-semibold. Inline callouts."),
        Component("Small", "Renders <small> with text-sm font-medium. Metadata and fine print."),
        Component("Muted", "Renders <p> with text-sm text-muted-foreground. Secondary text."),
        Component("Caption", "Renders <div> with uppercase tracking-wider font-medium. Category labels and eyebrows."),
        Component("InlineCode", "Renders <code> with bg-muted rounded mono styling."),
        Component("Blockquote", "Renders <blockquote> with border-l-2 italic styling."),
        Component("List", "Renders <ul> or <ol>. Auto-wraps non-li children in <li> elements.",
            [Prop("ordered", "bool", "Use <ol> with decimal markers instead of <ul> disc markers", "False")]),
        Component("Prose", "Renders <div> with @tailwindcss/typography classes. For markdown/long-form content.",
            [Prop("size", "Literal['sm','base','lg','xl']", "Typography scale", "'base'")]),
        Component("Kbd", "Renders <kbd> with bordered badge styling for keyboard shortcuts."),
        Component("Mark", "Renders <mark> with primary-tinted highlight. Same hue in light and dark mode."),
        Component("Hr", "Renders <hr> with my-8 border-t border-border. Pass cls='my-4' for tighter spacing."),
        Component("Figure", "Renders <figure> with my-8 and space-y-3 for contained content."),
        Component("Figcaption", "Renders <figcaption> with centered italic muted text."),
    ]
)


def create_typography_docs():
    """Create typography documentation page using convention-based approach."""
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)
