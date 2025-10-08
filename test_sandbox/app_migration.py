#!/usr/bin/env python3
"""Minimal test app for migrating components one by one."""

# IMPORTANT: Monkey-patch starhtml.datastar BEFORE any imports
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
# import patch_datastar

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
from src.starui.registry.components.select import (
    Select, SelectTrigger, SelectValue, SelectContent, SelectItem,
    SelectGroup, SelectLabel, SelectWithLabel
)
from src.starui.registry.components.separator import Separator
from src.starui.registry.components.sheet import (
    Sheet, SheetTrigger, SheetContent, SheetHeader, SheetFooter,
    SheetTitle, SheetDescription, SheetClose
)
from src.starui.registry.components.skeleton import Skeleton
from src.starui.registry.components.switch import Switch, SwitchWithLabel
from src.starui.registry.components.table import (
    Table, TableHeader, TableBody, TableFooter, TableRow,
    TableHead, TableCell, TableCaption
)
from src.starui.registry.components.textarea import Textarea, TextareaWithLabel
from src.starui.registry.components.tabs import Tabs, TabsList, TabsTrigger, TabsContent
from src.starui.registry.components.theme_toggle import ThemeToggle
from src.starui.registry.components.toast import Toaster, toast, ToastQueue
from src.starui.registry.components.toggle import Toggle
from src.starui.registry.components.toggle_group import ToggleGroup
from src.starui.registry.components.tooltip import Tooltip, TooltipTrigger, TooltipContent, TooltipProvider
from src.starui.registry.components.typography import (
    Display, Subtitle, Lead, Large, Small, Muted, Caption,
    Text, InlineCode, Blockquote, List, Prose, Figure, Figcaption, Hr
)

import asyncio
import time
from starhtml import execute_script, sse, signals

styles = Link(rel="stylesheet", href="/static/css/starui.css", type="text/css")


def Page(*children, title="Component Test", show_back_link=True):
    """Wrapper for consistent page layout with theme toggle and back link."""
    return Div(
        Toaster(position="bottom-right"),
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
            A("Select", href="/select", cls="text-primary hover:underline block"),
            A("Separator", href="/separator", cls="text-primary hover:underline block"),
            A("Sheet", href="/sheet", cls="text-primary hover:underline block"),
            A("Skeleton", href="/skeleton", cls="text-primary hover:underline block"),
            A("Switch", href="/switch", cls="text-primary hover:underline block"),
            A("Table", href="/table", cls="text-primary hover:underline block"),
            A("Textarea", href="/textarea", cls="text-primary hover:underline block"),
            A("Tabs", href="/tabs", cls="text-primary hover:underline block"),
            A("Toast", href="/toast", cls="text-primary hover:underline block"),
            A("Toast - Server & Client Patterns", href="/toast-server", cls="text-primary hover:underline block ml-4 text-sm"),
            A("Toggle", href="/toggle", cls="text-primary hover:underline block"),
            A("Toggle Group", href="/toggle_group", cls="text-primary hover:underline block"),
            A("Tooltip", href="/tooltip", cls="text-primary hover:underline block"),
            A("Typography", href="/typography", cls="text-primary hover:underline block"),
            A("Theme Toggle", href="/theme-toggle", cls="text-primary hover:underline block"),
            cls="space-y-2"
        ),
        cls="container mx-auto"
    )


# Component test routes - add as we migrate each component

@rt("/accordion")
def test_accordion():
    return Page(
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
        title="Accordion"
    )


@rt("/alert")
def test_alert():
    return Page(
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

        title="Alert"
    )


@rt("/avatar")
def test_avatar():
    return Page(
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

        title="Avatar"
    )


@rt("/badge")
def test_badge():
    return Page(
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

        title="Badge"
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
    return Page(
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
                data_on_click=status.set(
                    match(status,
                        pending="processing",
                        processing="success",
                        success="error",
                        error="pending"
                    )
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
                data_on_click=status.set("pending"),
            ),
            P("✓ Better for 3+ states: Only one icon element, state-driven", cls="text-xs text-muted-foreground mt-2"),
            cls="flex flex-wrap gap-2 items-start max-w-2xl"
        ),

        H2("Pattern 3: Real Backend Loading (data-indicator)", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Uses Datastar's built-in data-indicator for actual backend requests:", cls="text-sm text-muted-foreground mb-2"),
        Div(
            (fetching := Signal("fetching", _ref_only=True)),
            Button(
                Icon("lucide:loader-2", cls="animate-spin", data_show=fetching),
                Icon("lucide:download", data_show=~fetching),
                data_text=fetching.if_("Fetching...", "Fetch Data"),
                data_on_click=get("/api/data"),
                data_indicator=fetching,
                data_attr_disabled=fetching,
                variant="outline",
            ),
            Div(
                P("Response will appear here...", cls="text-muted-foreground text-sm italic"),
                id="api-response",
                cls="mt-2"
            ),
            P("✓ Automatic: 'fetching' signal created by Datastar during requests", cls="text-xs text-muted-foreground mt-2"),
            P("Click button to see 2-second simulated network delay", cls="text-xs text-muted-foreground"),
            cls="flex flex-col gap-2 max-w-2xl"
        ),

        title="Button"
    )


@rt("/alert-dialog")
def test_alert_dialog():
    return Page(
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
        title="Alert Dialog"
    )


@rt("/calendar")
def test_calendar():
    cal_single = Calendar(mode="single")
    cal_range = Calendar(        
        mode="range",
        selected=["2025-09-15", "2025-09-25"],
        month=9,
        year=2025
    )
    cal_multiple = Calendar(        
        mode="multiple",
        selected=["2025-09-10", "2025-09-15", "2025-09-20"],
        month=9,
        year=2025
    )

    return Page(
        H2("Single Mode", cls="text-2xl font-semibold mb-4 mt-8"),
        Div(
            cal_single,
            Div(
                P("Selected: ", Span(data_text=cal_single.selected.or_("None"), cls="font-mono text-sm")),
                cls="mt-4 text-sm"
            ),
            cls="flex flex-col items-center"
        ),

        H2("Range Mode", cls="text-2xl font-semibold mb-4 mt-8"),
        Div(
            cal_range,
            Div(
                P("Range: ", Span(data_text=cal_range.selected.or_("None"), cls="font-mono text-sm")),
                cls="mt-4 text-sm"
            ),
            cls="flex flex-col items-center"
        ),

        H2("Multiple Mode", cls="text-2xl font-semibold mb-4 mt-8"),
        Div(
            cal_multiple,
            Div(
                P("Selected: ", Span(data_text=cal_multiple.selected.join(' | ').or_("None"), cls="font-mono")),
                cls="mt-4 text-sm"
            ),
            cls="flex flex-col items-center"
        ),

        H2("Disabled", cls="text-2xl font-semibold mb-4 mt-8"),
        Div(
            Calendar(mode="single", disabled=True),
            cls="flex flex-col items-center"
        ),
        title="Calendar"
    )


@rt("/card")
def test_card():
    return Page(
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
        title="Card"
    )


@rt("/checkbox")
def test_checkbox():
    return Page(
        H2("Checkbox Variants", cls="text-2xl font-semibold mb-4 mt-8"),
        Div(
            CheckboxWithLabel(
                label="Accept terms and conditions",                
                required=True
            ),
            CheckboxWithLabel(
                label="Subscribe to newsletter",                
                helper_text="Get weekly updates about new features",
            ),
            CheckboxWithLabel(
                label="Enable notifications",                
                checked=True
            ),
            CheckboxWithLabel(
                label="Disabled option",
                disabled=True,
                helper_text="This option is currently unavailable",
            ),
            CheckboxWithLabel(
                label="Error state example",                
                error_text="This field is required",
            ),
            cls="space-y-4"
        ),

        H2("Custom Styled Checkbox", cls="text-2xl font-semibold mb-4 mt-8"),
        Div(
            CheckboxWithLabel(
                label="Custom blue checkbox",                
                helper_text="With custom blue styling when checked",
                checkbox_cls="checked:!bg-blue-600 checked:!border-blue-600 dark:checked:!bg-blue-700 dark:checked:!border-blue-700",
                indicator_cls="!text-white",
            ),
            cls="p-4 border rounded-lg max-w-md",
        ),
        title="Checkbox"
    )


@rt("/code-block")
def test_code_block():
    return Page(
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
        title="Code Block"
    )


@rt("/date-picker")
def test_date_picker():
    return Page(
        H2("Date Picker Variants", cls="text-2xl font-semibold mb-4 mt-8"),

        Div(
            # Single date picker
            Div(
                H3("Single Date", cls="text-lg font-medium mb-2"),
                (single_picker := DatePicker(           
                    mode="single",
                    placeholder="Pick a date",
                )),
                Div(
                    P("Selected: ", Span(data_text=single_picker.selected.or_("None"), cls="font-mono text-sm")),
                    cls="mt-2 text-sm text-muted-foreground"
                ),
            ),
            # Date range picker
            Div(
                H3("Date Range", cls="text-lg font-medium mb-2"),
                (range_picker := DatePicker(                    
                    mode="range",
                    placeholder="Pick a date range",
                )),
                Div(
                    P("Range: ", Span(data_text=range_picker.selected.join(' - ').or_("None"), cls="font-mono text-sm")),
                    cls="mt-2 text-sm text-muted-foreground"
                ),
            ),
            # Date picker with presets
            Div(
                H3("With Presets", cls="text-lg font-medium mb-2"),
                (presets_picker := DatePicker(                    
                    with_presets=True,
                    placeholder="Select a date",
                )),
                Div(
                    P("Selected: ", Span(data_text=presets_picker.selected.or_("None"), cls="font-mono text-sm")),
                    cls="mt-2 text-sm text-muted-foreground"
                ),
            ),
            # Multiple date selection
            Div(
                H3("Multiple Dates", cls="text-lg font-medium mb-2"),
                (multiple_picker := DatePicker(                    
                    mode="multiple",
                    placeholder="Select multiple dates",
                )),
                Div(
                    P("Selected: ", Span(data_text=multiple_picker.selected.join(' | ').or_("None"), cls="font-mono text-sm")),
                    cls="mt-2 text-sm text-muted-foreground"
                ),
            ),
            # Date and time picker
            Div(
                H3("Date & Time", cls="text-lg font-medium mb-2"),
                (datetime_picker := DateTimePicker(
                    placeholder="Select date and time",
                )),
                Div(
                    P("Selected: ", Span(data_text=js(f"{datetime_picker.datetime}.replace('T', ' at ').replace(':00', '') || 'None'"), cls="font-mono text-sm")),
                    cls="mt-2 text-sm text-muted-foreground"
                ),
            ),
            # Date picker with input
            Div(
                H3("With Input Field", cls="text-lg font-medium mb-2"),
                (input_picker := DatePickerWithInput(
                    placeholder="YYYY-MM-DD",
                )),
                Div(
                    P("Value: ", Span(data_text=input_picker.selected.or_("None"), cls="font-mono text-sm")),
                    cls="mt-2 text-sm text-muted-foreground"
                ),
            ),
            cls="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
        ),
        title="Date Picker"
    )


@rt("/dialog")
def test_dialog():
    return Page(
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
                        Label("Name", fr="dialog-name"),
                        Input(
                            id="dialog-name",
                            placeholder="Your name",
                            cls="mt-1",
                        ),
                        cls="space-y-2",
                    ),
                    Div(
                        Label("Email", fr="dialog-email"),
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
            modal=False,
            size="md",
            cls="top-4 right-4 left-auto m-0",
        ),
        title="Dialog"
    )


