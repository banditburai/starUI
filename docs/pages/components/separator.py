"""
Separator component documentation - Visual dividers for content organization.
Clean, minimal dividers that help structure layouts.
"""

# Component metadata for auto-discovery
TITLE = "Separator"
DESCRIPTION = "Visually or semantically separates content with horizontal or vertical dividers."
CATEGORY = "ui"
ORDER = 25
STATUS = "stable"

from starhtml import Div, P, H3, H4, Span, Article, Header, Icon
from starhtml.datastar import ds_signals, ds_on_click, ds_text, value
from starui.registry.components.separator import Separator
from starui.registry.components.button import Button
from starui.registry.components.badge import Badge
from utils import with_code, Component, Prop, build_api_reference, auto_generate_page
from widgets.component_preview import ComponentPreview


def examples():
    """Generate separator examples using ComponentPreview with tabs."""
    
    # Card content separation
    @with_code
    def card_content_separation_example():
        return Div(
            Div(
                Div(
                    Div(cls="w-12 h-12 bg-gradient-to-r from-purple-400 to-pink-400 rounded-full"),
                    Div(
                        H4("John Doe", cls="font-medium"),
                        P("Software Engineer", cls="text-sm text-muted-foreground"),
                        cls="ml-3"
                    ),
                    cls="flex items-center"
                ),
                Separator(cls="my-4"),
                Div(
                    P("Bio", cls="text-sm font-medium mb-2"),
                    P("Passionate developer with 5+ years of experience building web applications.", cls="text-sm text-muted-foreground"),
                    cls="mb-4"
                ),
                Separator(cls="my-4"),
                Div(
                    P("Contact", cls="text-sm font-medium mb-2"),
                    P("john.doe@example.com", cls="text-sm text-muted-foreground"),
                    cls=""
                ),
                cls="p-6 border rounded-lg"
            ),
            cls="max-w-sm mx-auto"
        )

    yield ComponentPreview(
        card_content_separation_example(),
        card_content_separation_example.code,
        title="Card Content Separation",
        description="Use horizontal separators to divide sections within cards or panels"
    )
    
    # Content sections with clear divisions
    @with_code
    def content_section_dividers_example():
        return Div(
            Div(
                Div(
                    H3("Getting Started", cls="text-lg font-semibold mb-2"),
                    P("Learn the basics of using our platform with this comprehensive guide.", cls="text-sm text-muted-foreground mb-4"),
                ),
                Separator(cls="my-6"),
                Div(
                    H3("Key Features", cls="text-lg font-semibold mb-2"),
                    P("Discover the powerful features that make our platform unique.", cls="text-sm text-muted-foreground mb-4"),
                ),
                Separator(cls="my-6"),
                Div(
                    H3("Additional Resources", cls="text-lg font-semibold mb-2"),
                    P("Find helpful documentation, tutorials, and community support.", cls="text-sm text-muted-foreground"),
                ),
                cls="max-w-2xl p-6 border rounded-lg"
            ),
            cls=""
        )

    yield ComponentPreview(
        content_section_dividers_example(),
        content_section_dividers_example.code,
        title="Content Section Dividers",
        description="Organize content areas with clear visual separation"
    )
    
    # Vertical separators in toolbars
    @with_code
    def toolbar_dividers_example():
        return Div(
            Div(
                Button(Icon("lucide:bold", cls="w-4 h-4"), variant="ghost", size="sm"),
                Button(Icon("lucide:italic", cls="w-4 h-4"), variant="ghost", size="sm"),
                Button(Icon("lucide:underline", cls="w-4 h-4"), variant="ghost", size="sm"),
                Separator(orientation="vertical", cls="mx-2 h-6"),
                Button(Icon("lucide:align-left", cls="w-4 h-4"), variant="ghost", size="sm"),
                Button(Icon("lucide:align-center", cls="w-4 h-4"), variant="ghost", size="sm"),
                Button(Icon("lucide:align-right", cls="w-4 h-4"), variant="ghost", size="sm"),
                Separator(orientation="vertical", cls="mx-2 h-6"),
                Button(Icon("lucide:list", cls="w-4 h-4"), variant="ghost", size="sm"),
                Button(Icon("lucide:list-ordered", cls="w-4 h-4"), variant="ghost", size="sm"),
                cls="flex items-center p-2 border rounded-lg"
            ),
            cls="flex justify-center"
        )

    yield ComponentPreview(
        toolbar_dividers_example(),
        toolbar_dividers_example.code,
        title="Toolbar Dividers",
        description="Use vertical separators to group related actions in toolbars"
    )
    
    # Breadcrumb separators
    @with_code
    def breadcrumb_navigation_example():
        return Div(
            Div(
                Span("Home", cls="text-sm text-muted-foreground cursor-pointer hover:text-foreground"),
                Separator(orientation="vertical", cls="mx-2 h-4"),
                Span("Products", cls="text-sm text-muted-foreground cursor-pointer hover:text-foreground"),
                Separator(orientation="vertical", cls="mx-2 h-4"),
                Span("Electronics", cls="text-sm text-muted-foreground cursor-pointer hover:text-foreground"),
                Separator(orientation="vertical", cls="mx-2 h-4"),
                Span("Laptops", cls="text-sm font-medium"),
                cls="flex items-center"
            ),
            cls="p-4"
        )

    yield ComponentPreview(
        breadcrumb_navigation_example(),
        breadcrumb_navigation_example.code,
        title="Breadcrumb Navigation",
        description="Create clean breadcrumb trails with vertical separators"
    )
    
    # Stats dashboard with separators
    @with_code
    def dashboard_stats_example():
        return Div(
            Div(
                Div(
                    P("Total Revenue", cls="text-sm text-muted-foreground"),
                    P("$45,231.89", cls="text-2xl font-bold"),
                    P("+20.1% from last month", cls="text-sm text-green-600"),
                    cls="text-center"
                ),
                Separator(orientation="vertical", cls="mx-8 h-16"),
                Div(
                    P("Subscriptions", cls="text-sm text-muted-foreground"),
                    P("+2350", cls="text-2xl font-bold"),
                    P("+180.1% from last month", cls="text-sm text-green-600"),
                    cls="text-center"
                ),
                Separator(orientation="vertical", cls="mx-8 h-16"),
                Div(
                    P("Sales", cls="text-sm text-muted-foreground"),
                    P("+12,234", cls="text-2xl font-bold"),
                    P("+19% from last month", cls="text-sm text-green-600"),
                    cls="text-center"
                ),
                cls="flex items-center justify-center p-6 border rounded-lg"
            ),
            cls=""
        )

    yield ComponentPreview(
        dashboard_stats_example(),
        dashboard_stats_example.code,
        title="Dashboard Stats",
        description="Separate key metrics with vertical dividers for clear visual hierarchy"
    )
    
    # Complex layout with mixed orientations
    @with_code
    def article_layout_example():
        return Div(
            Article(
                Header(
                    H3("Getting Started with StarUI", cls="text-xl font-bold mb-2"),
                    P("Learn how to build beautiful user interfaces", cls="text-muted-foreground"),
                    Div(
                        Badge("Tutorial"),
                        Separator(orientation="vertical", cls="mx-2 h-4"),
                        Badge("Beginner", variant="secondary"),
                        Separator(orientation="vertical", cls="mx-2 h-4"),  
                        Span("5 min read", cls="text-sm text-muted-foreground"),
                        cls="flex items-center mt-3"
                    ),
                    cls="mb-6"
                ),
                Separator(cls="mb-6"),
                Div(
                    H4("Introduction", cls="font-semibold mb-3"),
                    P("StarUI is a modern component library that makes it easy to build beautiful, accessible user interfaces.", cls="text-sm text-muted-foreground leading-relaxed"),
                    cls="mb-6"
                ),
                Separator(cls="mb-6"),
                Div(
                    H4("Quick Start", cls="font-semibold mb-3"),
                    P("Get up and running in minutes with our simple installation process.", cls="text-sm text-muted-foreground leading-relaxed"),
                    cls="mb-6"
                ),
                Separator(cls="mb-6"),
                Div(
                    Span("Published on March 15, 2024", cls="text-xs text-muted-foreground"),
                    Separator(orientation="vertical", cls="mx-3 h-6"),
                    Span("Updated March 20, 2024", cls="text-xs text-muted-foreground"),
                    cls="flex items-center mt-auto"
                ),
                cls="max-w-2xl p-6 border rounded-lg flex flex-col min-h-[300px]"
            ),
            cls=""
        )

    yield ComponentPreview(
        article_layout_example(),
        article_layout_example.code,
        title="Article Layout",
        description="Complex content layouts using both horizontal and vertical separators"
    )
    
    # Custom styled separators
    @with_code
    def custom_styling_example():
        return Div(
            H4("Custom Separator Styles", cls="text-center mb-6"),
            Div(
                P("Default separator", cls="text-center text-sm text-muted-foreground mb-2"),
                Separator(),
                cls="mb-6"
            ),
            Div(
                P("Thick separator", cls="text-center text-sm text-muted-foreground mb-2"),
                Separator(cls="h-0.5 bg-muted-foreground"),
                cls="mb-6"
            ),
            Div(
                P("Colored separator", cls="text-center text-sm text-muted-foreground mb-2"),
                Separator(cls="bg-blue-500"),
                cls="mb-6"
            ),
            Div(
                P("Dashed separator", cls="text-center text-sm text-muted-foreground mb-2"),
                Separator(cls="border-t border-dashed border-muted-foreground bg-transparent h-0"),
                cls="mb-6"
            ),
            Div(
                P("Gradient separator", cls="text-center text-sm text-muted-foreground mb-2"),
                Separator(cls="bg-gradient-to-r from-transparent via-muted-foreground to-transparent"),
                cls=""
            ),
            cls="max-w-md mx-auto p-6 border rounded-lg"
        )

    yield ComponentPreview(
        custom_styling_example(),
        custom_styling_example.code,
        title="Custom Styling",
        description="Customize separators with different styles, colors, and effects"
    )


