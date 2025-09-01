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
from widgets.component_preview import ComponentPreview


def examples():
    """Generate separator examples using ComponentPreview with tabs."""
    
    # Card content separation
    yield ComponentPreview(
        Div(
            # User profile card
            Div(
                Div(
                    Div("Profile", cls="w-12 h-12 bg-primary rounded-full flex items-center justify-center text-primary-foreground font-semibold"),
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
                    P("Passionate developer with 5+ years of experience building web applications.", 
                      cls="text-sm text-muted-foreground"),
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
        ),
        '''from starui.registry.components.separator import Separator
from starhtml import Div, H4, P

Div(
    # Profile header
    Div("Profile info here"),
    Separator(cls="my-4"),
    # Bio section  
    Div("Bio content here"),
    Separator(cls="my-4"),
    # Contact section
    Div("Contact info here"),
    cls="p-6 border rounded-lg"
)''',
        title="Card Content Separation",
        description="Use horizontal separators to divide sections within cards or panels"
    )
    
    # Menu and navigation
    yield ComponentPreview(
        Div(
            # Sidebar menu
            Div(
                H3("Navigation", cls="text-sm font-semibold mb-3"),
                Div(
                    P("Dashboard", cls="p-2 hover:bg-muted rounded cursor-pointer text-sm"),
                    P("Analytics", cls="p-2 hover:bg-muted rounded cursor-pointer text-sm"),
                    P("Reports", cls="p-2 hover:bg-muted rounded cursor-pointer text-sm"),
                ),
                Separator(cls="my-4"),
                H3("Settings", cls="text-sm font-semibold mb-3"),
                Div(
                    P("Profile", cls="p-2 hover:bg-muted rounded cursor-pointer text-sm"),
                    P("Preferences", cls="p-2 hover:bg-muted rounded cursor-pointer text-sm"),
                    P("Security", cls="p-2 hover:bg-muted rounded cursor-pointer text-sm"),
                ),
                Separator(cls="my-4"),
                H3("Support", cls="text-sm font-semibold mb-3"),
                Div(
                    P("Help Center", cls="p-2 hover:bg-muted rounded cursor-pointer text-sm"),
                    P("Contact", cls="p-2 hover:bg-muted rounded cursor-pointer text-sm"),
                ),
                cls="w-48 p-4 border rounded-lg"
            ),
            cls=""
        ),
        '''from starui.registry.components.separator import Separator
from starhtml import Div, H3, P

Div(
    H3("Navigation", cls="text-sm font-semibold mb-3"),
    Div("Dashboard", "Analytics", "Reports"),
    
    Separator(cls="my-4"),
    
    H3("Settings", cls="text-sm font-semibold mb-3"), 
    Div("Profile", "Preferences", "Security"),
    
    Separator(cls="my-4"),
    
    H3("Support", cls="text-sm font-semibold mb-3"),
    Div("Help Center", "Contact"),
    cls="w-48 p-4 border rounded-lg"
)''',
        title="Menu Section Dividers",
        description="Organize navigation menus with clear section separators"
    )
    
    # Vertical separators in toolbars
    yield ComponentPreview(
        Div(
            # Toolbar with vertical separators
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
        ),
        '''from starui.registry.components.separator import Separator
from starui.registry.components.button import Button
from starhtml import Icon, Div

Div(
    # Text formatting
    Button(Icon("lucide:bold"), variant="ghost", size="sm"),
    Button(Icon("lucide:italic"), variant="ghost", size="sm"),
    Button(Icon("lucide:underline"), variant="ghost", size="sm"),
    
    Separator(orientation="vertical", cls="mx-2 h-6"),
    
    # Alignment
    Button(Icon("lucide:align-left"), variant="ghost", size="sm"),
    Button(Icon("lucide:align-center"), variant="ghost", size="sm"),
    Button(Icon("lucide:align-right"), variant="ghost", size="sm"),
    
    Separator(orientation="vertical", cls="mx-2 h-6"),
    
    # Lists
    Button(Icon("lucide:list"), variant="ghost", size="sm"),
    Button(Icon("lucide:list-ordered"), variant="ghost", size="sm"),
    
    cls="flex items-center p-2 border rounded-lg"
)''',
        title="Toolbar Dividers",
        description="Use vertical separators to group related actions in toolbars"
    )
    
    # Breadcrumb separators
    yield ComponentPreview(
        Div(
            # Breadcrumb navigation
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
        ),
        '''from starui.registry.components.separator import Separator
from starhtml import Div, Span

Div(
    Span("Home", cls="text-sm text-muted-foreground cursor-pointer hover:text-foreground"),
    Separator(orientation="vertical", cls="mx-2 h-4"),
    Span("Products", cls="text-sm text-muted-foreground cursor-pointer hover:text-foreground"),
    Separator(orientation="vertical", cls="mx-2 h-4"),
    Span("Electronics", cls="text-sm text-muted-foreground cursor-pointer hover:text-foreground"),
    Separator(orientation="vertical", cls="mx-2 h-4"),
    Span("Laptops", cls="text-sm font-medium"),
    cls="flex items-center"
)''',
        title="Breadcrumb Navigation",
        description="Create clean breadcrumb trails with vertical separators"
    )
    
    # Stats dashboard with separators
    yield ComponentPreview(
        Div(
            # Stats grid with separators
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
        ),
        '''from starui.registry.components.separator import Separator
from starhtml import Div, P

Div(
    # Revenue stat
    Div(
        P("Total Revenue", cls="text-sm text-muted-foreground"),
        P("$45,231.89", cls="text-2xl font-bold"),
        P("+20.1% from last month", cls="text-sm text-green-600"),
        cls="text-center"
    ),
    
    Separator(orientation="vertical", cls="mx-8 h-16"),
    
    # Subscriptions stat
    Div(
        P("Subscriptions", cls="text-sm text-muted-foreground"),
        P("+2350", cls="text-2xl font-bold"),
        P("+180.1% from last month", cls="text-sm text-green-600"),
        cls="text-center"
    ),
    
    Separator(orientation="vertical", cls="mx-8 h-16"),
    
    # Sales stat
    Div(
        P("Sales", cls="text-sm text-muted-foreground"),
        P("+12,234", cls="text-2xl font-bold"),
        P("+19% from last month", cls="text-sm text-green-600"),
        cls="text-center"
    ),
    
    cls="flex items-center justify-center p-6 border rounded-lg"
)''',
        title="Dashboard Stats",
        description="Separate key metrics with vertical dividers for clear visual hierarchy"
    )
    
    # Complex layout with mixed orientations
    yield ComponentPreview(
        Div(
            # Article with multiple sections
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
                    P("StarUI is a modern component library that makes it easy to build beautiful, accessible user interfaces.", 
                      cls="text-sm text-muted-foreground leading-relaxed"),
                    cls="mb-6"
                ),
                
                Separator(cls="mb-6"),
                
                Div(
                    H4("Quick Start", cls="font-semibold mb-3"),
                    P("Get up and running in minutes with our simple installation process.", 
                      cls="text-sm text-muted-foreground leading-relaxed"),
                    cls="mb-6"
                ),
                
                Separator(cls="mb-6"),
                
                Div(
                    P("Published on March 15, 2024", cls="text-xs text-muted-foreground"),
                    Separator(orientation="vertical", cls="mx-2 h-3"),
                    P("Updated March 20, 2024", cls="text-xs text-muted-foreground"),
                    cls="flex items-center text-center"
                ),
                
                cls="max-w-2xl p-6 border rounded-lg"
            ),
            cls=""
        ),
        '''from starui.registry.components.separator import Separator
from starui.registry.components.badge import Badge
from starhtml import Article, Header, H3, H4, P, Div, Span

Article(
    Header(
        H3("Getting Started with StarUI", cls="text-xl font-bold mb-2"),
        P("Learn how to build beautiful user interfaces", cls="text-muted-foreground"),
        
        # Meta information with vertical separators
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
    
    # Section separators
    Separator(cls="mb-6"),
    
    Div(
        H4("Introduction"),
        P("Content here..."),
        cls="mb-6"
    ),
    
    Separator(cls="mb-6"),
    
    Div(
        H4("Quick Start"),
        P("Content here..."),
        cls="mb-6"
    ),
    
    Separator(cls="mb-6"),
    
    # Footer with inline separators
    Div(
        P("Published on March 15, 2024"),
        Separator(orientation="vertical", cls="mx-2 h-3"),
        P("Updated March 20, 2024"),
        cls="flex items-center"
    )
)''',
        title="Article Layout",
        description="Complex content layouts using both horizontal and vertical separators"
    )
    
    # Custom styled separators
    yield ComponentPreview(
        Div(
            H4("Custom Separator Styles", cls="text-center mb-6"),
            
            # Default
            Div(
                P("Default separator", cls="text-center text-sm text-muted-foreground mb-2"),
                Separator(),
                cls="mb-6"
            ),
            
            # Thicker 
            Div(
                P("Thick separator", cls="text-center text-sm text-muted-foreground mb-2"),
                Separator(cls="h-0.5 bg-muted-foreground"),
                cls="mb-6"
            ),
            
            # Colored
            Div(
                P("Colored separator", cls="text-center text-sm text-muted-foreground mb-2"),
                Separator(cls="bg-blue-500"),
                cls="mb-6"
            ),
            
            # Dashed
            Div(
                P("Dashed separator", cls="text-center text-sm text-muted-foreground mb-2"),
                Separator(cls="border-t border-dashed border-muted-foreground bg-transparent h-0"),
                cls="mb-6"
            ),
            
            # Gradient
            Div(
                P("Gradient separator", cls="text-center text-sm text-muted-foreground mb-2"),
                Separator(cls="bg-gradient-to-r from-transparent via-muted-foreground to-transparent"),
                cls=""
            ),
            
            cls="max-w-md mx-auto p-6 border rounded-lg"
        ),
        '''from starui.registry.components.separator import Separator
from starhtml import Div, P, H4

# Default separator
Separator()

# Thick separator  
Separator(cls="h-0.5 bg-muted-foreground")

# Colored separator
Separator(cls="bg-blue-500")

# Dashed separator
Separator(cls="border-t border-dashed border-muted-foreground bg-transparent h-0")

# Gradient separator
Separator(cls="bg-gradient-to-r from-transparent via-muted-foreground to-transparent")''',
        title="Custom Styling",
        description="Customize separators with different styles, colors, and effects"
    )


