"""
Sheet component documentation - Sliding side panels.
Versatile overlay panels for navigation, filters, settings, and forms.
"""

# Component metadata for auto-discovery
TITLE = "Sheet"
DESCRIPTION = "A side panel component that slides in from the screen edge. Perfect for navigation menus, filter panels, settings drawers, and detail views."
CATEGORY = "overlay"
ORDER = 150
STATUS = "stable"

import re

from starhtml import Div, P, H3, H4, Span, Icon, Img, Form, Hr, Signal, js
from starui.registry.components.sheet import (
    Sheet, SheetTrigger, SheetContent, SheetClose,
    SheetHeader, SheetFooter, SheetTitle, SheetDescription
)
from starui.registry.components.button import Button
from starui.registry.components.input import InputWithLabel
from starui.registry.components.textarea import TextareaWithLabel
from starui.registry.components.badge import Badge
from starui.registry.components.separator import Separator
from starui.registry.components.select import SelectWithLabel, Select, SelectTrigger, SelectValue, SelectContent, SelectItem
from starui.registry.components.checkbox import CheckboxWithLabel
from starui.registry.components.avatar import Avatar
from starui.registry.components.switch import Switch
from utils import auto_generate_page, with_code, Component, build_api_reference


@with_code
def navigation_menu_sheet_example():
    def NavItem(icon, label, badge=None):
        def item(*, sheet_open, **_):
            return Div(
                Icon(icon, cls="h-4 w-4 mr-3"),
                Span(label),
                Badge(badge, variant="secondary", cls="ml-auto") if badge else None,
                data_on_click=sheet_open.set(False),
                cls="flex items-center py-3 px-4 rounded-lg hover:bg-muted/50 cursor-pointer transition-colors"
            )
        return item

    return Sheet(
        SheetTrigger(
            Icon("lucide:menu", cls="h-4 w-4 mr-2"),
            "Menu",
            variant="outline"
        ),
        SheetContent(
            SheetHeader(
                SheetTitle("Navigation"),
                SheetDescription("Browse through the app sections")
            ),
            Div(
                NavItem("lucide:home", "Home"),
                NavItem("lucide:bar-chart-3", "Dashboard"),
                NavItem("lucide:users", "Team"),
                NavItem("lucide:folder", "Projects", badge="12"),
                Separator(cls="my-4"),
                NavItem("lucide:settings", "Settings"),
                NavItem("lucide:help-circle", "Help & Support"),
                cls="space-y-1 px-6 flex-1 overflow-hidden"
            ),
            SheetFooter(
                Div(
                    Avatar(
                        Img(src="https://github.com/shadcn.png", alt="User"),
                        size="sm",
                        cls="mr-3"
                    ),
                    Div(
                        P("John Doe", cls="text-sm font-medium"),
                        P("john@example.com", cls="text-xs text-muted-foreground"),
                        cls="flex-1"
                    ),
                    SheetClose(
                        Icon("lucide:log-out", cls="h-4 w-4"),
                        variant="ghost",
                        size="icon",
                        cls="ml-2"
                    ),
                    cls="flex items-center w-full"
                )
            ),
            side="left",
            size="md"
        ),        
    )


