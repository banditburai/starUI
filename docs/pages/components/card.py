"""
Card component documentation - Flexible content containers.
"""

# Component metadata for auto-discovery
TITLE = "Card"
DESCRIPTION = "Displays a card with header, content, and footer."
CATEGORY = "layout"
ORDER = 10
STATUS = "stable"

from starhtml import Div, P, H3, H4, Span, Icon, A, Img, if_
from starhtml.datastar import (
    ds_on_click, ds_show, ds_text, ds_signals, value, ds_class,
    ds_bind, ds_disabled, ds_on_mouseenter, ds_on_mouseleave, toggle_signal, ds_on_input, ds_computed, ds_style, if_
)
from starui.registry.components.card import (
    Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter, CardAction
)
from starui.registry.components.button import Button
from starui.registry.components.badge import Badge
from starui.registry.components.input import Input
from starui.registry.components.label import Label
from widgets.component_preview import ComponentPreview


def examples():
    """Generate Card examples using ComponentPreview with tabs."""
    
    # Note: Basic card moved to hero example
    # This will be the first example after the hero
    
    # Interactive profile cards with follow functionality
    yield ComponentPreview(
        Div(
            Card(
                CardHeader(
                    Div(
                        Div("JD", cls="w-12 h-12 rounded-full bg-blue-500 flex items-center justify-center text-white font-bold"),
                        Div(
                            CardTitle("John Doe", cls="text-lg"),
                            CardDescription("Product Designer"),
                            Badge(
                                "online",
                                variant="default",
                                cls="bg-green-100 text-green-800 text-xs"
                            ),
                            cls="ml-4 space-y-1"
                        ),
                        cls="flex items-center"
                    )
                ),
                CardContent(
                    P("Passionate about creating user-centered designs that solve real problems.", cls="text-sm text-muted-foreground")
                ),
                CardFooter(
                    Button(
                        ds_text("$following1 ? 'Following' : 'Follow'"),
                        ds_on_click(toggle_signal("following1")),
                        variant="outline", size="sm", cls="mr-2",
                        ds_class={
                            "bg-green-50 text-green-700 border-green-200": "$following1",
                            "hover:bg-green-50": "$following1"
                        },                        
                    ),
                    Button("Message", size="sm", ds_on_click="alert('Message sent to John!')")
                )
            ),
            Card(
                CardHeader(
                    Div(
                        Div("AS", cls="w-12 h-12 rounded-full bg-green-500 flex items-center justify-center text-white font-bold"),
                        Div(
                            CardTitle("Anna Smith", cls="text-lg"),
                            CardDescription("Frontend Developer"),
                            Badge(
                                "away",
                                variant="secondary",
                                cls="bg-yellow-100 text-yellow-800 text-xs"
                            ),
                            cls="ml-4 space-y-1"
                        ),
                        cls="flex items-center"
                    )
                ),
                CardContent(
                    P("Full-stack developer with expertise in Python and modern web technologies.", cls="text-sm text-muted-foreground")
                ),
                CardFooter(
                    Button(
                        ds_text("$following2 ? 'Following' : 'Follow'"),
                        ds_on_click(toggle_signal("following2")),
                        variant="outline", size="sm", cls="mr-2",
                        ds_class={
                            "bg-green-50 text-green-700 border-green-200": "$following2",
                            "hover:bg-green-50": "$following2"
                        },                        
                    ),
                    Button("Message", size="sm", ds_on_click="alert('Message sent to Anna!')")
                )
            ),
            ds_signals(following1=False, following2=False),
            cls="grid grid-cols-1 md:grid-cols-2 gap-4 max-w-2xl"
        ),
        '''Card(
    CardHeader(
        Div(
            Div("JD", cls="w-12 h-12 rounded-full bg-blue-500 flex items-center justify-center text-white font-bold"),
            Div(
                CardTitle("John Doe"),
                CardDescription("Product Designer"),
                Badge("online", variant="default"),
                cls="ml-4"
            ),
            cls="flex items-center"
        )
    ),
    CardContent(
        P("Passionate about creating user-centered designs.")
    ),
    CardFooter(
        Button(
            ds_text("$following ? 'Following' : 'Follow'"),
            variant="outline",
            ds_class={"bg-green-50 text-green-700": "$following"},
            ds_on_click=toggle_signal("following")
        ),
        Button("Message", ds_on_click="alert('Message sent!')")
    )
)''',
        title="Interactive Profile Cards",
        description="Profile cards with follow/unfollow functionality and status badges"
    )
    
    # Interactive dashboard stats with period selection
    yield ComponentPreview(
        Div(
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
                        ds_on_click("$period = '1d'; $revenue = 3421; $revenue_change = 12.3; $users = 573; $users_change = 5.2; $conversion = 2.8; $conversion_change = 0.2"),
                        size="sm",
                        variant="ghost",
                        ds_class={"bg-muted": "$period === '1d'"},                        
                    ),
                    Button(
                        "Week",
                        ds_on_click("$period = '7d'; $revenue = 24567; $revenue_change = 18.5; $users = 1847; $users_change = 8.9; $conversion = 3.1; $conversion_change = 0.4"),
                        size="sm",
                        variant="ghost",
                        ds_class={"bg-muted": "$period === '7d'"},                        
                    ),
                    Button(
                        "Month",
                        ds_on_click("$period = '30d'; $revenue = 98234; $revenue_change = 23.2; $users = 7892; $users_change = 15.7; $conversion = 3.4; $conversion_change = -0.1"),
                        size="sm",
                        variant="ghost",
                        ds_class={"bg-muted": "$period === '30d'"},                        
                    ),
                    Button(
                        "Year",
                        ds_on_click("$period = '365d'; $revenue = 892451; $revenue_change = 42.8; $users = 45123; $users_change = 31.2; $conversion = 3.9; $conversion_change = 0.8"),
                        size="sm",
                        variant="ghost",
                        ds_class={"bg-muted": "$period === '365d'"},                        
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
                        CardDescription(ds_text("`${$period === '1d' ? 'Today' : $period === '7d' ? 'Last 7 days' : $period === '30d' ? 'Last 30 days' : 'Last 365 days'}`"))
                    ),
                    CardContent(
                        Div(
                            Div(
                                Span(ds_text("`$${$revenue.toLocaleString()}`"), cls="text-2xl font-bold tracking-tight"),
                                cls="flex items-baseline gap-2"
                            ),
                            P(
                                Span(
                                    ds_style(color="$revenue_change > 0 ? 'rgb(34, 197, 94)' : ($revenue_change < 0 ? 'rgb(239, 68, 68)' : 'rgb(107, 114, 128)')"),
                                    ds_text("($revenue_change >= 0 ? '+' : '') + $revenue_change + '%'"),
                                    cls="font-medium",                                    
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
                        CardDescription(ds_text("`${$period === '1d' ? 'Today' : $period === '7d' ? 'Daily average' : $period === '30d' ? 'Daily average' : 'Monthly average'}`"))
                    ),
                    CardContent(
                        Div(
                            Div(
                                Span(ds_text("`${$users.toLocaleString()}`"), cls="text-2xl font-bold tracking-tight"),
                                cls="flex items-baseline gap-2"
                            ),
                            P(
                                Span(
                                    ds_style(color="$users_change > 0 ? 'rgb(34, 197, 94)' : ($users_change < 0 ? 'rgb(239, 68, 68)' : 'rgb(107, 114, 128)')"),
                                    ds_text("($users_change >= 0 ? '+' : '') + $users_change + '%'"),
                                    cls="font-medium",                                    
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
                        CardDescription(ds_text("`${$period === '1d' ? 'Today' : $period === '7d' ? 'This week' : $period === '30d' ? 'This month' : 'This year'}`"))
                    ),
                    CardContent(
                        Div(
                            Div(
                                Span(ds_text("`${$conversion}%`"), cls="text-2xl font-bold tracking-tight"),
                                cls="flex items-baseline gap-2"
                            ),
                            P(
                                Span(
                                    ds_style(color="$conversion_change > 0 ? 'rgb(34, 197, 94)' : ($conversion_change < 0 ? 'rgb(239, 68, 68)' : 'rgb(107, 114, 128)')"),
                                    ds_text("($conversion_change >= 0 ? '+' : '') + $conversion_change"),
                                    cls="font-medium",
                                    
                                ),
                                Span(" percentage points", cls="text-muted-foreground"),
                                cls="text-sm mt-1"
                            )
                        )
                    )
                ),
                cls="grid grid-cols-1 md:grid-cols-3 gap-4"
            ),
            
            # Use snake_case for all signals (consistent across Python/HTML/JS)
            ds_signals(
                period=value("1d"),
                revenue=3421,
                revenue_change=12.3,
                users=573,
                users_change=5.2,
                conversion=2.8,
                conversion_change=0.2
            ),
            
            
            cls="w-full"
        ),
        '''Div(
    # Period selector buttons
    Div(
        Button("Today", variant="ghost",
               ds_class={"bg-muted": "$period === '1d'"},
               ds_on_click="$period = '1d'"),
        Button("Week", variant="ghost",
               ds_class={"bg-muted": "$period === '7d'"},
               ds_on_click="$period = '7d'"),
        Button("Month", variant="ghost",
               ds_class={"bg-muted": "$period === '30d'"},
               ds_on_click="$period = '30d'"),
        cls="inline-flex rounded-md bg-muted/30 p-1"
    ),
    
    # Stats cards with dynamic updates
    Card(
        CardHeader(
            CardTitle("Total Revenue"),
            CardDescription(ds_text("`Last ${$period === '1d' ? 'day' : $period === '7d' ? 'week' : 'month'}`"))
        ),
        CardContent(
            Div(
                Span(ds_text("'$' + $revenue.toLocaleString()"), cls="text-2xl font-bold"),
                P(
                    Span(ds_text("`${$revenueChange >= 0 ? '+' : ''}${$revenueChange}%`"),
                         ds_class={"text-emerald-600": "$revenueChange > 0", "text-red-600": "$revenueChange < 0"}),
                    Span(" from last period", cls="text-muted-foreground"),
                    cls="text-sm mt-1"
                )
            )
        )
    ),
    ds_signals(period=value("30d"), revenue=value(98234), revenueChange=value(23.2)),
    ds_bind("""
        // Auto-update stats when period changes
        if ($period === '1d') {
            $revenue = 3421; $revenueChange = 12.3;
        } else if ($period === '7d') {
            $revenue = 24567; $revenueChange = 18.5;
        } else if ($period === '30d') {
            $revenue = 98234; $revenueChange = 23.2;
        }
    """)
)''',
        title="Interactive Dashboard Stats",
        description="Dynamic stats cards with period selection and real-time updates"
    )
    
    # Interactive form card with validation
    yield ComponentPreview(
        Card(
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
                        ds_on_click("alert('Create account clicked!')"),
                        cls="w-full mb-2",
                        
                    ),
                    P(
                        "Already have an account? ", 
                        A("Sign in", href="#", cls="underline hover:text-primary"), 
                        cls="text-sm text-center text-muted-foreground"
                    ),
                    cls="w-full"
                )
            ),
            
            # Form validation signals
            ds_signals(
                email=value(""),
                password=value(""),
                confirmPassword=value(""),
                emailValid=value(False),
                creating=value(False)
            ),
            
            cls="w-full max-w-md"
        ),
        '''Card(
    CardHeader(
        CardTitle("Create Account"),
        CardDescription("Enter your details below")
    ),
    CardContent(
        Div(
            Div(
                Label("Email", for_="email"),
                Input(
                    signal="email",
                    type="email",
                    placeholder="name@example.com",
                    ds_class={
                        "border-red-300": "$email.length > 0 && !$emailValid",
                        "border-green-300": "$emailValid"
                    }
                ),
                P(
                    "Please enter a valid email address",
                    ds_show="$email.length > 0 && !$emailValid",
                    cls="text-red-500 text-sm mt-1"
                ),
                cls="space-y-2"
            ),
            Div(
                Label("Password", for_="password"),
                Input(
                    signal="password",
                    type="password",
                    placeholder="Enter your password",
                    ds_class={
                        "border-red-300": "$password.length > 0 && $password.length < 8",
                        "border-green-300": "$password.length >= 8"
                    }
                ),
                P(
                    "Password must be at least 8 characters",
                    ds_show="$password.length > 0 && $password.length < 8",
                    cls="text-red-500 text-sm mt-1"
                )
            ),
            cls="space-y-4"
        )
    ),
    CardFooter(
        Button(
            ds_text("$creating ? 'Creating Account...' : 'Create Account'"),
            ds_disabled("!$emailValid || $password.length < 8 || $creating"),
            ds_on_click="createAccount()",
            cls="w-full"
        )
    ),
    ds_signals(email="", password="", emailValid=False, creating=False),
    ds_bind("$emailValid = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test($email)")
)''',
        title="Interactive Form Card",
        description="Form with real-time validation and dynamic button states"
    )
    
    # Interactive shopping cart card
    yield ComponentPreview(
        Card(
            CardHeader(
                CardTitle("Shopping Cart"),
                CardDescription(ds_text("`${$items.length} item${$items.length !== 1 ? 's' : ''} in cart`"))
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
                                    ds_on_click("$items = $items.filter(item => item !== 'MacBook Pro 14'); $total = ($items.includes('AirPods Pro (2nd gen)') ? 249 : 0)"),
                                    Icon("lucide:trash-2", cls="h-3 w-3"),
                                    variant="ghost", size="sm",                                    
                                    cls="ml-2 p-1 h-6 w-6"
                                ),
                                cls="flex items-center"
                            ),
                            ds_show("$items.includes('MacBook Pro 14')"),
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
                                    ds_on_click("$items = $items.filter(item => item !== 'AirPods Pro (2nd gen)'); $total = ($items.includes('MacBook Pro 14') ? 2399 : 0)"),
                                    Icon("lucide:trash-2", cls="h-3 w-3"),
                                    variant="ghost", size="sm",                                    
                                    cls="ml-2 p-1 h-6 w-6"
                                ),
                                cls="flex items-center"
                            ),
                            ds_show("$items.includes('AirPods Pro (2nd gen)')"),
                            cls="flex items-start justify-between py-2"
                        ),
                        cls="space-y-1"
                    ),
                    
                    # Empty cart message (only shows when cart is empty)
                    Div(
                        Div("🛍️", cls="text-5xl text-center mb-3"),
                        P("Your cart is empty", cls="text-center text-muted-foreground font-medium"),
                        P("Add some items to get started", cls="text-center text-sm text-muted-foreground"),
                        ds_show("$items.length === 0"),
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
                            Span(ds_text("`$${$total.toFixed(2)}`"), cls="font-bold"),
                            cls="flex justify-between w-full mb-2"
                        ),
                        Div(
                            Span("Tax: ", cls="text-sm"),
                            Span(ds_text("`$${($total * 0.08).toFixed(2)}`"), cls="text-sm"),
                            cls="flex justify-between w-full mb-2 text-muted-foreground"
                        ),
                        Div(
                            Span("Total: ", cls="font-medium"),
                            Span(ds_text("`$${($total * 1.08).toFixed(2)}`"), cls="font-bold text-lg"),
                            cls="flex justify-between w-full border-t pt-2 mt-2"
                        ),
                        ds_show("$items.length > 0"),
                        cls="w-full mb-4"
                    ),
                    
                    Div(
                        Button(
                            ds_on_click("$items = ['MacBook Pro 14', 'AirPods Pro (2nd gen)']; $total = 2648"),
                            "Add Sample Items",
                            variant="outline", size="sm",                            
                            cls="w-full mb-2"
                        ),
                        ds_show("$items.length === 0")
                    ),
                    
                    Button(
                        ds_on_click("$checking_out = true; setTimeout(() => { alert('Order placed successfully!'); $items = []; $total = 0; $checking_out = false; }, 2000)"),
                        ds_text("$checking_out ? 'Processing...' : 'Checkout'"),
                        ds_disabled="$items.length === 0 || $checking_out",                        
                        cls="w-full",
                        ds_class={
                            "opacity-50 cursor-not-allowed": "$items.length === 0 || $checking_out"
                        }
                    ),
                    
                    cls="w-full"
                )
            ),
            
            # Shopping cart state management
            ds_signals(
                items=value(["MacBook Pro 14", "AirPods Pro (2nd gen)"]),
                total=2648.0,
                checking_out=False
            ),
            
            cls="w-full max-w-md"
        ),
        '''Card(
    CardHeader(
        CardTitle("Shopping Cart"),
        CardDescription(ds_text("`${$items.length} item${$items.length !== 1 ? 's' : ''}`"))
    ),
    CardContent(
        Div(
            # Cart items list
            Div(
                Div(
                    P("MacBook Pro 14\"", cls="font-medium"),
                    P("$2,399", cls="font-bold"),
                    Button(Icon("lucide:trash-2"), variant="ghost", size="sm",
                           ds_on_click="removeItem(0)"),
                    cls="flex justify-between items-center py-2"
                ),
                ds_show("$items.length > 0")
            ),
            # Empty state
            P("Your cart is empty", ds_show("$items.length === 0"), cls="text-center py-8")
        )
    ),
    CardFooter(
        Div(
            Span("Total: ", Span(ds_text("`$${$total.toFixed(2)}`"), cls="font-bold")),
            Button("Checkout", ds_disabled="$items.length === 0", ds_on_click="checkout()"),
            cls="w-full flex justify-between items-center"
        )
    ),
    ds_signals(items=["MacBook Pro 14"], total=2399.00)
)''',
        title="Interactive Shopping Cart",
        description="Dynamic cart with add/remove items, total calculation, and checkout flow"
    )
    
    # Notification cards
    yield ComponentPreview(
        Div(
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
                               ds_on_click="alert('Receipt downloaded!')"),
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
                               ds_on_click="alert('Verification email sent!')"),
                        cls="p-4"
                    )
                )
            ),
            cls="space-y-3 max-w-md"
        ),
        '''Card(
    CardContent(
        Div(
            Icon("lucide:check-circle", width="20", height="20", cls="text-green-500"),
            Div(
                P("Payment successful", cls="font-medium"),
                P("Your payment has been processed.", cls="text-muted-foreground"),
                cls="ml-3"
            ),
            cls="flex items-start"
        ),
        Button("View Receipt", variant="ghost", size="sm", 
               ds_on_click="alert('Receipt downloaded!')")
    )
)''',
        title="Interactive Notifications",
        description="Alert and notification cards with action handlers"
    )
    
    # Product/E-commerce cards with interactive features
    yield ComponentPreview(
        Div(
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
                                        ds_class={"border-primary": "$selectedColor === 'titanium'"},
                                        ds_on_click="$selectedColor = 'titanium'"
                                    ),
                                    Button(
                                        "", 
                                        variant="ghost", size="sm",
                                        cls="w-8 h-8 rounded-full bg-blue-500 border-2 p-0 ml-2",
                                        ds_class={"border-primary": "$selectedColor === 'blue'"},
                                        ds_on_click="$selectedColor = 'blue'"
                                    ),
                                    Button(
                                        "", 
                                        variant="ghost", size="sm",
                                        cls="w-8 h-8 rounded-full bg-white border-2 p-0 ml-2",
                                        ds_class={"border-primary": "$selectedColor === 'white'"},
                                        ds_on_click="$selectedColor = 'white'"
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
                                 ds_class={"fill-current text-red-500": "$favorited"}),
                            ds_text("$favorited ? 'Favorited' : 'Add to Favorites'"),
                            variant="outline", size="sm",
                            ds_on_click=toggle_signal("favorited"),
                            cls="mr-2"
                        ),
                        Button(
                            Icon("lucide:shopping-cart", cls="h-4 w-4 mr-2"),
                            ds_text("$addedToCart ? 'Added!' : 'Add to Cart'"),
                            ds_disabled="$addingToCart",
                            ds_on_click="$addingToCart = true; setTimeout(() => { $addedToCart = true; $addingToCart = false; setTimeout(() => $addedToCart = false, 2000); }, 800)",
                            ds_class={
                                "bg-green-600 hover:bg-green-700": "$addedToCart",
                                "opacity-50 cursor-not-allowed": "$addingToCart"
                            },
                            size="sm"
                        ),
                        cls="flex w-full gap-2"
                    )
                ),
                
                # Product interaction state
                ds_signals(
                    selectedColor=value("titanium"),
                    favorited=False,
                    addedToCart=False,
                    addingToCart=False
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
                                 ds_class={"fill-current text-red-500": "$favorited2"}),
                            ds_text("$favorited2 ? 'Favorited' : 'Add to Favorites'"),
                            variant="outline", size="sm",
                            ds_on_click=toggle_signal("favorited2"),
                            cls="mr-2"
                        ),
                        Button(
                            Icon("lucide:shopping-cart", cls="h-4 w-4 mr-2"),
                            ds_text("$addedToCart2 ? 'Added!' : 'Add to Cart'"),
                            ds_disabled="$addingToCart2",
                            ds_on_click="$addingToCart2 = true; setTimeout(() => { $addedToCart2 = true; $addingToCart2 = false; setTimeout(() => $addedToCart2 = false, 2000); }, 800)",
                            ds_class={
                                "bg-green-600 hover:bg-green-700": "$addedToCart2",
                                "opacity-50 cursor-not-allowed": "$addingToCart2"
                            },
                            size="sm"
                        ),
                        cls="flex w-full gap-2"
                    )
                ),
                
                # Product interaction state
                ds_signals(
                    favorited2=False,
                    addedToCart2=False,
                    addingToCart2=False
                ),
                
                cls="w-full max-w-xs hover:shadow-lg transition-shadow duration-200"
            ),
            
            cls="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-2xl"
        ),
        '''Card(
    CardContent(
        Div(
            # Product image
            Div("📱", cls="text-6xl h-32 bg-gray-50 rounded-lg mb-4"),
            
            CardTitle("iPhone 15 Pro"),
            CardDescription("Natural Titanium, 128GB"),
            
            # Rating
            Div(
                Span("★★★★★", cls="text-yellow-400 text-sm"),
                Span("4.9 (1,234 reviews)", cls="text-sm text-muted-foreground ml-2")
            ),
            
            # Price
            Div(
                Span("$999", cls="text-2xl font-bold text-primary"),
                Span("$1,099", cls="text-sm line-through text-muted-foreground"),
                Badge("9% OFF", variant="destructive")
            ),
            
            # Color selection
            Div(
                P("Color:", cls="text-sm font-medium"),
                Div(
                    Button("", cls="w-8 h-8 rounded-full bg-gray-800 border-2",
                           ds_class={"border-primary": "$selectedColor === 'titanium'"},
                           ds_on_click="$selectedColor = 'titanium'"),
                    # More color options...
                )
            )
        )
    ),
    CardFooter(
        Button(
            Icon("lucide:heart", ds_class={"fill-current text-red-500": "$favorited"}),
            ds_text("$favorited ? 'Favorited' : 'Add to Favorites'"),
            variant="outline",
            ds_on_click=toggle_signal("favorited")
        ),
        Button(
            Icon("lucide:shopping-cart"),
            ds_text("$addedToCart ? 'Added!' : 'Add to Cart'"),
            ds_on_click="addToCart()"
        )
    ),
    ds_signals(selectedColor="titanium", favorited=False, addedToCart=False)
)''',
        title="Product Cards",
        description="E-commerce product cards with color selection, favorites, and cart functionality"
    )


def create_card_docs():
    """Create card documentation page using convention-based approach."""
    from utils import auto_generate_page
    
    # Hero example - basic card structure
    hero_example = ComponentPreview(
        Card(
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
        ),
        '''Card(
    CardHeader(
        CardTitle("Card Title"),
        CardDescription("Card description with supporting text below.")
    ),
    CardContent(
        P("This is the main content area of the card.")
    ),
    CardFooter(
        Button("Action"),
        Button("Cancel", variant="outline")
    )
)'''
    )
    
    return auto_generate_page(
        TITLE,
        DESCRIPTION,
        list(examples()),
        cli_command="star add card",
        hero_example=hero_example,
        component_slug="card",
        api_reference={
            "components": [
                {
                    "name": "Card",
                    "description": "The main card container"
                },
                {
                    "name": "CardHeader",
                    "description": "Contains the card title and description"
                },
                {
                    "name": "CardTitle",
                    "description": "The main heading of the card"
                },
                {
                    "name": "CardDescription",
                    "description": "Supporting text for the card title"
                },
                {
                    "name": "CardContent",
                    "description": "The main content area of the card"
                },
                {
                    "name": "CardFooter",
                    "description": "Contains actions and additional information"
                }
            ]
        }
    )