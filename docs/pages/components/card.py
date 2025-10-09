TITLE = "Card"
DESCRIPTION = "Displays a card with header, content, and footer."
CATEGORY = "layout"
ORDER = 10
STATUS = "stable"

from starhtml import Div, P, H3, Span, Icon, A, Signal, match, switch
from starhtml.datastar import js
from starui.registry.components.card import (
    Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter
)
from starui.registry.components.button import Button
from starui.registry.components.badge import Badge
from starui.registry.components.input import Input
from starui.registry.components.label import Label
from utils import auto_generate_page, Component, build_api_reference, with_code
from widgets.component_preview import ComponentPreview


# ============================================================================
# EXAMPLE FUNCTIONS (decorated with @with_code for markdown generation)
# ============================================================================

@with_code
def interactive_profile_cards_example():
    following1 = Signal("following1", False)
    following2 = Signal("following2", False)

    profiles = [
        ("JD", "bg-blue-500", "John Doe", "Product Designer", "online", "bg-green-100 text-green-800", "Passionate about creating user-centered designs that solve real problems.", following1, "John"),
        ("AS", "bg-green-500", "Anna Smith", "Frontend Developer", "away", "bg-yellow-100 text-yellow-800", "Full-stack developer with expertise in Python and modern web technologies.", following2, "Anna")
    ]

    def create_profile_card(initials, avatar_color, name, role, status, status_color, bio, follow_signal, message_name):
        return Card(
            CardHeader(
                Div(
                    Div(initials, cls=f"w-12 h-12 rounded-full {avatar_color} flex items-center justify-center text-white font-bold"),
                    Div(
                        CardTitle(name, cls="text-lg"),
                        CardDescription(role),
                        Badge(status, variant="default", cls=f"{status_color} text-xs"),
                        cls="ml-4 space-y-1"
                    ),
                    cls="flex items-center"
                )
            ),
            CardContent(
                P(bio, cls="text-sm text-muted-foreground")
            ),
            CardFooter(
                Button(
                    data_text=follow_signal.if_("Following", "Follow"),
                    data_on_click=follow_signal.toggle(),
                    variant="outline", size="sm", cls="mr-2",
                    data_attr_class=follow_signal.if_("bg-green-50 text-green-700 border-green-200 hover:bg-green-50", "")
                ),
                Button("Message", size="sm", data_on_click=f"alert('Message sent to {message_name}!')")
            )
        )

    profile_cards = [create_profile_card(*profile) for profile in profiles]

    return Div(
        following1,
        following2,
        *profile_cards,
        cls="grid grid-cols-1 md:grid-cols-2 gap-4 max-w-2xl"
    )