def create_separator_docs():
    """Create separator documentation page using convention-based approach."""
    
    # Hero example showcasing both orientations
    @with_code
    def hero_separator_example():
        return Div(
            Div(
                P("Content above", cls="text-center py-4"),
                Separator(),
                P("Content below", cls="text-center py-4"),
                cls="border rounded-lg p-4 mr-4"
            ),
            Div(
                P("Left", cls="px-4 text-center"),
                Separator(orientation="vertical", cls="h-16"),
                P("Center", cls="px-4 text-center"),
                Separator(orientation="vertical", cls="h-16"),
                P("Right", cls="px-4 text-center"),
                cls="flex items-center border rounded-lg p-4"
            ),
            cls="flex flex-col sm:flex-row gap-4 items-center"
        )

    hero_example = ComponentPreview(
        hero_separator_example(),
        hero_separator_example.code,
        copy_button=True
    )
    
    # For Separator, users need the primary props that affect layout and accessibility.
    api_reference = build_api_reference(
        main_props=[
            Prop("orientation", "Literal['horizontal', 'vertical']", "Orientation of the separator", "'horizontal'"),
            Prop("decorative", "bool", "If False, adds role and aria-orientation for accessibility", "True"),
            Prop("cls", "str", "Additional CSS classes", "''"),
            Prop("class_name", "str", "Alternative CSS classes prop (merged with cls)", "''"),
        ]
    )
    
    return auto_generate_page(
        TITLE,
        DESCRIPTION,
        list(examples()),
        cli_command="star add separator",
        api_reference=api_reference,
        hero_example=hero_example,
        component_slug="separator"
    )