#!/usr/bin/env python3
"""Minimal test app for migrating components one by one."""

# IMPORTANT: Monkey-patch starhtml.datastar BEFORE any imports
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
import patch_datastar  # noqa: F401

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
from src.starui.registry.components.card import Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter
from src.starui.registry.components.checkbox import Checkbox, CheckboxWithLabel
from src.starui.registry.components.code_block import CodeBlock, CodeBlockStyles
from src.starui.registry.components.date_picker import (
    DatePicker, DateTimePicker, DatePickerWithInput
)
from src.starui.registry.components.dialog import (
    Dialog, DialogTrigger, DialogContent, DialogClose,
    DialogHeader, DialogFooter, DialogTitle, DialogDescription
)
from src.starui.registry.components.dropdown_menu import (
    DropdownMenu, DropdownMenuTrigger, DropdownMenuContent, DropdownMenuItem,
    DropdownMenuCheckboxItem, DropdownMenuRadioGroup, DropdownMenuRadioItem,
    DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuShortcut,
    DropdownMenuGroup, DropdownMenuSub, DropdownMenuSubTrigger, DropdownMenuSubContent
)
from src.starui.registry.components.hover_card import HoverCard, HoverCardTrigger, HoverCardContent
from src.starui.registry.components.popover import Popover, PopoverTrigger, PopoverContent, PopoverClose
from src.starui.registry.components.command import (
    Command, CommandDialog, CommandInput, CommandList, CommandEmpty,
    CommandGroup, CommandItem, CommandSeparator, CommandShortcut
)
from src.starui.registry.components.input import Input, InputWithLabel
from src.starui.registry.components.label import Label
from src.starui.registry.components.progress import Progress
from src.starui.registry.components.radio_group import RadioGroup, RadioGroupItem, RadioGroupWithLabel
from src.starui.registry.components.theme_toggle import ThemeToggle

styles = Link(rel="stylesheet", href="/static/css/starui.css", type="text/css")


def Page(*children, title="Component Test", show_back_link=True):
    """Wrapper for consistent page layout with theme toggle and back link."""
    return Div(
        A(
            Icon("lucide:arrow-left", width=20, height=20),
            href="/",
            cls="absolute top-4 left-4 inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors hover:bg-accent hover:text-accent-foreground h-10 w-10"
        ) if show_back_link else None,
        Div(ThemeToggle(), cls="absolute top-4 right-4"),
        H1(title, cls="text-3xl font-bold mb-8 mt-16"),
        *children,
        cls="container mx-auto"
    )