@with_code
def interactive_dashboard_stats_example():
    period = Signal("period", "1d")
    revenue = Signal("revenue", 3421)
    revenue_change = Signal("revenue_change", 12.3)
    users = Signal("users", 573)
    users_change = Signal("users_change", 5.2)
    conversion = Signal("conversion", 2.8)
    conversion_change = Signal("conversion_change", 0.2)

    return Div(
        period, revenue, revenue_change, users, users_change, conversion, conversion_change,

        # Dashboard header
        Div(
            Div(
                Icon("lucide:bar-chart-3", cls="h-5 w-5 text-muted-foreground mr-2"),
                H3("Dashboard Overview", cls="text-lg font-semibold"),
                cls="flex items-center mb-2"
            ),
            P("Track your key metrics across different time periods", cls="text-sm text-muted-foreground mb-4")
        ),

        # Time period selector with toggle group style
        Div(
            Div(
                Button(
                    "Today",
                    data_on_click=js("$period = '1d'; $revenue = 3421; $revenue_change = 12.3; $users = 573; $users_change = 5.2; $conversion = 2.8; $conversion_change = 0.2"),
                    size="sm",
                    variant="ghost",
                    data_class_bg_muted=period.eq("1d")
                ),
                Button(
                    "Week",
                    data_on_click=js("$period = '7d'; $revenue = 24567; $revenue_change = 18.5; $users = 1847; $users_change = 8.9; $conversion = 3.1; $conversion_change = 0.4"),
                    size="sm",
                    variant="ghost",
                    data_class_bg_muted=period.eq("7d")
                ),
                Button(
                    "Month",
                    data_on_click=js("$period = '30d'; $revenue = 98234; $revenue_change = 23.2; $users = 7892; $users_change = 15.7; $conversion = 3.4; $conversion_change = -0.1"),
                    size="sm",
                    variant="ghost",
                    data_class_bg_muted=period.eq("30d")
                ),
                Button(
                    "Year",
                    data_on_click=js("$period = '365d'; $revenue = 892451; $revenue_change = 42.8; $users = 45123; $users_change = 31.2; $conversion = 3.9; $conversion_change = 0.8"),
                    size="sm",
                    variant="ghost",
                    data_class_bg_muted=period.eq("365d")
                ),
                cls="inline-flex items-center justify-center rounded-md bg-muted/30 p-1 text-muted-foreground"
            ),
            cls="flex justify-center mb-6"
        ),

        # Stats cards that update based on period
        Div(
            Card(
                CardHeader(
                    Div(
                        Icon("lucide:dollar-sign", width="24", height="24", cls="text-green-600"),
                        cls="mb-2"
                    ),
                    CardTitle("Total Revenue", cls="text-sm font-medium"),
                    CardDescription(data_text=match(period, **{"1d": "Today", "7d": "Last 7 days", "30d": "Last 30 days", "365d": "Last 365 days"}))
                ),
                CardContent(
                    Div(
                        Div(
                            Span(data_text=js("`$${$revenue.toLocaleString()}`"), cls="text-2xl font-bold tracking-tight"),
                            cls="flex items-baseline gap-2"
                        ),
                        P(
                            Span(
                                data_attr_style=js("color: $revenue_change > 0 ? 'rgb(34, 197, 94)' : ($revenue_change < 0 ? 'rgb(239, 68, 68)' : 'rgb(107, 114, 128)')"),
                                data_text=js("($revenue_change >= 0 ? '+' : '') + $revenue_change + '%'"),
                                cls="font-medium"
                            ),
                            Span(" from last period", cls="text-muted-foreground"),
                            cls="text-sm mt-1"
                        )
                    )
                )
            ),
            Card(
                CardHeader(
                    Div(
                        Icon("lucide:users", width="24", height="24", cls="text-blue-600"),
                        cls="mb-2"
                    ),
                    CardTitle("Active Users", cls="text-sm font-medium"),
                    CardDescription(data_text=match(period, **{"1d": "Today", "7d": "Daily average", "30d": "Daily average", "365d": "Monthly average"}))
                ),
                CardContent(
                    Div(
                        Div(
                            Span(data_text=js("`${$users.toLocaleString()}`"), cls="text-2xl font-bold tracking-tight"),
                            cls="flex items-baseline gap-2"
                        ),
                        P(
                            Span(
                                data_attr_style=js("color: $users_change > 0 ? 'rgb(34, 197, 94)' : ($users_change < 0 ? 'rgb(239, 68, 68)' : 'rgb(107, 114, 128)')"),
                                data_text=js("($users_change >= 0 ? '+' : '') + $users_change + '%'"),
                                cls="font-medium"
                            ),
                            Span(" from last period", cls="text-muted-foreground"),
                            cls="text-sm mt-1"
                        )
                    )
                )
            ),
            Card(
                CardHeader(
                    Div(
                        Icon("lucide:trending-up", width="24", height="24", cls="text-purple-600"),
                        cls="mb-2"
                    ),
                    CardTitle("Conversion Rate", cls="text-sm font-medium"),
                    CardDescription(data_text=match(period, **{"1d": "Today", "7d": "This week", "30d": "This month", "365d": "This year"}))
                ),
                CardContent(
                    Div(
                        Div(
                            Span(data_text=js("`${$conversion}%`"), cls="text-2xl font-bold tracking-tight"),
                            cls="flex items-baseline gap-2"
                        ),
                        P(
                            Span(
                                data_attr_style=js("color: $conversion_change > 0 ? 'rgb(34, 197, 94)' : ($conversion_change < 0 ? 'rgb(239, 68, 68)' : 'rgb(107, 114, 128)')"),
                                data_text=js("($conversion_change >= 0 ? '+' : '') + $conversion_change"),
                                cls="font-medium"
                            ),
                            Span(" percentage points", cls="text-muted-foreground"),
                            cls="text-sm mt-1"
                        )
                    )
                )
            ),
            cls="grid grid-cols-1 md:grid-cols-3 gap-4"
        ),

        cls="w-full"
    )


