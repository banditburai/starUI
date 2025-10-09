"""
Sheet component documentation - Side panels/drawers that slide in from screen edges.
"""

# Component metadata for auto-discovery
TITLE = "Sheet"
DESCRIPTION = "A side panel component that slides in from the screen edge. Perfect for navigation menus, filter panels, settings drawers, and detail views."
CATEGORY = "overlay"
ORDER = 150
STATUS = "stable"

from starhtml import Div, P, H3, H4, Span, Icon, A, Img, Form, Label, Hr, Ul, Li, Strong, Signal, js
from starui.registry.components.sheet import (
    Sheet, SheetTrigger, SheetContent, SheetClose,
    SheetHeader, SheetFooter, SheetTitle, SheetDescription
)
from starui.registry.components.button import Button
from starui.registry.components.input import Input as UIInput, InputWithLabel
from starui.registry.components.textarea import TextareaWithLabel
from starui.registry.components.card import Card, CardHeader, CardContent, CardTitle, CardDescription
from starui.registry.components.badge import Badge
from starui.registry.components.separator import Separator
from starui.registry.components.select import SelectWithLabel, Select, SelectTrigger, SelectValue, SelectContent, SelectItem
from starui.registry.components.checkbox import CheckboxWithLabel
from starui.registry.components.avatar import Avatar
from starui.registry.components.switch import Switch
from utils import auto_generate_page, with_code, Component, build_api_reference
from widgets.component_preview import ComponentPreview


# ============================================================================
# EXAMPLE FUNCTIONS (decorated with @with_code for markdown generation)
# ============================================================================

# Navigation menu sheet (left side)
@with_code
def navigation_menu_sheet_example():
    return Sheet(
        SheetTrigger(
            Icon("lucide:menu", cls="h-4 w-4 mr-2"),
            "Menu",
            signal="nav_sheet",
            variant="outline"
        ),
        SheetContent(
            SheetHeader(
                SheetTitle("Navigation"),
                SheetDescription("Browse through the app sections")
            ),
            Div(
                Div(
                    Icon("lucide:home", cls="h-4 w-4 mr-3"),
                    Span("Home"),
                    cls="flex items-center py-3 px-4 rounded-lg hover:bg-muted/50 cursor-pointer transition-colors"
                ),
                Div(
                    Icon("lucide:bar-chart-3", cls="h-4 w-4 mr-3"),
                    Span("Dashboard"),
                    cls="flex items-center py-3 px-4 rounded-lg hover:bg-muted/50 cursor-pointer transition-colors"
                ),
                Div(
                    Icon("lucide:users", cls="h-4 w-4 mr-3"),
                    Span("Team"),
                    cls="flex items-center py-3 px-4 rounded-lg hover:bg-muted/50 cursor-pointer transition-colors"
                ),
                Div(
                    Icon("lucide:folder", cls="h-4 w-4 mr-3"),
                    Span("Projects"),
                    Badge("12", variant="secondary", cls="ml-auto"),
                    cls="flex items-center py-3 px-4 rounded-lg hover:bg-muted/50 cursor-pointer transition-colors"
                ),
                Separator(cls="my-4"),
                Div(
                    Icon("lucide:settings", cls="h-4 w-4 mr-3"),
                    Span("Settings"),
                    cls="flex items-center py-3 px-4 rounded-lg hover:bg-muted/50 cursor-pointer transition-colors"
                ),
                Div(
                    Icon("lucide:help-circle", cls="h-4 w-4 mr-3"),
                    Span("Help & Support"),
                    cls="flex items-center py-3 px-4 rounded-lg hover:bg-muted/50 cursor-pointer transition-colors"
                ),
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
                    Button(
                        Icon("lucide:log-out", cls="h-4 w-4"),
                        variant="ghost",
                        size="icon",
                        cls="ml-2"
                    ),
                    cls="flex items-center w-full"
                )
            ),
            signal="nav_sheet",
            side="left",
            size="md"
        ),
        signal="nav_sheet"
    )