@with_code
def shopping_cart_sheet_example():
    price_headphones = 99.99
    price_shoes = 129.99
    shipping = 9.99
    tax_rate = 0.08

    qty_headphones = Signal("qty_headphones", 1)
    qty_shoes = Signal("qty_shoes", 2)
    subtotal = Signal("subtotal", qty_headphones * price_headphones + qty_shoes * price_shoes)
    tax = Signal("tax", subtotal * tax_rate)
    total = Signal("total", subtotal + tax + shipping)
    total_items = Signal("total_items", qty_headphones + qty_shoes)

    def create_cart_item(image_url, name, description, price_str, qty_signal):
        return Div(
            Img(
                src=image_url,
                alt="Product",
                cls="w-16 h-16 rounded-lg object-cover"
            ),
            Div(
                H4(name, cls="text-sm font-medium"),
                P(description, cls="text-xs text-muted-foreground"),
                Div(
                    Span(price_str, cls="text-sm font-bold"),
                    Div(
                        Button(
                            "-",
                            data_on_click=(qty_signal > 0).then(qty_signal.add(-1)),
                            size="sm",
                            variant="outline",
                            cls="h-6 w-6 p-0"
                        ),
                        Span(data_text=qty_signal, cls="mx-2 text-sm"),
                        Button(
                            "+",
                            data_on_click=qty_signal.add(1),
                            size="sm",
                            variant="outline",
                            cls="h-6 w-6 p-0"
                        ),
                        cls="flex items-center ml-auto"
                    ),
                    cls="flex items-center justify-between mt-2"
                ),
                cls="flex-1 ml-3"
            ),
            cls="flex items-start p-4 border-b"
        )

    return Sheet(
        SheetTrigger(
            Icon("lucide:shopping-cart", cls="h-4 w-4 mr-2"),
            Span("Cart (", Span(data_text=total_items), ")"),
            variant="outline"
        ),
        SheetContent(
            SheetHeader(
                SheetTitle("Shopping Cart"),
                SheetDescription(
                    Span(data_text=total_items + " items in your cart")
                )
            ),
            Div(
                qty_headphones, qty_shoes, subtotal, tax, total, total_items,
                create_cart_item(
                    "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=100&h=100&fit=crop",
                    "Wireless Headphones",
                    "Premium quality sound",
                    f"${price_headphones}",
                    qty_headphones
                ),
                create_cart_item(
                    "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=100&h=100&fit=crop",
                    "Running Shoes",
                    "Comfortable and durable",
                    f"${price_shoes}",
                    qty_shoes
                ),
                Div(
                    Div(
                        Div(
                            Span("Subtotal", cls="text-sm"),
                            Span("$", data_text=js("$subtotal.toFixed(2)"), cls="text-sm font-bold"),
                            cls="flex justify-between"
                        ),
                        Div(
                            Span("Shipping", cls="text-sm"),
                            Span(f"${shipping}", cls="text-sm"),
                            cls="flex justify-between"
                        ),
                        Div(
                            Span(f"Tax ({int(tax_rate * 100)}%)", cls="text-sm"),
                            Span("$", data_text=js("$tax.toFixed(2)"), cls="text-sm"),
                            cls="flex justify-between"
                        ),
                        Hr(cls="my-3"),
                        Div(
                            Span("Total", cls="text-base font-bold"),
                            Span("$", data_text=js("$total.toFixed(2)"), cls="text-base font-bold"),
                            cls="flex justify-between"
                        ),
                        cls="space-y-2"
                    ),
                    cls="p-4"
                ),
                cls="flex-1 overflow-y-auto"
            ),
            SheetFooter(
                Div(
                    SheetClose("Continue Shopping", variant="outline", size="sm", cls="flex-1 mr-2"),
                    SheetClose("Checkout", variant="default", size="sm", cls="flex-1"),
                    cls="flex gap-2 w-full"
                )
            ),
            side="right",
            size="lg"
        ),        
    )


