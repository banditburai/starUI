"""
Sheet component documentation - Side panels/drawers that slide in from screen edges.
"""

# Component metadata for auto-discovery
TITLE = "Sheet"
DESCRIPTION = "A side panel component that slides in from the screen edge. Perfect for navigation menus, filter panels, settings drawers, and detail views."
CATEGORY = "overlay"
ORDER = 150
STATUS = "stable"

from starhtml import Div, P, H3, H4, Span, Icon, A, Img, Form, Label, Hr, Ul, Li, Strong
from starhtml.datastar import (
    ds_on_click, ds_show, ds_text, ds_signals, value,
    ds_bind, ds_disabled, ds_on_change, ds_effect, ds_class, toggle_signal
)
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


def examples():
    """Generate sheet examples using ComponentPreview with tabs."""
    
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
                    SheetTitle("Navigation", signal="nav_sheet"),
                    SheetDescription("Browse through the app sections", signal="nav_sheet")
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

    yield ComponentPreview(
        navigation_menu_sheet_example(),
        navigation_menu_sheet_example.code,
        title="Navigation Menu",
        description="Left-side navigation sheet with menu items and user profile"
    )
    
    # Shopping cart sheet (right side)
    @with_code
    def shopping_cart_sheet_example():
        return Sheet(
            SheetTrigger(
                Icon("lucide:shopping-cart", cls="h-4 w-4 mr-2"),
                Span("Cart (", ds_text("($qty_headphones + $qty_shoes)"), ")"),
                signal="cart_sheet",
                variant="outline"
            ),
            SheetContent(
                SheetHeader(
                    SheetTitle("Shopping Cart", signal="cart_sheet"),
                    SheetDescription(
                        Span(ds_text("($qty_headphones + $qty_shoes) + ' items in your cart'")),
                        signal="cart_sheet"
                    )
                ),
                Div(
                    Div(
                        Img(
                            src="https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=100&h=100&fit=crop",
                            alt="Product",
                            cls="w-16 h-16 rounded-lg object-cover"
                        ),
                        Div(
                            H4("Wireless Headphones", cls="text-sm font-medium"),
                            P("Premium quality sound", cls="text-xs text-muted-foreground"),
                            Div(
                                Span("$99.99", cls="text-sm font-bold"),
                                Div(
                                    Button(
                                        "-",
                                        ds_on_click("$qty_headphones = Math.max(0, $qty_headphones - 1)"),
                                        size="sm", 
                                        variant="outline", 
                                        cls="h-6 w-6 p-0"
                                    ),
                                    Span(ds_text("$qty_headphones"), cls="mx-2 text-sm"),
                                    Button(
                                        "+",
                                        ds_on_click("$qty_headphones = $qty_headphones + 1"),
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
                    ),
                    Div(
                        Img(
                            src="https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=100&h=100&fit=crop",
                            alt="Product",
                            cls="w-16 h-16 rounded-lg object-cover"
                        ),
                        Div(
                            H4("Running Shoes", cls="text-sm font-medium"),
                            P("Comfortable and durable", cls="text-xs text-muted-foreground"),
                            Div(
                                Span("$129.99", cls="text-sm font-bold"),
                                Div(
                                    Button(
                                        "-",
                                        ds_on_click("$qty_shoes = Math.max(0, $qty_shoes - 1)"),
                                        size="sm", 
                                        variant="outline", 
                                        cls="h-6 w-6 p-0"
                                    ),
                                    Span(ds_text("$qty_shoes"), cls="mx-2 text-sm"),
                                    Button(
                                        "+",
                                        ds_on_click("$qty_shoes = $qty_shoes + 1"),
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
                    ),
                    Div(
                        Div(
                            Div(
                                Span("Subtotal", cls="text-sm"),
                                Span(
                                    "$",
                                    ds_text("(($qty_headphones * 99.99 + $qty_shoes * 129.99).toFixed(2))"),
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
                                    ds_text("((($qty_headphones * 99.99 + $qty_shoes * 129.99) * 0.08).toFixed(2))"),
                                    cls="text-sm"
                                ),
                                cls="flex justify-between"
                            ),
                            Hr(cls="my-3"),
                            Div(
                                Span("Total", cls="text-base font-bold"),
                                Span(
                                    "$",
                                    ds_text("(($qty_headphones * 99.99 + $qty_shoes * 129.99) * 1.08 + 9.99).toFixed(2)"),
                                    cls="text-base font-bold"
                                ),
                                cls="flex justify-between"
                            ),
                            cls="space-y-2"
                        ),
                        cls="p-4"
                    ),
                    ds_signals(qty_headphones=value(1), qty_shoes=value(2)),
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

    yield ComponentPreview(
        shopping_cart_sheet_example(),
        shopping_cart_sheet_example.code,
        title="Shopping Cart",
        description="Right-side cart drawer with product items and checkout actions"
    )
    
    # Filter panel sheet (left side)
    @with_code
    def filter_panel_sheet_example():
        return Sheet(
            SheetTrigger(
                Icon("lucide:sliders-horizontal", cls="h-4 w-4 mr-2"),
                "Filters",
                signal="filter_sheet",
                variant="outline"
            ),
            SheetContent(
                SheetHeader(
                    SheetTitle("Filter Products", signal="filter_sheet"),
                    SheetDescription("Refine your search results", signal="filter_sheet")
                ),
                Div(
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
                                        ds_on_click(f"$min_rating = {i+1}"),
                                        ds_class(
                                            text_yellow_500=f"$min_rating >= {i+1}",
                                            text_gray_300=f"$min_rating < {i+1}"
                                        ),
                                        cls="text-xl cursor-pointer transition-colors hover:text-yellow-400"
                                    )
                                    for i in range(5)
                                ],
                                cls="flex gap-1"
                            ),
                            Span(ds_text("$min_rating > 0 ? $min_rating + '+ stars' : 'Any rating'"), cls="text-sm text-muted-foreground mt-2"),
                            cls="space-y-2"
                        ),
                        cls="mb-6"
                    ),
                    ds_signals(
                        min_price=value(""),
                        max_price=value(""),
                        cat_electronics=False,
                        cat_clothing=False,
                        cat_books=False,
                        cat_home=False,
                        cat_sports=False,
                        selected_brand=value(""),
                        min_rating=value(1)
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
                            ds_on_click="""
                                $min_price = ''; $max_price = '';
                                $cat_electronics = false; $cat_clothing = false;
                                $cat_books = false; $cat_home = false; $cat_sports = false;
                                $selected_brand = ''; $min_rating = 1;
                            """
                        ),
                        Button("Apply Filters", size="sm", cls="flex-1", ds_on_click="alert('Filters applied!')"),
                        cls="flex gap-2 w-full"
                    )
                ),
                signal="filter_sheet",
                side="left",
                size="sm"
            ),
            signal="filter_sheet"
        )

    yield ComponentPreview(
        filter_panel_sheet_example(),
        filter_panel_sheet_example.code,
        title="Filter Panel",
        description="Left-side filter drawer for product search with multiple filter options"
    )
    
    # Settings drawer (right side)
    @with_code
    def settings_drawer_sheet_example():
        return Sheet(
            SheetTrigger(
                Icon("lucide:settings", cls="h-4 w-4 mr-2"),
                "Settings",
                signal="settings_sheet",
                variant="outline"
            ),
            SheetContent(
                SheetHeader(
                    SheetTitle("Application Settings", signal="settings_sheet"),
                    SheetDescription("Customize your experience", signal="settings_sheet")
                ),
                Div(
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
                                initial_value="system",
                                initial_label="System",
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
                                initial_value="en",
                                initial_label="English",
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
                    ds_signals(theme_pref=value("system"), language_pref=value("en"), push_notifications=True, email_notifications=True),
                    cls="px-6 flex-1 overflow-y-auto"
                ),
                SheetFooter(Div(Button("Reset to Defaults", variant="outline", size="sm", cls="flex-1 mr-2"), Button("Save Changes", size="sm", cls="flex-1"), cls="flex gap-2 w-full")),
                signal="settings_sheet",
                side="right",
                size="md"
            ),
            signal="settings_sheet"
        )

    yield ComponentPreview(
        settings_drawer_sheet_example(),
        settings_drawer_sheet_example.code,
        title="Settings Drawer",
        description="Right-side settings panel with user preferences and toggles"
    )
    
    # Notification panel (top side)
    @with_code
    def notification_panel_sheet_example():
        return Sheet(
            SheetTrigger(
                Icon("lucide:bell", cls="h-4 w-4 mr-2"),
                "Notifications",
                Badge(
                    ds_text("""
                        let count = 0;
                        if ($notif_1) count++;
                        if ($notif_2) count++;
                        if ($notif_3) count++;
                        if ($notif_4) count++;
                        count
                    """),
                    ds_show("$notif_1 || $notif_2 || $notif_3 || $notif_4"),
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
                            ds_text("""
                                let count = 0;
                                if ($notif_1) count++;
                                if ($notif_2) count++;
                                if ($notif_3) count++;
                                if ($notif_4) count++;
                                count > 0 ? count : ''
                            """),
                            ds_show("""
                                $notif_1 || $notif_2 || $notif_3 || $notif_4
                            """),
                            variant="destructive",
                            cls="ml-2 text-xs"
                        ),
                        signal="notifications_sheet"
                    ),
                    SheetDescription("Stay up to date with your latest activity", signal="notifications_sheet")
                ),
                Div(
                    Div(
                        Icon("lucide:check-circle", cls="h-5 w-5 text-green-500 mt-1 mr-3"),
                        Div(
                            P("Payment successful", cls="text-sm font-medium"),
                            P("Your monthly subscription has been processed", cls="text-xs text-muted-foreground mb-2"),
                            P("2 minutes ago", cls="text-xs text-muted-foreground"),
                            cls="flex-1"
                        ),
                        Button(Icon("lucide:x", cls="h-4 w-4"), ds_on_click("$notif_1 = false"), variant="ghost", size="sm", cls="h-8 w-8 p-0 text-muted-foreground hover:text-foreground hover:bg-muted"),
                        ds_show("$notif_1"),
                        cls="flex items-start p-4 border-b hover:bg-muted/30 transition-colors"
                    ),
                    Div(
                        Icon("lucide:user-plus", cls="h-5 w-5 text-blue-500 mt-1 mr-3"),
                        Div(
                            P("New team member", cls="text-sm font-medium"),
                            P("Sarah Johnson joined your workspace", cls="text-xs text-muted-foreground mb-2"),
                            P("1 hour ago", cls="text-xs text-muted-foreground"),
                            cls="flex-1"
                        ),
                        Button(Icon("lucide:x", cls="h-4 w-4"), ds_on_click("$notif_2 = false"), variant="ghost", size="sm", cls="h-8 w-8 p-0 text-muted-foreground hover:text-foreground hover:bg-muted"),
                        ds_show("$notif_2"),
                        cls="flex items-start p-4 border-b hover:bg-muted/30 transition-colors"
                    ),
                    Div(
                        Icon("lucide:alert-triangle", cls="h-5 w-5 text-orange-500 mt-1 mr-3"),
                        Div(
                            P("Action required", cls="text-sm font-medium"),
                            P("Please update your billing information", cls="text-xs text-muted-foreground mb-2"),
                            P("3 hours ago", cls="text-xs text-muted-foreground"),
                            cls="flex-1"
                        ),
                        Button(Icon("lucide:x", cls="h-4 w-4"), ds_on_click("$notif_3 = false"), variant="ghost", size="sm", cls="h-8 w-8 p-0 text-muted-foreground hover:text-foreground hover:bg-muted"),
                        ds_show("$notif_3"),
                        cls="flex items-start p-4 border-b hover:bg-muted/30 transition-colors"
                    ),
                    Div(
                        Icon("lucide:calendar", cls="h-5 w-5 text-purple-500 mt-1 mr-3"),
                        Div(
                            P("Meeting reminder", cls="text-sm font-medium"),
                            P("Team standup in 15 minutes", cls="text-xs text-muted-foreground mb-2"),
                            P("5 hours ago", cls="text-xs text-muted-foreground"),
                            cls="flex-1"
                        ),
                        Button(Icon("lucide:x", cls="h-4 w-4"), ds_on_click("$notif_4 = false"), variant="ghost", size="sm", cls="h-8 w-8 p-0 text-muted-foreground hover:text-foreground hover:bg-muted"),
                        ds_show("$notif_4"),
                        cls="flex items-start p-4 border-b hover:bg-muted/30 transition-colors"
                    ),
                    Div(
                        Icon("lucide:inbox", cls="h-12 w-12 text-muted-foreground mb-2"),
                        P("No notifications", cls="text-sm text-muted-foreground"),
                        ds_show("!($notif_1 || $notif_2 || $notif_3 || $notif_4)"),
                        cls="flex flex-col items-center justify-center py-12"
                    ),
                    ds_signals(notif_1=True, notif_2=True, notif_3=True, notif_4=True),
                    cls="flex-1 overflow-y-auto min-h-[200px]"
                ),
                SheetFooter(Div(Button("Mark All Read", ds_on_click("$notif_1 = false; $notif_2 = false; $notif_3 = false; $notif_4 = false"), variant="outline", size="sm", cls="flex-1 mr-2"), Button("View All", ds_on_click("alert('Navigate to full notifications page')"), size="sm", cls="flex-1"), cls="flex gap-2 w-full")),
                signal="notifications_sheet",
                side="top",
                size="md"
            ),
            signal="notifications_sheet"
        )

    yield ComponentPreview(
        notification_panel_sheet_example(),
        notification_panel_sheet_example.code,
        title="Notification Panel",
        description="Top-sliding notification panel with action buttons and dismissible items"
    )
    
    # Action sheet (bottom side) - Mobile-friendly
    @with_code
    def action_sheet_example():
        return Sheet(
            SheetTrigger(Icon("lucide:more-horizontal", cls="h-4 w-4 mr-2"), "Actions", signal="actions_sheet", variant="outline"),
            SheetContent(
                SheetHeader(SheetTitle("Quick Actions", signal="actions_sheet"), SheetDescription("Choose an action to perform", signal="actions_sheet")),
                Div(
                    Button(Icon("lucide:share", cls="h-5 w-5 mr-3"), Div(P("Share", cls="font-medium"), P("Share this item with others", cls="text-sm text-muted-foreground"), cls="text-left"), variant="ghost", cls="w-full justify-start p-4 h-auto"),
                    Button(Icon("lucide:copy", cls="h-5 w-5 mr-3"), Div(P("Copy Link", cls="font-medium"), P("Copy the link to your clipboard", cls="text-sm text-muted-foreground"), cls="text-left"), variant="ghost", cls="w-full justify-start p-4 h-auto"),
                    Button(Icon("lucide:download", cls="h-5 w-5 mr-3"), Div(P("Download", cls="font-medium"), P("Save to your device", cls="text-sm text-muted-foreground"), cls="text-left"), variant="ghost", cls="w/full justify-start p-4 h-auto"),
                    Button(Icon("lucide:bookmark", cls="h-5 w-5 mr-3"), Div(P("Add to Favorites", cls="font-medium"), P("Save for quick access later", cls="text-sm text-muted-foreground"), cls="text-left"), variant="ghost", cls="w/full justify-start p-4 h-auto"),
                    Separator(cls="my-2"),
                    Button(Icon("lucide:flag", cls="h-5 w-5 mr-3"), Div(P("Report", cls="font-medium text-orange-600"), P("Report inappropriate content", cls="text-sm text-muted-foreground"), cls="text-left"), variant="ghost", cls="w/full justify-start p-4 h-auto"),
                    Button(Icon("lucide:trash-2", cls="h-5 w-5 mr-3"), Div(P("Delete", cls="font-medium text-red-600"), P("Permanently remove this item", cls="text-sm text-muted-foreground"), cls="text-left"), variant="ghost", cls="w/full justify-start p-4 h-auto"),
                    cls="px-6 space-y-1"
                ),
                SheetFooter(SheetClose("Cancel", signal="actions_sheet", variant="outline", cls="w/full")),
                signal="actions_sheet",
                side="bottom",
                size="md"
            ),
            signal="actions_sheet"
        )

    yield ComponentPreview(
        action_sheet_example(),
        action_sheet_example.code,
        title="Action Sheet",
        description="Bottom-sliding mobile-friendly action sheet with contextual options"
    )
    
    # Contact form sheet
    @with_code
    def contact_form_sheet_example():
        return Sheet(
            SheetTrigger(Icon("lucide:mail", cls="h-4 w-4 mr-2"), "Contact Us", signal="contact_sheet"),
            SheetContent(
                SheetHeader(SheetTitle("Contact Us", signal="contact_sheet"), SheetDescription("Send us a message and we'll get back to you as soon as possible.", signal="contact_sheet")),
                Form(
                    Div(
                        InputWithLabel(label="Name", placeholder="Your full name", signal="contact_name", required=True),
                        InputWithLabel(label="Email", type="email", placeholder="your.email@example.com", signal="contact_email", required=True),
                        SelectWithLabel(label="Subject", options=[("", "Select a topic"), ("support", "Technical Support"), ("billing", "Billing Question"), ("feedback", "Product Feedback"), ("other", "Other")], signal="contact_subject", required=True),
                        TextareaWithLabel(label="Message", placeholder="Tell us how we can help you...", rows=4, signal="contact_message", required=True),
                        CheckboxWithLabel(label="I'd like to receive updates about new features and improvements", signal="contact_updates"),
                        ds_signals(contact_name=value(""), contact_email=value(""), contact_subject=value(""), contact_message=value(""), contact_updates=False),
                        cls="space-y-4 px-6"
                    )
                ),
                SheetFooter(Div(SheetClose("Cancel", signal="contact_sheet", variant="outline", cls="flex-1 mr-2"), Button("Send Message", ds_disabled="!$contact_name || !$contact_email || !$contact_subject || !$contact_message", ds_on_click="""
                                if ($contact_name && $contact_email && $contact_subject && $contact_message) {
                                    alert('Message sent! We\\'ll get back to you soon.');
                                    $contact_name = ''; $contact_email = ''; 
                                    $contact_subject = ''; $contact_message = '';
                                    $contact_updates = false;
                                }
                            """, cls="flex-1"), cls="flex gap-2 w-full")),
                signal="contact_sheet",
                side="right",
                size="lg"
            ),
            signal="contact_sheet"
        )

    yield ComponentPreview(
        contact_form_sheet_example(),
        contact_form_sheet_example.code,
        title="Contact Form",
        description="Complete contact form in a right-side sheet with validation"
    )
    
    # Different sizes demo
    @with_code
    def sheet_sizes_example():
        return Div(
            P("Different sheet sizes for various content needs:", cls="text-sm text-muted-foreground mb-4"),
            Div(
                Sheet(
                    SheetTrigger("Small", signal="small_size_sheet", variant="outline", size="sm"),
                    SheetContent(
                        SheetHeader(SheetTitle("Small Sheet", signal="small_size_sheet"), SheetDescription("Compact size for simple content", signal="small_size_sheet")),
                        Div(P("This is a small sheet (max-w-sm) - perfect for simple forms, quick actions, or narrow content.", cls="text-sm"), cls="px-6"),
                        signal="small_size_sheet",
                        side="right",
                        size="sm"
                    ),
                    signal="small_size_sheet",
                    cls="mr-2"
                ),
                Sheet(
                    SheetTrigger("Medium", signal="medium_size_sheet", variant="outline", size="sm"),
                    SheetContent(
                        SheetHeader(SheetTitle("Medium Sheet", signal="medium_size_sheet"), SheetDescription("Standard size for most content", signal="medium_size_sheet")),
                        Div(P("This is a medium sheet (max-w-md) - the default size for most use cases including forms, settings, and moderate content.", cls="text-sm"), cls="px-6"),
                        signal="medium_size_sheet",
                        side="right",
                        size="md"
                    ),
                    signal="medium_size_sheet",
                    cls="mr-2"
                ),
                Sheet(
                    SheetTrigger("Large", signal="large_size_sheet", variant="outline", size="sm"),
                    SheetContent(
                        SheetHeader(SheetTitle("Large Sheet", signal="large_size_sheet"), SheetDescription("More space for complex content", signal="large_size_sheet")),
                        Div(P("This is a large sheet (max-w-lg) - great for detailed forms, complex interfaces, shopping carts, and content that needs more horizontal space.", cls="text-sm"), cls="px-6"),
                        signal="large_size_sheet",
                        side="right",
                        size="lg"
                    ),
                    signal="large_size_sheet",
                    cls="mr-2"
                ),
                Sheet(
                    SheetTrigger("Extra Large", signal="xl_size_sheet", variant="outline", size="sm"),
                    SheetContent(
                        SheetHeader(SheetTitle("Extra Large Sheet", signal="xl_size_sheet"), SheetDescription("Maximum width for extensive content", signal="xl_size_sheet")),
                        Div(P("This is an extra large sheet (max-w-xl) - ideal for comprehensive dashboards, data tables, detailed settings panels, or any content requiring maximum horizontal space.", cls="text-sm"), cls="px-6"),
                        signal="xl_size_sheet",
                        side="right",
                        size="xl"
                    ),
                    signal="xl_size_sheet"
                ),
                cls="flex flex-wrap gap-2 justify-center"
            ),
            cls="text-center"
        )

    yield ComponentPreview(
        sheet_sizes_example(),
        sheet_sizes_example.code,
        title="Sheet Sizes",
        description="Different sheet sizes for various content requirements"
    )


def create_sheet_docs():
    """Create sheet documentation page using convention-based approach."""
    
    # Intentional API: Sheet is a composite. Users benefit from understanding
    # the building blocks and key content props (side, size), not every prop.
    api_reference = build_api_reference(
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
    
    # Hero example
    @with_code
    def hero_sheet_example():
        return Sheet(
            SheetTrigger("Open Sheet", signal="hero_sheet"),
            SheetContent(
                SheetHeader(
                    SheetTitle("Edit Profile", signal="hero_sheet"),
                    SheetDescription("Make changes to your profile here. Click save when you're done.", signal="hero_sheet")
        ),
        Div(
            InputWithLabel(label="Name", placeholder="Pedro Duarte", signal="profile_name"),
            InputWithLabel(label="Username", placeholder="@peduarte", signal="profile_username"),
                    ds_signals(profile_name=value(""), profile_username=value("")),
            cls="space-y-4 px-6 py-4"
        ),
                SheetFooter(SheetClose("Cancel", signal="hero_sheet", variant="outline"), Button("Save changes")),
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
        api_reference=api_reference,
        hero_example=hero_example,
        component_slug="sheet"
    )