# Shopping cart sheet (right side)
@with_code
def shopping_cart_sheet_example():
    qty_headphones = Signal("qty_headphones", 1)
    qty_shoes = Signal("qty_shoes", 2)

    def create_cart_item(image_url, name, description, price, qty_signal):
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
                    Span(price, cls="text-sm font-bold"),
                    Div(
                        Button(
                            "-",
                            data_on_click=js(f"${qty_signal} = Math.max(0, ${qty_signal} - 1)"),
                            size="sm",
                            variant="outline",
                            cls="h-6 w-6 p-0"
                        ),
                        Span(data_text=js(f"${qty_signal}"), cls="mx-2 text-sm"),
                        Button(
                            "+",
                            data_on_click=js(f"${qty_signal} = ${qty_signal} + 1"),
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
            Span(
                "Cart (",
                Span(data_text=js("$qty_headphones + $qty_shoes")),
                ")"
            ),
            signal="cart_sheet",
            variant="outline"
        ),
        SheetContent(
            SheetHeader(
                SheetTitle("Shopping Cart"),
                SheetDescription(
                    Span(data_text=js("($qty_headphones + $qty_shoes) + ' items in your cart'"))
                )
            ),
            Div(
                qty_headphones, qty_shoes,
                create_cart_item(
                    "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=100&h=100&fit=crop",
                    "Wireless Headphones",
                    "Premium quality sound",
                    "$99.99",
                    "qty_headphones"
                ),
                create_cart_item(
                    "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=100&h=100&fit=crop",
                    "Running Shoes",
                    "Comfortable and durable",
                    "$129.99",
                    "qty_shoes"
                ),
                Div(
                    Div(
                        Div(
                            Span("Subtotal", cls="text-sm"),
                            Span(
                                "$",
                                data_text=js("(($qty_headphones * 99.99 + $qty_shoes * 129.99).toFixed(2))"),
                                cls="text-sm font-bold"
                            ),
                            cls="flex justify-between"
                        ),
                        Div(
                            Span("Shipping", cls="text-sm"),
                            Span("$9.99", cls="text-sm"),
                            cls="flex justify-between"
                        ),
                        Div(
                            Span("Tax (8%)", cls="text-sm"),
                            Span(
                                "$",
                                data_text=js("((($qty_headphones * 99.99 + $qty_shoes * 129.99) * 0.08).toFixed(2))"),
                                cls="text-sm"
                            ),
                            cls="flex justify-between"
                        ),
                        Hr(cls="my-3"),
                        Div(
                            Span("Total", cls="text-base font-bold"),
                            Span(
                                "$",
                                data_text=js("(($qty_headphones * 99.99 + $qty_shoes * 129.99) * 1.08 + 9.99).toFixed(2)"),
                                cls="text-base font-bold"
                            ),
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
                    Button("Continue Shopping", variant="outline", size="sm", cls="flex-1 mr-2"),
                    Button("Checkout", size="sm", cls="flex-1"),
                    cls="flex gap-2 w-full"
                )
            ),
            signal="cart_sheet",
            side="right",
            size="lg"
        ),
        signal="cart_sheet"
    )


# Filter panel sheet (left side)
@with_code
def filter_panel_sheet_example():
    min_price = Signal("min_price", "")
    max_price = Signal("max_price", "")
    cat_electronics = Signal("cat_electronics", False)
    cat_clothing = Signal("cat_clothing", False)
    cat_books = Signal("cat_books", False)
    cat_home = Signal("cat_home", False)
    cat_sports = Signal("cat_sports", False)
    selected_brand = Signal("selected_brand", "")
    min_rating = Signal("min_rating", 1)

    return Sheet(
        SheetTrigger(
            Icon("lucide:sliders-horizontal", cls="h-4 w-4 mr-2"),
            "Filters",
            signal="filter_sheet",
            variant="outline"
        ),
        SheetContent(
            SheetHeader(
                SheetTitle("Filter Products"),
                SheetDescription("Refine your search results")
            ),
            Div(
                min_price, max_price,
                cat_electronics, cat_clothing, cat_books, cat_home, cat_sports,
                selected_brand, min_rating,
                Div(
                    H3("Price Range", cls="text-sm font-semibold mb-3"),
                    Div(
                        InputWithLabel(
                            label="Min Price",
                            type="number",
                            placeholder="$0",
                            signal="min_price",
                            cls="mb-3"
                        ),
                        InputWithLabel(
                            label="Max Price",
                            type="number",
                            placeholder="$1000",
                            signal="max_price"
                        ),
                        cls="space-y-2"
                    ),
                    cls="mb-6"
                ),
                Div(
                    H3("Categories", cls="text-sm font-semibold mb-3"),
                    Div(
                        CheckboxWithLabel(label="Electronics", signal="cat_electronics"),
                        CheckboxWithLabel(label="Clothing", signal="cat_clothing"),
                        CheckboxWithLabel(label="Books", signal="cat_books"),
                        CheckboxWithLabel(label="Home & Garden", signal="cat_home"),
                        CheckboxWithLabel(label="Sports", signal="cat_sports"),
                        cls="space-y-3"
                    ),
                    cls="mb-6"
                ),
                Div(
                    H3("Brand", cls="text-sm font-semibold mb-3"),
                    SelectWithLabel(
                        label="Select Brand",
                        options=[
                            ("", "Any Brand"),
                            ("apple", "Apple"),
                            ("samsung", "Samsung"),
                            ("nike", "Nike"),
                            ("sony", "Sony")
                        ],
                        signal="selected_brand",
                        show_label=False
                    ),
                    cls="mb-6"
                ),
                Div(
                    H3("Minimum Rating", cls="text-sm font-semibold mb-3"),
                    Div(
                        Div(
                            *[
                                Span(
                                    "★",
                                    data_on_click=js(f"$min_rating = {i+1}"),
                                    data_class=js(f"$min_rating >= {i+1} ? 'text-yellow-500' : 'text-gray-300'"),
                                    cls="text-xl cursor-pointer transition-colors hover:text-yellow-400"
                                )
                                for i in range(5)
                            ],
                            cls="flex gap-1"
                        ),
                        Span(data_text=js("$min_rating > 0 ? $min_rating + '+ stars' : 'Any rating'"), cls="text-sm text-muted-foreground mt-2"),
                        cls="space-y-2"
                    ),
                    cls="mb-6"
                ),
                cls="px-6 flex-1 overflow-y-auto"
            ),
            SheetFooter(
                Div(
                    Button(
                        "Clear All",
                        variant="outline",
                        size="sm",
                        cls="flex-1 mr-2",
                        data_on_click=js("""
                            $min_price = ''; $max_price = '';
                            $cat_electronics = false; $cat_clothing = false;
                            $cat_books = false; $cat_home = false; $cat_sports = false;
                            $selected_brand = ''; $min_rating = 1;
                        """)
                    ),
                    Button("Apply Filters", size="sm", cls="flex-1", data_on_click=js("alert('Filters applied!')")),
                    cls="flex gap-2 w-full"
                )
            ),
            signal="filter_sheet",
            side="left",
            size="sm"
        ),
        signal="filter_sheet"
    )


# Settings drawer (right side)
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
            signal="settings_sheet",
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
                            SelectTrigger(SelectValue(signal="theme_pref"), signal="theme_pref", cls="w-full"),
                            SelectContent(
                                SelectItem("light", "Light", signal="theme_pref"),
                                SelectItem("dark", "Dark", signal="theme_pref"),
                                SelectItem("system", "System", signal="theme_pref"),
                                signal="theme_pref"
                            ),
                            default_value="system",
                            default_label="System",
                            signal="theme_pref"
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
                            SelectTrigger(SelectValue(signal="language_pref"), signal="language_pref", cls="w-full"),
                            SelectContent(
                                SelectItem("en", "English", signal="language_pref"),
                                SelectItem("es", "Spanish", signal="language_pref"),
                                SelectItem("fr", "French", signal="language_pref"),
                                SelectItem("de", "German", signal="language_pref"),
                                signal="language_pref"
                            ),
                            default_value="en",
                            default_label="English",
                            signal="language_pref"
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
                        Switch(signal="push_notifications", checked=True, cls="ml-auto"),
                        cls="flex items-start mb-4"
                    ),
                    Div(
                        Icon("lucide:mail", cls="h-4 w-4 text-muted-foreground mt-0.5"),
                        Div(P("Email Notifications", cls="text-sm font-medium"), P("Get email updates for your account", cls="text-xs text-muted-foreground"), cls="ml-3 flex-1"),
                        Switch(signal="email_notifications", checked=True, cls="ml-auto"),
                        cls="flex items-start"
                    )
                ),
                cls="px-6 flex-1 overflow-y-auto"
            ),
            SheetFooter(
                Div(
                    Button("Reset to Defaults", variant="outline", size="sm", cls="flex-1 mr-2"),
                    Button("Save Changes", size="sm", cls="flex-1"),
                    cls="flex gap-2 w-full"
                )
            ),
            signal="settings_sheet",
            side="right",
            size="md"
        ),
        signal="settings_sheet"
    )