@with_code
def interactive_form_card_example():
    return Card(
        CardHeader(
            CardTitle("Create Account"),
            CardDescription("Enter your details below to create your account")
        ),
        CardContent(
            Div(
                Div(
                    Label("Email", for_="email"),
                    Input(
                        type="email",
                        id="email",
                        placeholder="name@example.com",
                        cls="w-full"
                    ),
                    cls="space-y-2"
                ),
                Div(
                    Label("Password", for_="password"),
                    Input(
                        type="password",
                        id="password",
                        placeholder="Enter your password",
                        cls="w-full"
                    ),
                    cls="space-y-2"
                ),
                Div(
                    Label("Confirm Password", for_="confirm"),
                    Input(
                        type="password",
                        id="confirm",
                        placeholder="Confirm your password",
                        cls="w-full"
                    ),
                    cls="space-y-2"
                ),
                cls="space-y-4"
            )
        ),
        CardFooter(
            Div(
                Button(
                    "Create Account",
                    data_on_click="alert('Create account clicked!')",
                    cls="w-full mb-2"
                ),
                P(
                    "Already have an account? ",
                    A("Sign in", href="#", cls="underline hover:text-primary"),
                    cls="text-sm text-center text-muted-foreground"
                ),
                cls="w-full"
            )
        ),
        cls="w-full max-w-md"
    )


@with_code
def interactive_shopping_cart_example():
    items = Signal("items", ["MacBook Pro 14", "AirPods Pro (2nd gen)"])
    total = Signal("total", 2648.0)
    checking_out = Signal("checking_out", False)

    return Card(
        items, total, checking_out,
        CardHeader(
            CardTitle("Shopping Cart"),
            CardDescription(data_text=js("`${$items.length} item${$items.length !== 1 ? 's' : ''} in cart`"))
        ),
        CardContent(
            Div(
                # Cart items list (only shows when cart has items)
                Div(
                    # Item 1 - MacBook Pro
                    Div(
                        Div(
                            Div("💻", cls="text-2xl mr-3"),
                            Div(
                                P("MacBook Pro 14\"", cls="font-medium text-sm"),
                                P("Space Gray, 16GB RAM", cls="text-xs text-muted-foreground"),
                                cls="flex-1"
                            ),
                            cls="flex items-start"
                        ),
                        Div(
                            P("$2,399", cls="font-bold text-sm"),
                            Button(                                
                                Icon("lucide:trash-2", cls="h-3 w-3"),
                                data_on_click=js("$items = $items.filter(item => item !== 'MacBook Pro 14'); $total = ($items.includes('AirPods Pro (2nd gen)') ? 249 : 0)"),
                                variant="ghost", size="sm",
                                cls="ml-2 p-1 h-6 w-6"
                            ),
                            cls="flex items-center"
                        ),
                        data_show=js("$items.includes('MacBook Pro 14')"),
                        cls="flex items-start justify-between py-2 border-b"
                    ),
                    # Item 2 - AirPods
                    Div(
                        Div(
                            Div("🎧", cls="text-2xl mr-3"),
                            Div(
                                P("AirPods Pro (2nd gen)", cls="font-medium text-sm"),
                                P("with MagSafe Case", cls="text-xs text-muted-foreground"),
                                cls="flex-1"
                            ),
                            cls="flex items-start"
                        ),
                        Div(
                            P("$249", cls="font-bold text-sm"),
                            Button(                                
                                Icon("lucide:trash-2", cls="h-3 w-3"),
                                data_on_click=js("$items = $items.filter(item => item !== 'AirPods Pro (2nd gen)'); $total = ($items.includes('MacBook Pro 14') ? 2399 : 0)"),
                                variant="ghost", size="sm",
                                cls="ml-2 p-1 h-6 w-6"
                            ),
                            cls="flex items-center"
                        ),
                        data_show=js("$items.includes('AirPods Pro (2nd gen)')"),
                        cls="flex items-start justify-between py-2"
                    ),
                    cls="space-y-1"
                ),

                # Empty cart message (only shows when cart is empty)
                Div(
                    Div("🛍️", cls="text-5xl text-center mb-3"),
                    P("Your cart is empty", cls="text-center text-muted-foreground font-medium"),
                    P("Add some items to get started", cls="text-center text-sm text-muted-foreground"),
                    data_show=js("$items.length === 0"),
                    cls="py-8"
                ),

                cls="min-h-[120px]"
            )
        ),
        CardFooter(
            Div(
                Div(
                    Div(
                        Span("Subtotal: ", cls="text-sm"),
                        Span(data_text=js("`$${$total.toFixed(2)}`"), cls="font-bold"),
                        cls="flex justify-between w-full mb-2"
                    ),
                    Div(
                        Span("Tax: ", cls="text-sm"),
                        Span(data_text=js("`$${($total * 0.08).toFixed(2)}`"), cls="text-sm"),
                        cls="flex justify-between w-full mb-2 text-muted-foreground"
                    ),
                    Div(
                        Span("Total: ", cls="font-medium"),
                        Span(data_text=js("`$${($total * 1.08).toFixed(2)}`"), cls="font-bold text-lg"),
                        cls="flex justify-between w-full border-t pt-2 mt-2"
                    ),
                    data_show=js("$items.length > 0"),
                    cls="w-full mb-4"
                ),

                Div(
                    Button(
                        "Add Sample Items",
                        data_on_click=js("$items = ['MacBook Pro 14', 'AirPods Pro (2nd gen)']; $total = 2648"),                        
                        variant="outline", size="sm",
                        cls="w-full mb-2"
                    ),
                    data_show=js("$items.length === 0")
                ),

                Button(
                    data_on_click=js("$checking_out = true; setTimeout(() => { alert('Order placed successfully!'); $items = []; $total = 0; $checking_out = false; }, 2000)"),
                    data_text=checking_out.if_("Processing...", "Checkout"),
                    data_attr_disabled=js("$items.length === 0 || $checking_out"),
                    cls="w-full",
                    data_attr_class=js("($items.length === 0 || $checking_out) ? 'opacity-50 cursor-not-allowed' : ''")
                ),

                cls="w-full"
            )
        ),
        cls="w-full max-w-md"
    )