@with_code
def filter_panel_sheet_example():
    categories = ["Electronics", "Clothing", "Books", "Home & Garden", "Sports"]
    brands = [("", "Any Brand"), ("apple", "Apple"), ("samsung", "Samsung"), ("nike", "Nike"), ("sony", "Sony")]

    min_price = Signal("min_price", "")
    max_price = Signal("max_price", "")
    category_signals = {cat: Signal(f"cat_{re.sub(r'[^a-z0-9]+', '_', cat.lower())}", False) for cat in categories}
    selected_brand = Signal("selected_brand", "")
    min_rating = Signal("min_rating", 1)

    def PriceRangeSection():
        return Div(
            H3("Price Range", cls="text-sm font-semibold mb-3"),
            Div(
                InputWithLabel(label="Min Price", type="number", placeholder="$0", signal=min_price, cls="mb-3"),
                InputWithLabel(label="Max Price", type="number", placeholder="$1000", signal=max_price),
                cls="space-y-2"
            ),
            cls="mb-6"
        )

    def CategoriesSection():
        return Div(
            H3("Categories", cls="text-sm font-semibold mb-3"),
            Div(
                *[CheckboxWithLabel(label=cat, signal=category_signals[cat]) for cat in categories],
                cls="space-y-3"
            ),
            cls="mb-6"
        )

    def BrandSection():
        return Div(
            H3("Brand", cls="text-sm font-semibold mb-3"),
            SelectWithLabel(label="Select Brand", options=brands, signal=selected_brand, show_label=False),
            cls="mb-6"
        )

    def RatingSection():
        return Div(
            H3("Minimum Rating", cls="text-sm font-semibold mb-3"),
            Div(
                Div(
                    *[Span("★", data_on_click=min_rating.set(i+1), data_attr_cls=(min_rating >= i+1).if_("text-yellow-500", "text-gray-300"), cls="text-xl cursor-pointer transition-colors hover:text-yellow-400") for i in range(5)],
                    cls="flex gap-1"
                ),
                Span(data_text=(min_rating > 0).if_(min_rating + "+ stars", "Any rating"), cls="text-sm text-muted-foreground mt-2"),
                cls="space-y-2"
            ),
            cls="mb-6"
        )

    return Sheet(
        SheetTrigger(
            Icon("lucide:sliders-horizontal", cls="h-4 w-4 mr-2"),
            "Filters",
            variant="outline"
        ),
        SheetContent(
            SheetHeader(
                SheetTitle("Filter Products"),
                SheetDescription("Refine your search results")
            ),
            Div(
                min_price, max_price, *category_signals.values(), selected_brand, min_rating,
                PriceRangeSection(),
                CategoriesSection(),
                BrandSection(),
                RatingSection(),
                cls="px-6 flex-1 overflow-y-auto"
            ),
            SheetFooter(
                Div(
                    Button(
                        "Clear All",
                        variant="outline",
                        size="sm",
                        cls="flex-1 mr-2",
                        data_on_click=[
                            min_price.set(""),
                            max_price.set(""),
                            *[sig.set(False) for sig in category_signals.values()],
                            selected_brand.set(""),
                            min_rating.set(1)
                        ]
                    ),
                    SheetClose(
                        "Apply Filters",
                        variant="default",
                        size="sm",
                        cls="flex-1"
                    ),
                    cls="flex gap-2 w-full"
                )
            ),
            side="left",
            size="sm"
        ),        
    )


@with_code
def settings_drawer_sheet_example():
    theme_pref = Signal("theme_pref", "system")
    language_pref = Signal("language_pref", "en")
    push_notifications = Signal("push_notifications", True)
    email_notifications = Signal("email_notifications", True)

    return Sheet(
        SheetTrigger(
            Icon("lucide:settings", cls="h-4 w-4 mr-2"),
            "Settings",
            variant="outline"
        ),
        SheetContent(
            SheetHeader(
                SheetTitle("Application Settings"),
                SheetDescription("Customize your experience")
            ),
            Div(
                theme_pref, language_pref, push_notifications, email_notifications,
                Div(
                    H3("Account", cls="text-sm font-semibold mb-3"),
                    Div(
                        Avatar(Img(src="https://github.com/shadcn.png", alt="Profile"), size="md", cls="mr-3"),
                        Div(
                            H4("John Doe", cls="font-medium"),
                            P("john.doe@example.com", cls="text-sm text-muted-foreground"),
                            cls="flex-1"
                        ),
                        cls="flex items-center mb-3"
                    ),
                    Button("Edit Profile", size="sm", variant="outline", cls="w-full"),
                    cls="pb-4 mb-4 border-b"
                ),
                Div(
                    H3("Preferences", cls="text-sm font-semibold mb-3"),
                    Div(
                        Div(
                            Icon("lucide:palette", cls="h-4 w-4 text-muted-foreground"),
                            Div(P("Theme", cls="text-sm font-medium"), P("Choose your interface theme", cls="text-xs text-muted-foreground"), cls="ml-3"),
                            cls="flex items-start mb-2"
                        ),
                        Select(
                            SelectTrigger(SelectValue(), cls="w-full"),
                            SelectContent(
                                SelectItem("Light", value="light"),
                                SelectItem("Dark", value="dark"),
                                SelectItem("System", value="system")
                            ),
                            value="system",
                            label="System",
                            signal=theme_pref
                        ),
                        cls="mb-4"
                    ),
                    Div(
                        Div(
                            Icon("lucide:globe", cls="h-4 w-4 text-muted-foreground"),
                            Div(P("Language", cls="text-sm font-medium"), P("Select your preferred language", cls="text-xs text-muted-foreground"), cls="ml-3"),
                            cls="flex items-start mb-2"
                        ),
                        Select(
                            SelectTrigger(SelectValue(), cls="w-full"),
                            SelectContent(
                                SelectItem("English", value="en"),
                                SelectItem("Spanish", value="es"),
                                SelectItem("French", value="fr"),
                                SelectItem("German", value="de")
                            ),
                            value="en",
                            label="English",
                            signal=language_pref
                        ),
                        cls="mb-4"
                    ),
                    cls="pb-4 mb-4 border-b"
                ),
                Div(
                    H3("Notifications", cls="text-sm font-semibold mb-3"),
                    Div(
                        Icon("lucide:bell", cls="h-4 w-4 text-muted-foreground mt-0.5"),
                        Div(P("Push Notifications", cls="text-sm font-medium"), P("Receive notifications for important updates", cls="text-xs text-muted-foreground"), cls="ml-3 flex-1"),
                        Switch(signal=push_notifications, checked=True, cls="ml-auto"),
                        cls="flex items-start mb-4"
                    ),
                    Div(
                        Icon("lucide:mail", cls="h-4 w-4 text-muted-foreground mt-0.5"),
                        Div(P("Email Notifications", cls="text-sm font-medium"), P("Get email updates for your account", cls="text-xs text-muted-foreground"), cls="ml-3 flex-1"),
                        Switch(signal=email_notifications, checked=True, cls="ml-auto"),
                        cls="flex items-start"
                    )
                ),
                cls="px-6 flex-1 overflow-y-auto"
            ),
            SheetFooter(
                Div(
                    SheetClose("Reset to Defaults", variant="outline", size="sm", cls="flex-1 mr-2"),
                    SheetClose("Save Changes", variant="default", size="sm", cls="flex-1"),
                    cls="flex gap-2 w-full"
                )
            ),
            side="right",
            size="md"
        ),        
    )


