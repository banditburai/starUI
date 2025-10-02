#!/usr/bin/env python3
"""Minimal test app for migrating components one by one."""
from starhtml import *

# Use registry_loader to set up paths, but don't load all components yet
# (we'll manually import only the ones we've migrated)
import registry_loader  # This adds parent dir to sys.path

# Import components as we migrate them
from src.starui.registry.components.accordion import Accordion, AccordionItem, AccordionTrigger, AccordionContent
from src.starui.registry.components.alert import Alert, AlertTitle, AlertDescription
from src.starui.registry.components.alert_dialog import (
    AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent,
    AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle, AlertDialogTrigger
)
from src.starui.registry.components.avatar import Avatar, AvatarImage, AvatarFallback, AvatarWithFallback
from src.starui.registry.components.badge import Badge
from src.starui.registry.components.button import Button
from src.starui.registry.components.calendar import Calendar
from src.starui.registry.components.theme_toggle import ThemeToggle

styles = Link(rel="stylesheet", href="/static/css/starui.css", type="text/css")

app, rt = star_app(
    live=True,
    hdrs=(
        fouc_script(use_data_theme=True),
        styles,
        position_handler(),
    ),
    htmlkw=dict(lang="en", dir="ltr"),
    bodykw=dict(
        cls="min-h-screen bg-background text-foreground p-8",
    ),
    iconify=True,
    clipboard=True
)


@rt("/")
def index():
    """Index page with links to each component test."""
    return Div(
        # Theme toggle in top-right
        Div(ThemeToggle(), cls="absolute top-4 right-4"),

        H1("Component Migration Test Suite", cls="text-4xl font-bold mb-8"),
        P("Click a component to test it individually:", cls="text-muted-foreground mb-4"),

        Div(
            A("Accordion", href="/accordion", cls="text-primary hover:underline block"),
            A("Alert", href="/alert", cls="text-primary hover:underline block"),
            A("Alert Dialog", href="/alert-dialog", cls="text-primary hover:underline block"),
            A("Avatar", href="/avatar", cls="text-primary hover:underline block"),
            A("Badge", href="/badge", cls="text-primary hover:underline block"),
            A("Button", href="/button", cls="text-primary hover:underline block"),
            A("Calendar", href="/calendar", cls="text-primary hover:underline block"),
            A("Theme Toggle", href="/theme-toggle", cls="text-primary hover:underline block"),
            cls="space-y-2"
        ),
        cls="container mx-auto"
    )


# Component test routes - add as we migrate each component

@rt("/accordion")
def test_accordion():
    return Div(
        # Theme toggle in top-right
        Div(ThemeToggle(), cls="absolute top-4 right-4"),

        H1("Accordion Component Test", cls="text-3xl font-bold mb-6"),
        A("← Back to Index", href="/", cls="text-primary hover:underline mb-4 inline-block"),

        H2("Single Mode (Collapsible)", cls="text-2xl font-semibold mb-4 mt-8"),
        Accordion(
            AccordionItem(
                AccordionTrigger("Is it accessible?"),
                AccordionContent("Yes. It adheres to the WAI-ARIA design pattern."),
                value="item-1"
            ),
            AccordionItem(
                AccordionTrigger("Is it styled?"),
                AccordionContent("Yes. It comes with default styles that match the other components."),
                value="item-2"
            ),
            AccordionItem(
                AccordionTrigger("Is it animated?"),
                AccordionContent("Yes. It's animated by default, but you can disable it if needed."),
                value="item-3"
            ),
            type="single",
            collapsible=True,
            cls="max-w-2xl"
        ),

        H2("Multiple Mode", cls="text-2xl font-semibold mb-4 mt-8"),
        Accordion(
            AccordionItem(
                AccordionTrigger("Can I open multiple items?"),
                AccordionContent("Yes! In multiple mode, you can have several items expanded at once."),
                value="multi-1"
            ),
            AccordionItem(
                AccordionTrigger("Does it remember state?"),
                AccordionContent("Yes, the state is managed via signals."),
                value="multi-2"
            ),
            AccordionItem(
                AccordionTrigger("Is it customizable?"),
                AccordionContent("Yes, you can pass custom classes and styling."),
                value="multi-3"
            ),
            type="multiple",
            default_value=["multi-1"],
            cls="max-w-2xl"
        ),

        cls="container mx-auto"
    )