@with_code
def notification_cards_example():
    return Div(
        Card(
            CardContent(
                Div(
                    Div(
                        Icon("lucide:check-circle", width="20", height="20", cls="text-green-500"),
                        Div(
                            P("Payment successful", cls="font-medium text-sm"),
                            P("Your payment has been processed successfully.", cls="text-sm text-muted-foreground"),
                            cls="ml-3"
                        ),
                        cls="flex items-start"
                    ),
                    Button("View Receipt", variant="ghost", size="sm", cls="mt-3",
                           data_on_click="alert('Receipt downloaded!')"),
                    cls="p-4"
                )
            )
        ),
        Card(
            CardContent(
                Div(
                    Div(
                        Icon("lucide:alert-circle", width="20", height="20", cls="text-orange-500"),
                        Div(
                            P("Action required", cls="font-medium text-sm"),
                            P("Please verify your email address to continue.", cls="text-sm text-muted-foreground"),
                            cls="ml-3"
                        ),
                        cls="flex items-start"
                    ),
                    Button("Verify Email", size="sm", cls="mt-3",
                           data_on_click="alert('Verification email sent!')"),
                    cls="p-4"
                )
            )
        ),
        cls="space-y-3 max-w-md"
    )


@with_code
def product_ecommerce_cards_example():
    # Product 1 signals
    selected_color = Signal("selected_color", "titanium")
    favorited = Signal("favorited", False)
    added_to_cart = Signal("added_to_cart", False)
    adding_to_cart = Signal("adding_to_cart", False)

    # Product 2 signals
    favorited2 = Signal("favorited2", False)
    added_to_cart2 = Signal("added_to_cart2", False)
    adding_to_cart2 = Signal("adding_to_cart2", False)

    return Div(
        selected_color, favorited, added_to_cart, adding_to_cart,
        favorited2, added_to_cart2, adding_to_cart2,
        Card(
            CardContent(
                Div(
                    # Product image placeholder
                    Div(
                        "📱",
                        cls="text-6xl flex items-center justify-center h-32 bg-gray-50 rounded-lg mb-4"
                    ),

                    # Product info
                    Div(
                        CardTitle("iPhone 15 Pro", cls="text-lg mb-1"),
                        CardDescription("Natural Titanium, 128GB"),

                        # Rating stars
                        Div(
                            Span("★★★★★", cls="text-yellow-400 text-sm"),
                            Span("4.9 (1,234 reviews)", cls="text-sm text-muted-foreground ml-2"),
                            cls="flex items-center mt-2 mb-3"
                        ),

                        # Price and discount
                        Div(
                            Span("$999", cls="text-2xl font-bold text-primary mr-2"),
                            Span("$1,099", cls="text-sm line-through text-muted-foreground"),
                            Badge("9% OFF", variant="destructive", cls="ml-2"),
                            cls="flex items-center mb-4"
                        ),

                        # Color options
                        Div(
                            P("Color:", cls="text-sm font-medium mb-2"),
                            Div(
                                Button(
                                    "",
                                    variant="ghost", size="sm",
                                    cls="w-8 h-8 rounded-full bg-gray-800 border-2 p-0",
                                    data_class_border_primary=selected_color.eq("titanium"),
                                    data_on_click=selected_color.set("titanium")
                                ),
                                Button(
                                    "",
                                    variant="ghost", size="sm",
                                    cls="w-8 h-8 rounded-full bg-blue-500 border-2 p-0 ml-2",
                                    data_class_border_primary=selected_color.eq("blue"),
                                    data_on_click=selected_color.set("blue")
                                ),
                                Button(
                                    "",
                                    variant="ghost", size="sm",
                                    cls="w-8 h-8 rounded-full bg-white border-2 p-0 ml-2",
                                    data_class_border_primary=selected_color.eq("white"),
                                    data_on_click=selected_color.set("white")
                                ),
                                cls="flex items-center"
                            ),
                            cls="mb-4"
                        )
                    ),

                    cls="p-0"
                )
            ),
            CardFooter(
                Div(
                    Button(
                        Icon("lucide:heart", cls="h-4 w-4 mr-2",
                             data_attr_class=favorited.if_("fill-current text-red-500", "")),
                        data_text=favorited.if_("Favorited", "Add to Favorites"),
                        variant="outline", size="sm",
                        data_on_click=favorited.toggle(),
                        cls="mr-2"
                    ),
                    Button(
                        Icon("lucide:shopping-cart", cls="h-4 w-4 mr-2"),
                        data_text=added_to_cart.if_("Added!", "Add to Cart"),
                        data_attr_disabled=adding_to_cart,
                        data_on_click=js("$adding_to_cart = true; setTimeout(() => { $added_to_cart = true; $adding_to_cart = false; setTimeout(() => $added_to_cart = false, 2000); }, 800)"),
                        data_attr_class=switch([
                            (added_to_cart, "bg-green-600 hover:bg-green-700"),
                            (adding_to_cart, "opacity-50 cursor-not-allowed")
                        ], default=""),
                        size="sm"
                    ),
                    cls="flex w-full gap-2"
                )
            ),
            cls="w-full max-w-xs hover:shadow-lg transition-shadow duration-200"
        ),

        Card(
            CardContent(
                Div(
                    # Product image placeholder
                    Div(
                        "🎧",
                        cls="text-6xl flex items-center justify-center h-32 bg-gray-50 rounded-lg mb-4"
                    ),

                    # Product info
                    Div(
                        CardTitle("AirPods Pro", cls="text-lg mb-1"),
                        CardDescription("2nd Generation with MagSafe"),

                        # Rating stars
                        Div(
                            Span("★★★★★", cls="text-yellow-400 text-sm"),
                            Span("4.8 (892 reviews)", cls="text-sm text-muted-foreground ml-2"),
                            cls="flex items-center mt-2 mb-3"
                        ),

                        # Price
                        Div(
                            Span("$249", cls="text-2xl font-bold text-primary"),
                            Badge("Best Seller", variant="secondary", cls="ml-2"),
                            cls="flex items-center mb-4"
                        ),

                        # Quick specs
                        Div(
                            P("✓ Active Noise Cancellation", cls="text-sm text-muted-foreground mb-1"),
                            P("✓ Spatial Audio", cls="text-sm text-muted-foreground mb-1"),
                            P("✓ 6hr battery + 24hr case", cls="text-sm text-muted-foreground"),
                            cls="mb-4"
                        )
                    ),

                    cls="p-0"
                )
            ),
            CardFooter(
                Div(
                    Button(
                        Icon("lucide:heart", cls="h-4 w-4 mr-2",
                             data_attr_class=favorited2.if_("fill-current text-red-500", "")),
                        data_text=favorited2.if_("Favorited", "Add to Favorites"),
                        variant="outline", size="sm",
                        data_on_click=favorited2.toggle(),
                        cls="mr-2"
                    ),
                    Button(
                        Icon("lucide:shopping-cart", cls="h-4 w-4 mr-2"),
                        data_text=added_to_cart2.if_("Added!", "Add to Cart"),
                        data_attr_disabled=adding_to_cart2,
                        data_on_click=js("$adding_to_cart2 = true; setTimeout(() => { $added_to_cart2 = true; $adding_to_cart2 = false; setTimeout(() => $added_to_cart2 = false, 2000); }, 800)"),
                        data_attr_class=switch([
                            (added_to_cart2, "bg-green-600 hover:bg-green-700"),
                            (adding_to_cart2, "opacity-50 cursor-not-allowed")
                        ], default=""),
                        size="sm"
                    ),
                    cls="flex w-full gap-2"
                )
            ),
            cls="w-full max-w-xs hover:shadow-lg transition-shadow duration-200"
        ),

        cls="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-2xl"
    )