@with_code
def notification_panel_sheet_example():
    notifications = [
        {"icon": "lucide:check-circle", "color": "text-green-500", "title": "Payment successful", "message": "Your monthly subscription has been processed", "time": "2 minutes ago"},
        {"icon": "lucide:user-plus", "color": "text-blue-500", "title": "New team member", "message": "Sarah Johnson joined your workspace", "time": "1 hour ago"},
        {"icon": "lucide:alert-triangle", "color": "text-orange-500", "title": "Action required", "message": "Please update your billing information", "time": "3 hours ago"},
        {"icon": "lucide:calendar", "color": "text-purple-500", "title": "Meeting reminder", "message": "Team standup in 15 minutes", "time": "5 hours ago"}
    ]

    notif_signals = [Signal(f"notif_{i+1}", True) for i in range(len(notifications))]
    notif_count = Signal("notif_count", sum(notif_signals))
    has_notifications = Signal("has_notifications", sum(notif_signals) > 0)

    def create_notification(icon, icon_color, title, message, time, notif_signal):
        return Div(
            Icon(icon, cls=f"h-5 w-5 {icon_color} mt-1 mr-3"),
            Div(
                P(title, cls="text-sm font-medium"),
                P(message, cls="text-xs text-muted-foreground mb-2"),
                P(time, cls="text-xs text-muted-foreground"),
                cls="flex-1"
            ),
            Button(
                Icon("lucide:x", cls="h-4 w-4"),
                data_on_click=notif_signal.set(False),
                variant="ghost",
                size="sm",
                cls="h-8 w-8 p-0 text-muted-foreground hover:text-foreground hover:bg-muted"
            ),
            style="display: none",
            data_show=notif_signal,
            cls="flex items-start p-4 border-b hover:bg-muted/30 transition-colors"
        )

    return Sheet(
        SheetTrigger(
            Icon("lucide:bell", cls="h-4 w-4 mr-2"),
            "Notifications",
            Badge(
                data_text=notif_count,
                style="display: none",
                data_show=has_notifications,
                variant="destructive",
                cls="ml-2 text-xs"
            ),
            variant="outline"
        ),
        SheetContent(
            SheetHeader(
                SheetTitle(
                    "Recent Notifications",
                    Badge(
                        data_text=notif_count.if_(notif_count, ""),
                        style="display: none",
                        data_show=has_notifications,
                        variant="destructive",
                        cls="ml-2 text-xs"
                    )
                ),
                SheetDescription("Stay up to date with your latest activity")
            ),
            Div(
                *notif_signals, notif_count, has_notifications,
                *[create_notification(n["icon"], n["color"], n["title"], n["message"], n["time"], notif_signals[i]) for i, n in enumerate(notifications)],
                Div(
                    Icon("lucide:inbox", cls="h-12 w-12 text-muted-foreground mb-2"),
                    P("No notifications", cls="text-sm text-muted-foreground"),
                    style="display: none",
                    data_show=~has_notifications,
                    cls="flex flex-col items-center justify-center py-12"
                ),
                cls="flex-1 overflow-y-auto min-h-[200px]"
            ),
            SheetFooter(
                Div(
                    Button(
                        "Mark All Read",
                        data_on_click=[sig.set(False) for sig in notif_signals],
                        variant="outline",
                        size="sm",
                        cls="flex-1 mr-2"
                    ),
                    SheetClose(
                        "View All",
                        variant="default",
                        size="sm",
                        cls="flex-1"
                    ),
                    cls="flex gap-2 w-full"
                )
            ),
            side="top",
            size="md"
        ),        
    )