@rt("/alert")
def test_alert():
    return Div(
        # Theme toggle in top-right
        Div(ThemeToggle(), cls="absolute top-4 right-4"),

        H1("Alert Component Test", cls="text-3xl font-bold mb-6"),
        A("← Back to Index", href="/", cls="text-primary hover:underline mb-4 inline-block"),

        H2("Alert Variants", cls="text-2xl font-semibold mb-4 mt-8"),
        Div(
            Alert(
                AlertTitle("Default Alert"),
                AlertDescription("This is a default alert message."),
            ),
            Alert(
                AlertTitle("Destructive Alert"),
                AlertDescription("This is a destructive alert message."),
                variant="destructive",
            ),
            cls="space-y-4 max-w-2xl"
        ),

        H2("Alert with Icon", cls="text-2xl font-semibold mb-4 mt-8"),
        Div(
            Alert(
                Icon("lucide:info"),
                AlertTitle("Heads up!"),
                AlertDescription("You can add icons to alerts for better visual communication."),
            ),
            Alert(
                Icon("lucide:alert-triangle"),
                AlertTitle("Warning"),
                AlertDescription("This alert includes an icon to draw attention to important information."),
                variant="destructive",
            ),
            cls="space-y-4 max-w-2xl"
        ),

        cls="container mx-auto"
    )