# ============================================================================
# EXAMPLES GENERATOR (for rendering on the page)
# ============================================================================

def examples():
    yield ComponentPreview(
        interactive_profile_cards_example(),
        interactive_profile_cards_example.code,
        title="Interactive Profile Cards",
        description="Profile cards with follow/unfollow functionality and status badges"
    )

    yield ComponentPreview(
        interactive_dashboard_stats_example(),
        interactive_dashboard_stats_example.code,
        title="Interactive Dashboard Stats",
        description="Dynamic stats cards with period selection and real-time updates"
    )

    yield ComponentPreview(
        interactive_form_card_example(),
        interactive_form_card_example.code,
        title="Interactive Form Card",
        description="Form with real-time validation and dynamic button states"
    )

    yield ComponentPreview(
        interactive_shopping_cart_example(),
        interactive_shopping_cart_example.code,
        title="Interactive Shopping Cart",
        description="Dynamic cart with add/remove items, total calculation, and checkout flow"
    )

    yield ComponentPreview(
        notification_cards_example(),
        notification_cards_example.code,
        title="Interactive Notifications",
        description="Alert and notification cards with action handlers"
    )

    yield ComponentPreview(
        product_ecommerce_cards_example(),
        product_ecommerce_cards_example.code,
        title="Product Cards",
        description="E-commerce product cards with color selection, favorites, and cart functionality"
    )