# Notification panel (top side)
@with_code
def notification_panel_sheet_example():
    notif_1 = Signal("notif_1", True)
    notif_2 = Signal("notif_2", True)
    notif_3 = Signal("notif_3", True)
    notif_4 = Signal("notif_4", True)

    def create_notification(icon, icon_color, title, message, time, signal_num):
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
                data_on_click=js(f"$notif_{signal_num} = false"),
                variant="ghost",
                size="sm",
                cls="h-8 w-8 p-0 text-muted-foreground hover:text-foreground hover:bg-muted"
            ),
            data_show=js(f"$notif_{signal_num}"),
            cls="flex items-start p-4 border-b hover:bg-muted/30 transition-colors"
        )

    return Sheet(
        SheetTrigger(
            Icon("lucide:bell", cls="h-4 w-4 mr-2"),
            "Notifications",
            Badge(
                data_text=js("""
                    let count = 0;
                    if ($notif_1) count++;
                    if ($notif_2) count++;
                    if ($notif_3) count++;
                    if ($notif_4) count++;
                    count
                """),
                data_show=js("$notif_1 || $notif_2 || $notif_3 || $notif_4"),
                variant="destructive",
                cls="ml-2 text-xs"
            ),
            signal="notifications_sheet",
            variant="outline"
        ),
        SheetContent(
            SheetHeader(
                SheetTitle(
                    "Recent Notifications",
                    Badge(
                        data_text=js("""
                            let count = 0;
                            if ($notif_1) count++;
                            if ($notif_2) count++;
                            if ($notif_3) count++;
                            if ($notif_4) count++;
                            count > 0 ? count : ''
                        """),
                        data_show=js("$notif_1 || $notif_2 || $notif_3 || $notif_4"),
                        variant="destructive",
                        cls="ml-2 text-xs"
                    )
                ),
                SheetDescription("Stay up to date with your latest activity")
            ),
            Div(
                notif_1, notif_2, notif_3, notif_4,
                create_notification(
                    "lucide:check-circle", "text-green-500",
                    "Payment successful", "Your monthly subscription has been processed",
                    "2 minutes ago", 1
                ),
                create_notification(
                    "lucide:user-plus", "text-blue-500",
                    "New team member", "Sarah Johnson joined your workspace",
                    "1 hour ago", 2
                ),
                create_notification(
                    "lucide:alert-triangle", "text-orange-500",
                    "Action required", "Please update your billing information",
                    "3 hours ago", 3
                ),
                create_notification(
                    "lucide:calendar", "text-purple-500",
                    "Meeting reminder", "Team standup in 15 minutes",
                    "5 hours ago", 4
                ),
                Div(
                    Icon("lucide:inbox", cls="h-12 w-12 text-muted-foreground mb-2"),
                    P("No notifications", cls="text-sm text-muted-foreground"),
                    data_show=js("!($notif_1 || $notif_2 || $notif_3 || $notif_4)"),
                    cls="flex flex-col items-center justify-center py-12"
                ),
                cls="flex-1 overflow-y-auto min-h-[200px]"
            ),
            SheetFooter(
                Div(
                    Button(
                        "Mark All Read",
                        data_on_click=js("$notif_1 = false; $notif_2 = false; $notif_3 = false; $notif_4 = false"),
                        variant="outline",
                        size="sm",
                        cls="flex-1 mr-2"
                    ),
                    Button(
                        "View All",
                        data_on_click=js("alert('Navigate to full notifications page')"),
                        size="sm",
                        cls="flex-1"
                    ),
                    cls="flex gap-2 w-full"
                )
            ),
            signal="notifications_sheet",
            side="top",
            size="md"
        ),
        signal="notifications_sheet"
    )