app, rt = star_app(
    live=True,
    hdrs=(
        fouc_script(use_data_theme=True),
        CodeBlockStyles(
            custom_css=".code-container pre { border-radius: 8px; }"
        ),
        styles,
        position_handler(),
    ),
    htmlkw=dict(lang="en", dir="ltr"),
    bodykw=dict(
        cls="min-h-screen bg-background text-foreground px-8 pt-8 pb-96",
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
            A("Card", href="/card", cls="text-primary hover:underline block"),
            A("Checkbox", href="/checkbox", cls="text-primary hover:underline block"),
            A("Code Block", href="/code-block", cls="text-primary hover:underline block"),
            A("Command", href="/command", cls="text-primary hover:underline block"),
            A("Date Picker", href="/date-picker", cls="text-primary hover:underline block"),
            A("Dialog", href="/dialog", cls="text-primary hover:underline block"),
            A("Dropdown Menu", href="/dropdown-menu", cls="text-primary hover:underline block"),
            A("Hover Card", href="/hover-card", cls="text-primary hover:underline block"),
            A("Input", href="/input", cls="text-primary hover:underline block"),
            A("Label", href="/label", cls="text-primary hover:underline block"),
            A("Popover", href="/popover", cls="text-primary hover:underline block"),
            A("Progress", href="/progress", cls="text-primary hover:underline block"),
            A("Radio Group", href="/radio-group", cls="text-primary hover:underline block"),
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

    return Fragment(
        Div(
            P("✓ Data fetched successfully!", cls="text-green-600 font-medium"),
            P(f"Fetched at: {__import__('datetime').datetime.now().strftime('%H:%M:%S')}", cls="text-xs text-green-600"),
            id="api-response",
            cls="mt-2 p-2 bg-green-50 rounded border border-green-200"
        )
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
                AlertDialogTrigger("Show Alert"),
                AlertDialogContent(
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
                AlertDialogTrigger("Delete Item", variant="destructive"),
                AlertDialogContent(
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
                AlertDialogTrigger("Confirm Action", variant="outline"),
                AlertDialogContent(
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
            (cal_single := Calendar(signal="test_single", mode="single")),
            Div(
                P("Selected: ", Span(data_text=cal_single.selected.if_(cal_single.selected, "'None'"), cls="font-mono text-sm")),
                cls="mt-4 text-sm"
            ),
            cls="flex flex-col items-center"
        ),

        H2("Range Mode", cls="text-2xl font-semibold mb-4 mt-8"),
        Div(
            (cal_range := Calendar(
                signal="test_range",
                mode="range",
                selected=["2025-09-15", "2025-09-25"],
                month=9,
                year=2025
            )),
            Div(
                P("Range: ", Span(data_text="JSON.stringify(" + cal_range.selected + ")", cls="font-mono text-sm")),
                cls="mt-4 text-sm"
            ),
            cls="flex flex-col items-center"
        ),

        H2("Multiple Mode", cls="text-2xl font-semibold mb-4 mt-8"),
        Div(
            (cal_multiple := Calendar(
                signal="test_multiple",
                mode="multiple",
                selected=["2025-09-10", "2025-09-15", "2025-09-20"],
                month=9,
                year=2025
            )),
            Div(
                P("Selected: ", Span(data_text="(" + cal_multiple.selected + " || []).length", cls="font-mono"), " dates"),
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


@rt("/card")
def test_card():
    return Div(
        # Theme toggle in top-right
        Div(ThemeToggle(), cls="absolute top-4 right-4"),

        H1("Card Component Test", cls="text-3xl font-bold mb-6"),
        A("← Back to Index", href="/", cls="text-primary hover:underline mb-4 inline-block"),

        H2("Basic Card", cls="text-2xl font-semibold mb-4 mt-8"),
        Card(
            CardHeader(
                CardTitle("Card Title"),
                CardDescription(
                    "This is a card description with some example text."
                ),
            ),
            CardContent(
                P("Card content goes here. You can add any elements you want."),
            ),
            CardFooter(
                Button("Cancel", variant="outline"),
                Button("Save"),
                cls="flex gap-2",
            ),
            cls="max-w-md",
        ),

        H2("Card with Input", cls="text-2xl font-semibold mb-4 mt-8"),
        Card(
            CardHeader(
                CardTitle("Login to your account"),
                CardDescription("Enter your email below to login to your account"),
            ),
            CardContent(
                Div(
                    Label("Email", For="email", cls="text-sm font-medium"),
                    Input(id="email", type="email", placeholder="m@example.com", cls="mt-1"),
                    cls="mb-4"
                ),
                Div(
                    Label("Password", For="password", cls="text-sm font-medium"),
                    Input(id="password", type="password", cls="mt-1"),
                    cls="mb-4"
                ),
            ),
            CardFooter(
                Button("Login", cls="w-full"),
            ),
            cls="max-w-md",
        ),

        H2("Card with Action", cls="text-2xl font-semibold mb-4 mt-8"),
        Card(
            CardHeader(
                CardTitle("Notifications", level="h4"),
                CardDescription("You have 3 unread messages"),
            ),
            CardContent(
                Div(
                    Div(
                        P("New message from Alice", cls="font-medium"),
                        P("Hey, are you available for a call?", cls="text-sm text-muted-foreground"),
                        cls="mb-3"
                    ),
                    Div(
                        P("Project update", cls="font-medium"),
                        P("The new feature has been deployed.", cls="text-sm text-muted-foreground"),
                        cls="mb-3"
                    ),
                    Div(
                        P("Reminder", cls="font-medium"),
                        P("Team meeting at 3 PM today.", cls="text-sm text-muted-foreground"),
                    ),
                ),
            ),
            CardFooter(
                Button("Mark all as read", variant="outline", cls="w-full"),
            ),
            cls="max-w-md",
        ),

        H2("Compact Card", cls="text-2xl font-semibold mb-4 mt-8"),
        Card(
            CardHeader(
                CardTitle("Quick Stats", level="h5"),
            ),
            CardContent(
                Div(
                    Div(
                        P("Total Users", cls="text-sm text-muted-foreground"),
                        P("1,234", cls="text-2xl font-bold"),
                        cls="mb-2"
                    ),
                    Div(
                        P("Active Sessions", cls="text-sm text-muted-foreground"),
                        P("89", cls="text-2xl font-bold"),
                    ),
                ),
            ),
            cls="max-w-xs",
        ),

        cls="container mx-auto"
    )


@rt("/checkbox")
def test_checkbox():
    return Div(
        # Theme toggle in top-right
        Div(ThemeToggle(), cls="absolute top-4 right-4"),

        H1("Checkbox Component Test", cls="text-3xl font-bold mb-6"),
        A("← Back to Index", href="/", cls="text-primary hover:underline mb-4 inline-block"),

        H2("Checkbox Variants", cls="text-2xl font-semibold mb-4 mt-8"),
        Div(
            CheckboxWithLabel(
                label="Accept terms and conditions",
                signal="terms",
                required=True
            ),
            CheckboxWithLabel(
                label="Subscribe to newsletter",
                signal="newsletter",
                helper_text="Get weekly updates about new features",
            ),
            CheckboxWithLabel(
                label="Enable notifications",
                signal="notifications",
                checked=True
            ),
            CheckboxWithLabel(
                label="Disabled option",
                disabled=True,
                helper_text="This option is currently unavailable",
            ),
            CheckboxWithLabel(
                label="Error state example",
                signal="error_checkbox",
                error_text="This field is required",
            ),
            cls="space-y-4"
        ),

        H2("Custom Styled Checkbox", cls="text-2xl font-semibold mb-4 mt-8"),
        Div(
            CheckboxWithLabel(
                label="Custom blue checkbox",
                signal="blue_checkbox",
                helper_text="With custom blue styling when checked",
                checkbox_cls="checked:!bg-blue-600 checked:!border-blue-600 dark:checked:!bg-blue-700 dark:checked:!border-blue-700",
                indicator_cls="!text-white",
            ),
            cls="p-4 border rounded-lg max-w-md",
        ),

        cls="container mx-auto"
    )


@rt("/code-block")
def test_code_block():
    return Div(
        Div(ThemeToggle(), cls="absolute top-4 right-4"),

        H1("Code Block Component Test", cls="text-3xl font-bold mb-6"),
        A("← Back to Index", href="/", cls="text-primary hover:underline mb-4 inline-block"),

        H2("Python Code", cls="text-2xl font-semibold mb-4 mt-8"),
        CodeBlock('''def hello_world():
    """A simple greeting function"""
    message = "Hello, world!"
    print(message)
    return 42''', "python"),

        H2("JavaScript Code", cls="text-2xl font-semibold mb-4 mt-8"),
        CodeBlock('''function factorial(n) {
  if (n <= 1) return 1;
  return n * factorial(n - 1);
}

console.log(factorial(5));''', "javascript"),

        H2("Theme Switching", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Click the theme toggle (top-right) to test:", cls="mb-2"),
        Ul(
            Li("Code blocks should switch between light/dark themes"),
            Li("Light mode: white background with dark text"),
            Li("Dark mode: dark background with light text"),
            Li("Syntax colors should adapt to the theme"),
            Li("No page reload needed - instant CSS switch"),
            cls="list-disc list-inside space-y-1 text-muted-foreground mb-4"
        ),

        H2("Expected Styling", cls="text-2xl font-semibold mb-4 mt-8"),
        P("All code blocks should have:", cls="mb-2"),
        Ul(
            Li("Syntax highlighting with proper token colors"),
            Li("Theme-aware background and text colors"),
            Li("Rounded corners (8px border-radius)"),
            Li("Proper padding (20px)"),
            Li("Horizontal scrollbar if content overflows"),
            Li("Monospace font (Monaco, Menlo, etc.)"),
            cls="list-disc list-inside space-y-1 text-muted-foreground"
        ),

        H2("Custom Styled Block", cls="text-2xl font-semibold mb-4 mt-8"),
        P("This code block has custom border styling:", cls="mb-2"),
        CodeBlock('''print("Custom styling test")
x = 1 + 2
print(f"Result: {x}")''', "python", cls="!border-4 !border-primary !rounded-xl"),

        cls="container mx-auto"
    )


@rt("/date-picker")
def test_date_picker():
    return Div(
        # Theme toggle in top-right
        Div(ThemeToggle(), cls="absolute top-4 right-4"),

        H1("Date Picker Component Test", cls="text-3xl font-bold mb-6"),
        A("← Back to Index", href="/", cls="text-primary hover:underline mb-4 inline-block"),

        H2("Date Picker Variants", cls="text-2xl font-semibold mb-4 mt-8"),

        Div(
            # Single date picker
            Div(
                H3("Single Date", cls="text-lg font-medium mb-2"),
                DatePicker(
                    signal="single_date",
                    mode="single",
                    placeholder="Pick a date",
                ),
                Div(
                    P("Selected: ", Span(data_text="$single_date_selected || 'None'", cls="font-mono text-sm")),
                    cls="mt-2 text-sm text-muted-foreground"
                ),
            ),
            # Date range picker
            Div(
                H3("Date Range", cls="text-lg font-medium mb-2"),
                DatePicker(
                    signal="date_range",
                    mode="range",
                    placeholder="Pick a date range",
                ),
                Div(
                    P("Range: ", Span(data_text="$date_range_selected || '[]'", cls="font-mono text-sm")),
                    cls="mt-2 text-sm text-muted-foreground"
                ),
            ),
            # Date picker with presets
            Div(
                H3("With Presets", cls="text-lg font-medium mb-2"),
                DatePicker(
                    signal="date_presets",
                    with_presets=True,
                    placeholder="Select a date",
                ),
                Div(
                    P("Selected: ", Span(data_text="$date_presets_selected || 'None'", cls="font-mono text-sm")),
                    cls="mt-2 text-sm text-muted-foreground"
                ),
            ),
            # Multiple date selection
            Div(
                H3("Multiple Dates", cls="text-lg font-medium mb-2"),
                DatePicker(
                    signal="multiple_dates",
                    mode="multiple",
                    placeholder="Select multiple dates",
                ),
                Div(
                    P("Selected: ", Span(data_text="JSON.stringify($multiple_dates_selected || [])", cls="font-mono text-sm")),
                    cls="mt-2 text-sm text-muted-foreground"
                ),
            ),
            # Date and time picker
            Div(
                H3("Date & Time", cls="text-lg font-medium mb-2"),
                DateTimePicker(
                    signal="datetime",
                    placeholder="Select date and time",
                ),
                Div(
                    P("Selected: ", Span(data_text="$datetime_datetime || 'None'", cls="font-mono text-sm")),
                    cls="mt-2 text-sm text-muted-foreground"
                ),
            ),
            # Date picker with input
            Div(
                H3("With Input Field", cls="text-lg font-medium mb-2"),
                DatePickerWithInput(
                    signal="date_input",
                    placeholder="YYYY-MM-DD",
                ),
                Div(
                    P("Value: ", Span(data_text="$date_input_selected || 'None'", cls="font-mono text-sm")),
                    cls="mt-2 text-sm text-muted-foreground"
                ),
            ),
            cls="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
        ),

        cls="container mx-auto"
    )


@rt("/dialog")
def test_dialog():
    return Div(
        Div(ThemeToggle(), cls="absolute top-4 right-4"),

        H1("Dialog Component Test", cls="text-3xl font-bold mb-6"),
        A("← Back to Index", href="/", cls="text-primary hover:underline mb-4 inline-block"),

        H2("Basic Dialog (Modal)", cls="text-2xl font-semibold mb-4 mt-8"),
        Dialog(
            DialogTrigger("Edit Profile"),
            DialogContent(
                DialogHeader(
                    DialogTitle("Edit Profile"),
                    DialogDescription(
                        "Make changes to your profile here. Click save when you're done."
                    ),
                ),
                Div(
                    Div(
                        Label("Name", for_="dialog-name"),
                        Input(
                            id="dialog-name",
                            placeholder="Your name",
                            cls="mt-1",
                        ),
                        cls="space-y-2",
                    ),
                    Div(
                        Label("Email", for_="dialog-email"),
                        Input(
                            id="dialog-email",
                            type="email",
                            placeholder="your@email.com",
                            cls="mt-1",
                        ),
                        cls="space-y-2",
                    ),
                    cls="grid gap-4 py-4",
                ),
                DialogFooter(
                    DialogClose("Cancel", variant="outline"),
                    DialogClose("Save changes"),
                ),
            ),
            signal="edit_profile_dialog",
            size="md",
        ),

        H2("Dialog with Different Size", cls="text-2xl font-semibold mb-4 mt-8"),
        Dialog(
            DialogTrigger("Delete Account", variant="destructive"),
            DialogContent(
                DialogHeader(
                    DialogTitle("Are you absolutely sure?"),
                    DialogDescription(
                        "This action cannot be undone. This will permanently delete your "
                        "account and remove your data from our servers."
                    ),
                ),
                DialogFooter(
                    DialogClose("Cancel", variant="outline"),
                    DialogClose("Yes, delete account", variant="destructive"),
                ),
            ),
            signal="delete_dialog",
            size="sm",
        ),

        H2("Non-Modal Dialog", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Non-modal dialogs allow interaction with the page behind them. Click outside won't close it.", cls="text-muted-foreground mb-4"),
        Dialog(
            DialogTrigger("Open Non-Modal Dialog", variant="outline"),
            DialogContent(
                DialogHeader(
                    DialogTitle("Non-Modal Dialog"),
                    DialogDescription(
                        "You can still interact with the page behind this dialog. "
                        "Click outside won't close it - use the close button or escape key."
                    ),
                ),
                Div(
                    P("This is useful for:"),
                    Ul(
                        Li("Persistent tool windows"),
                        Li("Floating panels"),
                        Li("Non-critical notifications"),
                        cls="list-disc list-inside space-y-1 mt-2"
                    ),
                    cls="py-4",
                ),
                DialogFooter(
                    DialogClose("Close"),
                ),
            ),
            signal="nonmodal_dialog",
            modal=False,
            size="md",
            cls="top-4 right-4 left-auto m-0",
        ),

        cls="container mx-auto"
    )


@rt("/popover")
def test_popover():
    return Div(
        # Theme toggle in top-right
        Div(ThemeToggle(), cls="absolute top-4 right-4"),

        H1("Popover Component Test", cls="text-3xl font-bold mb-6"),
        A("← Back to Index", href="/", cls="text-primary hover:underline mb-4 inline-block"),

        H2("Popover Examples", cls="text-2xl font-semibold mb-4 mt-8"),
        Div(
            # Basic popover
            Popover(
                PopoverTrigger("Open Popover"),
                PopoverContent(
                    H3("About this feature", cls="font-semibold mb-2"),
                    P("This is a popover component that displays rich content in a floating panel.", cls="text-sm text-muted-foreground mb-3"),
                    PopoverClose("✕"),
                    aria_label="Feature information",
                ),
            ),
            # Popover with different positioning
            Popover(
                PopoverTrigger("Top Popover", variant="outline"),
                PopoverContent(
                    H3("Top positioned", cls="font-semibold mb-2"),
                    P("This popover appears above the trigger.", cls="text-sm"),
                    side="top",
                    aria_label="Positioning information",
                ),
            ),
            # Popover with form/settings
            Popover(
                PopoverTrigger("Settings", variant="secondary"),
                PopoverContent(
                    H3("Quick Settings", cls="font-semibold mb-3"),
                    Div(
                        Label("Theme", cls="text-sm font-medium"),
                        Button("Toggle", variant="outline", size="sm"),
                        cls="flex justify-between items-center mb-2",
                    ),
                    Div(
                        Label("Notifications", cls="text-sm font-medium"),
                        Checkbox(signal="notif_setting"),
                        cls="flex justify-between items-center mb-2",
                    ),
                    PopoverClose("Done", variant="ghost"),
                    aria_label="Quick settings menu",
                ),
            ),
            cls="flex flex-wrap gap-4"
        ),

        cls="container mx-auto"
    )


@rt("/command")
def test_command():
    return Div(
        # Theme toggle in top-right
        Div(ThemeToggle(), cls="absolute top-4 right-4"),

        H1("Command Component Test", cls="text-3xl font-bold mb-6"),
        A("← Back to Index", href="/", cls="text-primary hover:underline mb-4 inline-block"),

        H2("Basic Command Palette", cls="text-2xl font-semibold mb-4 mt-8"),
        Command(
            CommandInput(placeholder="Type a command or search..."),
            CommandList(
                CommandEmpty("No results found."),
                CommandGroup(
                    CommandItem(
                        Icon("lucide:file"),
                        Span("New File", cls="ml-2"),
                        value="new-file",
                        onclick="console.log('New file')",
                    ),
                    CommandItem(
                        Icon("lucide:folder"),
                        Span("New Folder", cls="ml-2"),
                        value="new-folder",
                        onclick="console.log('New folder')",
                    ),
                    CommandItem(
                        Icon("lucide:save"),
                        Span("Save", cls="ml-2"),
                        CommandShortcut("⌘S"),
                        value="save",
                        onclick="console.log('Save')",
                    ),
                    heading="File",
                ),
                CommandSeparator(),
                CommandGroup(
                    CommandItem(
                        Icon("lucide:settings"),
                        Span("Settings", cls="ml-2"),
                        CommandShortcut("⌘,"),
                        value="settings",
                        onclick="console.log('Settings')",
                    ),
                    CommandItem(
                        Icon("lucide:user"),
                        Span("Profile", cls="ml-2"),
                        value="profile",
                        onclick="console.log('Profile')",
                    ),
                    CommandItem(
                        Icon("lucide:log-out"),
                        Span("Log Out", cls="ml-2"),
                        value="logout",
                        onclick="console.log('Logout')",
                    ),
                    heading="User",
                ),
            ),
            signal="basic_command",
            size="md",
            cls="max-w-md mb-8",
        ),

        H2("Command Dialog", cls="text-2xl font-semibold mb-4 mt-8"),
        CommandDialog(
            trigger=Button(
                Icon("lucide:terminal"),
                Span("Open Command Palette", cls="ml-2"),
                variant="outline",
            ),
            content=[
                CommandInput(placeholder="Search commands..."),
                CommandList(
                    CommandEmpty("No commands found."),
                    CommandGroup(
                        CommandItem(
                            Icon("lucide:copy"),
                            Span("Copy", cls="ml-2"),
                            CommandShortcut("⌘C"),
                            value="copy",
                            onclick="console.log('Copy')",
                        ),
                        CommandItem(
                            Icon("lucide:clipboard"),
                            Span("Paste", cls="ml-2"),
                            CommandShortcut("⌘V"),
                            value="paste",
                            onclick="console.log('Paste')",
                        ),
                        CommandItem(
                            Icon("lucide:scissors"),
                            Span("Cut", cls="ml-2"),
                            CommandShortcut("⌘X"),
                            value="cut",
                            onclick="console.log('Cut')",
                        ),
                        heading="Edit",
                    ),
                    CommandSeparator(),
                    CommandGroup(
                        CommandItem(
                            Icon("lucide:layout"),
                            Span("Toggle Sidebar", cls="ml-2"),
                            CommandShortcut("⌘B"),
                            value="toggle-sidebar",
                            onclick="console.log('Toggle sidebar')",
                        ),
                        CommandItem(
                            Icon("lucide:moon"),
                            Span("Toggle Theme", cls="ml-2"),
                            CommandShortcut("⌘T"),
                            value="toggle-theme",
                            onclick="console.log('Toggle theme')",
                        ),
                        heading="View",
                    ),
                    CommandSeparator(),
                    CommandGroup(
                        CommandItem(
                            Icon("lucide:help-circle"),
                            Span("Help", cls="ml-2"),
                            CommandShortcut("⌘?"),
                            value="help",
                            onclick="console.log('Help')",
                        ),
                        CommandItem(
                            Icon("lucide:keyboard"),
                            Span("Keyboard Shortcuts", cls="ml-2"),
                            value="shortcuts",
                            onclick="console.log('Shortcuts')",
                        ),
                        heading="Help",
                    ),
                ),
            ],
            signal="cmd_dialog",
        ),

        H2("Searchable Command Palette", cls="text-2xl font-semibold mb-4 mt-8"),
        Command(
            CommandInput(placeholder="Search frameworks..."),
            CommandList(
                CommandEmpty("No framework found."),
                CommandGroup(
                    CommandItem(
                        "React",
                        value="react",
                        keywords="javascript frontend",
                        onclick="alert('Selected: React')",
                    ),
                    CommandItem(
                        "Vue",
                        value="vue",
                        keywords="javascript frontend",
                        onclick="alert('Selected: Vue')",
                    ),
                    CommandItem(
                        "Angular",
                        value="angular",
                        keywords="typescript frontend",
                        onclick="alert('Selected: Angular')",
                    ),
                    heading="Frontend",
                ),
                CommandSeparator(),
                CommandGroup(
                    CommandItem(
                        "Django",
                        value="django",
                        keywords="python backend",
                        onclick="alert('Selected: Django')",
                    ),
                    CommandItem(
                        "FastAPI",
                        value="fastapi",
                        keywords="python backend api",
                        onclick="alert('Selected: FastAPI')",
                    ),
                    CommandItem(
                        "Express",
                        value="express",
                        keywords="javascript nodejs backend",
                        onclick="alert('Selected: Express')",
                    ),
                    heading="Backend",
                ),
                CommandSeparator(),
                CommandGroup(
                    CommandItem(
                        "Next.js",
                        value="nextjs",
                        keywords="react fullstack",
                        onclick="alert('Selected: Next.js')",
                    ),
                    CommandItem(
                        "Nuxt",
                        value="nuxt",
                        keywords="vue fullstack",
                        onclick="alert('Selected: Nuxt')",
                    ),
                    CommandItem(
                        "SvelteKit",
                        value="sveltekit",
                        keywords="svelte fullstack",
                        onclick="alert('Selected: SvelteKit')",
                    ),
                    heading="Full Stack",
                ),
            ),
            signal="framework_command",
            size="lg",
            cls="max-w-md mb-8",
        ),

        H2("Command with Disabled Items", cls="text-2xl font-semibold mb-4 mt-8"),
        Command(
            CommandInput(placeholder="Search actions..."),
            CommandList(
                CommandEmpty("No action found."),
                CommandItem(
                    Icon("lucide:check"),
                    Span("Available Action", cls="ml-2"),
                    value="available",
                    onclick="alert('Action executed')",
                ),
                CommandItem(
                    Icon("lucide:lock"),
                    Span("Premium Feature", cls="ml-2"),
                    Badge("Pro", variant="secondary", cls="ml-auto"),
                    value="premium",
                    disabled=True,
                ),
                CommandItem(
                    Icon("lucide:shield"),
                    Span("Admin Only", cls="ml-2"),
                    value="admin",
                    disabled=True,
                ),
                CommandItem(
                    Icon("lucide:play"),
                    Span("Run Task", cls="ml-2"),
                    value="run",
                    onclick="alert('Task started')",
                ),
            ),
            signal="disabled_command",
            size="sm",
            cls="max-w-md",
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


@rt("/input")
def test_input():
    return Div(
        H1("Input Component Test", cls="text-3xl font-bold mb-6"),
        A("← Back to Index", href="/", cls="text-primary hover:underline mb-4 inline-block"),

        H2("Basic Inputs", cls="text-2xl font-semibold mb-4 mt-8"),
        Div(
            Div(
                Label("Text Input", for_="text-input", cls="block text-sm font-medium mb-1.5"),
                Input(id="text-input", placeholder="Enter text...", signal="name"),
                P(Signal("name"), cls="text-sm text-muted-foreground mt-1.5"),
                cls="space-y-1",
            ),
            Div(
                Label("Email Input", for_="email-input", cls="block text-sm font-medium mb-1.5"),
                Input(id="email-input", type="email", placeholder="email@example.com", signal="email"),
                P(Signal("email"), cls="text-sm text-muted-foreground mt-1.5"),
                cls="space-y-1",
            ),
            Div(
                Label("Password Input", for_="password-input", cls="block text-sm font-medium mb-1.5"),
                Input(id="password-input", type="password", placeholder="••••••••"),
                cls="space-y-1",
            ),
            Div(
                Label("Disabled Input", for_="disabled-input", cls="block text-sm font-medium mb-1.5"),
                Input(id="disabled-input", placeholder="Cannot edit", disabled=True),
                cls="space-y-1",
            ),
            cls="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8",
        ),

        H2("Width Override Test (StarMerge)", cls="text-2xl font-semibold mb-4 mt-8"),
        P("These inputs test that StarMerge correctly overrides the default w-full width:", cls="text-muted-foreground mb-4"),
        Div(
            Div(
                Label("Default width (w-full)", cls="block text-sm font-medium mb-1.5"),
                Input(placeholder="Full width input"),
                P("Should be full width", cls="text-xs text-muted-foreground mt-1"),
                cls="mb-4",
            ),
            Div(
                Label("Override: w-1/2", cls="block text-sm font-medium mb-1.5"),
                Input(placeholder="Half width", cls="w-1/2"),
                P("Should be 50% width", cls="text-xs text-muted-foreground mt-1"),
                cls="mb-4",
            ),
            Div(
                Label("Override: w-64", cls="block text-sm font-medium mb-1.5"),
                Input(placeholder="Fixed width", cls="w-64"),
                P("Should be w-64 (16rem)", cls="text-xs text-muted-foreground mt-1"),
                cls="mb-4",
            ),
            Div(
                Label("Override: max-w-sm", cls="block text-sm font-medium mb-1.5"),
                Input(placeholder="Max width", cls="max-w-sm"),
                P("Should have max-w-sm constraint", cls="text-xs text-muted-foreground mt-1"),
                cls="mb-4",
            ),
            cls="max-w-2xl mb-8",
        ),

        H2("InputWithLabel Component", cls="text-2xl font-semibold mb-4 mt-8"),
        Div(
            InputWithLabel(
                label="Full Name",
                placeholder="John Doe",
                signal="full_name",
                required=True,
            ),
            InputWithLabel(
                label="Email Address",
                type="email",
                placeholder="john@example.com",
                signal="user_email",
                helper_text="We'll never share your email.",
            ),
            InputWithLabel(
                label="Age",
                type="number",
                placeholder="18",
                min=0,
                max=120,
                helper_text="Must be 18 or older",
            ),
            InputWithLabel(
                label="Website",
                type="url",
                placeholder="https://example.com",
                error_text="Please enter a valid URL",
            ),
            cls="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8 max-w-4xl",
        ),

        H2("Validation Example", cls="text-2xl font-semibold mb-4 mt-8"),
        Div(
            Label("Age (must be >= 18)", for_="age-input", cls="block text-sm font-medium mb-1.5"),
            Input(
                id="age-input",
                type="text",
                placeholder="Enter age",
                signal="age",
                data_on_input="$age_valid = Number($age) >= 18",
            ),
            P(
                Span("✓ Valid", cls="text-green-600", style="display: none", data_show="$age && $age_valid"),
                Span("✗ Must be 18+", cls="text-destructive", style="display: none", data_show="$age && !$age_valid"),
                Span("Enter your age to validate", cls="text-muted-foreground", data_show="!$age || $age === ''"),
                cls="text-sm mt-1.5",
            ),
            cls="max-w-md mb-8",
        ),

        cls="container mx-auto"
    )


@rt("/label")
def test_label():
    return Div(
        Div(ThemeToggle(), cls="absolute top-4 right-4"),

        H1("Label Component Test", cls="text-3xl font-bold mb-6"),
        A("← Back to Index", href="/", cls="text-primary hover:underline mb-4 inline-block"),

        H2("Basic Label Usage", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Labels are used with form inputs to provide accessible names:", cls="text-muted-foreground mb-4"),
        Div(
            Div(
                Label("Text Input", for_="text-input"),
                Input(
                    id="text-input",
                    placeholder="Enter text...",
                    signal="name",
                ),
                cls="space-y-2",
            ),
            Div(
                Label("Email Input", for_="email-input"),
                Input(
                    id="email-input",
                    type="email",
                    placeholder="email@example.com",
                    signal="email",
                ),
                cls="space-y-2",
            ),
            Div(
                Label("Password Input", for_="password-input"),
                Input(
                    id="password-input",
                    type="password",
                    placeholder="••••••••"
                ),
                cls="space-y-2",
            ),
            cls="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8 max-w-4xl",
        ),

        H2("Label with Disabled Input", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Labels automatically style for disabled inputs using peer-disabled (input must come before label in DOM):", cls="text-muted-foreground mb-4"),
        Div(
            Input(
                id="disabled-input",
                placeholder="Cannot edit",
                disabled=True,
            ),
            Label("Disabled Input", for_="disabled-input"),
            cls="flex flex-col-reverse gap-2 max-w-md",
        ),

        H2("Label with Checkbox", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Labels work with checkboxes and other form elements:", cls="text-muted-foreground mb-4"),
        Div(
            CheckboxWithLabel(
                label="Accept terms and conditions",
                signal="terms",
            ),
            CheckboxWithLabel(
                label="Enable notifications",
                signal="notifications",
                checked=True,
            ),
            cls="space-y-4 max-w-md",
        ),

        H2("Custom Styled Labels", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Labels can be customized with additional classes:", cls="text-muted-foreground mb-4"),
        Div(
            Div(
                Label("Bold Label", for_="bold-input", cls="!font-bold text-lg"),
                Input(id="bold-input", placeholder="With bold label"),
                cls="space-y-2",
            ),
            Div(
                Label("Primary Colored Label", for_="primary-input", cls="!text-primary !text-base"),
                Input(id="primary-input", placeholder="With primary colored label"),
                cls="space-y-2",
            ),
            Div(
                Label("Destructive Label", for_="destructive-input", cls="!text-destructive"),
                Input(id="destructive-input", placeholder="With destructive colored label"),
                cls="space-y-2",
            ),
            cls="space-y-6 max-w-md",
        ),

        cls="container mx-auto"
    )


@rt("/progress")
def test_progress():
    return Div(
        Div(ThemeToggle(), cls="absolute top-4 right-4"),

        H1("Progress Component Test", cls="text-3xl font-bold mb-6"),
        A("← Back to Index", href="/", cls="text-primary hover:underline mb-4 inline-block"),

        H2("Basic Progress", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Static progress bars showing different completion levels:", cls="text-muted-foreground mb-4"),
        Div(
            P("25% Complete:", cls="mb-2 text-sm font-medium"),
            Progress(value=25),
            P("50% Complete:", cls="mt-4 mb-2 text-sm font-medium"),
            Progress(value=50),
            P("75% Complete:", cls="mt-4 mb-2 text-sm font-medium"),
            Progress(value=75),
            P("100% Complete:", cls="mt-4 mb-2 text-sm font-medium"),
            Progress(value=100),
            cls="max-w-2xl"
        ),

        H2("Interactive Progress", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Control progress with buttons:", cls="text-muted-foreground mb-4"),
        Div(
            (demo_progress := Signal("demo_progress", 35)),
            Progress(value=35, signal="demo_progress"),
            Div(
                Button(
                    Icon("lucide:plus"),
                    "Increase",
                    data_on_click=js(f"{demo_progress} = Math.min(100, {demo_progress} + 10)"),
                ),
                Button(
                    Icon("lucide:minus"),
                    "Decrease",
                    variant="secondary",
                    data_on_click=js(f"{demo_progress} = Math.max(0, {demo_progress} - 10)"),
                ),
                Button(
                    Icon("lucide:rotate-ccw"),
                    "Reset",
                    variant="outline",
                    data_on_click=demo_progress.set(0),
                ),
                cls="flex gap-2 mt-4",
            ),
            P(
                "Current: ",
                Span(data_text="Math.round(" + demo_progress + ") + '%'", cls="font-mono"),
                cls="text-sm text-muted-foreground mt-4"
            ),
            cls="max-w-2xl"
        ),

        H2("Auto-incrementing Progress", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Automatically increment progress over time:", cls="text-muted-foreground mb-4"),
        Div(
            (auto_progress := Signal("auto_progress", 0)),
            Progress(value=0, signal="auto_progress"),
            Div(
                Button(
                    Icon("lucide:play"),
                    "Start",
                    data_on_click=js(f"""
                        if (!window.autoProgressInterval) {{
                            window.autoProgressInterval = setInterval(() => {{
                                {auto_progress} = ({auto_progress} + 5) % 105;
                            }}, 200);
                        }}
                    """),
                ),
                Button(
                    Icon("lucide:square"),
                    "Stop",
                    variant="secondary",
                    data_on_click=js("""
                        if (window.autoProgressInterval) {
                            clearInterval(window.autoProgressInterval);
                            window.autoProgressInterval = null;
                        }
                    """),
                ),
                Button(
                    Icon("lucide:rotate-ccw"),
                    "Reset",
                    variant="outline",
                    data_on_click=js(f"""
                        if (window.autoProgressInterval) {{
                            clearInterval(window.autoProgressInterval);
                            window.autoProgressInterval = null;
                        }}
                        {auto_progress.set(0)}
                    """),
                ),
                cls="flex gap-2 mt-4",
            ),
            cls="max-w-2xl"
        ),

        H2("Custom Styling", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Progress bars with custom heights and colors:", cls="text-muted-foreground mb-4"),
        Div(
            P("Large progress bar (h-4):", cls="mb-2 text-sm font-medium"),
            Progress(value=60, cls="h-4"),
            P("Extra large (h-6):", cls="mt-4 mb-2 text-sm font-medium"),
            Progress(value=80, cls="h-6"),
            P("Custom green color:", cls="mt-4 mb-2 text-sm font-medium"),
            Progress(
                value=75,
                cls="bg-green-500/20 [&>div]:bg-green-500"
            ),
            P("Custom blue color:", cls="mt-4 mb-2 text-sm font-medium"),
            Progress(
                value=90,
                cls="bg-blue-500/20 [&>div]:bg-blue-500"
            ),
            cls="max-w-2xl"
        ),

        cls="container mx-auto"
    )


@rt("/dropdown-menu")
def test_dropdown_menu():
    return Page(
        H2("Basic Dropdown", cls="text-2xl font-semibold mb-4 mt-8"),
        P("A dropdown menu with labels, separators, and keyboard shortcuts:", cls="text-muted-foreground mb-4"),
        DropdownMenu(
            DropdownMenuTrigger("Open Menu"),
            DropdownMenuContent(
                DropdownMenuLabel("My Account"),
                DropdownMenuSeparator(),
                DropdownMenuItem(
                    Icon("lucide:user", cls="mr-2 h-4 w-4"),
                    "Profile",
                    DropdownMenuShortcut("⇧⌘P")
                ),
                DropdownMenuItem(
                    Icon("lucide:credit-card", cls="mr-2 h-4 w-4"),
                    "Billing",
                    DropdownMenuShortcut("⌘B")
                ),
                DropdownMenuItem(
                    Icon("lucide:settings", cls="mr-2 h-4 w-4"),
                    "Settings",
                    DropdownMenuShortcut("⌘S")
                ),
                DropdownMenuSeparator(),
                DropdownMenuItem(
                    Icon("lucide:log-out", cls="mr-2 h-4 w-4"),
                    "Log out",
                    DropdownMenuShortcut("⇧⌘Q"),
                    variant="destructive"
                ),
            ),
        ),

        H2("Checkbox Items", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Dropdown with checkbox items for toggling options:", cls="text-muted-foreground mb-4"),
        Div(
            (status_bar := Signal("status_bar", True)),
            (activity_bar := Signal("activity_bar", False)),
            (panel := Signal("panel", False)),
            DropdownMenu(
                DropdownMenuTrigger("View Options", variant="secondary"),
                DropdownMenuContent(
                    DropdownMenuLabel("Appearance"),
                    DropdownMenuSeparator(),
                    DropdownMenuCheckboxItem("Status Bar", signal="status_bar"),
                    DropdownMenuCheckboxItem("Activity Bar", signal="activity_bar"),
                    DropdownMenuCheckboxItem("Panel", signal="panel"),
                ),
            ),
            P(
                "Status Bar: ",
                Span(data_text=status_bar.if_("On", "Off"), cls="font-mono text-sm"),
                " | Activity Bar: ",
                Span(data_text=activity_bar.if_("On", "Off"), cls="font-mono text-sm"),
                " | Panel: ",
                Span(data_text=panel.if_("On", "Off"), cls="font-mono text-sm"),
                cls="text-sm text-muted-foreground mt-4"
            ),
        ),

        H2("Radio Group", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Dropdown with radio items for single selection:", cls="text-muted-foreground mb-4"),
        Div(
            (position := Signal("position", "bottom")),
            DropdownMenu(
                DropdownMenuTrigger("Select Position", variant="outline"),
                DropdownMenuContent(
                    DropdownMenuLabel("Position"),
                    DropdownMenuSeparator(),
                    DropdownMenuRadioGroup(
                        DropdownMenuRadioItem("Top", value="top"),
                        DropdownMenuRadioItem("Bottom", value="bottom"),
                        DropdownMenuRadioItem("Right", value="right"),
                        signal="position",
                    ),
                ),
            ),
            P(
                "Selected position: ",
                Span(data_text=position, cls="font-mono text-sm"),
                cls="text-sm text-muted-foreground mt-4"
            ),
        ),

        H2("Grouped Items", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Dropdown with grouped menu items:", cls="text-muted-foreground mb-4"),
        DropdownMenu(
            DropdownMenuTrigger("Actions", variant="outline"),
            DropdownMenuContent(
                DropdownMenuGroup(
                    DropdownMenuItem(
                        Icon("lucide:plus", cls="mr-2 h-4 w-4"),
                        "New File"
                    ),
                    DropdownMenuItem(
                        Icon("lucide:folder-plus", cls="mr-2 h-4 w-4"),
                        "New Folder"
                    ),
                ),
                DropdownMenuSeparator(),
                DropdownMenuGroup(
                    DropdownMenuItem(
                        Icon("lucide:download", cls="mr-2 h-4 w-4"),
                        "Download"
                    ),
                    DropdownMenuItem(
                        Icon("lucide:upload", cls="mr-2 h-4 w-4"),
                        "Upload"
                    ),
                ),
                DropdownMenuSeparator(),
                DropdownMenuItem(
                    Icon("lucide:trash", cls="mr-2 h-4 w-4"),
                    "Delete",
                    variant="destructive"
                ),
            ),
        ),

        H2("Sub-menus", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Dropdown with nested sub-menus:", cls="text-muted-foreground mb-4"),
        DropdownMenu(
            DropdownMenuTrigger("More Options", variant="secondary"),
            DropdownMenuContent(
                DropdownMenuItem(
                    Icon("lucide:mail", cls="mr-2 h-4 w-4"),
                    "Email"
                ),
                DropdownMenuItem(
                    Icon("lucide:message-square", cls="mr-2 h-4 w-4"),
                    "Message"
                ),
                DropdownMenuSeparator(),
                DropdownMenuSub(
                    DropdownMenuSubTrigger(
                        Icon("lucide:share", cls="mr-2 h-4 w-4"),
                        "Share"
                    ),
                    DropdownMenuSubContent(
                        DropdownMenuItem(
                            Icon("lucide:twitter", cls="mr-2 h-4 w-4"),
                            "Twitter"
                        ),
                        DropdownMenuItem(
                            Icon("lucide:facebook", cls="mr-2 h-4 w-4"),
                            "Facebook"
                        ),
                        DropdownMenuItem(
                            Icon("lucide:linkedin", cls="mr-2 h-4 w-4"),
                            "LinkedIn"
                        ),
                    ),
                ),
            ),
        ),
        title="Dropdown Menu",
    )


@rt("/hover-card")
def test_hover_card():
    return Page(
        H2("Basic", cls="text-2xl font-semibold mb-4"),
        P("Hover over the username to see the user profile card:", cls="text-muted-foreground mb-4"),
        HoverCard(
            HoverCardTrigger(
                Span("@username", cls="text-blue-600 underline cursor-pointer"),
            ),
            HoverCardContent(
                Div(
                    Div("👤", cls="w-12 h-12 bg-muted rounded-full flex items-center justify-center text-2xl mb-3"),
                    H3("John Doe", cls="font-semibold mb-1"),
                    P("@username", cls="text-sm text-muted-foreground mb-2"),
                    P("Full-stack developer passionate about building great user experiences.", cls="text-sm"),
                    cls="text-center",
                ),
            ),
        ),

        H2("Top Positioning", cls="text-2xl font-semibold mb-4 mt-8"),
        P("This hover card appears above the trigger:", cls="text-muted-foreground mb-4"),
        HoverCard(
            HoverCardTrigger(
                Button("Hover for info", variant="outline"),
            ),
            HoverCardContent(
                Div(
                    H3("Quick Info", cls="font-semibold mb-2"),
                    P("This hover card appears when you hover over the trigger element.", cls="text-sm text-muted-foreground mb-2"),
                    P("It stays open while you're hovering over either the trigger or the content.", cls="text-sm"),
                ),
                side="top",
            ),
        ),

        H2("Left Positioning", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Hover over the badge to see product information:", cls="text-muted-foreground mb-4"),
        HoverCard(
            HoverCardTrigger(
                Badge("Product Info", variant="secondary"),
            ),
            HoverCardContent(
                Div(
                    H3("StarUI Components", cls="font-semibold mb-2"),
                    Badge("v1.0.0", variant="outline", cls="mb-2"),
                    P("A modern component library built with StarHTML and Datastar for reactive Python web apps.", cls="text-sm text-muted-foreground mb-3"),
                    Div(
                        Badge("Python"),
                        Badge("StarHTML", variant="secondary"),
                        Badge("Datastar", variant="outline"),
                        cls="flex gap-1",
                    ),
                ),
                side="left",
            ),
        ),
        title="Hover Card",
    )


@rt("/radio-group")
def test_radio_group():
    return Page(
        H2("With Label", cls="text-2xl font-semibold mb-4"),
        P("Complete radio group with label, helper text, and validation:", cls="text-muted-foreground mb-4"),
        Div(
            RadioGroupWithLabel(
                label="Select your plan",
                options=[
                    {"value": "free", "label": "Free - $0/month"},
                    {"value": "pro", "label": "Pro - $10/month"},
                    {"value": "enterprise", "label": "Enterprise - Custom"},
                ],
                value="free",
                signal="plan",
                helper_text="Choose the plan that best fits your needs",
            ),
            cls="mb-8",
        ),

        H2("Horizontal Orientation", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Radio group with horizontal layout:", cls="text-muted-foreground mb-4"),
        RadioGroupWithLabel(
            label="Notification preferences",
            options=[
                {"value": "all", "label": "All notifications"},
                {"value": "important", "label": "Important only"},
                {"value": "none", "label": "No notifications"},
            ],
            signal="notifications_radio",
            orientation="horizontal",
            required=True,
        ),

        H2("With Error State", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Radio group with validation error:", cls="text-muted-foreground mb-4"),
        RadioGroupWithLabel(
            label="Size",
            options=[
                {"value": "sm", "label": "Small"},
                {"value": "md", "label": "Medium"},
                {"value": "lg", "label": "Large"},
                {"value": "xl", "label": "Extra Large", "disabled": True},
            ],
            signal="size_radio",
            required=True,
            error_text="Please select a size",
        ),

        H2("Simple Radio Group", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Basic radio group without wrapper label:", cls="text-muted-foreground mb-4"),
        Div(
            RadioGroup(
                RadioGroupItem("small", "Small"),
                RadioGroupItem("medium", "Medium"),
                RadioGroupItem("large", "Large"),
                initial_value="medium",
                signal="simple_radio",
            ),
            cls="p-4 border rounded-lg",
        ),

        H2("Custom Styled Indicators", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Radio group with custom blue indicators:", cls="text-muted-foreground mb-4"),
        Div(
            RadioGroup(
                RadioGroupItem(
                    "option1",
                    "Option 1",
                    indicator_cls="[&>div]:bg-blue-600 dark:[&>div]:bg-blue-500",
                ),
                RadioGroupItem(
                    "option2",
                    "Option 2",
                    indicator_cls="[&>div]:bg-blue-600 dark:[&>div]:bg-blue-500",
                ),
                RadioGroupItem(
                    "option3",
                    "Option 3",
                    disabled=True,
                    indicator_cls="[&>div]:bg-blue-600 dark:[&>div]:bg-blue-500",
                ),
                initial_value="option2",
                signal="custom_radio",
            ),
            cls="p-4 border rounded-lg",
        ),
        title="Radio Group",
    )


serve()