@with_code
def action_sheet_example():
    standard_actions = [
        {"icon": "lucide:share", "title": "Share", "description": "Share this item with others"},
        {"icon": "lucide:copy", "title": "Copy Link", "description": "Copy the link to your clipboard"},
        {"icon": "lucide:download", "title": "Download", "description": "Save to your device"},
        {"icon": "lucide:bookmark", "title": "Add to Favorites", "description": "Save for quick access later"},
    ]

    destructive_actions = [
        {"icon": "lucide:flag", "title": "Report", "description": "Report inappropriate content", "title_class": "font-medium text-orange-600"},
        {"icon": "lucide:trash-2", "title": "Delete", "description": "Permanently remove this item", "title_class": "font-medium text-red-600"},
    ]

    def ActionItem(action):
        def item(*, sheet_open, **_):
            return Button(
                Icon(action["icon"], cls="h-5 w-5 mr-3"),
                Div(
                    P(action["title"], cls=action.get("title_class", "font-medium")),
                    P(action["description"], cls="text-sm text-muted-foreground"),
                    cls="text-left"
                ),
                data_on_click=sheet_open.set(False),
                variant="ghost",
                cls="w-full justify-start p-4 h-auto"
            )
        return item

    return Sheet(
        SheetTrigger(
            Icon("lucide:more-horizontal", cls="h-4 w-4 mr-2"),
            "Actions",
            variant="outline"
        ),
        SheetContent(
            SheetHeader(
                SheetTitle("Quick Actions"),
                SheetDescription("Choose an action to perform")
            ),
            Div(
                *[ActionItem(action) for action in standard_actions],
                Separator(cls="my-2"),
                *[ActionItem(action) for action in destructive_actions],
                cls="px-6 space-y-1"
            ),
            SheetFooter(
                SheetClose("Cancel", variant="outline", cls="w-full")
            ),
            side="bottom",
            size="md"
        ),
    )


@with_code
def contact_form_sheet_example():
    return Sheet(
        SheetTrigger(
            Icon("lucide:mail", cls="h-4 w-4 mr-2"),
            "Contact Us"
        ),
        SheetContent(
            SheetHeader(
                SheetTitle("Contact Us"),
                SheetDescription("Send us a message and we'll get back to you as soon as possible.")
            ),
            Form(
                Div(
                    (contact_name := Signal("contact_name", "")),
                    (contact_email := Signal("contact_email", "")),
                    (contact_subject := Signal("contact_subject", _ref_only=True)),
                    (contact_subject_value := Signal("contact_subject_value", _ref_only=True)),
                    (contact_message := Signal("contact_message", "")),
                    (contact_updates := Signal("contact_updates", False)),
                    InputWithLabel(label="Name", placeholder="Your full name", signal=contact_name, required=True),
                    InputWithLabel(label="Email", type="email", placeholder="your.email@example.com", signal=contact_email, required=True),
                    SelectWithLabel(
                        label="Subject",
                        options=[
                            ("", "Select a topic"),
                            ("support", "Technical Support"),
                            ("billing", "Billing Question"),
                            ("feedback", "Product Feedback"),
                            ("other", "Other")
                        ],
                        signal=contact_subject,
                        required=True
                    ),
                    TextareaWithLabel(label="Message", placeholder="Tell us how we can help you...", rows=4, signal=contact_message, required=True),
                    CheckboxWithLabel(label="I'd like to receive updates about new features and improvements", signal=contact_updates),
                    cls="space-y-4 px-6"
                )
            ),
            SheetFooter(
                Div(
                    SheetClose("Cancel", variant="outline", cls="flex-1 mr-2"),
                    Button(
                        "Send Message",
                        type="submit",
                        data_attr_disabled=~(contact_name & contact_email & contact_subject_value & contact_message),
                        data_on_click="evt.preventDefault()",
                        cls="flex-1"
                    ),
                    cls="flex gap-2 w-full"
                )
            ),
            side="right",
            size="lg"
        ),        
    )