# Action sheet (bottom side) - Mobile-friendly
@with_code
def action_sheet_example():
    return Sheet(
        SheetTrigger(
            Icon("lucide:more-horizontal", cls="h-4 w-4 mr-2"),
            "Actions",
            signal="actions_sheet",
            variant="outline"
        ),
        SheetContent(
            SheetHeader(
                SheetTitle("Quick Actions"),
                SheetDescription("Choose an action to perform")
            ),
            Div(
                Button(
                    Icon("lucide:share", cls="h-5 w-5 mr-3"),
                    Div(
                        P("Share", cls="font-medium"),
                        P("Share this item with others", cls="text-sm text-muted-foreground"),
                        cls="text-left"
                    ),
                    variant="ghost",
                    cls="w-full justify-start p-4 h-auto"
                ),
                Button(
                    Icon("lucide:copy", cls="h-5 w-5 mr-3"),
                    Div(
                        P("Copy Link", cls="font-medium"),
                        P("Copy the link to your clipboard", cls="text-sm text-muted-foreground"),
                        cls="text-left"
                    ),
                    variant="ghost",
                    cls="w-full justify-start p-4 h-auto"
                ),
                Button(
                    Icon("lucide:download", cls="h-5 w-5 mr-3"),
                    Div(
                        P("Download", cls="font-medium"),
                        P("Save to your device", cls="text-sm text-muted-foreground"),
                        cls="text-left"
                    ),
                    variant="ghost",
                    cls="w-full justify-start p-4 h-auto"
                ),
                Button(
                    Icon("lucide:bookmark", cls="h-5 w-5 mr-3"),
                    Div(
                        P("Add to Favorites", cls="font-medium"),
                        P("Save for quick access later", cls="text-sm text-muted-foreground"),
                        cls="text-left"
                    ),
                    variant="ghost",
                    cls="w-full justify-start p-4 h-auto"
                ),
                Separator(cls="my-2"),
                Button(
                    Icon("lucide:flag", cls="h-5 w-5 mr-3"),
                    Div(
                        P("Report", cls="font-medium text-orange-600"),
                        P("Report inappropriate content", cls="text-sm text-muted-foreground"),
                        cls="text-left"
                    ),
                    variant="ghost",
                    cls="w-full justify-start p-4 h-auto"
                ),
                Button(
                    Icon("lucide:trash-2", cls="h-5 w-5 mr-3"),
                    Div(
                        P("Delete", cls="font-medium text-red-600"),
                        P("Permanently remove this item", cls="text-sm text-muted-foreground"),
                        cls="text-left"
                    ),
                    variant="ghost",
                    cls="w-full justify-start p-4 h-auto"
                ),
                cls="px-6 space-y-1"
            ),
            SheetFooter(
                SheetClose("Cancel", variant="outline", cls="w-full")
            ),
            signal="actions_sheet",
            side="bottom",
            size="md"
        ),
        signal="actions_sheet"
    )