@rt("/avatar")
def test_avatar():
    return Div(
        # Theme toggle in top-right
        Div(ThemeToggle(), cls="absolute top-4 right-4"),

        H1("Avatar Component Test", cls="text-3xl font-bold mb-6"),
        A("← Back to Index", href="/", cls="text-primary hover:underline mb-4 inline-block"),

        H2("Basic Avatar", cls="text-2xl font-semibold mb-4 mt-8"),
        Div(
            Avatar(
                AvatarImage(
                    src="https://github.com/shadcn.png",
                    alt="@shadcn"
                )
            ),
            Avatar(
                AvatarFallback("CN")
            ),
            Avatar(
                AvatarImage(
                    src="https://avatars.githubusercontent.com/u/1?v=4",
                    alt="User"
                )
            ),
            cls="flex gap-4 items-center"
        ),

        H2("Avatar Sizes", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Use size classes to customize:", cls="text-sm text-muted-foreground mb-2"),
        Div(
            Avatar(AvatarFallback("XS"), cls="size-6"),
            Avatar(AvatarFallback("SM"), cls="size-8"),
            Avatar(AvatarFallback("MD")),
            Avatar(AvatarFallback("LG"), cls="size-12"),
            Avatar(AvatarFallback("XL"), cls="size-16"),
            Avatar(AvatarFallback("2X"), cls="size-20"),
            cls="flex gap-4 items-center"
        ),

        H2("Automatic Fallback", cls="text-2xl font-semibold mb-4 mt-8"),
        P("The second avatar will show fallback as the image URL is invalid:", cls="text-sm text-muted-foreground mb-2"),
        Div(
            AvatarWithFallback(
                src="https://github.com/shadcn.png",
                alt="@shadcn",
                fallback="CN"
            ),
            AvatarWithFallback(
                src="https://invalid-url.com/image.jpg",
                alt="Invalid",
                fallback="IN"
            ),
            AvatarWithFallback(
                fallback="NI"
            ),
            cls="flex gap-4 items-center"
        ),

        cls="container mx-auto"
    )


@rt("/badge")
def test_badge():
    return Div(
        # Theme toggle in top-right
        Div(ThemeToggle(), cls="absolute top-4 right-4"),

        H1("Badge Component Test", cls="text-3xl font-bold mb-6"),
        A("← Back to Index", href="/", cls="text-primary hover:underline mb-4 inline-block"),

        H2("Badge Variants", cls="text-2xl font-semibold mb-4 mt-8"),
        Div(
            Badge("Default"),
            Badge("Secondary", variant="secondary"),
            Badge("Destructive", variant="destructive"),
            Badge("Outline", variant="outline"),
            cls="flex flex-wrap gap-2 max-w-2xl"
        ),

        H2("Badge with Icons", cls="text-2xl font-semibold mb-4 mt-8"),
        Div(
            Badge(Icon("lucide:check"), "Verified", variant="secondary"),
            Badge(Icon("lucide:star"), "Featured"),
            Badge(Icon("lucide:alert-triangle"), "Warning", variant="destructive"),
            Badge(Icon("lucide:info"), "Info", variant="outline"),
            cls="flex flex-wrap gap-2 max-w-2xl"
        ),

        H2("Clickable Badges", cls="text-2xl font-semibold mb-4 mt-8"),
        Div(
            (click_count := Signal("badge_clicks", 0)),
            Badge(
                "Click me",
                clickable=True,
                data_on_click=click_count.add(1),
            ),
            Badge(
                Icon("lucide:x"),
                "Dismiss",
                variant="destructive",
                clickable=True,
                data_on_click=js("alert('Dismissed!')"),
            ),
            P(data_text="Clicks: " + click_count, cls="text-sm text-muted-foreground mt-2"),
            cls="flex flex-wrap gap-2 max-w-2xl"
        ),

        H2("Badge as Link", cls="text-2xl font-semibold mb-4 mt-8"),
        Div(
            Badge("Home", href="/", variant="secondary"),
            Badge("Documentation", href="#docs", variant="outline"),
            Badge("GitHub", href="https://github.com", variant="default"),
            cls="flex flex-wrap gap-2 max-w-2xl"
        ),

        cls="container mx-auto"
    )


@rt("/api/data")
async def api_data():
    """Simulates a slow API endpoint for data-indicator demo."""
    import asyncio
    await asyncio.sleep(2)  # Simulate slow network

    content = Div(
        P("✓ Data fetched successfully!", cls="text-green-600 font-medium"),
        P(f"Fetched at: {__import__('datetime').datetime.now().strftime('%H:%M:%S')}", cls="text-xs text-green-600"),
        id="api-response",
        cls="mt-2 p-2 bg-green-50 rounded border border-green-200"
    )

    # Test: Response without to_xml()
    return Response(
        content=content,  # Pass FT directly - does Response handle conversion?
        media_type="text/html",
        headers={
            "datastar-selector": "#api-response",
            "datastar-mode": "outer"
        }
    )


@rt("/button")
def test_button():
    return Div(
        # Theme toggle in top-right
        Div(ThemeToggle(), cls="absolute top-4 right-4"),

        H1("Button Component Test", cls="text-3xl font-bold mb-6"),
        A("← Back to Index", href="/", cls="text-primary hover:underline mb-4 inline-block"),

        H2("Button Variants", cls="text-2xl font-semibold mb-4 mt-8"),
        Div(
            Button("Default"),
            Button("Destructive", variant="destructive"),
            Button("Outline", variant="outline"),
            Button("Secondary", variant="secondary"),
            Button("Ghost", variant="ghost"),
            Button("Link", variant="link"),
            cls="flex flex-wrap gap-2 max-w-2xl"
        ),

        H2("Button Sizes", cls="text-2xl font-semibold mb-4 mt-8"),
        Div(
            Button("Small", size="sm"),
            Button("Default", size="default"),
            Button("Large", size="lg"),
            Button(Icon("lucide:settings"), size="icon", variant="outline"),
            Button(Icon("lucide:trash"), size="icon", variant="destructive"),
            cls="flex flex-wrap gap-2 items-center max-w-2xl"
        ),

        H2("Buttons with Icons", cls="text-2xl font-semibold mb-4 mt-8"),
        Div(
            Button(Icon("lucide:mail"), "Email"),
            Button(Icon("lucide:download"), "Download", variant="secondary"),
            Button("Delete", Icon("lucide:trash"), variant="destructive"),
            Button(Icon("lucide:settings"), "Settings", variant="outline"),
            cls="flex flex-wrap gap-2 max-w-2xl"
        ),

        H2("Interactive Buttons", cls="text-2xl font-semibold mb-4 mt-8"),
        Div(
            (count := Signal("button_count", 0)),
            Button(
                Icon("lucide:plus"),
                "Increment",
                data_on_click=count.add(1),
            ),
            Button(
                Icon("lucide:minus"),
                "Decrement",
                variant="secondary",
                data_on_click=count.sub(1),
            ),
            Button(
                Icon("lucide:rotate-ccw"),
                "Reset",
                variant="outline",
                data_on_click=count.set(0),
            ),
            P(data_text="Count: " + count, cls="text-lg font-semibold"),
            cls="flex flex-wrap gap-2 items-center max-w-2xl"
        ),

        H2("Disabled State", cls="text-2xl font-semibold mb-4 mt-8"),
        Div(
            Button("Disabled Default", disabled=True),
            Button("Disabled Destructive", variant="destructive", disabled=True),
            Button("Disabled Outline", variant="outline", disabled=True),
            cls="flex flex-wrap gap-2 max-w-2xl"
        ),

        H2("Loading State Pattern 1: data-show Toggle (Best for 2 states)", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Both icons in DOM, toggled with data-show. Fast CSS-only switching.", cls="text-sm text-muted-foreground mb-2"),
        Div(
            (is_loading := Signal("is_loading", False)),
            Button(
                Icon("lucide:loader-2", cls="animate-spin", data_show=is_loading),
                Icon("lucide:save", data_show=~is_loading),
                Span(data_text=is_loading.if_("Loading...", "Save")),
                data_on_click=is_loading.toggle(),
                data_attr_disabled=is_loading,
            ),
            Button(
                Icon("lucide:loader-2", cls="animate-spin", data_show=is_loading),
                Icon("lucide:upload", data_show=~is_loading),
                Span(data_text=is_loading.if_("Uploading...", "Upload")),
                variant="secondary",
                data_on_click=is_loading.toggle(),
                data_attr_disabled=is_loading,
            ),
            P("✓ Fastest: Both icons preloaded, CSS toggle only", cls="text-xs text-muted-foreground mt-2"),
            cls="flex flex-wrap gap-2 items-start max-w-2xl"
        ),

        H2("Loading State Pattern 2: Signal Value (Best for 3+ states)", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Icon name stored in signal. Useful for multiple states, but requires icon re-render.", cls="text-sm text-muted-foreground mb-2"),
        Div(
            (status := Signal("status", "pending")),
            Button(
                Icon(
                    "lucide:clock",  # Initial icon
                    data_attr_icon=match(status,
                        pending="lucide:clock",
                        processing="lucide:loader-2",
                        success="lucide:check",
                        error="lucide:x"
                    ),
                    data_attr_class=match(status,
                        processing="animate-spin"
                    )
                ),
                Span(
                    data_text=match(status,
                        pending="Start Process",
                        processing="Processing...",
                        success="Success!",
                        error="Failed"
                    )
                ),
                data_on_click=js(
                    "$status = $status === 'pending' ? 'processing' : "
                    "$status === 'processing' ? 'success' : "
                    "$status === 'success' ? 'error' : 'pending'"
                ),
                data_attr_variant=match(status,
                    pending="default",
                    processing="secondary",
                    success="secondary",
                    error="destructive"
                ),
            ),
            Button(
                Icon("lucide:rotate-ccw"),
                "Reset",
                variant="outline",
                size="sm",
                data_on_click=status.set("pending"),
            ),
            P("✓ Better for 3+ states: Only one icon element, state-driven", cls="text-xs text-muted-foreground mt-2"),
            cls="flex flex-wrap gap-2 items-start max-w-2xl"
        ),

        H2("Pattern 3: Real Backend Loading (data-indicator)", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Uses Datastar's built-in data-indicator for actual backend requests:", cls="text-sm text-muted-foreground mb-2"),
        Div(
            Button(
                Icon("lucide:loader-2", cls="animate-spin", data_show="$fetching"),
                Icon("lucide:download", data_show="!$fetching"),
                data_text="$fetching ? 'Fetching...' : 'Fetch Data'",
                data_on_click=get("/api/data"),
                data_indicator_fetching=True,
                data_attr_disabled="$fetching",
                variant="outline",
            ),
            Div(
                P("Response will appear here...", cls="text-muted-foreground text-sm italic"),
                id="api-response",
                cls="mt-2"
            ),
            P("✓ Automatic: $fetching signal created by Datastar during requests", cls="text-xs text-muted-foreground mt-2"),
            P("Click button to see 2-second simulated network delay", cls="text-xs text-muted-foreground"),
            cls="flex flex-col gap-2 max-w-2xl"
        ),

        cls="container mx-auto"
    )


@rt("/alert-dialog")
def test_alert_dialog():
    return Div(
        # Theme toggle in top-right
        Div(ThemeToggle(), cls="absolute top-4 right-4"),

        H1("Alert Dialog Component Test", cls="text-3xl font-bold mb-6"),
        A("← Back to Index", href="/", cls="text-primary hover:underline mb-4 inline-block"),

        H2("Alert Dialog Variants", cls="text-2xl font-semibold mb-4 mt-8"),
        Div(
            # Basic alert dialog
            AlertDialog(
                trigger=AlertDialogTrigger("Show Alert"),
                content=AlertDialogContent(
                    AlertDialogHeader(
                        AlertDialogTitle("Are you absolutely sure?"),
                        AlertDialogDescription(
                            "This action cannot be undone. This will permanently delete your "
                            "account and remove your data from our servers."
                        ),
                    ),
                    AlertDialogFooter(
                        AlertDialogCancel("Cancel"),
                        AlertDialogAction(
                            "Continue",
                            action="console.log('Action confirmed!')",
                        ),
                    ),
                ),
            ),
            # Destructive alert dialog
            AlertDialog(
                trigger=AlertDialogTrigger("Delete Item", variant="destructive"),
                content=AlertDialogContent(
                    AlertDialogHeader(
                        AlertDialogTitle("Delete Item"),
                        AlertDialogDescription(
                            "Are you sure you want to delete this item? This action is irreversible."
                        ),
                    ),
                    AlertDialogFooter(
                        AlertDialogCancel("Cancel"),
                        AlertDialogAction(
                            "Delete",
                            variant="destructive",
                            action="console.log('Item deleted!')",
                        ),
                    ),
                ),
            ),
            # Alert dialog with custom action
            AlertDialog(
                trigger=AlertDialogTrigger("Confirm Action", variant="outline"),
                content=AlertDialogContent(
                    AlertDialogHeader(
                        AlertDialogTitle("Confirm Action"),
                        AlertDialogDescription(
                            "This will apply the changes you've made. Do you want to proceed?"
                        ),
                    ),
                    AlertDialogFooter(
                        AlertDialogCancel("Not now"),
                        AlertDialogAction(
                            "Yes, apply changes",
                            action="alert('Changes applied successfully!')",
                        ),
                    ),
                ),
            ),
            cls="flex flex-wrap gap-4",
        ),

        cls="container mx-auto"
    )


@rt("/calendar")
def test_calendar():
    return Div(
        # Theme toggle in top-right
        Div(ThemeToggle(), cls="absolute top-4 right-4"),

        H1("Calendar Component Test", cls="text-3xl font-bold mb-6"),
        A("← Back to Index", href="/", cls="text-primary hover:underline mb-4 inline-block"),

        H2("Single Mode", cls="text-2xl font-semibold mb-4 mt-8"),
        Div(
            Calendar(signal="test_single", mode="single"),
            Div(
                P("Selected: ", Span(data_text="$test_single_selected || 'None'", cls="font-mono text-sm")),
                cls="mt-4 text-sm"
            ),
            cls="flex flex-col items-center"
        ),

        H2("Range Mode", cls="text-2xl font-semibold mb-4 mt-8"),
        Div(
            Calendar(
                signal="test_range",
                mode="range",
                selected=["2025-09-15", "2025-09-25"],
                month=9,
                year=2025
            ),
            Div(                
                P("Range: ", Span(data_text="JSON.stringify($test_range_selected)", cls="font-mono text-sm")),
                cls="mt-4 text-sm"
            ),
            cls="flex flex-col items-center"
        ),

        H2("Multiple Mode", cls="text-2xl font-semibold mb-4 mt-8"),
        Div(
            Calendar(
                signal="test_multiple",
                mode="multiple",
                selected=["2025-09-10", "2025-09-15", "2025-09-20"],
                month=9,
                year=2025
            ),
            Div(
                P("Selected: ", Span(data_text="($test_multiple_selected || []).length", cls="font-mono"), " dates"),
                cls="mt-4 text-sm"
            ),
            cls="flex flex-col items-center"
        ),

        H2("Disabled", cls="text-2xl font-semibold mb-4 mt-8"),
        Div(
            Calendar(signal="test_disabled", mode="single", disabled=True),
            cls="flex flex-col items-center"
        ),

        cls="container mx-auto"
    )


@rt("/theme-toggle")
def test_theme_toggle():
    return Div(
        # Theme toggle in top-right
        Div(ThemeToggle(), cls="absolute top-4 right-4"),

        H1("Theme Toggle Component Test", cls="text-3xl font-bold mb-6"),
        A("← Back to Index", href="/", cls="text-primary hover:underline mb-4 inline-block"),

        H2("Instructions", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Click the theme toggle button in the top-right corner to switch between light and dark themes.", cls="text-muted-foreground mb-4"),
        P("The theme preference is saved to localStorage and will persist across page reloads.", cls="text-muted-foreground mb-4"),

        H2("Theme-aware Content", cls="text-2xl font-semibold mb-4 mt-8"),
        Div(
            P("This text should adapt to the current theme.", cls="mb-2"),
            P("Background and foreground colors are theme-aware.", cls="mb-2"),
            Div("Bordered box", cls="border border-border p-4 rounded-md bg-card text-card-foreground"),
            cls="space-y-4 max-w-2xl"
        ),

        cls="container mx-auto"
    )


serve()
