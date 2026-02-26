TITLE = "Card"
DESCRIPTION = "Displays a card with header, content, and footer."
CATEGORY = "layout"
ORDER = 10
STATUS = "stable"

from starhtml import Div, P, H3, Span, Icon, A, Signal, match, switch, all_
from starhtml.datastar import js, set_timeout
from starui.registry.components.card import (
    Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter
)
from starui.registry.components.button import Button
from starui.registry.components.badge import Badge
from starui.registry.components.input import Input
from starui.registry.components.label import Label
from utils import auto_generate_page, Component, build_api_reference, with_code
from widgets.component_preview import ComponentPreview



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


@with_code
def interactive_profile_cards_example():
    profiles = [
        {
            "id": "jdoe",
            "initials": "JD",
            "avatar_color": "bg-blue-500",
            "name": "John Doe",
            "role": "Product Designer",
            "status": "online",
            "status_color": "bg-green-100 text-green-800",
            "bio": "Passionate about creating user-centered designs that solve real problems.",
            "following": False
        },
        {
            "id": "asmith",
            "initials": "AS",
            "avatar_color": "bg-green-500",
            "name": "Anna Smith",
            "role": "Frontend Developer",
            "status": "away",
            "status_color": "bg-yellow-100 text-yellow-800",
            "bio": "Full-stack developer with expertise in Python and modern web technologies.",
            "following": False
        }
    ]

    for p in profiles:
        p["follow_signal"] = Signal(f"following_{p['id']}", p["following"])

    profile_cards = [
        Card(
            CardHeader(
                Div(
                    Div(p["initials"], cls=f"w-12 h-12 rounded-full {p['avatar_color']} flex items-center justify-center text-white font-bold"),
                    Div(
                        CardTitle(p["name"], cls="text-lg"),
                        CardDescription(p["role"]),
                        Badge(p["status"], variant="default", cls=f"{p['status_color']} text-xs"),
                        cls="ml-4 space-y-1"
                    ),
                    cls="flex items-center"
                )
            ),
            CardContent(
                P(p["bio"], cls="text-sm text-muted-foreground")
            ),
            CardFooter(
                Button(
                    data_text=p["follow_signal"].if_("Following", "Follow"),
                    data_on_click=p["follow_signal"].toggle(),
                    variant="outline",
                    size="sm",
                    cls="mr-2",
                    data_attr_cls=p["follow_signal"].if_("bg-green-50 text-green-700 border-green-200 hover:bg-green-100 hover:text-green-800")
                ),
                Button("Message", size="sm", data_on_click=f"alert('Message sent to {p['name'].split()[0]}!')")
            )
        )
        for p in profiles
    ]

    return Div(
        *[p["follow_signal"] for p in profiles],
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

    revenue_card = Card(
        CardHeader(
            Icon("lucide:dollar-sign", cls="h-6 w-6 text-green-600 mb-2"),
            CardTitle("Total Revenue", cls="text-sm font-medium"),
            CardDescription(data_text=match(period, **{"1d": "Today", "7d": "Last 7 days", "30d": "Last 30 days", "365d": "Last 365 days"}))
        ),
        CardContent(
            Span(data_text="$" + revenue.toLocaleString(), cls="text-2xl font-bold tracking-tight block mb-1"),
            P(
                Span(
                    data_text=(revenue_change >= 0).if_("+", "") + revenue_change + "%",
                    cls="font-medium",
                    data_attr_cls=switch([
                        (revenue_change > 0, "text-green-600"),
                        (revenue_change < 0, "text-red-600")
                    ], default="text-gray-500")
                ),
                " from last period",
                cls="text-sm text-muted-foreground"
            )
        )
    )

    users_card = Card(
        CardHeader(
            Icon("lucide:users", cls="h-6 w-6 text-blue-600 mb-2"),
            CardTitle("Active Users", cls="text-sm font-medium"),
            CardDescription(data_text=match(period, **{"1d": "Today", "7d": "Daily average", "30d": "Daily average", "365d": "Monthly average"}))
        ),
        CardContent(
            Span(data_text=users.toLocaleString(), cls="text-2xl font-bold tracking-tight block mb-1"),
            P(
                Span(
                    data_text=(users_change >= 0).if_("+", "") + users_change + "%",
                    cls="font-medium",
                    data_attr_cls=switch([
                        (users_change > 0, "text-green-600"),
                        (users_change < 0, "text-red-600")
                    ], default="text-gray-500")
                ),
                " from last period",
                cls="text-sm text-muted-foreground"
            )
        )
    )

    conversion_card = Card(
        CardHeader(
            Icon("lucide:trending-up", cls="h-6 w-6 text-purple-600 mb-2"),
            CardTitle("Conversion Rate", cls="text-sm font-medium"),
            CardDescription(data_text=match(period, **{"1d": "Today", "7d": "This week", "30d": "This month", "365d": "This year"}))
        ),
        CardContent(
            Span(data_text=conversion + "%", cls="text-2xl font-bold tracking-tight block mb-1"),
            P(
                Span(
                    data_text=(conversion_change >= 0).if_("+", "") + conversion_change + "%",
                    cls="font-medium",
                    data_attr_cls=switch([
                        (conversion_change > 0, "text-green-600"),
                        (conversion_change < 0, "text-red-600")
                    ], default="text-gray-500")
                ),
                " from last period",
                cls="text-sm text-muted-foreground"
            )
        )
    )

    period_data = [
        ("Today", "1d", 3421, 12.3, 573, 5.2, 2.8, 0.2),
        ("Week", "7d", 24567, 18.5, 1847, 8.9, 3.1, 0.4),
        ("Month", "30d", 98234, 23.2, 7892, 15.7, 3.4, -0.1),
        ("Year", "365d", 892451, 42.8, 45123, 31.2, 3.9, 0.8),
    ]

    return Div(
        period, revenue, revenue_change, users, users_change, conversion, conversion_change,

        Div(
            Icon("lucide:bar-chart-3", cls="h-5 w-5 text-muted-foreground mr-2"),
            H3("Dashboard Overview", cls="text-lg font-semibold"),
            cls="flex items-center mb-2"
        ),
        P("Track your key metrics across different time periods", cls="text-sm text-muted-foreground mb-4"),

        Div(
            *[
                Button(
                    label,
                    data_on_click=[
                        period.set(period_val),
                        revenue.set(rev),
                        revenue_change.set(rev_change),
                        users.set(usr),
                        users_change.set(usr_change),
                        conversion.set(conv),
                        conversion_change.set(conv_change)
                    ],
                    size="sm",
                    variant="ghost",
                    data_class_bg_muted=period.eq(period_val)
                )
                for label, period_val, rev, rev_change, usr, usr_change, conv, conv_change in period_data
            ],
            cls="inline-flex items-center justify-center rounded-md bg-muted/30 p-1 text-muted-foreground mb-6"
        ),

        Div(
            revenue_card,
            users_card,
            conversion_card,
            cls="grid grid-cols-1 md:grid-cols-3 gap-4"
        ),

        cls="w-full"
    )


@with_code
def interactive_form_card_example():
    email = Signal("email", "")
    password = Signal("password", "")
    confirm = Signal("confirm", "")

    email_valid = Signal("email_valid", email.contains("@") & email.contains("."))
    password_valid = Signal("password_valid", password.length >= 8)
    passwords_match = Signal("passwords_match", password.eq(confirm) & (confirm.length > 0))
    form_valid = Signal("form_valid", all_(email_valid, password_valid, passwords_match))

    return Card(
        email, password, confirm, email_valid, password_valid, passwords_match, form_valid,
        CardHeader(
            CardTitle("Create Account"),
            CardDescription("Enter your details below to create your account")
        ),
        CardContent(
            Div(
                Div(
                    Label("Email", fr="email"),
                    Input(
                        type="email",
                        id="email",
                        placeholder="name@example.com",
                        signal=email,
                        cls="w-full"
                    ),
                    P(
                        Icon("lucide:check-circle", cls="h-3 w-3 mr-1 inline-block"),
                        "Valid email",
                        data_show=email_valid & (email.length > 0),
                        cls="text-xs text-green-600 mt-1"
                    ),
                    cls="space-y-2"
                ),
                Div(
                    Label("Password", fr="password"),
                    Input(
                        type="password",
                        id="password",
                        placeholder="Enter your password",
                        signal=password,
                        cls="w-full"
                    ),
                    P(
                        data_text=password_valid.if_("✓ Strong password", "At least 8 characters required"),
                        data_show=password.length > 0,
                        cls="text-xs mt-1",
                        data_attr_cls=password_valid.if_("text-green-600", "text-muted-foreground")
                    ),
                    cls="space-y-2"
                ),
                Div(
                    Label("Confirm Password", fr="confirm"),
                    Input(
                        type="password",
                        id="confirm",
                        placeholder="Confirm your password",
                        signal=confirm,
                        cls="w-full"
                    ),
                    P(
                        data_text=passwords_match.if_("✓ Passwords match", "Passwords must match"),
                        data_show=confirm.length > 0,
                        cls="text-xs mt-1",
                        data_attr_cls=passwords_match.if_("text-green-600", "text-red-600")
                    ),
                    cls="space-y-2"
                ),
                cls="space-y-4"
            )
        ),
        CardFooter(
            Div(
                Button(
                    data_text=form_valid.if_("Create Account ✓", "Create Account"),
                    data_on_click=js("alert('Account created for ' + $email + '!')"),
                    data_attr_disabled=~form_valid,
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
    macbook_in_cart = Signal("macbook_in_cart", True)
    airpods_in_cart = Signal("airpods_in_cart", True)
    checking_out = Signal("checking_out", False)

    item_count = Signal("item_count", macbook_in_cart + airpods_in_cart)
    total = Signal("total", macbook_in_cart * 2399 + airpods_in_cart * 249)

    def cart_item(emoji, name, description, price, in_cart_signal, border=True):
        return Div(
            Div(
                Div(emoji, cls="text-2xl mr-3"),
                Div(
                    P(name, cls="font-medium text-sm"),
                    P(description, cls="text-xs text-muted-foreground"),
                    cls="flex-1"
                ),
                cls="flex items-start"
            ),
            Div(
                P(price, cls="font-bold text-sm"),
                Button(
                    Icon("lucide:trash-2", cls="h-3 w-3"),
                    data_on_click=in_cart_signal.set(False),
                    variant="ghost", size="sm",
                    cls="ml-2 p-1 h-6 w-6"
                ),
                cls="flex items-center"
            ),
            data_show=in_cart_signal,
            cls=f"flex items-start justify-between py-2{' border-b' if border else ''}"
        )

    empty_cart_state = Div(
        Div("🛍️", cls="text-5xl text-center mb-3"),
        P("Your cart is empty", cls="text-center text-muted-foreground font-medium"),
        P("Add some items to get started", cls="text-center text-sm text-muted-foreground"),
        data_show=item_count == 0,
        cls="py-8"
    )

    pricing_summary = Div(
        Div(
            Span("Subtotal: ", cls="text-sm"),
            Span(data_text="$" + total.toFixed(2), cls="font-bold"),
            cls="flex justify-between w-full mb-2"
        ),
        Div(
            Span("Tax: ", cls="text-sm"),
            Span(data_text="$" + (total * 0.08).toFixed(2), cls="text-sm"),
            cls="flex justify-between w-full mb-2 text-muted-foreground"
        ),
        Div(
            Span("Total: ", cls="font-medium"),
            Span(data_text="$" + (total * 1.08).toFixed(2), cls="font-bold text-lg"),
            cls="flex justify-between w-full border-t pt-2 mt-2"
        ),
        data_show=item_count > 0,
        cls="w-full mb-4"
    )

    add_items_button = Div(
        Button(
            "Add Sample Items",
            data_on_click=[macbook_in_cart.set(True), airpods_in_cart.set(True)],
            variant="outline", size="sm",
            cls="w-full mb-2"
        ),
        data_show=item_count == 0
    )

    checkout_button = Button(
        data_on_click=[
            checking_out.set(True),
            set_timeout([
                js("alert('Order placed successfully!')"),
                macbook_in_cart.set(False),
                airpods_in_cart.set(False),
                checking_out.set(False)
            ], 2000)
        ],
        data_text=checking_out.if_("Processing...", "Checkout"),
        data_attr_disabled=(item_count == 0) | checking_out,
        cls="w-full",
        data_attr_cls=((item_count == 0) | checking_out).if_("opacity-50 cursor-not-allowed", "")
    )

    return Card(
        macbook_in_cart, airpods_in_cart, checking_out, item_count, total,
        CardHeader(
            CardTitle("Shopping Cart"),
            CardDescription(data_text=item_count + " item" + (item_count != 1).if_("s", "") + " in cart")
        ),
        CardContent(
            Div(
                Div(
                    cart_item("💻", "MacBook Pro 14\"", "Space Gray, 16GB RAM", "$2,399", macbook_in_cart),
                    cart_item("🎧", "AirPods Pro (2nd gen)", "with MagSafe Case", "$249", airpods_in_cart, border=False),
                    cls="space-y-1"
                ),
                empty_cart_state,
                cls="min-h-[120px]"
            )
        ),
        CardFooter(
            Div(
                pricing_summary,
                add_items_button,
                checkout_button,
                cls="w-full"
            )
        ),
        cls="w-full max-w-md"
    )


@with_code
def notification_cards_example():
    def notification_card(icon_name, icon_color, title, message, button_text, button_action, button_variant="default"):
        return Card(
            CardContent(
                Div(
                    Icon(icon_name, cls=f"h-5 w-5 {icon_color}"),
                    Div(
                        P(title, cls="font-medium text-sm"),
                        P(message, cls="text-sm text-muted-foreground"),
                        cls="ml-3 flex-1"
                    ),
                    cls="flex items-start"
                ),
                Button(
                    button_text,
                    variant=button_variant,
                    size="sm",
                    cls="mt-3",
                    data_on_click=button_action
                ),
                cls="p-4"
            )
        )

    return Div(
        notification_card(
            "lucide:check-circle",
            "text-green-500",
            "Payment successful",
            "Your payment has been processed successfully.",
            "View Receipt",
            "alert('Receipt downloaded!')",
            "ghost"
        ),
        notification_card(
            "lucide:alert-circle",
            "text-orange-500",
            "Action required",
            "Please verify your email address to continue.",
            "Verify Email",
            "alert('Verification email sent!')",
            "ghost"
        ),
        cls="space-y-3 max-w-md"
    )


@with_code
def product_ecommerce_cards_example():
    selected_color = Signal("selected_color", "titanium")
    favorited = Signal("favorited", False)
    just_added = Signal("just_added", False)

    titanium_qty = Signal("titanium_qty", 0)
    blue_qty = Signal("blue_qty", 0)
    white_qty = Signal("white_qty", 0)

    favorited2 = Signal("favorited2", False)
    airpods_qty = Signal("airpods_qty", 0)
    just_added2 = Signal("just_added2", False)

    cart_count = Signal("cart_count", titanium_qty + blue_qty + white_qty + airpods_qty)

    def product_card(emoji, title, description, price, reviews, special_badge, features, signals, has_color_picker=False, color_quantities=None):
        if has_color_picker and color_quantities:
            fav_signal, animation_signal = signals
            titanium_sig, blue_sig, white_sig = color_quantities['titanium'], color_quantities['blue'], color_quantities['white']
        else:
            fav_signal, cart_signal, animation_signal = signals

        card_content = [
            Div(emoji, cls="text-6xl flex items-center justify-center h-32 bg-gray-50 rounded-lg mb-4"),
            Div(
                CardTitle(title, cls="text-lg mb-1"),
                CardDescription(description),
                Div(
                    Span("★★★★★", cls="text-yellow-400 text-sm"),
                    Span(reviews, cls="text-sm text-muted-foreground ml-2"),
                    cls="flex items-center mt-2 mb-3"
                ),
                Div(
                    Span(price, cls="text-2xl font-bold text-primary" + (" mr-2" if special_badge else "")),
                    special_badge if special_badge else None,
                    cls="flex items-center mb-4"
                )
            )
        ]

        if has_color_picker:
            colors = [("titanium", "bg-gray-800"), ("blue", "bg-blue-500"), ("white", "bg-white")]
            card_content[1] = Div(
                *card_content[1].children[:4],
                Div(
                    P("Color:", cls="text-sm font-medium mb-2"),
                    Div(
                        *[Button(
                            "",
                            variant="ghost",
                            size="sm",
                            cls=f"w-8 h-8 rounded-full {color_cls} border-2 p-0 {'ml-2' if i > 0 else ''} hover:scale-110 transition-transform",
                            data_attr_cls=selected_color.eq(color_name).if_("border-primary ring-2 ring-primary ring-offset-2", "border-gray-300"),
                            data_on_click=selected_color.set(color_name)
                        ) for i, (color_name, color_cls) in enumerate(colors)],
                        cls="flex items-center"
                    ),
                    cls="mb-4"
                )
            )
        elif features:
            card_content[1] = Div(
                *card_content[1].children,
                Div(*[P(feat, cls="text-sm text-muted-foreground mb-1") for feat in features], cls="mb-4")
            )

        return Card(
            CardContent(Div(*card_content, cls="p-6")),
            CardFooter(
                Button(
                    Icon("lucide:heart", cls="h-4 w-4 mr-2",
                    data_attr_cls=fav_signal.if_("fill-current text-red-500", "")),
                    data_text=fav_signal.if_("Favorited", "Add to Favorites"),
                    variant="outline",
                    size="sm",
                    data_on_click=fav_signal.toggle(),
                    cls="min-w-[140px] select-none"
                ),
                Button(
                    Icon("lucide:shopping-cart", cls="h-4 w-4 mr-2", data_show=~animation_signal),
                    Icon("lucide:check", cls="h-4 w-4 mr-2", data_show=animation_signal),
                    data_text=animation_signal.if_("Added!", "Add to Cart"),
                    data_on_click=(
                        [cart_signal.add(1), animation_signal.set(True), set_timeout([animation_signal.set(False)], 1000)]
                        if not has_color_picker else
                        # Boolean signals (.eq) evaluate to 0 or 1, enabling conditional increment
                        [
                            titanium_sig.set(titanium_sig + selected_color.eq("titanium")),
                            blue_sig.set(blue_sig + selected_color.eq("blue")),
                            white_sig.set(white_sig + selected_color.eq("white")),
                            animation_signal.set(True),
                            set_timeout([animation_signal.set(False)], 1000)
                        ]
                    ),
                    data_attr_disabled=animation_signal,
                    variant="outline",
                    size="sm",
                    cls="flex-1 min-w-[120px] select-none",
                    data_attr_cls=animation_signal.if_("bg-green-50 text-green-700 border-green-300 hover:bg-green-100")
                ),
                cls="flex gap-2"
            ),
            cls="w-full max-w-xs hover:shadow-lg transition-shadow duration-200"
        )

    return Div(
        selected_color, favorited, just_added, titanium_qty, blue_qty, white_qty, favorited2, airpods_qty, just_added2, cart_count,

        # Cart indicator
        Div(
            Div(
                Div(
                    Icon("lucide:shopping-cart", cls="h-5 w-5 mr-2"),
                    Span("Shopping Cart", cls="font-semibold text-lg"),
                    cls="flex items-center mb-3"
                ),
                Div(
                    *[Div(
                        Span("• ", cls="mr-2"),
                        Span(f"iPhone 15 Pro - {color} ", cls="font-medium"),
                        Span(data_text="(x" + qty + ")", cls="text-muted-foreground"),
                        data_show=qty > 0,
                        cls="text-sm mb-1"
                    ) for color, qty in [("Titanium", titanium_qty), ("Blue", blue_qty), ("White", white_qty)]],
                    Div(
                        Span("• ", cls="mr-2"),
                        Span("AirPods Pro (2nd gen) ", cls="font-medium"),
                        Span(data_text="(x" + airpods_qty + ")", cls="text-muted-foreground"),
                        data_show=airpods_qty > 0,
                        cls="text-sm mb-1"
                    ),
                    P(
                        "No items in cart",
                        data_show=cart_count == 0,
                        cls="text-sm text-muted-foreground italic"
                    ),
                    cls="space-y-1"
                ),
                Div(
                    Span("Total items: ", cls="text-sm text-muted-foreground"),
                    Span(data_text=cart_count, cls="font-bold text-primary"),
                    data_show=cart_count > 0,
                    cls="mt-3 pt-3 border-t"
                )
            ),
            cls="mb-8 p-4 bg-muted/50 rounded-lg border"
        ),

        # Product cards
        Div(
            product_card(
                "📱",
                "iPhone 15 Pro",
                "Natural Titanium, 128GB",
                "$999",
                "4.9 (1,234 reviews)",
                Div(Span("$1,099", cls="text-sm line-through text-muted-foreground"), Badge("9% OFF", variant="destructive", cls="ml-2")),
                None,
                (favorited, just_added),
                has_color_picker=True,
                color_quantities={
                    'titanium': titanium_qty,
                    'blue': blue_qty,
                    'white': white_qty
                }
            ),
            product_card(
                "🎧",
                "AirPods Pro",
                "2nd Generation with MagSafe",
                "$249",
                "4.8 (892 reviews)",
                Badge("Best Seller", variant="secondary", cls="ml-2"),
                ["✓ Active Noise Cancellation", "✓ Spatial Audio", "✓ 6hr battery + 24hr case"],
                (favorited2, airpods_qty, just_added2)
            ),
            cls="grid grid-cols-1 md:grid-cols-2 gap-6"
        ),

        cls="w-full max-w-2xl"
    )


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


EXAMPLES_DATA = [
    {"title": "Card", "description": "Display content in a card with header, content, and footer", "fn": hero_card_example},
    {"title": "Interactive Profile Cards", "description": "Profile cards with follow/unfollow functionality and status badges", "fn": interactive_profile_cards_example},
    {"title": "Interactive Dashboard Stats", "description": "Dynamic stats cards with period selection and real-time updates", "fn": interactive_dashboard_stats_example},
    {"title": "Interactive Form Card", "description": "Form with real-time validation and dynamic button states", "fn": interactive_form_card_example},
    {"title": "Interactive Shopping Cart", "description": "Dynamic cart with add/remove items, total calculation, and checkout flow", "fn": interactive_shopping_cart_example},
    {"title": "Interactive Notifications", "description": "Alert and notification cards with action handlers", "fn": notification_cards_example},
    {"title": "Product Cards", "description": "E-commerce product cards with color selection, favorites, and cart functionality", "fn": product_ecommerce_cards_example},
]


def create_card_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)