# ============================================================================
# API REFERENCE
# ============================================================================

API_REFERENCE = build_api_reference(
    components=[
        Component("Card", "The main card container"),
        Component("CardHeader", "Contains the card title and description"),
        Component("CardTitle", "The main heading of the card"),
        Component("CardDescription", "Supporting text for the card title"),
        Component("CardContent", "The main content area of the card"),
        Component("CardFooter", "Contains actions and additional information"),
    ]
)


# ============================================================================
# EXAMPLES DATA (for markdown generation with code)
# ============================================================================

EXAMPLES_DATA = [
    {"title": "Interactive Profile Cards", "description": "Profile cards with follow/unfollow functionality and status badges", "code": interactive_profile_cards_example.code},
    {"title": "Interactive Dashboard Stats", "description": "Dynamic stats cards with period selection and real-time updates", "code": interactive_dashboard_stats_example.code},
    {"title": "Interactive Form Card", "description": "Form with real-time validation and dynamic button states", "code": interactive_form_card_example.code},
    {"title": "Interactive Shopping Cart", "description": "Dynamic cart with add/remove items, total calculation, and checkout flow", "code": interactive_shopping_cart_example.code},
    {"title": "Interactive Notifications", "description": "Alert and notification cards with action handlers", "code": notification_cards_example.code},
    {"title": "Product Cards", "description": "E-commerce product cards with color selection, favorites, and cart functionality", "code": product_ecommerce_cards_example.code},
]


# ============================================================================
# DOCS PAGE
# ============================================================================

@with_code
def hero_card_example():
    return Card(
        CardHeader(
            CardTitle("Card Title"),
            CardDescription("Card description with supporting text below.")
        ),
        CardContent(
            P("This is the main content area of the card where you can place any content you need.")
        ),
        CardFooter(
            Button("Action", cls="mr-2"),
            Button("Cancel", variant="outline")
        ),
        cls="w-full max-w-md"
    )


def create_card_docs():
    hero_example = ComponentPreview(
        hero_card_example(),
        hero_card_example.code,
        copy_button=True
    )

    return auto_generate_page(
        TITLE,
        DESCRIPTION,
        list(examples()),
        cli_command="star add card",
        api_reference=API_REFERENCE,
        hero_example=hero_example,
        component_slug="card"
    )