# Contact form sheet
@with_code
def contact_form_sheet_example():
    contact_name = Signal("contact_name", "")
    contact_email = Signal("contact_email", "")
    contact_subject = Signal("contact_subject", "")
    contact_message = Signal("contact_message", "")
    contact_updates = Signal("contact_updates", False)

    return Sheet(
        SheetTrigger(
            Icon("lucide:mail", cls="h-4 w-4 mr-2"),
            "Contact Us",
            signal="contact_sheet"
        ),
        SheetContent(
            SheetHeader(
                SheetTitle("Contact Us"),
                SheetDescription("Send us a message and we'll get back to you as soon as possible.")
            ),
            Form(
                Div(
                    contact_name, contact_email, contact_subject, contact_message, contact_updates,
                    InputWithLabel(label="Name", placeholder="Your full name", signal="contact_name", required=True),
                    InputWithLabel(label="Email", type="email", placeholder="your.email@example.com", signal="contact_email", required=True),
                    SelectWithLabel(
                        label="Subject",
                        options=[
                            ("", "Select a topic"),
                            ("support", "Technical Support"),
                            ("billing", "Billing Question"),
                            ("feedback", "Product Feedback"),
                            ("other", "Other")
                        ],
                        signal="contact_subject",
                        required=True
                    ),
                    TextareaWithLabel(label="Message", placeholder="Tell us how we can help you...", rows=4, signal="contact_message", required=True),
                    CheckboxWithLabel(label="I'd like to receive updates about new features and improvements", signal="contact_updates"),
                    cls="space-y-4 px-6"
                )
            ),
            SheetFooter(
                Div(
                    SheetClose("Cancel", variant="outline", cls="flex-1 mr-2"),
                    Button(
                        "Send Message",
                        data_attr_disabled=js("!$contact_name || !$contact_email || !$contact_subject || !$contact_message"),
                        data_on_click=js("""
                            if ($contact_name && $contact_email && $contact_subject && $contact_message) {
                                alert('Message sent! We\\'ll get back to you soon.');
                                $contact_name = ''; $contact_email = '';
                                $contact_subject = ''; $contact_message = '';
                                $contact_updates = false;
                            }
                        """),
                        cls="flex-1"
                    ),
                    cls="flex gap-2 w-full"
                )
            ),
            signal="contact_sheet",
            side="right",
            size="lg"
        ),
        signal="contact_sheet"
    )