@rt("/popover")
def test_popover():
    return Page(
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
                        Checkbox(),
                        cls="flex justify-between items-center mb-2",
                    ),
                    PopoverClose("Done", variant="ghost"),
                    aria_label="Quick settings menu",
                ),
            ),
            cls="flex flex-wrap gap-4"
        ),

        title="Popover"
    )


@rt("/command")
def test_command():
    return Page(
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
            size="sm",
            cls="max-w-md",
        ),

        title="Command"
    )


@rt("/theme-toggle")
def test_theme_toggle():
    return Page(
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

        title="Theme Toggle"
    )


@rt("/input")
def test_input():
    return Page(
        H2("Basic Inputs", cls="text-2xl font-semibold mb-4 mt-8"),
        Div(
            Div(
                (name := Signal("name", _ref_only=True)),
                Label("Text Input", fr="text-input", cls="block text-sm font-medium mb-1.5"),
                Input(id="text-input", placeholder="Enter text...", signal=name),
                P(data_text=name, cls="text-sm text-muted-foreground mt-1.5"),
                cls="space-y-1",
            ),
            Div(
                (email := Signal("email", _ref_only=True)),
                Label("Email Input", fr="email-input", cls="block text-sm font-medium mb-1.5"),
                Input(id="email-input", type="email", placeholder="email@example.com", signal=email),
                P(data_text=email, cls="text-sm text-muted-foreground mt-1.5"),
                cls="space-y-1",
            ),
            Div(
                Label("Password Input", fr="password-input", cls="block text-sm font-medium mb-1.5"),
                Input(id="password-input", type="password", placeholder="••••••••"),
                cls="space-y-1",
            ),
            Div(
                Label("Disabled Input", fr="disabled-input", cls="block text-sm font-medium mb-1.5"),
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
                required=True,
            ),
            InputWithLabel(
                label="Email Address",
                type="email",
                placeholder="john@example.com",
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
            (age := Signal("age", _ref_only=True)),
            (age_valid := Signal("age_valid", _ref_only=True)),
            Label("Age (must be >= 18)", fr="age-input", cls="block text-sm font-medium mb-1.5"),
            Input(
                id="age-input",
                type="text",
                placeholder="Enter age",
                signal=age,
                data_on_input=js(f"{age_valid} = Number({age}) >= 18"),
            ),
            P(
                Span("✓ Valid", cls="text-green-600", style="display: none", data_show=age & age_valid),
                Span("✗ Must be 18+", cls="text-destructive", style="display: none", data_show=age & ~age_valid),
                Span("Enter your age to validate", cls="text-muted-foreground", data_show=~age | age.eq("")),
                cls="text-sm mt-1.5",
            ),
            cls="max-w-md mb-8",
        ),

        title="Input"
    )


@rt("/label")
def test_label():
    return Page(
        H2("Basic Label Usage", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Labels are used with form inputs to provide accessible names:", cls="text-muted-foreground mb-4"),
        Div(
            Div(
                Label("Text Input", fr="text-input"),
                Input(
                    id="text-input",
                    placeholder="Enter text...",
                ),
                cls="space-y-2",
            ),
            Div(
                Label("Email Input", fr="email-input"),
                Input(
                    id="email-input",
                    type="email",
                    placeholder="email@example.com",
                ),
                cls="space-y-2",
            ),
            Div(
                Label("Password Input", fr="password-input"),
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
            Label("Disabled Input", fr="disabled-input"),
            cls="flex flex-col-reverse gap-2 max-w-md",
        ),

        H2("Label with Checkbox", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Labels work with checkboxes and other form elements:", cls="text-muted-foreground mb-4"),
        Div(
            CheckboxWithLabel(
                label="Accept terms and conditions",
            ),
            CheckboxWithLabel(
                label="Enable notifications",
                checked=True,
            ),
            cls="space-y-4 max-w-md",
        ),

        H2("Custom Styled Labels", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Labels can be customized with additional classes:", cls="text-muted-foreground mb-4"),
        Div(
            Div(
                Label("Bold Label", fr="bold-input", cls="!font-bold text-lg"),
                Input(id="bold-input", placeholder="With bold label"),
                cls="space-y-2",
            ),
            Div(
                Label("Primary Colored Label", fr="primary-input", cls="!text-primary !text-base"),
                Input(id="primary-input", placeholder="With primary colored label"),
                cls="space-y-2",
            ),
            Div(
                Label("Destructive Label", fr="destructive-input", cls="!text-destructive"),
                Input(id="destructive-input", placeholder="With destructive colored label"),
                cls="space-y-2",
            ),
            cls="space-y-6 max-w-md",
        ),

        title="Label"
    )


@rt("/progress")
def test_progress():
    return Page(
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
            (demo_progress := Signal("demo_progress", _ref_only=True)),
            Progress(value=35, signal=demo_progress),
            Div(
                Button(
                    Icon("lucide:plus"),
                    "Increase",
                    data_on_click=demo_progress.set((demo_progress + 10).min(100)),
                ),
                Button(
                    Icon("lucide:minus"),
                    "Decrease",
                    variant="secondary",
                    data_on_click=demo_progress.set((demo_progress - 10).max(0)),
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
                Span(data_text=demo_progress.round() + " + '%'", cls="font-mono"),
                cls="text-sm text-muted-foreground mt-4"
            ),
            cls="max-w-2xl"
        ),

        H2("Auto-incrementing Progress", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Automatically increment progress over time:", cls="text-muted-foreground mb-4"),
        Div(
            (auto_progress := Signal("auto_progress", _ref_only=True)),
            Progress(value=0, signal=auto_progress),
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

        title="Progress"
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
            (status_bar := Signal("status_bar", _ref_only=True)),
            (activity_bar := Signal("activity_bar", _ref_only=True)),
            (panel := Signal("panel", _ref_only=True)),
            DropdownMenu(
                DropdownMenuTrigger("View Options", variant="secondary"),
                DropdownMenuContent(
                    DropdownMenuLabel("Appearance"),
                    DropdownMenuSeparator(),
                    DropdownMenuCheckboxItem("Status Bar", signal=status_bar, checked=True),
                    DropdownMenuCheckboxItem("Activity Bar", signal=activity_bar),
                    DropdownMenuCheckboxItem("Panel", signal=panel),
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
            (position := Signal("position", _ref_only=True)),
            DropdownMenu(
                DropdownMenuTrigger("Select Position", variant="outline"),
                DropdownMenuContent(
                    DropdownMenuLabel("Position"),
                    DropdownMenuSeparator(),
                    DropdownMenuRadioGroup(
                        DropdownMenuRadioItem("Top", value="top"),
                        DropdownMenuRadioItem("Bottom", value="bottom"),
                        DropdownMenuRadioItem("Right", value="right"),
                        signal=position,
                        value="bottom",
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
                default_value="medium",
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
                default_value="option2",
            ),
            cls="p-4 border rounded-lg",
        ),
        title="Radio Group",
    )


@rt("/select")
def test_select():
    return Page(
        H2("Basic Select", cls="text-2xl font-semibold mb-4"),
        P("Select component with string options:", cls="text-muted-foreground mb-4"),
        Div(
            SelectWithLabel(
                label="Country",
                options=["United States", "Canada", "Mexico", "United Kingdom", "France", "Germany"],
                placeholder="Choose a country",
                helper_text="Select your country of residence",
            ),
            cls="mb-8",
        ),

        H2("Value/Label Tuples", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Select with separate values and labels:", cls="text-muted-foreground mb-4"),
        SelectWithLabel(
            label="Language",
            options=[
                ("en", "English"),
                ("es", "Spanish"),
                ("fr", "French"),
                ("de", "German"),
                ("jp", "Japanese"),
            ],
            value="en",
            helper_text="Choose your preferred language",
        ),

        H2("Grouped Options", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Select with option groups:", cls="text-muted-foreground mb-4"),
        SelectWithLabel(
            label="Framework",
            options=[
                {"group": "Frontend", "items": ["React", "Vue", "Angular", "Svelte"]},
                {"group": "Backend", "items": [("django", "Django"), ("fastapi", "FastAPI"), ("flask", "Flask")]},
                {"group": "Full Stack", "items": ["Next.js", "Nuxt", "SvelteKit"]},
            ],
            placeholder="Select a framework",
            required=True,
        ),

        H2("Error State", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Select with validation error:", cls="text-muted-foreground mb-4"),
        SelectWithLabel(
            label="Department",
            options=["Engineering", "Design", "Marketing", "Sales", "Support"],
            error_text="Please select a valid department",
            required=True,
        ),

        H2("Disabled State", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Disabled select with pre-selected value:", cls="text-muted-foreground mb-4"),
        SelectWithLabel(
            label="Plan",
            options=["Free", "Pro", "Enterprise"],
            value="Free",
            disabled=True,
            helper_text="Upgrade your account to change plans",
        ),

        H2("Simple Select", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Basic select without label wrapper:", cls="text-muted-foreground mb-4"),
        Div(
            Select(
                SelectTrigger(
                    SelectValue(placeholder="Pick an option"),
                ),
                SelectContent(
                    SelectItem("Option 1", value="opt1"),
                    SelectItem("Option 2", value="opt2"),
                    SelectItem("Option 3", value="opt3"),
                    SelectItem("Disabled", value="disabled", disabled=True),
                ),
            ),
            cls="p-4 border rounded-lg mb-8",
        ),

        H2("With Icons", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Select items with icons (using children):", cls="text-muted-foreground mb-4"),
        Div(
            Select(
                SelectTrigger(
                    SelectValue(placeholder="Select a status"),
                ),
                SelectContent(
                    SelectItem(
                        Icon("lucide:check-circle", cls="mr-2 h-4 w-4"),
                        "Completed",
                        value="completed"
                    ),
                    SelectItem(
                        Icon("lucide:clock", cls="mr-2 h-4 w-4"),
                        "In Progress",
                        value="in-progress"
                    ),
                    SelectItem(
                        Icon("lucide:circle", cls="mr-2 h-4 w-4"),
                        "Not Started",
                        value="not-started"
                    ),
                ),
            ),
            cls="p-4 border rounded-lg",
        ),

        title="Select",
    )


@rt("/separator")
def test_separator():
    return Page(
        H2("Basic Separator", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Horizontal separator dividing content:", cls="text-muted-foreground mb-4"),
        Div(
            P("Content above separator", cls="mb-4"),
            Separator(),
            P("Content below separator", cls="mt-4"),
            cls="mb-8",
        ),

        H2("Vertical Separators", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Vertical separator in flex layout:", cls="text-muted-foreground mb-4"),
        Div(
            Span("Left content"),
            Separator(orientation="vertical", cls="mx-4"),
            Span("Right content"),
            cls="flex items-center h-8 mb-8",
        ),

        H2("Custom Styling", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Separators with custom colors and thickness:", cls="text-muted-foreground mb-4"),
        Div(
            P("Custom colored separator below:", cls="mb-2"),
            Separator(cls="bg-red-500 h-0.5"),
            P("Thicker separator with different color:", cls="mt-4 mb-2"),
            Separator(cls="bg-blue-500 h-1"),
            cls="mb-8",
        ),

        title="Separator",
    )


@rt("/sheet")
def test_sheet():
    return Page(
        H2("Right Side Sheet", cls="text-2xl font-semibold mb-4"),
        P("Modal drawer that slides in from the right:", cls="text-muted-foreground mb-4"),
        Div(
            Sheet(
                SheetTrigger("Open Right Sheet"),
                SheetContent(
                    SheetHeader(
                        SheetTitle("Edit Profile"),
                        SheetDescription(
                            "Make changes to your profile here. Click save when you're done."
                        ),
                    ),
                    Div(
                        P("Sheet content goes here. Press ESC or click outside to close."),
                        Input(placeholder="Enter your name"),
                        Input(placeholder="Enter your email", type="email"),
                        cls="p-6 space-y-4",
                    ),
                    SheetFooter(
                        SheetClose("Cancel", variant="outline"),
                        SheetClose("Save Changes"),
                    ),
                    side="right",
                    size="md",
                ),
            ),
            cls="mb-8",
        ),

        H2("Left Side Sheet", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Sheet sliding from the left side:", cls="text-muted-foreground mb-4"),
        Div(
            Sheet(
                SheetTrigger("Open Left Sheet", variant="secondary"),
                SheetContent(
                    SheetHeader(
                        SheetTitle("Navigation"),
                        SheetDescription("Browse through the menu items."),
                    ),
                    Div(
                        SheetClose("Menu Item 1", variant="ghost", cls="w-full justify-start p-2 hover:bg-accent rounded"),
                        SheetClose("Menu Item 2", variant="ghost", cls="w-full justify-start p-2 hover:bg-accent rounded"),
                        SheetClose("Menu Item 3", variant="ghost", cls="w-full justify-start p-2 hover:bg-accent rounded"),
                        SheetClose("Menu Item 4", variant="ghost", cls="w-full justify-start p-2 hover:bg-accent rounded"),
                        cls="p-6 space-y-2 flex flex-col",
                    ),
                    side="left",
                    size="sm",
                ),
            ),
            cls="mb-8",
        ),

        H2("Top Side Sheet", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Sheet sliding from the top:", cls="text-muted-foreground mb-4"),
        Div(
            Sheet(
                SheetTrigger("Open Top Sheet", variant="outline"),
                SheetContent(
                    SheetHeader(
                        SheetTitle("Notification"),
                        SheetDescription("You have a new message."),
                    ),
                    Div(
                        P("This is a notification banner that slides in from the top."),
                        cls="p-6",
                    ),
                    side="top",
                ),
            ),
            cls="mb-8",
        ),

        H2("Bottom Side Sheet", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Sheet sliding from the bottom:", cls="text-muted-foreground mb-4"),
        Div(
            Sheet(
                SheetTrigger("Open Bottom Sheet", variant="destructive"),
                SheetContent(
                    SheetHeader(
                        SheetTitle("Confirm Action"),
                        SheetDescription(
                            "Are you sure you want to proceed?"
                        ),
                    ),
                    Div(
                        P("This action cannot be undone. Please confirm to continue."),
                        cls="p-6",
                    ),
                    SheetFooter(
                        SheetClose("Cancel", variant="outline"),
                        SheetClose("Confirm", variant="destructive"),
                    ),
                    side="bottom",
                ),
            ),
            cls="mb-8",
        ),

        H2("Large Sheet", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Sheet with large size:", cls="text-muted-foreground mb-4"),
        Div(
            Sheet(
                SheetTrigger("Open Large Sheet"),
                SheetContent(
                    SheetHeader(
                        SheetTitle("Large Content Area"),
                        SheetDescription("A wider sheet for more content."),
                    ),
                    Div(
                        P("This sheet has more horizontal space for complex layouts."),
                        Div(
                            Input(placeholder="First Name", cls="mb-2"),
                            Input(placeholder="Last Name", cls="mb-2"),
                            Input(placeholder="Email", type="email", cls="mb-2"),
                            Input(placeholder="Phone", type="tel"),
                        ),
                        cls="p-6 space-y-4",
                    ),
                    SheetFooter(
                        SheetClose("Close", variant="outline"),
                        SheetClose("Submit"),
                    ),
                    side="right",
                    size="lg",
                ),
            ),
            cls="mb-8",
        ),

        title="Sheet",
    )


@rt("/skeleton")
def test_skeleton():
    return Page(
        H2("Basic Shapes", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Simple skeleton placeholders for text content:", cls="text-muted-foreground mb-4"),
        Div(
            Skeleton(cls="h-4 w-64"),  # Text line
            Skeleton(cls="h-4 w-48"),  # Shorter text line
            Skeleton(cls="h-4 w-56"),  # Another text line
            cls="space-y-2 max-w-2xl"
        ),

        H2("Card Skeleton", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Skeleton for a card with avatar and content:", cls="text-muted-foreground mb-4"),
        Div(
            Div(
                Skeleton(cls="h-12 w-12 rounded-full"),  # Avatar
                Div(
                    Skeleton(cls="h-4 w-32"),  # Name
                    Skeleton(cls="h-3 w-24"),  # Subtitle
                    cls="space-y-2",
                ),
                cls="flex items-center space-x-4",
            ),
            Skeleton(cls="h-32 w-full mt-4"),  # Content area
            Skeleton(cls="h-4 w-full mt-4"),  # Footer line
            cls="p-4 border rounded-lg max-w-2xl"
        ),

        H2("Article Skeleton", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Skeleton for an article with title, date, text, and image:", cls="text-muted-foreground mb-4"),
        Div(
            Skeleton(cls="h-8 w-3/4 mb-4"),  # Title
            Skeleton(cls="h-3 w-32 mb-6"),  # Date
            Div(
                Skeleton(cls="h-4 w-full"),
                Skeleton(cls="h-4 w-full"),
                Skeleton(cls="h-4 w-2/3"),
                cls="space-y-2 mb-4",
            ),
            Skeleton(cls="h-40 w-full"),  # Image placeholder
            cls="p-4 border rounded-lg max-w-2xl"
        ),

        H2("Loading State Toggle", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Toggle between skeleton loading state and actual content:", cls="text-muted-foreground mb-4"),
        Div(
            (loading := Signal("loading", True)),
            Button(
                data_text=loading.if_("Stop Loading", "Start Loading"),
                data_on_click=loading.toggle(),
                variant="outline",
                cls="mb-4",
            ),
            # Skeleton shown while loading
            Div(
                Skeleton(cls="h-6 w-48 mb-2"),
                Skeleton(cls="h-4 w-64 mb-4"),
                Skeleton(cls="h-20 w-full"),
                style="display: none",
                data_show=loading,
            ),
            # Actual content shown when loaded
            Div(
                H4("Content Loaded!", cls="text-lg font-semibold mb-2"),
                P("This content appears when loading is complete.", cls="mb-4"),
                Div(
                    "This is the actual content that would load.",
                    cls="p-4 bg-muted rounded-lg",
                ),
                style="display: none",
                data_show=~loading,
            ),
            cls="p-4 border rounded-lg max-w-2xl"
        ),

        title="Skeleton"
    )


@rt("/switch")
def test_switch():
    return Page(
        H2("Switch Variants", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Switches with labels, helper text, and various states:", cls="text-muted-foreground mb-4"),
        Div(
            SwitchWithLabel(
                label="Enable notifications",
                checked=True,
                helper_text="Receive email notifications about updates",
            ),
            SwitchWithLabel(
                label="Marketing emails",
                helper_text="Get promotional emails and special offers",
            ),
            SwitchWithLabel(
                label="Two-factor authentication",
                required=True,
                helper_text="Enhanced security for your account",
            ),
            SwitchWithLabel(
                label="Disabled option",
                disabled=True,
                helper_text="This feature is not available in your plan",
            ),
            SwitchWithLabel(
                label="Error state example",
                error_text="This setting requires admin approval",
            ),
            cls="space-y-4"
        ),

        H2("Simple Switches", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Basic switches without labels:", cls="text-muted-foreground mb-4"),
        Div(
            P("Simple switches:", cls="text-sm font-medium mb-2"),
            Div(
                Switch(checked=True),
                Switch(),
                Switch(disabled=True),
                cls="flex gap-4",
            ),
            cls="p-4 border rounded-lg max-w-md"
        ),

        H2("Interactive Demo", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Toggle the switch to see state changes in real-time:", cls="text-muted-foreground mb-4"),
        Div(
            (demo_switch := Signal("demo_switch", _ref_only=True)),
            SwitchWithLabel(
                label="Demo Switch",
                signal=demo_switch,
                helper_text="Toggle to see the state below",
            ),
            Div(
                P(
                    Span("Status: ", cls="font-medium"),
                    Span(
                        data_text=demo_switch.if_("ON", "OFF"),
                        data_attr_class=demo_switch.if_(
                            "text-green-600 dark:text-green-400 font-semibold",
                            "text-red-600 dark:text-red-400 font-semibold"
                        ),
                    ),
                    cls="text-sm"
                ),
                cls="mt-4 p-4 bg-muted rounded-lg"
            ),
            cls="p-4 border rounded-lg max-w-md"
        ),

        title="Switch"
    )


@rt("/table")
def test_table():
    return Page(
        H2("Basic Table", cls="text-2xl font-semibold mb-4 mt-8"),
        P("A simple table with invoices and payment information:", cls="text-muted-foreground mb-4"),
        Table(
            TableHeader(
                TableRow(
                    TableHead("Invoice"),
                    TableHead("Status"),
                    TableHead("Method"),
                    TableHead("Amount", cls="text-right"),
                )
            ),
            TableBody(
                TableRow(
                    TableCell("INV001"),
                    TableCell(Badge("Paid", variant="secondary")),
                    TableCell("Credit Card"),
                    TableCell("$250.00", cls="text-right"),
                ),
                TableRow(
                    TableCell("INV002"),
                    TableCell(Badge("Pending", variant="outline")),
                    TableCell("PayPal"),
                    TableCell("$150.00", cls="text-right"),
                ),
                TableRow(
                    TableCell("INV003"),
                    TableCell(Badge("Unpaid", variant="destructive")),
                    TableCell("Bank Transfer"),
                    TableCell("$350.00", cls="text-right"),
                ),
                TableRow(
                    TableCell("INV004"),
                    TableCell(Badge("Paid", variant="secondary")),
                    TableCell("Credit Card"),
                    TableCell("$450.00", cls="text-right"),
                ),
            ),
            TableFooter(
                TableRow(
                    TableCell("Total", colspan="3", cls="font-medium"),
                    TableCell("$1,200.00", cls="text-right font-medium"),
                )
            ),
        ),

        H2("Table with Selection", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Table with selectable rows and checkboxes:", cls="text-muted-foreground mb-4"),
        Table(
            TableCaption("A list of users with selection capabilities."),
            TableHeader(
                TableRow(
                    TableHead("Select"),
                    TableHead("Name"),
                    TableHead("Email"),
                    TableHead("Role"),
                    TableHead("Actions"),
                )
            ),
            TableBody(
                TableRow(
                    TableCell(Checkbox()),
                    TableCell("John Doe"),
                    TableCell("john@example.com"),
                    TableCell(Badge("Admin")),
                    TableCell(
                        Button("Edit", variant="ghost", size="sm"),
                    ),
                ),
                TableRow(
                    TableCell(Checkbox(checked=True)),
                    TableCell("Jane Smith"),
                    TableCell("jane@example.com"),
                    TableCell(Badge("User", variant="secondary")),
                    TableCell(
                        Button("Edit", variant="ghost", size="sm"),
                    ),
                    selected=True,
                ),
                TableRow(
                    TableCell(Checkbox()),
                    TableCell("Bob Johnson"),
                    TableCell("bob@example.com"),
                    TableCell(Badge("User", variant="secondary")),
                    TableCell(
                        Button("Edit", variant="ghost", size="sm"),
                    ),
                ),
            ),
        ),

        H2("Compact Table", cls="text-2xl font-semibold mb-4 mt-8"),
        P("A compact table with custom sizing:", cls="text-muted-foreground mb-4"),
        Table(
            TableHeader(
                TableRow(
                    TableHead("Product"),
                    TableHead("Price"),
                    TableHead("Stock"),
                    TableHead("Category"),
                )
            ),
            TableBody(
                TableRow(
                    TableCell("Laptop"),
                    TableCell("$999"),
                    TableCell("12"),
                    TableCell("Electronics"),
                ),
                TableRow(
                    TableCell("Mouse"),
                    TableCell("$29"),
                    TableCell("45"),
                    TableCell("Electronics"),
                ),
                TableRow(
                    TableCell("Keyboard"),
                    TableCell("$79"),
                    TableCell("8"),
                    TableCell("Electronics"),
                ),
                TableRow(
                    TableCell("Monitor"),
                    TableCell("$299"),
                    TableCell("15"),
                    TableCell("Electronics"),
                ),
            ),
            cls="text-xs [&_th]:h-8 [&_td]:p-1 [&_th]:p-1",
        ),

        title="Table"
    )


@rt("/textarea")
def test_textarea():
    return Page(
        H2("Textarea Variants", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Textareas with labels, helper text, and various states:", cls="text-muted-foreground mb-4"),
        Div(
            TextareaWithLabel(
                label="Description",
                placeholder="Enter your description here...",
                helper_text="Provide a detailed description",
            ),
            TextareaWithLabel(
                label="Bio",
                placeholder="Tell us about yourself",
                required=True,
                error_text="Bio is required and must be at least 50 characters",
            ),
            TextareaWithLabel(
                label="Notes",
                value="This field is currently disabled",
                disabled=True,
                helper_text="This field will be enabled after verification",
            ),
            TextareaWithLabel(
                label="Comments",
                placeholder="Share your thoughts...",
                rows=5,
                helper_text="Fixed height with 5 rows",
            ),
            cls="space-y-4"
        ),

        H2("Simple Textarea", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Basic textarea without label:", cls="text-muted-foreground mb-4"),
        Div(
            P("Simple textarea:", cls="text-sm font-medium mb-2"),
            Textarea(
                placeholder="Type something...",
                resize="vertical",
            ),
            cls="p-4 border rounded-lg max-w-2xl"
        ),

        H2("Interactive Demo", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Type in the textarea to see live preview:", cls="text-muted-foreground mb-4"),
        Div(
            (reactive_text := Signal("reactive_text", _ref_only=True)),
            Textarea(
                placeholder="Type here to test reactive binding...",
                signal=reactive_text,
                rows=3,
                cls="mb-4",
            ),
            Div(
                P("Live Preview:", cls="font-medium mb-2"),
                P(
                    data_text=reactive_text.if_(reactive_text, "(nothing typed yet)"),
                    cls="p-3 border rounded bg-muted min-h-[3rem]"
                ),
            ),
            cls="p-4 border rounded-lg max-w-2xl"
        ),

        title="Textarea"
    )


@rt("/tabs")
def test_tabs():
    return Page(
        H2("Default Variant (Boxed Style)", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Auto-indexed tabs - no need to specify id, defaults to first tab:", cls="text-muted-foreground mb-4"),
        Tabs(
            TabsList(
                TabsTrigger("Preview"),
                TabsTrigger("Code"),
                TabsTrigger("Settings"),
            ),
            TabsContent(
                Div(
                    H3("Preview Content", cls="text-lg font-semibold mb-2"),
                    P("This is the preview tab content with the default boxed style."),
                    Button("Action in Preview", variant="secondary", cls="mt-4"),
                ),
            ),
            TabsContent(
                Div(
                    H3("Code Content", cls="text-lg font-semibold mb-2"),
                    Pre(
                        Code("# Example code\ndef hello_world():\n    print('Hello, World!')", cls="text-sm"),
                        cls="bg-muted p-4 rounded-md overflow-x-auto"
                    ),
                ),
            ),
            TabsContent(
                Div(
                    H3("Settings Content", cls="text-lg font-semibold mb-2"),
                    P("Configure your preferences here."),
                    Div(
                        Label("Enable notifications", fr="notifications_default"),
                        Checkbox(checked=True),
                        cls="flex items-center gap-2 mt-4",
                    ),
                ),
            ),
            variant="default",
        ),

        H2("Plain Variant (Text Style)", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Plain variant with auto-indexed tabs:", cls="text-muted-foreground mb-4"),
        Tabs(
            TabsList(
                TabsTrigger("Account"),
                TabsTrigger("Password"),
                TabsTrigger("Team"),
                TabsTrigger("Billing"),
            ),
            TabsContent(
                Div(
                    H3("Account Settings", cls="text-lg font-semibold mb-2"),
                    P("Manage your account settings and preferences."),
                    Div(
                        Label("Username", fr="username_plain"),
                        Input(id="username_plain", placeholder="Enter username"),
                        Label("Email", fr="email_plain", cls="mt-2"),
                        Input(id="email_plain", type="email", placeholder="Enter email"),
                        cls="space-y-2 mt-4",
                    ),
                ),
            ),
            TabsContent(
                Div(
                    H3("Password & Security", cls="text-lg font-semibold mb-2"),
                    P("Update your password and security settings."),
                    Button("Change Password", variant="outline", cls="mt-4"),
                ),
            ),
            TabsContent(
                Div(
                    H3("Team Members", cls="text-lg font-semibold mb-2"),
                    P("Manage your team and collaborate with others."),
                ),
            ),
            TabsContent(
                Div(
                    H3("Billing Information", cls="text-lg font-semibold mb-2"),
                    P("View and manage your subscription and payment methods."),
                ),
            ),
            variant="plain",
        ),

        H2("With Semantic IDs", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Using semantic string IDs with custom default_id (starts on 'profile' tab):", cls="text-muted-foreground mb-4"),
        Tabs(
            TabsList(
                TabsTrigger(
                    Icon("lucide:home"),
                    "Home",
                    id="home",
                ),
                TabsTrigger(
                    Icon("lucide:user"),
                    "Profile",
                    id="profile",
                ),
                TabsTrigger(
                    Icon("lucide:settings"),
                    "Settings",
                    id="settings_icon",
                ),
            ),
            TabsContent(
                Div(
                    H3("Home Tab", cls="text-lg font-semibold mb-2"),
                    P("Welcome to the home section."),
                ),
                id="home",
            ),
            TabsContent(
                Div(
                    H3("Profile Tab", cls="text-lg font-semibold mb-2"),
                    P("View and edit your profile information."),
                ),
                id="profile",
            ),
            TabsContent(
                Div(
                    H3("Settings Tab", cls="text-lg font-semibold mb-2"),
                    P("Manage your application settings."),
                ),
                id="settings_icon",
            ),
            default_value="profile",
            variant="default",
        ),

        title="Tabs"
    )


@rt("/toggle")
def test_toggle():
    return Page(
        H2("Toggles", cls="text-2xl font-semibold mb-4"),

        # Basic toggles
        Div(
            P("Basic toggles:", cls="text-sm font-medium mb-2"),
            Div(
                Toggle(Icon("lucide:bold")),
                Toggle(Icon("lucide:italic"), pressed=True),
                Toggle(Icon("lucide:underline")),
                Toggle(Icon("lucide:strikethrough"), disabled=True),
                cls="flex gap-1",
            ),
            cls="mb-4",
        ),

        # Outline variant toggles
        Div(
            P("Outline variant:", cls="text-sm font-medium mb-2"),
            Div(
                Toggle(Icon("lucide:align-left"), variant="outline"),
                Toggle(Icon("lucide:align-center"), variant="outline", pressed=True),
                Toggle(Icon("lucide:align-right"), variant="outline"),
                Toggle(Icon("lucide:align-justify"), variant="outline"),
                cls="flex gap-1",
            ),
            cls="mb-4",
        ),

        # Different sizes
        Div(
            P("Different sizes:", cls="text-sm font-medium mb-2"),
            Div(
                Toggle("Small", size="sm", variant="outline"),
                Toggle("Default", size="default", variant="outline"),
                Toggle("Large", size="lg", variant="outline"),
                cls="flex gap-2 items-center",
            ),
            cls="mb-4",
        ),

        # Toggle with text
        Div(
            P("Toggle with text:", cls="text-sm font-medium mb-2"),
            Div(
                Toggle(
                    Icon("lucide:wifi"),
                    Span("WiFi", cls="ml-1"),
                    variant="outline",
                ),
                Toggle(
                    Icon("lucide:bluetooth"),
                    Span("Bluetooth", cls="ml-1"),
                    variant="outline",
                    pressed=True,
                ),
                Toggle(
                    Icon("lucide:plane"),
                    Span("Airplane Mode", cls="ml-1"),
                    variant="outline",
                ),
                cls="flex gap-2",
            ),
            cls="mb-4",
        ),

        title="Toggle"
    )


@rt("/toggle_group")
def test_toggle_group():
    return Page(
        H2("Single Selection Toggle Groups", cls="text-2xl font-semibold mb-4"),
        P("Click items to toggle selection. Only one item can be selected at a time.", cls="text-muted-foreground mb-4"),

        Div(
            P("Text formatting (bold pre-selected):", cls="text-sm font-medium mb-2"),
            ToggleGroup(
                ("bold", Icon("lucide:bold")),
                ("italic", Icon("lucide:italic")),
                ("underline", Icon("lucide:underline")),
                type="single",
                variant="outline",
                default_value="bold",
            ),
            cls="mb-6",
        ),

        Div(
            P("Text alignment (center pre-selected):", cls="text-sm font-medium mb-2"),
            ToggleGroup(
                ("left", Icon("lucide:align-left")),
                ("center", Icon("lucide:align-center")),
                ("right", Icon("lucide:align-right")),
                ("justify", Icon("lucide:align-justify")),
                type="single",
                variant="default",
                default_value="center",
            ),
            cls="mb-6",
        ),

        Div(
            P("Size selection (no pre-selection):", cls="text-sm font-medium mb-2"),
            ToggleGroup(
                ("sm", "Small"),
                ("md", "Medium"),
                ("lg", "Large"),
                ("xl", "Extra Large"),
                type="single",
                variant="outline",
                size="lg",
            ),
            cls="mb-6",
        ),

        Div(
            P("View mode:", cls="text-sm font-medium mb-2"),
            ToggleGroup(
                ("list", Div(Icon("lucide:list"), Span("List", cls="ml-1"), cls="flex items-center")),
                ("grid", Div(Icon("lucide:layout-grid"), Span("Grid", cls="ml-1"), cls="flex items-center")),
                ("gallery", Div(Icon("lucide:image"), Span("Gallery", cls="ml-1"), cls="flex items-center")),
                type="single",
                variant="outline",
            ),
            cls="mb-8",
        ),

        H2("Multiple Selection Toggle Groups", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Click items to toggle selection. Multiple items can be selected.", cls="text-muted-foreground mb-4"),

        Div(
            P("Text options (multiple selection, bold and italic pre-selected):", cls="text-sm font-medium mb-2"),
            ToggleGroup(
                ("bold", Icon("lucide:bold")),
                ("italic", Icon("lucide:italic")),
                ("underline", Icon("lucide:underline")),
                ("strikethrough", Icon("lucide:strikethrough")),
                type="multiple",
                variant="outline",
                default_value=["bold", "italic"],
            ),
            cls="mb-8",
        ),

        H2("States", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Toggle groups in different states:", cls="text-muted-foreground mb-4"),

        Div(
            P("Disabled group:", cls="text-sm font-medium mb-2"),
            ToggleGroup(
                ("option1", "Option 1"),
                ("option2", "Option 2"),
                ("option3", "Option 3"),
                type="single",
                variant="outline",
                disabled=True,
            ),
            cls="mb-6",
        ),

        title="Toggle Group"
    )


@rt("/toast")
def test_toast():
    return Page(
        H2("Basic Toast Types", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Click the buttons to trigger different toast variants:", cls="text-muted-foreground mb-4"),
        Div(
            Button(
                "Default Toast",
                data_on_click=toast('Event has been created', 'Your event is now live'),
                variant="outline"
            ),
            Button(
                "Success Toast",
                data_on_click=toast.success('Success!', 'Operation completed successfully'),
                variant="outline"
            ),
            Button(
                "Error Toast",
                data_on_click=toast.error('Error!', 'Something went wrong'),
                variant="outline"
            ),
            Button(
                "Warning Toast",
                data_on_click=toast.warning('Warning!', 'Please be careful'),
                variant="outline"
            ),
            Button(
                "Info Toast",
                data_on_click=toast.info('Info', 'Here is some information'),
                variant="outline"
            ),
            cls="flex flex-wrap gap-2"
        ),

        H2("Custom Duration", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Control how long toasts stay visible:", cls="text-muted-foreground mb-4"),
        Div(
            Button(
                "Quick Toast (1s)",
                data_on_click=toast('Quick!', 'This disappears fast', duration=1000),
                variant="secondary"
            ),
            Button(
                "Long Toast (10s)",
                data_on_click=toast('Long Toast', 'This stays for 10 seconds', duration=10000),
                variant="secondary"
            ),
            Button(
                "Persistent Toast",
                data_on_click=toast('Persistent', 'Click X to dismiss', duration=0),
                variant="secondary"
            ),
            cls="flex flex-wrap gap-2"
        ),

        H2("Multiple Toasts", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Trigger multiple toasts in sequence:", cls="text-muted-foreground mb-4"),
        Div(
            Button(
                "Spam Toasts",
                data_on_click=f"""
                    {toast.info('First toast', 'This is the first one')}
                    setTimeout(() => {{ {toast.success('Second toast', 'This is the second one')} }}, 500);
                    setTimeout(() => {{ {toast.warning('Third toast', 'This is the third one')} }}, 1000);
                """,
                variant="destructive"
            ),
            cls="flex gap-2"
        ),

        H2("Promise Pattern", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Simulate loading states with sequential toasts (loading toast is replaced by result):", cls="text-muted-foreground mb-4"),
        Div(
            Button(
                "Promise Toast",
                data_on_click=f"""
                    {toast('Loading...', 'Please wait...', duration=0)}
                    setTimeout(() => {{
                        $toasts = $toasts.filter(t => t.title !== 'Loading...');
                        {toast.success('Success!', 'Promise resolved successfully')}
                    }}, 2000);
                """,
                variant="outline"
            ),
            Button(
                "Rich Colors Demo",
                data_on_click=toast.success('Rich Colors', 'Notice the rich background gradients'),
                variant="outline"
            ),
            cls="flex gap-2"
        ),

        title="Toast"
    )


@rt("/toast/sse-example")
@sse
async def toast_sse_example():
    """Server-side SSE toast example - demonstrates hypermedia pattern."""
    import random

    t = ToastQueue()

    yield t.info("Processing...", "Starting server operation")
    await asyncio.sleep(1)

    yield t.show("Step 1 Complete", "Validating data...")
    await asyncio.sleep(1)

    yield t.warning("Step 2", "Checking permissions...")
    await asyncio.sleep(1)

    if random.choice([True, False]):
        yield t.success("Success!", "Operation completed successfully")
    else:
        yield t.error("Failed", "Operation encountered an error")

    await asyncio.sleep(4)
    yield t.clear()


@rt("/toast-server")
def test_toast_server():
    """Toast examples showing both client-side and server-side (SSE) patterns."""
    return Page(
        H2("Server-Side Toasts (Hypermedia Pattern)", cls="text-2xl font-semibold mb-4 mt-8"),
        P("These toasts are triggered by server-sent events (SSE), demonstrating the hypermedia approach:", cls="text-muted-foreground mb-4"),
        Div(
            Button(
                "Server-Side Toast",
                data_on_click=get("/toast/sse-example"),
                variant="default"
            ),
            P("Click to trigger a server process that sends toast notifications via SSE.", cls="text-sm text-muted-foreground mt-2"),
            cls="space-y-2"
        ),

        H2("Client-Side Toasts", cls="text-2xl font-semibold mb-4 mt-8"),
        P("These toasts are triggered directly in the browser:", cls="text-muted-foreground mb-4"),
        Div(
            Button(
                "Client-Side Toast",
                data_on_click=toast.success('Client-Side', 'This was triggered directly in the browser'),
                variant="outline"
            ),
            P("Click to trigger a toast using client-side JavaScript.", cls="text-sm text-muted-foreground mt-2"),
            cls="space-y-2"
        ),

        H2("Architecture Comparison", cls="text-2xl font-semibold mb-4 mt-8"),
        Card(
            CardHeader(
                CardTitle("Client-Side Pattern"),
                CardDescription("JavaScript executes directly in the browser")
            ),
            CardContent(
                CodeBlock('''Button(
    "Show Toast",
    data_on_click=toast('Message', 'Description')
)''', language="python"),
                P("Best for: Immediate UI feedback, form validation", cls="text-sm text-muted-foreground mt-4")
            ),
            cls="mb-4"
        ),

        Card(
            CardHeader(
                CardTitle("Server-Side Pattern (SSE)"),
                CardDescription("Server sends toast via Server-Sent Events")
            ),
            CardContent(
                CodeBlock('''@rt("/process")
@sse
async def process():
    t = ToastQueue()
    yield t.success('Message', 'Description')

Button(
    "Process",
    data_on_click=get("/process")
)''', language="python"),
                P("Best for: Long-running operations, multi-step processes, server notifications", cls="text-sm text-muted-foreground mt-4")
            )
        ),

        title="Toast - Server & Client Patterns"
    )


@rt("/typography")
def test_typography():
    return Page(
        H1("Typography System"),
        Subtitle("Beautiful, consistent text styling with pragmatic defaults for your Star UI applications."),
        Lead("Explore our comprehensive typography components designed for accessibility, readability, and visual hierarchy."),

        Hr(),

        # Typography scale showcase
        Section(
            H2("Typography Scale", section=True),
            Lead("A comprehensive hierarchy designed for optimal readability and visual balance."),

            # Display Example
            Div(
                Caption("DISPLAY"),
                Display("The quick brown fox jumps", cls="!mt-0 !mb-4"),
                cls="py-6 border-b border-border last:border-0"
            ),

            # H1 Example
            Div(
                Caption("H1 - PRIMARY HEADING"),
                H1("The quick brown fox jumps over the lazy dog", cls="!mt-0 !mb-4"),
                cls="py-6 border-b border-border last:border-0"
            ),

            # H2 Example
            Div(
                Caption("H2 - SECONDARY HEADING"),
                H2("The quick brown fox jumps over the lazy dog", cls="!mt-0 !mb-4"),
                cls="py-6 border-b border-border last:border-0"
            ),

            # H3 Example
            Div(
                Caption("H3 - TERTIARY HEADING"),
                H3("The quick brown fox jumps over the lazy dog", cls="!mt-0 !mb-4"),
                cls="py-6 border-b border-border last:border-0"
            ),

            # H4-H6 Examples in grid
            Div(
                Div(
                    Caption("H4 - QUATERNARY"),
                    H4("The quick brown fox", cls="!mt-0 !mb-4"),
                ),
                Div(
                    Caption("H5 - FIFTH LEVEL"),
                    H5("The quick brown fox", cls="!mt-0 !mb-4"),
                ),
                Div(
                    Caption("H6 - SIXTH LEVEL"),
                    H6("The quick brown fox", cls="!mt-0 !mb-4"),
                ),
                cls="grid grid-cols-1 md:grid-cols-3 gap-6 py-6"
            ),
        ),

        Hr(),

        # Text variants
        Section(
            H2("Text Variants", section=True),
            Lead("Semantic text components for different content types and emphasis levels."),

            # Lead
            Div(
                Caption("LEAD - INTRODUCTORY TEXT"),
                Lead("A modal dialog that interrupts the user with important content and expects a response.", cls="!mt-0 !mb-4"),
                cls="py-6 border-b border-border last:border-0"
            ),

            # Subtitle
            Div(
                Caption("SUBTITLE - SECONDARY DESCRIPTION"),
                Subtitle("Perfect for supporting information that accompanies main headings.", cls="!mt-0 !mb-4"),
                cls="py-6 border-b border-border last:border-0"
            ),

            # Paragraph
            Div(
                Caption("PARAGRAPH - BODY TEXT"),
                P("The king thought long and hard, and finally came up with a brilliant plan: he would tax the jokes in the kingdom. This is the standard body text with optimal line height for reading.", cls="!mt-0 !mb-4"),
                cls="py-6 border-b border-border last:border-0"
            ),

            # Large
            Div(
                Caption("LARGE - EMPHASIZED TEXT"),
                Large("Are you absolutely sure you want to proceed with this action?", cls="!mt-0 !mb-4"),
                cls="py-6 border-b border-border last:border-0"
            ),

            # Small, Muted, Caption grid
            Div(
                Div(
                    Caption("SMALL - FINE PRINT"),
                    Small("Terms and conditions apply"),
                ),
                Div(
                    Caption("MUTED - DE-EMPHASIZED"),
                    Muted("Enter your email address to continue.", cls="!mt-0 !mb-4"),
                ),
                Div(
                    Caption("CAPTION - METADATA"),
                    Caption("Last updated: March 2024"),
                ),
                cls="grid grid-cols-1 md:grid-cols-3 gap-6 py-6 border-b border-border last:border-0"
            ),

            # Text component variants (removed invalid weight= and align= parameters)
            Div(
                Caption("TEXT COMPONENT - FLEXIBLE VARIANTS"),
                Div(
                    Text("Body variant with normal weight", variant="body"),
                    Text("Lead variant for emphasis", variant="lead"),
                    Text("Small variant for fine print", variant="small"),
                    cls="space-y-4"
                ),
                cls="py-6 border-b border-border last:border-0"
            ),

            # Inline Code
            Div(
                Caption("INLINE CODE - CODE SNIPPETS"),
                P("Use the ", InlineCode("H1"), " component for main headings and ", InlineCode("<Text variant='body'>"), " for flexible body text with variants.", cls="!mt-0 !mb-4"),
                cls="py-6"
            ),
        ),

        Hr(),

        # Special elements
        Section(
            H2("Special Elements", section=True),
            Lead("Specialized components for quotes, lists, and structured content."),

            # Blockquote
            Div(
                Caption("BLOCKQUOTE - QUOTED CONTENT"),
                Blockquote(
                    "Design is not just what it looks like and feels like. Design is how it works. Great typography is the foundation of all great design.",
                    cls="!mt-0 !mb-4"
                ),
                cls="py-6 border-b border-border last:border-0"
            ),

            # Lists
            Div(
                Div(
                    Caption("UNORDERED LIST"),
                    List(
                        Li("Consistent vertical rhythm throughout all components"),
                        Li("Semantic HTML elements for accessibility"),
                        Li("Responsive typography that scales beautifully"),
                        Li("Dark mode support with proper contrast ratios"),
                        cls="!mt-0 !mb-4"
                    ),
                ),
                Div(
                    Caption("ORDERED LIST"),
                    List(
                        Li("Analyze your content hierarchy needs"),
                        Li("Choose appropriate heading levels (H1-H6)"),
                        Li("Select text variants based on semantic meaning"),
                        Li("Apply consistent spacing using our scale"),
                        ordered=True,
                        cls="!mt-0 !mb-4"
                    ),
                ),
                cls="grid grid-cols-1 lg:grid-cols-2 gap-8 py-6 border-b border-border last:border-0"
            ),

            # Figure and Figcaption
            Div(
                Caption("FIGURE - IMAGE WITH CAPTION"),
                Figure(
                    Div(
                        "📊",
                        cls="w-full h-48 bg-muted rounded-lg flex items-center justify-center text-6xl"
                    ),
                    Figcaption("Fig 1. Typography usage statistics across modern web applications showing consistent hierarchy patterns."),
                    cls="!mt-0 !mb-4"
                ),
                cls="py-6"
            ),
        ),

        Hr(),

        # Prose component demo
        Section(
            H2("Prose Component", section=True),
            Lead("The Prose component uses the Tailwind Typography plugin for beautiful, consistent styling of content-rich areas like articles, blog posts, and documentation."),
            Subtitle("Powered by @tailwindcss/typography with design system integration. Compare different sizes and see how the typography scales consistently."),

            # Size comparison
            Div(
                # Small prose example
                Div(
                    Caption("SIZE: SMALL - COMPACT CONTENT"),
                    Div(
                        Prose(
                            H2("Typography Principles"),
                            P("Good typography creates hierarchy, guides the eye, and enhances readability. It should be invisible to the reader while making content easy to consume."),
                            Ul(
                                Li("Consistent spacing and rhythm"),
                                Li("Clear visual hierarchy"),
                                Li("Optimal line lengths and heights")
                            ),
                            size="sm"
                        ),
                        cls="bg-card rounded-lg border p-6"
                    ),
                    cls="mb-8"
                ),

                # Base prose example
                Div(
                    Caption("SIZE: BASE - STANDARD CONTENT"),
                    Div(
                        Prose(
                            H1("The Power of Typography"),
                            P("Typography is the art and technique of arranging type to make written language legible, readable, and appealing when displayed. It's one of the most important aspects of design."),

                            H2("Why Typography Matters"),
                            P("Good typography can make the difference between content that engages and content that frustrates. It guides the reader's eye and creates a hierarchy that makes information easy to process."),

                            Blockquote(
                                "Typography is the craft of endowing human language with a durable visual form."
                            ),

                            H3("Key Principles"),
                            P("When working with typography, consider these essential elements:"),

                            Ul(
                                Li("Hierarchy - Use size, weight, and spacing to create clear information levels"),
                                Li("Contrast - Ensure sufficient contrast for accessibility and readability"),
                                Li("Consistency - Maintain uniform spacing and styling throughout"),
                                Li("Readability - Choose appropriate line heights and lengths")
                            ),

                            P("Modern web typography also needs to be ", InlineCode("responsive"), " and work across all devices and screen sizes."),

                            size="base"
                        ),
                        cls="bg-card rounded-lg border p-8"
                    ),
                    cls="mb-8"
                ),

                # Large prose example
                Div(
                    Caption("SIZE: LARGE - FEATURE CONTENT"),
                    Div(
                        Prose(
                            H1("Design at Scale"),
                            P("Creating typography systems that work at scale requires careful consideration of every detail, from the smallest caption to the largest display text."),

                            H2("Implementation"),
                            P("Our typography system uses semantic tokens and consistent spacing to ensure harmony across all components."),

                            size="lg"
                        ),
                        cls="bg-card rounded-lg border p-8"
                    ),
                ),

                cls="space-y-8 mt-8"
            ),
        ),

        Hr(),

        # Usage examples
        Section(
            H2("Usage Examples", section=True),
            Lead("See how typography components work together in real-world scenarios."),

            Div(
                # Card example
                Div(
                    Caption("CARD LAYOUT WITH TYPOGRAPHY"),
                    Div(
                        H3("Welcome to StarUI"),
                        Subtitle("Build beautiful interfaces with our component library"),
                        P("StarUI provides a comprehensive set of components designed for modern web applications. Each component follows accessibility best practices and supports dark mode out of the box."),
                        Large("Key Features:"),
                        List(
                            Li("Accessible by default"),
                            Li("Dark mode support"),
                            Li("Responsive design"),
                            Li("TypeScript ready")
                        ),
                        Muted("Get started today with our comprehensive documentation."),
                        cls="bg-card rounded-lg border p-6"
                    ),
                ),

                # Documentation example (removed invalid props table)
                Div(
                    Caption("DOCUMENTATION LAYOUT"),
                    Div(
                        H2("API Reference"),
                        Lead("Complete guide to the Typography component API"),

                        H3("Components"),
                        P("The typography system provides semantic components for different text styles:"),

                        List(
                            Li(InlineCode("Display"), " - Extra large headings for hero sections"),
                            Li(InlineCode("H1-H6"), " - Standard heading hierarchy"),
                            Li(InlineCode("Lead"), " - Introductory paragraph text"),
                            Li(InlineCode("Subtitle"), " - Secondary descriptive text"),
                            Li(InlineCode("Text"), " - Flexible body text with variants"),
                            Li(InlineCode("Muted"), " - De-emphasized text"),
                            Li(InlineCode("Small"), " - Fine print and captions"),
                        ),

                        cls="bg-card rounded-lg border p-6"
                    ),
                ),

                cls="grid grid-cols-1 lg:grid-cols-2 gap-8 mt-8"
            ),
        ),

        title="Typography"
    )


@rt("/tooltip")
def test_tooltip():
    return Page(
        H2("Keyboard Accessible Tooltips", cls="text-2xl font-semibold mb-4"),
        P("Tooltips support both hover and keyboard focus. Tab through the buttons below.", cls="text-muted-foreground mb-4"),

        Div(
            Tooltip(
                TooltipTrigger(
                    Button("Focus me 1", variant="outline")
                ),
                TooltipContent("Opens on focus or hover"),
            ),
            Tooltip(
                TooltipTrigger(
                    Button("Focus me 2", variant="outline")
                ),
                TooltipContent("Press Escape to close"),
            ),
            Tooltip(
                TooltipTrigger(
                    Button("Focus me 3", variant="outline")
                ),
                TooltipContent("Fully keyboard accessible"),
            ),
            cls="flex gap-4"
        ),

        H2("Position Variants", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Hover over the buttons to see tooltips with different positions.", cls="text-muted-foreground mb-4"),

        Div(
            Tooltip(
                TooltipTrigger(
                    Button("Hover me (top)", variant="outline")
                ),
                TooltipContent("This is a tooltip on top", side="top"),
            ),
            Tooltip(
                TooltipTrigger(
                    Button("Hover me (right)", variant="outline")
                ),
                TooltipContent("This is a tooltip on the right", side="right"),
            ),
            Tooltip(
                TooltipTrigger(
                    Button("Hover me (bottom)", variant="outline")
                ),
                TooltipContent("This is a tooltip on the bottom", side="bottom"),
            ),
            Tooltip(
                TooltipTrigger(
                    Button("Hover me (left)", variant="outline")
                ),
                TooltipContent("This is a tooltip on the left", side="left"),
            ),
            cls="flex gap-4 flex-wrap"
        ),

        H2("Tooltip Alignment", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Tooltips can be aligned to start, center, or end relative to the trigger.", cls="text-muted-foreground mb-4"),

        Div(
            Tooltip(
                TooltipTrigger(
                    Button("Top Start", variant="outline", cls="w-48")
                ),
                TooltipContent("⬅ Start", side="top", align="start", cls="w-28"),
            ),
            Tooltip(
                TooltipTrigger(
                    Button("Top Center", variant="outline", cls="w-48")
                ),
                TooltipContent("⬆ Center", side="top", align="center", cls="w-28"),
            ),
            Tooltip(
                TooltipTrigger(
                    Button("Top End", variant="outline", cls="w-48")
                ),
                TooltipContent("End ➡", side="top", align="end", cls="w-28"),
            ),
            cls="flex gap-4 flex-wrap"
        ),

        H2("Custom Delays", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Tooltips can have custom show and hide delays.", cls="text-muted-foreground mb-4"),

        Div(
            Tooltip(
                TooltipTrigger(
                    Button("Instant (0ms)", variant="outline"),
                    delay_duration=0
                ),
                TooltipContent("Shows immediately on hover"),
            ),
            Tooltip(
                TooltipTrigger(
                    Button("Default (700ms)", variant="outline")
                ),
                TooltipContent("Shows after 700ms delay"),
            ),
            Tooltip(
                TooltipTrigger(
                    Button("Slow (1500ms)", variant="outline"),
                    delay_duration=1500
                ),
                TooltipContent("Shows after 1500ms delay"),
            ),
            Tooltip(
                TooltipTrigger(
                    Button("With hide delay", variant="outline"),
                    delay_duration=500,
                    hide_delay=300
                ),
                TooltipContent("Hides with 300ms delay"),
            ),
            cls="flex gap-4 flex-wrap"
        ),

        H2("Tooltip on Icon Button", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Tooltips are commonly used on icon buttons to explain their purpose.", cls="text-muted-foreground mb-4"),

        Div(
            Tooltip(
                TooltipTrigger(
                    Button(
                        Icon("lucide:settings", width=20, height=20),
                        variant="outline",
                        size="icon"
                    )
                ),
                TooltipContent("Settings"),
            ),
            Tooltip(
                TooltipTrigger(
                    Button(
                        Icon("lucide:bell", width=20, height=20),
                        variant="outline",
                        size="icon"
                    )
                ),
                TooltipContent("Notifications"),
            ),
            Tooltip(
                TooltipTrigger(
                    Button(
                        Icon("lucide:user", width=20, height=20),
                        variant="outline",
                        size="icon"
                    )
                ),
                TooltipContent("Profile"),
            ),
            Tooltip(
                TooltipTrigger(
                    Button(
                        Icon("lucide:help-circle", width=20, height=20),
                        variant="outline",
                        size="icon"
                    )
                ),
                TooltipContent("Help and support", side="bottom"),
            ),
            cls="flex gap-4"
        ),

        H2("Tooltip with Rich Content", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Tooltips can contain multiple elements.", cls="text-muted-foreground mb-4"),

        Tooltip(
            TooltipTrigger(
                Button("Rich tooltip", variant="outline")
            ),
            TooltipContent(
                Div(
                    P("This tooltip has multiple lines", cls="font-semibold mb-1"),
                    P("And can contain additional content", cls="text-xs"),
                ),
                side="top",
                cls="max-w-xs"
            ),
        ),

        title="Tooltip"
    )


serve()
