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
    ds_bind, ds_disabled, ds_on_change, ds_effect, ds_class, toggle
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
from starui.registry.components.select import SelectWithLabel
from starui.registry.components.checkbox import CheckboxWithLabel
from starui.registry.components.avatar import Avatar
from utils import auto_generate_page
from widgets.component_preview import ComponentPreview


def examples():
    """Generate sheet examples using ComponentPreview with tabs."""
    
    # Navigation menu sheet (left side)
    yield ComponentPreview(
        Sheet(
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
                    # Main navigation links
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
                    # Secondary navigation
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
                    cls="space-y-1 px-6"
                ),
                SheetFooter(
                    Div(
                        Div(
                            Avatar(
                                Img(src="https://github.com/shadcn.png", alt="User"),
                                size="sm",
                                cls="mr-3"
                            ),
                            Div(
                                P("John Doe", cls="text-sm font-medium"),
                                P("john@example.com", cls="text-xs text-muted-foreground"),
                            ),
                            cls="flex items-center"
                        ),
                        Button(
                            Icon("lucide:log-out", cls="h-4 w-4"),
                            variant="ghost",
                            size="sm",
                            cls="mt-4 w-full justify-start"
                        ),
                        cls="w-full"
                    )
                ),
                signal="nav_sheet",
                side="left",
                size="md"
            ),
            signal="nav_sheet"
        ),
        '''Sheet(
    SheetTrigger(
        Icon("lucide:menu"),
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
            # Navigation items
            Div(
                Icon("lucide:home"),
                Span("Home"),
                cls="flex items-center py-3 px-4 rounded-lg hover:bg-muted/50"
            ),
            Div(
                Icon("lucide:bar-chart-3"),
                Span("Dashboard"),
                cls="flex items-center py-3 px-4 rounded-lg hover:bg-muted/50"
            ),
            Div(
                Icon("lucide:folder"),
                Span("Projects"),
                Badge("12", variant="secondary", cls="ml-auto"),
                cls="flex items-center py-3 px-4 rounded-lg hover:bg-muted/50"
            ),
            cls="space-y-1 px-6"
        ),
        signal="nav_sheet",
        side="left",
        size="md"
    ),
    signal="nav_sheet"
)''',
        title="Navigation Menu",
        description="Left-side navigation sheet with menu items and user profile"
    )
    
    # Shopping cart sheet (right side)
    yield ComponentPreview(
        Sheet(
            SheetTrigger(
                Icon("lucide:shopping-cart", cls="h-4 w-4 mr-2"),
                "Cart (3)",
                signal="cart_sheet",
                variant="outline"
            ),
            SheetContent(
                SheetHeader(
                    SheetTitle("Shopping Cart", signal="cart_sheet"),
                    SheetDescription("3 items in your cart", signal="cart_sheet")
                ),
                Div(
                    # Cart items
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
                                    Button("-", size="sm", variant="outline", cls="h-6 w-6 p-0"),
                                    Span("1", cls="mx-2 text-sm"),
                                    Button("+", size="sm", variant="outline", cls="h-6 w-6 p-0"),
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
                                    Button("-", size="sm", variant="outline", cls="h-6 w-6 p-0"),
                                    Span("2", cls="mx-2 text-sm"),
                                    Button("+", size="sm", variant="outline", cls="h-6 w-6 p-0"),
                                    cls="flex items-center ml-auto"
                                ),
                                cls="flex items-center justify-between mt-2"
                            ),
                            cls="flex-1 ml-3"
                        ),
                        cls="flex items-start p-4 border-b"
                    ),
                    # Subtotal
                    Div(
                        Div(
                            Div(
                                Span("Subtotal", cls="text-sm"),
                                Span("$359.97", cls="text-sm font-bold"),
                                cls="flex justify-between"
                            ),
                            Div(
                                Span("Shipping", cls="text-sm"),
                                Span("$9.99", cls="text-sm"),
                                cls="flex justify-between"
                            ),
                            Div(
                                Span("Tax", cls="text-sm"),
                                Span("$29.60", cls="text-sm"),
                                cls="flex justify-between"
                            ),
                            Hr(cls="my-3"),
                            Div(
                                Span("Total", cls="text-base font-bold"),
                                Span("$399.56", cls="text-base font-bold"),
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
        ),
        '''Sheet(
    SheetTrigger(
        Icon("lucide:shopping-cart"),
        "Cart (3)",
        signal="cart_sheet",
        variant="outline"
    ),
    SheetContent(
        SheetHeader(
            SheetTitle("Shopping Cart", signal="cart_sheet"),
            SheetDescription("3 items in your cart", signal="cart_sheet")
        ),
        Div(
            # Cart items
            Div(
                Img(src="product-image.jpg", cls="w-16 h-16 rounded-lg object-cover"),
                Div(
                    H4("Wireless Headphones", cls="text-sm font-medium"),
                    P("Premium quality sound", cls="text-xs text-muted-foreground"),
                    Div(
                        Span("$99.99", cls="text-sm font-bold"),
                        Div(
                            Button("-", size="sm", variant="outline"),
                            Span("1", cls="mx-2 text-sm"),
                            Button("+", size="sm", variant="outline"),
                            cls="flex items-center ml-auto"
                        ),
                        cls="flex items-center justify-between mt-2"
                    ),
                    cls="flex-1 ml-3"
                ),
                cls="flex items-start p-4 border-b"
            ),
            # More items...
            # Subtotal section
            Div(
                Div("Subtotal", "$359.97", cls="flex justify-between"),
                Div("Total", "$399.56", cls="flex justify-between font-bold"),
                cls="p-4 space-y-2"
            ),
            cls="flex-1 overflow-y-auto"
        ),
        SheetFooter(
            Button("Continue Shopping", variant="outline"),
            Button("Checkout")
        ),
        signal="cart_sheet",
        side="right",
        size="lg"
    ),
    signal="cart_sheet"
)''',
        title="Shopping Cart",
        description="Right-side cart drawer with product items and checkout actions"
    )
    
    # Filter panel sheet (left side)
    yield ComponentPreview(
        Sheet(
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
                    # Price range
                    Div(
                        H3("Price Range", cls="text-sm font-semibold mb-3"),
                        Div(
                            InputWithLabel(
                                label="Min Price",
                                type="number",
                                placeholder="0",
                                signal="min_price"
                            ),
                            InputWithLabel(
                                label="Max Price",
                                type="number",
                                placeholder="1000",
                                signal="max_price"
                            ),
                            cls="grid grid-cols-2 gap-3"
                        ),
                        cls="mb-6"
                    ),
                    # Categories
                    Div(
                        H3("Categories", cls="text-sm font-semibold mb-3"),
                        Div(
                            CheckboxWithLabel(
                                label="Electronics",
                                signal="cat_electronics"
                            ),
                            CheckboxWithLabel(
                                label="Clothing",
                                signal="cat_clothing"
                            ),
                            CheckboxWithLabel(
                                label="Books",
                                signal="cat_books"
                            ),
                            CheckboxWithLabel(
                                label="Home & Garden",
                                signal="cat_home"
                            ),
                            CheckboxWithLabel(
                                label="Sports",
                                signal="cat_sports"
                            ),
                            cls="space-y-3"
                        ),
                        cls="mb-6"
                    ),
                    # Brand
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
                    # Rating
                    Div(
                        H3("Minimum Rating", cls="text-sm font-semibold mb-3"),
                        Div(
                            *[
                                Button(
                                    *["★" if i < rating else "☆" for i in range(5)],
                                    f" & up",
                                    variant="ghost",
                                    size="sm",
                                    cls="justify-start",
                                    ds_on_click=f"$min_rating = {rating}"
                                )
                                for rating in [4, 3, 2, 1]
                            ],
                            cls="space-y-1"
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
                        Button(
                            "Apply Filters",
                            size="sm",
                            cls="flex-1",
                            ds_on_click="alert('Filters applied!')"
                        ),
                        cls="flex gap-2 w-full"
                    )
                ),
                signal="filter_sheet",
                side="left",
                size="md"
            ),
            signal="filter_sheet"
        ),
        '''Sheet(
    SheetTrigger(
        Icon("lucide:sliders-horizontal"),
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
            # Price range
            Div(
                H3("Price Range", cls="text-sm font-semibold mb-3"),
                Div(
                    InputWithLabel(label="Min Price", type="number", signal="min_price"),
                    InputWithLabel(label="Max Price", type="number", signal="max_price"),
                    cls="grid grid-cols-2 gap-3"
                )
            ),
            # Categories
            Div(
                H3("Categories", cls="text-sm font-semibold mb-3"),
                Div(
                    CheckboxWithLabel(label="Electronics", signal="cat_electronics"),
                    CheckboxWithLabel(label="Clothing", signal="cat_clothing"),
                    CheckboxWithLabel(label="Books", signal="cat_books"),
                    cls="space-y-3"
                )
            ),
            # Brand selection
            Div(
                H3("Brand", cls="text-sm font-semibold mb-3"),
                SelectWithLabel(
                    options=[("", "Any"), ("apple", "Apple"), ("samsung", "Samsung")],
                    signal="selected_brand"
                )
            ),
            ds_signals(min_price="", max_price="", cat_electronics=False),
            cls="px-6 space-y-6"
        ),
        SheetFooter(
            Button("Clear All", variant="outline"),
            Button("Apply Filters")
        ),
        signal="filter_sheet",
        side="left",
        size="md"
    ),
    signal="filter_sheet"
)''',
        title="Filter Panel",
        description="Left-side filter drawer for product search with multiple filter options"
    )
    
    # Settings drawer (right side)
    yield ComponentPreview(
        Sheet(
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
                    # Account section
                    Div(
                        H3("Account", cls="text-sm font-semibold mb-4"),
                        Div(
                            Avatar(
                                Img(src="https://github.com/shadcn.png", alt="Profile"),
                                size="lg",
                                cls="mr-4"
                            ),
                            Div(
                                H4("John Doe", cls="font-medium"),
                                P("john.doe@example.com", cls="text-sm text-muted-foreground"),
                                Button("Edit Profile", size="sm", variant="outline", cls="mt-2")
                            ),
                            cls="flex items-start"
                        ),
                        cls="mb-8"
                    ),
                    # Preferences
                    Div(
                        H3("Preferences", cls="text-sm font-semibold mb-4"),
                        Div(
                            # Theme
                            Div(
                                Div(
                                    Icon("lucide:palette", cls="h-4 w-4 mr-3"),
                                    Div(
                                        P("Theme", cls="text-sm font-medium"),
                                        P("Choose your interface theme", cls="text-xs text-muted-foreground")
                                    ),
                                    cls="flex items-center flex-1"
                                ),
                                SelectWithLabel(
                                    options=[
                                        ("light", "Light"),
                                        ("dark", "Dark"),
                                        ("system", "System")
                                    ],
                                    value="system",
                                    signal="theme_pref",
                                    show_label=False
                                ),
                                cls="flex items-center justify-between py-3"
                            ),
                            # Language
                            Div(
                                Div(
                                    Icon("lucide:globe", cls="h-4 w-4 mr-3"),
                                    Div(
                                        P("Language", cls="text-sm font-medium"),
                                        P("Select your preferred language", cls="text-xs text-muted-foreground")
                                    ),
                                    cls="flex items-center flex-1"
                                ),
                                SelectWithLabel(
                                    options=[
                                        ("en", "English"),
                                        ("es", "Spanish"),
                                        ("fr", "French"),
                                        ("de", "German")
                                    ],
                                    value="en",
                                    signal="language_pref",
                                    show_label=False
                                ),
                                cls="flex items-center justify-between py-3"
                            ),
                            cls="space-y-1"
                        ),
                        cls="mb-8"
                    ),
                    # Notifications
                    Div(
                        H3("Notifications", cls="text-sm font-semibold mb-4"),
                        Div(
                            Div(
                                Div(
                                    Icon("lucide:bell", cls="h-4 w-4 mr-3"),
                                    Div(
                                        P("Push Notifications", cls="text-sm font-medium"),
                                        P("Receive notifications for important updates", cls="text-xs text-muted-foreground")
                                    ),
                                    cls="flex items-center flex-1"
                                ),
                                Button(
                                    ds_text("$push_notifications ? 'On' : 'Off'"),
                                    size="sm",
                                    variant="secondary",
                                    ds_on_click=toggle("push_notifications"),
                                    ds_class={"bg-green-100 text-green-800 hover:bg-green-200": "$push_notifications",
                                             "bg-gray-100 text-gray-800 hover:bg-gray-200": "!$push_notifications"}
                                ),
                                cls="flex items-center justify-between py-3"
                            ),
                            Div(
                                Div(
                                    Icon("lucide:mail", cls="h-4 w-4 mr-3"),
                                    Div(
                                        P("Email Notifications", cls="text-sm font-medium"),
                                        P("Get email updates for your account", cls="text-xs text-muted-foreground")
                                    ),
                                    cls="flex items-center flex-1"
                                ),
                                Button(
                                    ds_text("$email_notifications ? 'On' : 'Off'"),
                                    size="sm",
                                    variant="secondary",
                                    ds_on_click=toggle("email_notifications"),
                                    ds_class={"bg-green-100 text-green-800 hover:bg-green-200": "$email_notifications",
                                             "bg-gray-100 text-gray-800 hover:bg-gray-200": "!$email_notifications"}
                                ),
                                cls="flex items-center justify-between py-3"
                            ),
                            cls="space-y-1"
                        )
                    ),
                    ds_signals(
                        theme_pref=value("system"),
                        language_pref=value("en"),
                        push_notifications=True,
                        email_notifications=True
                    ),
                    cls="px-6 flex-1 overflow-y-auto"
                ),
                SheetFooter(
                    Div(
                        Button(
                            "Reset to Defaults",
                            variant="outline",
                            size="sm",
                            cls="flex-1 mr-2"
                        ),
                        Button(
                            "Save Changes",
                            size="sm",
                            cls="flex-1"
                        ),
                        cls="flex gap-2 w-full"
                    )
                ),
                signal="settings_sheet",
                side="right",
                size="lg"
            ),
            signal="settings_sheet"
        ),
        '''Sheet(
    SheetTrigger(
        Icon("lucide:settings"),
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
            # Account section
            Div(
                H3("Account", cls="text-sm font-semibold mb-4"),
                Div(
                    Avatar(Img(src="profile.jpg"), size="lg"),
                    Div(
                        H4("John Doe", cls="font-medium"),
                        P("john.doe@example.com", cls="text-sm text-muted-foreground"),
                        Button("Edit Profile", size="sm", variant="outline")
                    ),
                    cls="flex items-start"
                )
            ),
            # Theme preference
            Div(
                H3("Preferences", cls="text-sm font-semibold mb-4"),
                Div(
                    Icon("lucide:palette"),
                    Div("Theme", "Choose your interface theme"),
                    SelectWithLabel(
                        options=[("light", "Light"), ("dark", "Dark"), ("system", "System")],
                        signal="theme_pref"
                    ),
                    cls="flex items-center justify-between py-3"
                )
            ),
            # Notification toggles
            Div(
                H3("Notifications", cls="text-sm font-semibold mb-4"),
                Div(
                    Icon("lucide:bell"),
                    Div("Push Notifications", "Receive important updates"),
                    Button(
                        ds_text("$push_notifications ? 'On' : 'Off'"),
                        ds_on_click=toggle("push_notifications")
                    ),
                    cls="flex items-center justify-between py-3"
                )
            ),
            ds_signals(theme_pref="system", push_notifications=True),
            cls="px-6 space-y-8"
        ),
        SheetFooter(
            Button("Reset to Defaults", variant="outline"),
            Button("Save Changes")
        ),
        signal="settings_sheet",
        side="right",
        size="lg"
    ),
    signal="settings_sheet"
)''',
        title="Settings Drawer",
        description="Right-side settings panel with user preferences and toggles"
    )
    
    # Notification panel (top side)
    yield ComponentPreview(
        Sheet(
            SheetTrigger(
                Icon("lucide:bell", cls="h-4 w-4 mr-2"),
                "Notifications",
                Badge("3", variant="destructive", cls="ml-2 text-xs"),
                signal="notifications_sheet",
                variant="outline"
            ),
            SheetContent(
                SheetHeader(
                    SheetTitle("Recent Notifications", signal="notifications_sheet"),
                    SheetDescription("Stay up to date with your latest activity", signal="notifications_sheet")
                ),
                Div(
                    # Notification items
                    Div(
                        Icon("lucide:check-circle", cls="h-5 w-5 text-green-500 mt-1 mr-3"),
                        Div(
                            P("Payment successful", cls="text-sm font-medium"),
                            P("Your monthly subscription has been processed", cls="text-xs text-muted-foreground mb-2"),
                            P("2 minutes ago", cls="text-xs text-muted-foreground"),
                            cls="flex-1"
                        ),
                        Button("×", variant="ghost", size="sm", cls="h-6 w-6 p-0 text-muted-foreground"),
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
                        Button("×", variant="ghost", size="sm", cls="h-6 w-6 p-0 text-muted-foreground"),
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
                        Button("×", variant="ghost", size="sm", cls="h-6 w-6 p-0 text-muted-foreground"),
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
                        Button("×", variant="ghost", size="sm", cls="h-6 w-6 p-0 text-muted-foreground"),
                        cls="flex items-start p-4 border-b hover:bg-muted/30 transition-colors"
                    ),
                    cls="flex-1 overflow-y-auto"
                ),
                SheetFooter(
                    Div(
                        Button("Mark All Read", variant="outline", size="sm", cls="flex-1 mr-2"),
                        Button("View All", size="sm", cls="flex-1"),
                        cls="flex gap-2 w-full"
                    )
                ),
                signal="notifications_sheet",
                side="top",
                size="md"
            ),
            signal="notifications_sheet"
        ),
        '''Sheet(
    SheetTrigger(
        Icon("lucide:bell"),
        "Notifications",
        Badge("3", variant="destructive"),
        signal="notifications_sheet",
        variant="outline"
    ),
    SheetContent(
        SheetHeader(
            SheetTitle("Recent Notifications", signal="notifications_sheet"),
            SheetDescription("Stay up to date with your latest activity", signal="notifications_sheet")
        ),
        Div(
            # Notification items
            Div(
                Icon("lucide:check-circle", cls="h-5 w-5 text-green-500 mt-1 mr-3"),
                Div(
                    P("Payment successful", cls="text-sm font-medium"),
                    P("Your monthly subscription has been processed", cls="text-xs text-muted-foreground"),
                    P("2 minutes ago", cls="text-xs text-muted-foreground"),
                    cls="flex-1"
                ),
                Button("×", variant="ghost", size="sm"),
                cls="flex items-start p-4 border-b hover:bg-muted/30"
            ),
            Div(
                Icon("lucide:user-plus", cls="h-5 w-5 text-blue-500 mt-1 mr-3"),
                Div(
                    P("New team member", cls="text-sm font-medium"),
                    P("Sarah Johnson joined your workspace", cls="text-xs text-muted-foreground"),
                    P("1 hour ago", cls="text-xs text-muted-foreground")
                ),
                Button("×", variant="ghost", size="sm"),
                cls="flex items-start p-4 border-b hover:bg-muted/30"
            ),
            # More notifications...
            cls="flex-1 overflow-y-auto"
        ),
        SheetFooter(
            Button("Mark All Read", variant="outline"),
            Button("View All")
        ),
        signal="notifications_sheet",
        side="top",
        size="md"
    ),
    signal="notifications_sheet"
)''',
        title="Notification Panel",
        description="Top-sliding notification panel with action buttons and dismissible items"
    )
    
    # Action sheet (bottom side) - Mobile-friendly
    yield ComponentPreview(
        Sheet(
            SheetTrigger(
                Icon("lucide:more-horizontal", cls="h-4 w-4 mr-2"),
                "Actions",
                signal="actions_sheet",
                variant="outline"
            ),
            SheetContent(
                SheetHeader(
                    SheetTitle("Quick Actions", signal="actions_sheet"),
                    SheetDescription("Choose an action to perform", signal="actions_sheet")
                ),
                Div(
                    # Action buttons
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
                    SheetClose(
                        "Cancel",
                        signal="actions_sheet",
                        variant="outline",
                        cls="w-full"
                    )
                ),
                signal="actions_sheet",
                side="bottom",
                size="md"
            ),
            signal="actions_sheet"
        ),
        '''Sheet(
    SheetTrigger(
        Icon("lucide:more-horizontal"),
        "Actions",
        signal="actions_sheet",
        variant="outline"
    ),
    SheetContent(
        SheetHeader(
            SheetTitle("Quick Actions", signal="actions_sheet"),
            SheetDescription("Choose an action to perform", signal="actions_sheet")
        ),
        Div(
            # Action buttons
            Button(
                Icon("lucide:share"),
                Div(
                    P("Share", cls="font-medium"),
                    P("Share this item with others", cls="text-sm text-muted-foreground"),
                    cls="text-left"
                ),
                variant="ghost",
                cls="w-full justify-start p-4 h-auto"
            ),
            Button(
                Icon("lucide:copy"),
                Div(
                    P("Copy Link", cls="font-medium"),
                    P("Copy the link to your clipboard", cls="text-sm text-muted-foreground")
                ),
                variant="ghost",
                cls="w-full justify-start p-4 h-auto"
            ),
            Button(
                Icon("lucide:download"),
                Div("Download", "Save to your device"),
                variant="ghost",
                cls="w-full justify-start p-4 h-auto"
            ),
            Separator(),
            Button(
                Icon("lucide:trash-2"),
                Div("Delete", cls="font-medium text-red-600"),
                variant="ghost",
                cls="w-full justify-start p-4 h-auto"
            ),
            cls="px-6 space-y-1"
        ),
        SheetFooter(
            SheetClose("Cancel", signal="actions_sheet", variant="outline", cls="w-full")
        ),
        signal="actions_sheet",
        side="bottom",
        size="md"
    ),
    signal="actions_sheet"
)''',
        title="Action Sheet",
        description="Bottom-sliding mobile-friendly action sheet with contextual options"
    )
    
    # Contact form sheet
    yield ComponentPreview(
        Sheet(
            SheetTrigger(
                Icon("lucide:mail", cls="h-4 w-4 mr-2"),
                "Contact Us",
                signal="contact_sheet"
            ),
            SheetContent(
                SheetHeader(
                    SheetTitle("Contact Us", signal="contact_sheet"),
                    SheetDescription("Send us a message and we'll get back to you as soon as possible.", signal="contact_sheet")
                ),
                Form(
                    Div(
                        InputWithLabel(
                            label="Name",
                            placeholder="Your full name",
                            signal="contact_name",
                            required=True
                        ),
                        InputWithLabel(
                            label="Email",
                            type="email",
                            placeholder="your.email@example.com",
                            signal="contact_email",
                            required=True
                        ),
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
                        TextareaWithLabel(
                            label="Message",
                            placeholder="Tell us how we can help you...",
                            rows=4,
                            signal="contact_message",
                            required=True
                        ),
                        CheckboxWithLabel(
                            label="I'd like to receive updates about new features and improvements",
                            signal="contact_updates"
                        ),
                        ds_signals(
                            contact_name=value(""),
                            contact_email=value(""),
                            contact_subject=value(""),
                            contact_message=value(""),
                            contact_updates=False
                        ),
                        cls="space-y-4 px-6"
                    )
                ),
                SheetFooter(
                    Div(
                        SheetClose(
                            "Cancel",
                            signal="contact_sheet",
                            variant="outline",
                            cls="flex-1 mr-2"
                        ),
                        Button(
                            "Send Message",
                            ds_disabled="!$contact_name || !$contact_email || !$contact_subject || !$contact_message",
                            ds_on_click="""
                                if ($contact_name && $contact_email && $contact_subject && $contact_message) {
                                    alert('Message sent! We\\'ll get back to you soon.');
                                    $contact_name = ''; $contact_email = ''; 
                                    $contact_subject = ''; $contact_message = '';
                                    $contact_updates = false;
                                }
                            """,
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
        ),
        '''Sheet(
    SheetTrigger(
        Icon("lucide:mail"),
        "Contact Us",
        signal="contact_sheet"
    ),
    SheetContent(
        SheetHeader(
            SheetTitle("Contact Us", signal="contact_sheet"),
            SheetDescription("Send us a message and we'll get back to you.", signal="contact_sheet")
        ),
        Form(
            Div(
                InputWithLabel(
                    label="Name",
                    placeholder="Your full name",
                    signal="contact_name",
                    required=True
                ),
                InputWithLabel(
                    label="Email",
                    type="email",
                    placeholder="your.email@example.com",
                    signal="contact_email",
                    required=True
                ),
                SelectWithLabel(
                    label="Subject",
                    options=[
                        ("", "Select a topic"),
                        ("support", "Technical Support"),
                        ("billing", "Billing Question"),
                        ("feedback", "Product Feedback")
                    ],
                    signal="contact_subject"
                ),
                TextareaWithLabel(
                    label="Message",
                    placeholder="Tell us how we can help you...",
                    rows=4,
                    signal="contact_message",
                    required=True
                ),
                CheckboxWithLabel(
                    label="I'd like to receive updates",
                    signal="contact_updates"
                ),
                ds_signals(contact_name="", contact_email="", contact_subject=""),
                cls="space-y-4 px-6"
            )
        ),
        SheetFooter(
            SheetClose("Cancel", signal="contact_sheet", variant="outline"),
            Button(
                "Send Message",
                ds_disabled="!$contact_name || !$contact_email || !$contact_message",
                ds_on_click="sendContactMessage()"
            )
        ),
        signal="contact_sheet",
        side="right",
        size="lg"
    ),
    signal="contact_sheet"
)''',
        title="Contact Form",
        description="Complete contact form in a right-side sheet with validation"
    )
    
    # Different sizes demo
    yield ComponentPreview(
        Div(
            P("Different sheet sizes for various content needs:", cls="text-sm text-muted-foreground mb-4"),
            Div(
                Sheet(
                    SheetTrigger("Small", signal="small_size_sheet", variant="outline", size="sm"),
                    SheetContent(
                        SheetHeader(
                            SheetTitle("Small Sheet", signal="small_size_sheet"),
                            SheetDescription("Compact size for simple content", signal="small_size_sheet")
                        ),
                        Div(
                            P("This is a small sheet (max-w-sm) - perfect for simple forms, quick actions, or narrow content.", cls="text-sm"),
                            cls="px-6"
                        ),
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
                        SheetHeader(
                            SheetTitle("Medium Sheet", signal="medium_size_sheet"),
                            SheetDescription("Standard size for most content", signal="medium_size_sheet")
                        ),
                        Div(
                            P("This is a medium sheet (max-w-md) - the default size for most use cases including forms, settings, and moderate content.", cls="text-sm"),
                            cls="px-6"
                        ),
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
                        SheetHeader(
                            SheetTitle("Large Sheet", signal="large_size_sheet"),
                            SheetDescription("More space for complex content", signal="large_size_sheet")
                        ),
                        Div(
                            P("This is a large sheet (max-w-lg) - great for detailed forms, complex interfaces, shopping carts, and content that needs more horizontal space.", cls="text-sm"),
                            cls="px-6"
                        ),
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
                        SheetHeader(
                            SheetTitle("Extra Large Sheet", signal="xl_size_sheet"),
                            SheetDescription("Maximum width for extensive content", signal="xl_size_sheet")
                        ),
                        Div(
                            P("This is an extra large sheet (max-w-xl) - ideal for comprehensive dashboards, data tables, detailed settings panels, or any content requiring maximum horizontal space.", cls="text-sm"),
                            cls="px-6"
                        ),
                        signal="xl_size_sheet",
                        side="right",
                        size="xl"
                    ),
                    signal="xl_size_sheet"
                ),
                cls="flex flex-wrap gap-2 justify-center"
            ),
            cls="text-center"
        ),
        '''# Different sheet sizes
Sheet(SheetTrigger("Small"), SheetContent(...), signal="small", size="sm")
Sheet(SheetTrigger("Medium"), SheetContent(...), signal="medium", size="md")
Sheet(SheetTrigger("Large"), SheetContent(...), signal="large", size="lg")
Sheet(SheetTrigger("XL"), SheetContent(...), signal="xl", size="xl")''',
        title="Sheet Sizes",
        description="Different sheet sizes for various content requirements"
    )


def create_sheet_docs():
    """Create sheet documentation page using convention-based approach."""
    
    api_reference = {
        "props": [
            {
                "name": "signal",
                "type": "str",
                "description": "Unique identifier for the sheet state management"
            },
            {
                "name": "modal",
                "type": "bool", 
                "default": "True",
                "description": "Whether sheet blocks interaction with rest of page and shows overlay"
            },
            {
                "name": "default_open",
                "type": "bool",
                "default": "False", 
                "description": "Whether sheet is open by default"
            },
            {
                "name": "cls",
                "type": "str",
                "default": "''",
                "description": "Additional CSS classes for the container"
            }
        ],
        "sub_components": [
            {
                "name": "SheetTrigger",
                "description": "Button that opens the sheet",
                "props": [
                    {
                        "name": "signal",
                        "type": "str",
                        "description": "Must match the Sheet's signal"
                    },
                    {
                        "name": "variant",
                        "type": "Literal['default', 'secondary', 'destructive', 'outline', 'ghost', 'link']",
                        "default": "'outline'",
                        "description": "Button variant style"
                    },
                    {
                        "name": "cls",
                        "type": "str",
                        "default": "''",
                        "description": "Additional CSS classes"
                    }
                ]
            },
            {
                "name": "SheetContent",
                "description": "Container for the sheet panel content",
                "props": [
                    {
                        "name": "signal",
                        "type": "str", 
                        "description": "Must match the Sheet's signal"
                    },
                    {
                        "name": "side",
                        "type": "Literal['top', 'right', 'bottom', 'left']",
                        "default": "'right'",
                        "description": "Which side of the screen the sheet slides from"
                    },
                    {
                        "name": "size",
                        "type": "Literal['sm', 'md', 'lg', 'xl', 'full']",
                        "default": "'sm'",
                        "description": "Width of the sheet (for left/right) or height (for top/bottom)"
                    },
                    {
                        "name": "modal",
                        "type": "bool",
                        "default": "True",
                        "description": "Whether to show overlay and block page interaction"
                    },
                    {
                        "name": "show_close",
                        "type": "bool",
                        "default": "True",
                        "description": "Whether to show the X close button in top-right corner"
                    },
                    {
                        "name": "cls",
                        "type": "str",
                        "default": "''",
                        "description": "Additional CSS classes for content styling"
                    }
                ]
            },
            {
                "name": "SheetHeader",
                "description": "Container for sheet title and description"
            },
            {
                "name": "SheetTitle",
                "description": "The sheet's title heading",
                "props": [
                    {
                        "name": "signal",
                        "type": "str",
                        "description": "Must match the Sheet's signal for accessibility"
                    }
                ]
            },
            {
                "name": "SheetDescription", 
                "description": "Subtitle or description text",
                "props": [
                    {
                        "name": "signal",
                        "type": "str",
                        "description": "Must match the Sheet's signal for accessibility"
                    }
                ]
            },
            {
                "name": "SheetFooter",
                "description": "Container for action buttons at bottom of sheet"
            },
            {
                "name": "SheetClose",
                "description": "Button that closes the sheet",
                "props": [
                    {
                        "name": "signal",
                        "type": "str",
                        "description": "Must match the Sheet's signal"
                    },
                    {
                        "name": "variant",
                        "type": "Literal['default', 'secondary', 'destructive', 'outline', 'ghost', 'link']",
                        "default": "'ghost'",
                        "description": "Button variant style"
                    },
                    {
                        "name": "size",
                        "type": "Literal['default', 'sm', 'lg', 'icon']",
                        "default": "'sm'",
                        "description": "Button size"
                    },
                    {
                        "name": "cls",
                        "type": "str",
                        "default": "''",
                        "description": "Additional CSS classes"
                    }
                ]
            }
        ]
    }
    
    # Hero example
    hero_example = ComponentPreview(
        Sheet(
            SheetTrigger("Open Sheet", signal="hero_sheet"),
            SheetContent(
                SheetHeader(
                    SheetTitle("Edit Profile", signal="hero_sheet"),
                    SheetDescription("Make changes to your profile here. Click save when you're done.", signal="hero_sheet")
                ),
                Div(
                    InputWithLabel(
                        label="Name",
                        placeholder="Pedro Duarte",
                        signal="profile_name"
                    ),
                    InputWithLabel(
                        label="Username",
                        placeholder="@peduarte",
                        signal="profile_username"
                    ),
                    ds_signals(
                        profile_name=value(""),
                        profile_username=value("")
                    ),
                    cls="space-y-4 px-6 py-4"
                ),
                SheetFooter(
                    SheetClose("Cancel", signal="hero_sheet", variant="outline"),
                    Button("Save changes")
                ),
                signal="hero_sheet"
            ),
            signal="hero_sheet"
        ),
        '''Sheet(
    SheetTrigger("Open Sheet", signal="hero_sheet"),
    SheetContent(
        SheetHeader(
            SheetTitle("Edit Profile", signal="hero_sheet"),
            SheetDescription("Make changes to your profile here.", signal="hero_sheet")
        ),
        Div(
            InputWithLabel(label="Name", placeholder="Pedro Duarte", signal="profile_name"),
            InputWithLabel(label="Username", placeholder="@peduarte", signal="profile_username"),
            ds_signals(profile_name="", profile_username=""),
            cls="space-y-4 px-6 py-4"
        ),
        SheetFooter(
            SheetClose("Cancel", signal="hero_sheet", variant="outline"),
            Button("Save changes")
        ),
        signal="hero_sheet"
    ),
    signal="hero_sheet"
)''',
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