# Different sizes demo
@with_code
def sheet_sizes_example():
    sheet_configs = [
        ("Small", "small_size_sheet", "sm", "Small Sheet", "Compact size for simple content",
         "This is a small sheet (max-w-sm) - perfect for simple forms, quick actions, or narrow content."),
        ("Medium", "medium_size_sheet", "md", "Medium Sheet", "Standard size for most content",
         "This is a medium sheet (max-w-md) - the default size for most use cases including forms, settings, and moderate content."),
        ("Large", "large_size_sheet", "lg", "Large Sheet", "More space for complex content",
         "This is a large sheet (max-w-lg) - great for detailed forms, complex interfaces, shopping carts, and content that needs more horizontal space."),
        ("Extra Large", "xl_size_sheet", "xl", "Extra Large Sheet", "Maximum width for extensive content",
         "This is an extra large sheet (max-w-xl) - ideal for comprehensive dashboards, data tables, detailed settings panels, or any content requiring maximum horizontal space.")
    ]

    def create_size_demo(button_label, signal, size, title, description, content):
        return Sheet(
            SheetTrigger(button_label, signal=signal, variant="outline", size="sm"),
            SheetContent(
                SheetHeader(
                    SheetTitle(title),
                    SheetDescription(description)
                ),
                Div(P(content, cls="text-sm"), cls="px-6"),
                signal=signal,
                side="right",
                size=size
            ),
            signal=signal,
            cls="mr-2" if button_label != "Extra Large" else ""
        )

    return Div(
        P("Different sheet sizes for various content needs:", cls="text-sm text-muted-foreground mb-4"),
        Div(
            *[create_size_demo(button_label, signal, size, title, description, content)
              for button_label, signal, size, title, description, content in sheet_configs],
            cls="flex flex-wrap gap-2 justify-center"
        ),
        cls="text-center"
    )


# ============================================================================
# EXAMPLES DATA (for markdown generation with code)
# ============================================================================