def create_separator_docs():
    """Create separator documentation page using convention-based approach."""
    from utils import auto_generate_page
    
    # Hero example showcasing both orientations
    hero_example = ComponentPreview(
        Div(
            # Horizontal separators
            Div(
                P("Content above", cls="text-center py-4"),
                Separator(),
                P("Content below", cls="text-center py-4"),
                cls="border rounded-lg p-4 mr-4"
            ),
            
            # Vertical separators
            Div(
                P("Left", cls="px-4 text-center"),
                Separator(orientation="vertical", cls="h-16"),
                P("Center", cls="px-4 text-center"),
                Separator(orientation="vertical", cls="h-16"),
                P("Right", cls="px-4 text-center"),
                cls="flex items-center border rounded-lg p-4"
            ),
            
            cls="flex flex-col sm:flex-row gap-4 items-center"
        ),
        '''from starui.registry.components.separator import Separator
from starhtml import Div, P

# Horizontal separator
Div(
    P("Content above"),
    Separator(),
    P("Content below")
)

# Vertical separator
Div(
    P("Left"),
    Separator(orientation="vertical", cls="h-16"),
    P("Center"), 
    Separator(orientation="vertical", cls="h-16"),
    P("Right"),
    cls="flex items-center"
)''',
        copy_button=True
    )
    
    api_reference = {
        "props": [
            {
                "name": "orientation",
                "type": "Literal['horizontal', 'vertical']",
                "default": "'horizontal'",
                "description": "The orientation of the separator"
            },
            {
                "name": "decorative",
                "type": "bool",
                "default": "True",
                "description": "Whether the separator is purely decorative (affects accessibility attributes)"
            },
            {
                "name": "class_name",
                "type": "str",
                "default": "''",
                "description": "Additional CSS classes"
            },
            {
                "name": "cls",
                "type": "str", 
                "default": "''",
                "description": "CSS classes (alternative to class_name)"
            }
        ]
    }
    
    return auto_generate_page(
        TITLE,
        DESCRIPTION,
        list(examples()),
        cli_command="star add separator",
        api_reference=api_reference,
        hero_example=hero_example,
        component_slug="separator"
    )