@with_code
def sheet_sizes_example():
    sheet_configs = [
        {
            "button": "Small",
            "size": "sm",
            "title": "Small Sheet",
            "description": "Compact size for simple content",
            "content": "This is a small sheet (max-w-sm) - perfect for simple forms, quick actions, or narrow content."
        },
        {
            "button": "Medium",
            "size": "md",
            "title": "Medium Sheet",
            "description": "Standard size for most content",
            "content": "This is a medium sheet (max-w-md) - the default size for most use cases including forms, settings, and moderate content."
        },
        {
            "button": "Large",
            "size": "lg",
            "title": "Large Sheet",
            "description": "More space for complex content",
            "content": "This is a large sheet (max-w-lg) - great for detailed forms, complex interfaces, shopping carts, and content that needs more horizontal space."
        },
        {
            "button": "Extra Large",
            "size": "xl",
            "title": "Extra Large Sheet",
            "description": "Maximum width for extensive content",
            "content": "This is an extra large sheet (max-w-xl) - ideal for comprehensive dashboards, data tables, detailed settings panels, or any content requiring maximum horizontal space."
        }
    ]

    def create_size_demo(config):
        return Sheet(
            SheetTrigger(config["button"], variant="outline", size="sm"),
            SheetContent(
                SheetHeader(
                    SheetTitle(config["title"]),
                    SheetDescription(config["description"])
                ),
                Div(P(config["content"], cls="text-sm"), cls="px-6"),
                side="right",
                size=config["size"]
            ),
        )

    return Div(
        P("Different sheet sizes for various content needs:", cls="text-sm text-muted-foreground mb-4"),
        Div(
            *[create_size_demo(config) for config in sheet_configs],
            cls="flex flex-wrap gap-2 justify-center"
        ),
        cls="text-center"
    )


API_REFERENCE = build_api_reference(
    components=[
        Component("Sheet", "Root container that manages open state via Datastar signal"),
        Component("SheetTrigger", "Button that opens the sheet"),
        Component("SheetContent", "Panel container; supports side and size for placement and dimensions"),
        Component("SheetHeader", "Header layout area for title and description"),
        Component("SheetTitle", "Accessible title linked to content"),
        Component("SheetDescription", "Supplementary description text"),
        Component("SheetFooter", "Footer area for actions"),
        Component("SheetClose", "Action that closes the sheet"),
    ]
)


EXAMPLES_DATA = [
    {"fn": navigation_menu_sheet_example, "title": "Navigation Menu", "description": "Left-side navigation sheet with menu items and user profile"},
    {"fn": shopping_cart_sheet_example, "title": "Shopping Cart", "description": "Right-side cart drawer with product items and checkout actions"},
    {"fn": filter_panel_sheet_example, "title": "Filter Panel", "description": "Left-side filter drawer for product search with multiple filter options"},
    {"fn": settings_drawer_sheet_example, "title": "Settings Drawer", "description": "Right-side settings panel with user preferences and toggles"},
    {"fn": notification_panel_sheet_example, "title": "Notification Panel", "description": "Top-sliding notification panel with action buttons and dismissible items"},
    {"fn": action_sheet_example, "title": "Action Sheet", "description": "Bottom-sliding mobile-friendly action sheet with contextual options"},
    {"fn": contact_form_sheet_example, "title": "Contact Form", "description": "Complete contact form in a right-side sheet with validation"},
    {"fn": sheet_sizes_example, "title": "Sheet Sizes", "description": "Different sheet sizes for various content requirements"},
]


def create_sheet_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)