EXAMPLES_DATA = [
    {"title": "Navigation Menu", "description": "Left-side navigation sheet with menu items and user profile", "code": navigation_menu_sheet_example.code},
    {"title": "Shopping Cart", "description": "Right-side cart drawer with product items and checkout actions", "code": shopping_cart_sheet_example.code},
    {"title": "Filter Panel", "description": "Left-side filter drawer for product search with multiple filter options", "code": filter_panel_sheet_example.code},
    {"title": "Settings Drawer", "description": "Right-side settings panel with user preferences and toggles", "code": settings_drawer_sheet_example.code},
    {"title": "Notification Panel", "description": "Top-sliding notification panel with action buttons and dismissible items", "code": notification_panel_sheet_example.code},
    {"title": "Action Sheet", "description": "Bottom-sliding mobile-friendly action sheet with contextual options", "code": action_sheet_example.code},
    {"title": "Contact Form", "description": "Complete contact form in a right-side sheet with validation", "code": contact_form_sheet_example.code},
    {"title": "Sheet Sizes", "description": "Different sheet sizes for various content requirements", "code": sheet_sizes_example.code},
]


# ============================================================================
# API REFERENCE
# ============================================================================

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


# ============================================================================
# EXAMPLES GENERATOR (for rendering on the page)
# ============================================================================

def examples():
    yield ComponentPreview(
        navigation_menu_sheet_example(),
        navigation_menu_sheet_example.code,
        title="Navigation Menu",
        description="Left-side navigation sheet with menu items and user profile"
    )

    yield ComponentPreview(
        shopping_cart_sheet_example(),
        shopping_cart_sheet_example.code,
        title="Shopping Cart",
        description="Right-side cart drawer with product items and checkout actions"
    )

    yield ComponentPreview(
        filter_panel_sheet_example(),
        filter_panel_sheet_example.code,
        title="Filter Panel",
        description="Left-side filter drawer for product search with multiple filter options"
    )

    yield ComponentPreview(
        settings_drawer_sheet_example(),
        settings_drawer_sheet_example.code,
        title="Settings Drawer",
        description="Right-side settings panel with user preferences and toggles"
    )

    yield ComponentPreview(
        notification_panel_sheet_example(),
        notification_panel_sheet_example.code,
        title="Notification Panel",
        description="Top-sliding notification panel with action buttons and dismissible items"
    )

    yield ComponentPreview(
        action_sheet_example(),
        action_sheet_example.code,
        title="Action Sheet",
        description="Bottom-sliding mobile-friendly action sheet with contextual options"
    )

    yield ComponentPreview(
        contact_form_sheet_example(),
        contact_form_sheet_example.code,
        title="Contact Form",
        description="Complete contact form in a right-side sheet with validation"
    )

    yield ComponentPreview(
        sheet_sizes_example(),
        sheet_sizes_example.code,
        title="Sheet Sizes",
        description="Different sheet sizes for various content requirements"
    )


def create_sheet_docs():
    # Hero example
    @with_code
    def hero_sheet_example():
        profile_name = Signal("profile_name", "")
        profile_username = Signal("profile_username", "")

        return Sheet(
            SheetTrigger("Open Sheet", signal="hero_sheet"),
            SheetContent(
                SheetHeader(
                    SheetTitle("Edit Profile"),
                    SheetDescription("Make changes to your profile here. Click save when you're done.")
                ),
                Div(
                    profile_name, profile_username,
                    InputWithLabel(label="Name", placeholder="Pedro Duarte", signal="profile_name"),
                    InputWithLabel(label="Username", placeholder="@peduarte", signal="profile_username"),
                    cls="space-y-4 px-6 py-4"
                ),
                SheetFooter(
                    SheetClose("Cancel", variant="outline"),
                    Button("Save changes")
                ),
                signal="hero_sheet"
            ),
            signal="hero_sheet"
        )

    hero_example = ComponentPreview(
        hero_sheet_example(),
        hero_sheet_example.code,
        copy_button=True
    )

    return auto_generate_page(
        TITLE,
        DESCRIPTION,
        list(examples()),
        cli_command="star add sheet",
        api_reference=API_REFERENCE,
        hero_example=hero_example,
        component_slug="sheet"
    )