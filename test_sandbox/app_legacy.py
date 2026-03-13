#!/usr/bin/env python3
# Import starhtml first, then override with our custom components
from starhtml import *
from starhtml.datastar import expr

# Import all registry components at once (this will override starhtml components)
from registry_loader import *
from src.starui.registry.components.toast import Toaster, toast, success_toast, error_toast, warning_toast, info_toast
from src.starui.registry.components.command import (
    Command, CommandDialog, CommandInput, CommandList, CommandEmpty,
    CommandGroup, CommandItem, CommandSeparator, CommandShortcut
)
from src.starui.registry.components.date_picker import (
    DatePicker, DatePickerWithPresets, DateRangePicker,
    DateTimePicker, DatePickerWithInput
)

styles = Link(rel="stylesheet", href="/static/css/starui.css", type="text/css")

app, rt = star_app(
    live=True,
    hdrs=(
        theme_script(use_data_theme=True),
        styles,
        iconify_script(),
    ),
    htmlkw=dict(lang="en", dir="ltr"),
    bodykw=dict(cls="min-h-screen bg-background text-foreground"),
)
app.register(position, clipboard)


@rt("/")
def index():
    return Div(
        # Initialize toast container first so signals are available
        Toaster(position="bottom-right"),
        # Theme toggle in top-right corner
        Div(ThemeToggle(), cls="absolute top-4 right-4"),
        # Main content container
        Div(
            H1("StarUI Component Test", cls="mb-8 text-4xl font-bold"),
            # Button variants
            Div(
                H2("Buttons", cls="mb-4 text-2xl font-semibold"),
                Div(
                    Button("Default"),
                    Button("Destructive", variant="destructive"),
                    Button("Outline", variant="outline"),
                    Button("Secondary", variant="secondary"),
                    Button("Ghost", variant="ghost"),
                    Button("Link", variant="link"),
                    Button(Icon("lucide:settings"), variant="secondary", size="icon"),
                    Button("Disabled", disabled=True),
                    cls="mb-8 flex flex-wrap gap-2",
                ),
            ),
            # Badge variants
            Div(
                H2("Badges", cls="mb-4 text-2xl font-semibold"),
                Div(
                    Badge("Default"),
                    Badge("Secondary", variant="secondary"),
                    Badge("Destructive", variant="destructive"),
                    Badge("Outline", variant="outline"),
                    Badge("Clickable", ds_on_click("alert('Badge clicked!')")),
                    cls="mb-8 flex flex-wrap gap-2",
                ),
            ),
            # Input types
            Div(
                H2("Inputs", cls="mb-4 text-2xl font-semibold"),
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
                            id="password-input", type="password", placeholder="••••••••"
                        ),
                        cls="space-y-2",
                    ),
                    Div(
                        Label("Disabled Input", for_="disabled-input"),
                        Input(
                            id="disabled-input",
                            placeholder="Cannot edit",
                            disabled=True,
                        ),
                        cls="space-y-2",
                    ),
                    cls="mb-8 grid grid-cols-1 gap-4 md:grid-cols-2",
                ),
            ),
            # Card example
            Div(
                H2("Card", cls="mb-4 text-2xl font-semibold"),
                Card(
                    CardHeader(
                        CardTitle("Card Title"),
                        CardDescription(
                            "This is a card description with some example text."
                        ),
                    ),
                    CardContent(
                        P("Card content goes here. You can add any elements you want."),
                        Div(Input(placeholder="Card input field"), cls="mt-4"),
                    ),
                    CardFooter(
                        Button("Cancel", variant="outline"),
                        Button("Save"),
                        cls="flex gap-2",
                    ),
                    cls="mb-8 max-w-md",
                ),
            ),
            # Alert variants
            Div(
                H2("Alerts", cls="mb-4 text-2xl font-semibold"),
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
                    cls="mb-8 space-y-4",
                ),
            ),
            # Breadcrumb
            Div(
                H2("Breadcrumb", cls="mb-4 text-2xl font-semibold"),
                Breadcrumb(
                    BreadcrumbList(
                        BreadcrumbItem(BreadcrumbLink("Home", href="/")),
                        BreadcrumbSeparator(),
                        BreadcrumbItem(
                            BreadcrumbLink("Components", href="/components")
                        ),
                        BreadcrumbSeparator(),
                        BreadcrumbItem(BreadcrumbPage("Current Page")),
                    )
                ),
                cls="mb-8",
            ),
            # Tabs example - Default variant (boxed style)
            Div(
                H2("Tabs - Default Variant", cls="mb-4 text-2xl font-semibold"),
                Tabs(
                    TabsList(
                        TabsTrigger("Preview", id="preview"),
                        TabsTrigger("Code", id="code"),
                        TabsTrigger("Settings", id="settings"),
                    ),
                    TabsContent(
                        Div(
                            H3("Preview Content", cls="mb-2 text-lg font-semibold"),
                            P(
                                "This is the preview tab content with the default boxed style."
                            ),
                            Button(
                                "Action in Preview", variant="secondary", cls="mt-4"
                            ),
                        ),
                        id="preview",
                    ),
                    TabsContent(
                        Div(
                            H3("Code Content", cls="mb-2 text-lg font-semibold"),
                            Pre(
                                Code(
                                    "# Example code\ndef hello_world():\n    print('Hello, World!')",
                                    cls="block rounded bg-muted p-4",
                                )
                            ),
                        ),
                        id="code",
                    ),
                    TabsContent(
                        Div(
                            H3("Settings Content", cls="mb-2 text-lg font-semibold"),
                            P("Configure your preferences here."),
                            Div(
                                Label("Enable notifications", for_="notifications"),
                                Input(type="checkbox", id="notifications", cls="ml-2"),
                                cls="mt-4 flex items-center gap-2",
                            ),
                        ),
                        id="settings",
                    ),
                    default_value="preview",
                    variant="default",
                    cls="mb-8",
                ),
            ),
            # Tabs example - Plain variant (text style)
            Div(
                H2("Tabs - Plain Variant", cls="mb-4 text-2xl font-semibold"),
                Tabs(
                    TabsList(
                        TabsTrigger("Account", id="account"),
                        TabsTrigger("Password", id="password"),
                        TabsTrigger("Team", id="team"),
                        TabsTrigger("Billing", id="billing"),
                    ),
                    TabsContent(
                        Div(
                            H3("Account Settings", cls="mb-2 text-lg font-semibold"),
                            P("Manage your account settings and preferences."),
                            Div(
                                Label("Username", for_="username"),
                                Input(
                                    id="username",
                                    placeholder="Enter username",
                                    cls="max-w-sm",
                                ),
                                cls="mt-4 space-y-2",
                            ),
                        ),
                        id="account",
                    ),
                    TabsContent(
                        Div(
                            H3("Password & Security", cls="mb-2 text-lg font-semibold"),
                            P("Update your password and security settings."),
                            Button("Change Password", variant="outline", cls="mt-4"),
                        ),
                        id="password",
                    ),
                    TabsContent(
                        Div(
                            H3("Team Members", cls="mb-2 text-lg font-semibold"),
                            P("Manage your team and collaborate with others."),
                        ),
                        id="team",
                    ),
                    TabsContent(
                        Div(
                            H3("Billing Information", cls="mb-2 text-lg font-semibold"),
                            P("View and manage your subscription and payment methods."),
                        ),
                        id="billing",
                    ),
                    default_value="account",
                    variant="plain",
                    cls="mb-8",
                ),
            ),
            # Sheet example
            Div(
                H2("Sheet (Modal Drawer)", cls="mb-4 text-2xl font-semibold"),
                Sheet(
                    SheetTrigger("Open Sheet", signal="demo_sheet"),
                    SheetContent(
                        SheetHeader(
                            SheetTitle("Sheet Title", signal="demo_sheet"),
                            SheetDescription(
                                "This is a sheet description.", signal="demo_sheet"
                            ),
                        ),
                        Div(
                            P(
                                "Sheet content goes here. Press ESC or click outside to close."
                            ),
                            Input(placeholder="Type something..."),
                            cls="space-y-4 p-6",
                        ),
                        SheetFooter(
                            Button(
                                "Cancel",
                                ds_on_click("$demo_sheet_open = false"),
                                variant="outline",
                            ),
                            Button("Save Changes"),
                        ),
                        signal="demo_sheet",
                        side="right",
                        size="md",
                    ),
                    signal="demo_sheet",
                    side="right",
                    size="md",
                    modal=True,
                    default_open=False,
                ),
                cls="mb-8",
            ),
            # Dialog example
            Div(
                H2("Dialog (Modal)", cls="mb-4 text-2xl font-semibold"),
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
                cls="mb-8",
            ),
            # Dialog with different size and content
            Div(
                H2("Dialog (Small Size)", cls="mb-4 text-2xl font-semibold"),
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
                cls="mb-8",
            ),
            # Alert Dialog examples
            Div(
                H2("Alert Dialog", cls="mb-4 text-2xl font-semibold"),
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
                        signal="basic_alert",
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
                        signal="destructive_alert",
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
                        signal="custom_alert",
                    ),
                    cls="flex flex-wrap gap-4",
                ),
                cls="mb-8",
            ),
            # Radio Group examples
            Div(
                H2("Radio Groups", cls="mb-4 text-2xl font-semibold"),
                Div(
                    RadioGroupWithLabel(
                        "Select your plan",
                        options=[
                            {"value": "free", "label": "Free - $0/month"},
                            {"value": "pro", "label": "Pro - $10/month"},
                            {"value": "enterprise", "label": "Enterprise - Custom"},
                        ],
                        value="free",
                        signal="plan",
                        helper_text="Choose the plan that best fits your needs",
                    ),
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
                    Div(
                        P(
                            "Simple radio group (fully auto-managed):",
                            cls="mb-2 text-sm font-medium",
                        ),
                        RadioGroup(
                            RadioGroupItem("small", "Small"),
                            RadioGroupItem("medium", "Medium"),
                            RadioGroupItem("large", "Large"),
                            value="medium",
                        ),
                        cls="rounded-lg border p-4",
                    ),
                    Div(
                        P(
                            "Custom styled radio group (blue indicator):",
                            cls="mb-2 text-sm font-medium",
                        ),
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
                            value="option2",
                        ),
                        cls="rounded-lg border p-4",
                    ),
                    cls="mb-8 space-y-6",
                ),
            ),
            # Switch examples
            Div(
                H2("Switches", cls="mb-4 text-2xl font-semibold"),
                Div(
                    SwitchWithLabel(
                        "Enable notifications",
                        signal="switch_notifications",
                        checked=True,
                        helper_text="Receive email notifications about updates",
                    ),
                    SwitchWithLabel(
                        "Marketing emails",
                        signal="switch_marketing",
                        helper_text="Get promotional emails and special offers",
                    ),
                    SwitchWithLabel(
                        "Two-factor authentication",
                        signal="switch_2fa",
                        required=True,
                        helper_text="Enhanced security for your account",
                    ),
                    SwitchWithLabel(
                        "Disabled option",
                        disabled=True,
                        helper_text="This feature is not available in your plan",
                    ),
                    SwitchWithLabel(
                        "Error state example",
                        signal="switch_error",
                        error_text="This setting requires admin approval",
                    ),
                    # Simple switches without labels
                    Div(
                        P("Simple switches:", cls="mb-2 text-sm font-medium"),
                        Div(
                            Switch(signal="simple1", checked=True),
                            Switch(signal="simple2"),
                            Switch(disabled=True),
                            cls="flex gap-4",
                        ),
                        cls="rounded-lg border p-4",
                    ),
                    cls="mb-8 space-y-4",
                ),
            ),
            # Textarea examples
            Div(
                H2("Textareas", cls="mb-4 text-2xl font-semibold"),
                Div(
                    # Basic textarea
                    TextareaWithLabel(
                        "Description",
                        placeholder="Enter your description here...",
                        signal="description",
                        helper_text="Provide a detailed description",
                    ),
                    # Textarea with error
                    TextareaWithLabel(
                        "Bio",
                        placeholder="Tell us about yourself",
                        signal="bio",
                        required=True,
                        error_text="Bio is required and must be at least 50 characters",
                    ),
                    # Disabled textarea
                    TextareaWithLabel(
                        "Notes",
                        value="This field is currently disabled",
                        disabled=True,
                        helper_text="This field will be enabled after verification",
                    ),
                    # Textarea with fixed rows
                    TextareaWithLabel(
                        "Comments",
                        placeholder="Share your thoughts...",
                        signal="comments",
                        rows=5,
                        helper_text="Fixed height with 5 rows",
                    ),
                    # Simple textarea without label
                    Div(
                        P("Simple textarea:", cls="mb-2 text-sm font-medium"),
                        Textarea(
                            placeholder="Type something...",
                            signal="simple_textarea",
                            resize="vertical",
                        ),
                        cls="rounded-lg border p-4",
                    ),
                    cls="mb-8 space-y-4",
                ),
                # Reactive textarea test
                Div(
                    H3("Reactive Textarea Test", cls="mb-4 text-lg font-semibold"),
                    Div(
                        Textarea(
                            placeholder="Type here to test reactive binding...",
                            signal="reactiveTest",
                            rows=3,
                            cls="mb-4"
                        ),
                        Div(
                            P("Live Preview:", cls="mb-2 font-medium"),
                            P(ds_text("$reactiveTest || '(nothing typed yet)'"), cls="min-h-[3rem] rounded border bg-gray-50 p-3 dark:bg-gray-900"),
                            cls="mb-3"
                        ),
                        P(
                            "Characters: ",
                            ds_text("$reactiveTest.length || 0"),
                            cls="text-sm text-muted-foreground"
                        ),
                        ds_signals(reactiveTest=expr("")),
                        cls="rounded-lg border bg-background p-4"
                    ),
                    cls="mb-8"
                ),
            ),
            # Select examples
            Div(
                H2("Select", cls="mb-4 text-2xl font-semibold"),
                Div(
                    # Basic select
                    SelectWithLabel(
                        "Country",
                        options=["United States", "Canada", "Mexico", "United Kingdom", "France", "Germany"],
                        placeholder="Choose a country",
                        signal="country",
                        helper_text="Select your country of residence",
                    ),
                    # Select with value/label tuples
                    SelectWithLabel(
                        "Language",
                        options=[
                            ("en", "English"),
                            ("es", "Spanish"),
                            ("fr", "French"),
                            ("de", "German"),
                            ("jp", "Japanese"),
                        ],
                        value="en",
                        signal="language",
                        helper_text="Choose your preferred language",
                    ),
                    # Select with groups
                    SelectWithLabel(
                        "Framework",
                        options=[
                            {"group": "Frontend", "items": ["React", "Vue", "Angular", "Svelte"]},
                            {"group": "Backend", "items": [("django", "Django"), ("fastapi", "FastAPI"), ("flask", "Flask")]},
                            {"group": "Full Stack", "items": ["Next.js", "Nuxt", "SvelteKit"]},
                        ],
                        placeholder="Select a framework",
                        signal="framework",
                        required=True,
                    ),
                    # Select with error state
                    SelectWithLabel(
                        "Department",
                        options=["Engineering", "Design", "Marketing", "Sales", "Support"],
                        signal="department",
                        error_text="Please select a valid department",
                        required=True,
                    ),
                    # Disabled select
                    SelectWithLabel(
                        "Plan",
                        options=["Free", "Pro", "Enterprise"],
                        value="Free",
                        disabled=True,
                        helper_text="Upgrade your account to change plans",
                    ),
                    # Simple select without label
                    Div(
                        P("Simple select:", cls="mb-2 text-sm font-medium"),
                        Select(
                            SelectTrigger(
                                SelectValue(placeholder="Pick an option", signal="simple_select"),
                                signal="simple_select",
                            ),
                            SelectContent(
                                SelectItem("Option 1", signal="simple_select"),
                                SelectItem("Option 2", signal="simple_select"),
                                SelectItem("Option 3", signal="simple_select"),
                                SelectItem("Disabled", disabled=True, signal="simple_select"),
                                signal="simple_select",
                            ),
                            signal="simple_select",
                        ),
                        cls="rounded-lg border p-4",
                    ),
                    cls="mb-8 space-y-4",
                ),
            ),
            # Popover examples
            Div(
                H2("Popovers", cls="mb-4 text-2xl font-semibold"),
                Div(
                    # Basic popover
                    Popover(
                        PopoverTrigger("Open Popover"),
                        PopoverContent(
                            Div(
                                H3("About this feature", cls="mb-2 font-semibold"),
                                P("This is a popover component that displays rich content in a floating panel.", cls="mb-3 text-sm text-muted-foreground"),
                                PopoverClose("✕"),
                            ),
                        ),
                    ),
                    # Popover with different positioning
                    Popover(
                        PopoverTrigger("Top Popover", variant="outline"),
                        PopoverContent(
                            Div(
                                H3("Top positioned", cls="mb-2 font-semibold"),
                                P("This popover appears above the trigger.", cls="text-sm"),
                            ),
                            side="top",
                        ),
                    ),
                    # Popover with form
                    Popover(
                        PopoverTrigger("Settings", variant="secondary"),
                        PopoverContent(
                            Div(
                                H3("Quick Settings", cls="mb-3 font-semibold"),
                                Div(
                                    Label("Theme", cls="text-sm font-medium"),
                                    Button("Toggle", variant="outline", size="sm"),
                                    cls="mb-2 flex items-center justify-between",
                                ),
                                Div(
                                    Label("Notifications", cls="text-sm font-medium"),
                                    Switch(signal="notif_setting"),
                                    cls="flex items-center justify-between",
                                ),
                                PopoverClose("Done", variant="ghost"),
                            ),
                        ),
                    ),
                    cls="mb-8 flex flex-wrap gap-4",
                ),
            ),
            # Dropdown Menu examples
            Div(
                H2("Dropdown Menus", cls="mb-4 text-2xl font-semibold"),
                Div(
                    # Basic dropdown
                    DropdownMenu(
                        DropdownMenuTrigger("Open Menu"),
                        DropdownMenuContent(
                            DropdownMenuLabel("My Account"),
                            DropdownMenuSeparator(),
                            DropdownMenuItem("Profile", DropdownMenuShortcut("⇧⌘P")),
                            DropdownMenuItem("Billing", DropdownMenuShortcut("⌘B")),
                            DropdownMenuItem("Settings", DropdownMenuShortcut("⌘S")),
                            DropdownMenuSeparator(),
                            DropdownMenuItem("Log out", DropdownMenuShortcut("⇧⌘Q"), variant="destructive"),
                        ),
                    ),
                    # Dropdown with checkboxes
                    DropdownMenu(
                        DropdownMenuTrigger("Options", variant="secondary"),
                        DropdownMenuContent(
                            DropdownMenuLabel("Appearance"),
                            DropdownMenuSeparator(),
                            DropdownMenuCheckboxItem("Status Bar", signal="statusBar"),
                            DropdownMenuCheckboxItem("Activity Bar", signal="activityBar", disabled=True),
                            DropdownMenuCheckboxItem("Panel", signal="panel"),
                        ),
                        signal="checkbox_dropdown",
                    ),
                    # Dropdown with radio items
                    DropdownMenu(
                        DropdownMenuTrigger("Select Position", variant="outline"),
                        DropdownMenuContent(
                            DropdownMenuLabel("Position"),
                            DropdownMenuSeparator(),
                            DropdownMenuRadioGroup(
                                DropdownMenuRadioItem("Top", value="top", signal="position"),
                                DropdownMenuRadioItem("Bottom", value="bottom", signal="position"),
                                DropdownMenuRadioItem("Right", value="right", signal="position"),
                                signal="position",
                            ),
                        ),
                        signal="radio_dropdown",
                    ),
                    ds_signals({
                        "statusBar": True,
                        "activityBar": False,
                        "panel": False,
                        "position": expr("bottom"),
                    }),
                    cls="mb-8 flex flex-wrap gap-4",
                ),
            ),
            # HoverCard examples
            Div(
                H2("Hover Cards", cls="mb-4 text-2xl font-semibold"),
                Div(
                    # Basic hover card
                    HoverCard(
                        HoverCardTrigger(
                            Span("@username", cls="cursor-pointer text-blue-600 underline"),
                            signal="user_hover",
                        ),
                        HoverCardContent(
                            Div(
                                Div(
                                    Div("👤", cls="mb-3 flex h-12 w-12 items-center justify-center rounded-full bg-muted text-2xl"),
                                    H3("John Doe", cls="mb-1 font-semibold"),
                                    P("@username", cls="mb-2 text-sm text-muted-foreground"),
                                    P("Full-stack developer passionate about building great user experiences.", cls="text-sm"),
                                    cls="text-center",
                                ),
                            ),
                            signal="user_hover",
                        ),
                        signal="user_hover",
                    ),
                    # Hover card with different positioning
                    HoverCard(
                        HoverCardTrigger(
                            Button("Hover for info", variant="outline"),
                            signal="info_hover",
                        ),
                        HoverCardContent(
                            Div(
                                H3("Quick Info", cls="mb-2 font-semibold"),
                                P("This hover card appears when you hover over the trigger element.", cls="mb-2 text-sm text-muted-foreground"),
                                P("It stays open while you're hovering over either the trigger or the content.", cls="text-sm"),
                            ),
                            signal="info_hover",
                            side="top",
                        ),
                        signal="info_hover",
                    ),
                    # Product hover card
                    HoverCard(
                        HoverCardTrigger(
                            Badge("Product Info", variant="secondary"),
                            signal="product_hover",
                        ),
                        HoverCardContent(
                            Div(
                                Div(
                                    H3("StarUI Components", cls="mb-2 font-semibold"),
                                    Badge("v1.0.0", variant="outline", cls="mb-2"),
                                    P("A modern component library built with StarHTML and Datastar for reactive Python web apps.", cls="mb-3 text-sm text-muted-foreground"),
                                    Div(
                                        Badge("Python"),
                                        Badge("StarHTML", variant="secondary"),
                                        Badge("Datastar", variant="outline"),
                                        cls="flex gap-1",
                                    ),
                                ),
                            ),
                            signal="product_hover",
                            side="left",
                        ),
                        signal="product_hover",
                    ),
                    cls="mb-8 flex flex-wrap gap-4",
                ),
            ),
            # Tooltip examples
            Div(
                H2("Tooltips", cls="mb-4 text-2xl font-semibold"),
                TooltipProvider(
                    # Better spacing to prevent unwanted flipping
                    Div(
                        P("Basic directional tooltips:", cls="mb-4 text-sm text-muted-foreground"),
                        # Top tooltip centered alone
                        Div(
                            Tooltip(
                                TooltipTrigger(
                                    Button("Top", variant="outline"),
                                ),
                                TooltipContent(
                                    "This tooltip appears on top",
                                    side="top",
                                ),
                            ),
                            cls="mb-6 flex justify-center"
                        ),
                        # Left and Right with ample spacing
                        Div(
                            Tooltip(
                                TooltipTrigger(
                                    Button("Left", variant="outline"),
                                ),
                                TooltipContent(
                                    "This tooltip appears on left",
                                    side="left",
                                ),
                            ),
                            Div(cls="w-32"),  # Spacer to prevent collision
                            Tooltip(
                                TooltipTrigger(
                                    Button("Right", variant="outline"),
                                ),
                                TooltipContent(
                                    "This tooltip appears on right",
                                    side="right",
                                ),
                            ),
                            cls="mb-6 flex items-center justify-center gap-16"
                        ),
                        # Bottom tooltip centered alone
                        Div(
                            Tooltip(
                                TooltipTrigger(
                                    Button("Bottom", variant="outline"),
                                ),
                                TooltipContent(
                                    "This tooltip appears on bottom",
                                    side="bottom",
                                ),
                            ),
                            cls="mb-6 flex justify-center"
                        ),
                    ),
                Div(
                    P("Tooltip alignments:", cls="mb-2 text-sm text-muted-foreground"),
                    Div(
                        Tooltip(
                            TooltipTrigger(
                                Button("Start", variant="secondary", size="sm"),
                            ),
                            TooltipContent(
                                "Aligned to start of trigger",
                                side="bottom",
                                align="start",
                            ),
                        ),
                        Tooltip(
                            TooltipTrigger(
                                Button("Center", variant="secondary", size="sm"),
                            ),
                            TooltipContent(
                                "Aligned to center of trigger",
                                side="bottom",
                                align="center",
                            ),
                        ),
                        Tooltip(
                            TooltipTrigger(
                                Button("End", variant="secondary", size="sm"),
                            ),
                            TooltipContent(
                                "Aligned to end of trigger",
                                side="bottom",
                                align="end",
                            ),
                        ),
                        cls="mb-6 flex gap-2",
                    ),
                ),
                Div(
                    P("Custom delay and focus support:", cls="mb-2 text-sm text-muted-foreground"),
                    Div(
                        Tooltip(
                            TooltipTrigger(
                                Button("Fast tooltip", variant="ghost"),
                                delay_duration=100,
                            ),
                            TooltipContent(
                                "This appears quickly (100ms delay)",
                                side="top",
                            ),
                        ),
                        Tooltip(
                            TooltipTrigger(
                                Input(placeholder="Focus me for tooltip", cls="w-48"),
                                delay_duration=500,
                            ),
                            TooltipContent(
                                "Tooltips work on focus too!",
                                side="bottom",
                            ),
                        ),
                        cls="mb-8 flex gap-4",
                    ),
                ),
            ),
            ),
            # Checkbox examples
            Div(
                H2("Checkboxes", cls="mb-4 text-2xl font-semibold"),
                Div(
                    CheckboxWithLabel(
                        "Accept terms and conditions", signal="terms", required=True
                    ),
                    CheckboxWithLabel(
                        "Subscribe to newsletter",
                        signal="newsletter",
                        helper_text="Get weekly updates about new features",
                    ),
                    CheckboxWithLabel(
                        "Enable notifications", signal="notifications", checked=True
                    ),
                    CheckboxWithLabel(
                        "Disabled option",
                        disabled=True,
                        helper_text="This option is currently unavailable",
                    ),
                    CheckboxWithLabel(
                        "Error state example",
                        signal="error_checkbox",
                        error_text="This field is required",
                    ),
                    # Custom styled checkbox with blue background
                    Div(
                        CheckboxWithLabel(
                            "Custom blue checkbox",
                            signal="blue_checkbox",
                            helper_text="With custom blue styling when checked",
                            checkbox_cls="checked:!border-blue-600 checked:!bg-blue-600 dark:checked:!border-blue-700 dark:checked:!bg-blue-700",
                            indicator_cls="!text-white",
                        ),
                        cls="rounded-lg border p-4",
                    ),
                    cls="mb-8 space-y-4",
                ),
            ),
            # Toggle examples
            Div(
                H2("Toggles", cls="mb-4 text-2xl font-semibold"),
                Div(
                    # Basic toggles
                    Div(
                        P("Basic toggles:", cls="mb-2 text-sm font-medium"),
                        Div(
                            Toggle(Icon("lucide:bold"), signal="toggle_bold"),
                            Toggle(Icon("lucide:italic"), signal="toggle_italic", pressed=True),
                            Toggle(Icon("lucide:underline"), signal="toggle_underline"),
                            Toggle(Icon("lucide:strikethrough"), disabled=True),
                            cls="flex gap-1",
                        ),
                        cls="mb-4",
                    ),
                    # Outline variant toggles
                    Div(
                        P("Outline variant:", cls="mb-2 text-sm font-medium"),
                        Div(
                            Toggle(Icon("lucide:align-left"), variant="outline", signal="align_left"),
                            Toggle(Icon("lucide:align-center"), variant="outline", signal="align_center", pressed=True),
                            Toggle(Icon("lucide:align-right"), variant="outline", signal="align_right"),
                            Toggle(Icon("lucide:align-justify"), variant="outline", signal="align_justify"),
                            cls="flex gap-1",
                        ),
                        cls="mb-4",
                    ),
                    # Different sizes
                    Div(
                        P("Different sizes:", cls="mb-2 text-sm font-medium"),
                        Div(
                            Toggle("Small", size="sm", variant="outline", signal="size_sm"),
                            Toggle("Default", size="default", variant="outline", signal="size_default"),
                            Toggle("Large", size="lg", variant="outline", signal="size_lg"),
                            cls="flex items-center gap-2",
                        ),
                        cls="mb-4",
                    ),
                    # Toggle with text
                    Div(
                        P("Toggle with text:", cls="mb-2 text-sm font-medium"),
                        Div(
                            Toggle(
                                Icon("lucide:wifi"),
                                Span("WiFi", cls="ml-1"),
                                variant="outline",
                                signal="wifi_toggle",
                            ),
                            Toggle(
                                Icon("lucide:bluetooth"),
                                Span("Bluetooth", cls="ml-1"),
                                variant="outline",
                                signal="bluetooth_toggle",
                                pressed=True,
                            ),
                            Toggle(
                                Icon("lucide:plane"),
                                Span("Airplane Mode", cls="ml-1"),
                                variant="outline",
                                signal="airplane_toggle",
                            ),
                            cls="flex gap-2",
                        ),
                        cls="mb-4",
                    ),
                    cls="mb-8 space-y-4",
                ),
            ),
            # Toggle Group examples
            Div(
                H2("Toggle Groups", cls="mb-4 text-2xl font-semibold"),
                Div(
                    # Single selection toggle group
                    Div(
                        P("Text formatting (single selection):", cls="mb-2 text-sm font-medium"),
                        SingleToggleGroup(
                            ("bold", Icon("lucide:bold")),
                            ("italic", Icon("lucide:italic")),
                            ("underline", Icon("lucide:underline")),
                            signal="text_format",
                            variant="outline",
                        ),
                        cls="mb-4",
                    ),
                    # Multiple selection toggle group
                    Div(
                        P("Text options (multiple selection):", cls="mb-2 text-sm font-medium"),
                        MultipleToggleGroup(
                            ("bold", Icon("lucide:bold")),
                            ("italic", Icon("lucide:italic")),
                            ("underline", Icon("lucide:underline")),
                            ("strikethrough", Icon("lucide:strikethrough")),
                            signal="text_options",
                            variant="outline",
                        ),
                        cls="mb-4",
                    ),
                    # Alignment toggle group
                    Div(
                        P("Text alignment:", cls="mb-2 text-sm font-medium"),
                        SingleToggleGroup(
                            ("left", Icon("lucide:align-left")),
                            ("center", Icon("lucide:align-center")),
                            ("right", Icon("lucide:align-right")),
                            ("justify", Icon("lucide:align-justify")),
                            signal="alignment",
                            variant="default",
                        ),
                        cls="mb-4",
                    ),
                    # Size toggle group
                    Div(
                        P("Size selection:", cls="mb-2 text-sm font-medium"),
                        SingleToggleGroup(
                            ("sm", "Small"),
                            ("md", "Medium"),
                            ("lg", "Large"),
                            ("xl", "Extra Large"),
                            signal="size_selection",
                            variant="outline",
                            size="lg",
                        ),
                        cls="mb-4",
                    ),
                    # View mode toggle group
                    Div(
                        P("View mode:", cls="mb-2 text-sm font-medium"),
                        SingleToggleGroup(
                            ("list", Div(Icon("lucide:list"), Span("List", cls="ml-1"))),
                            ("grid", Div(Icon("lucide:layout-grid"), Span("Grid", cls="ml-1"))),
                            ("gallery", Div(Icon("lucide:image"), Span("Gallery", cls="ml-1"))),
                            signal="view_mode",
                            variant="outline",
                        ),
                        cls="mb-4",
                    ),
                    # Disabled toggle group
                    Div(
                        P("Disabled group:", cls="mb-2 text-sm font-medium"),
                        SingleToggleGroup(
                            ("option1", "Option 1"),
                            ("option2", "Option 2"),
                            ("option3", "Option 3"),
                            signal="disabled_group",
                            variant="outline",
                            disabled=True,
                        ),
                        cls="mb-4",
                    ),
                    cls="mb-8 space-y-4",
                ),
            ),
            # Accordion examples
            Div(
                H2("Accordion", cls="mb-4 text-2xl font-semibold"),
                Div(
                    # Single accordion with collapsible
                    Div(
                        P(
                            "Single selection (collapsible):",
                            cls="mb-2 text-sm font-medium",
                        ),
                        Accordion(
                            AccordionItem(
                                AccordionTrigger("Is it accessible?", value="item-1"),
                                AccordionContent(
                                    "Yes. It adheres to the WAI-ARIA design pattern.",
                                    value="item-1",
                                ),
                                value="item-1",
                            ),
                            AccordionItem(
                                AccordionTrigger("Is it styled?", value="item-2"),
                                AccordionContent(
                                    "Yes. It comes with default styles that matches the other components' aesthetic.",
                                    value="item-2",
                                ),
                                value="item-2",
                            ),
                            AccordionItem(
                                AccordionTrigger("Is it animated?", value="item-3"),
                                AccordionContent(
                                    "Yes. It's animated by default, but you can disable it if you prefer.",
                                    value="item-3",
                                ),
                                value="item-3",
                            ),
                            type="single",
                            collapsible=True,
                            default_value="item-1",
                            signal="accordion_single",
                            cls="w-full",
                        ),
                        cls="mb-6",
                    ),
                    # Multiple selection accordion
                    Div(
                        P("Multiple selection:", cls="mb-2 text-sm font-medium"),
                        Accordion(
                            AccordionItem(
                                AccordionTrigger(
                                    "Getting Started", value="getting-started"
                                ),
                                AccordionContent(
                                    Div(
                                        P(
                                            "To get started with our product, follow these steps:",
                                            cls="mb-2",
                                        ),
                                        Ul(
                                            Li("1. Sign up for an account"),
                                            Li("2. Complete your profile"),
                                            Li("3. Explore the dashboard"),
                                            cls="list-disc pl-6",
                                        ),
                                    ),
                                    value="getting-started",
                                ),
                                value="getting-started",
                            ),
                            AccordionItem(
                                AccordionTrigger("Features", value="features"),
                                AccordionContent(
                                    Div(
                                        P(
                                            "Our platform offers these key features:",
                                            cls="mb-2",
                                        ),
                                        Ul(
                                            Li("Real-time collaboration"),
                                            Li("Advanced analytics"),
                                            Li("Custom integrations"),
                                            Li("24/7 support"),
                                            cls="list-disc pl-6",
                                        ),
                                    ),
                                    value="features",
                                ),
                                value="features",
                            ),
                            AccordionItem(
                                AccordionTrigger("Pricing", value="pricing"),
                                AccordionContent(
                                    Div(
                                        P(
                                            "We offer flexible pricing plans:",
                                            cls="mb-2",
                                        ),
                                        Div(
                                            Div(
                                                "Free: $0/month - Basic features",
                                                cls="py-1",
                                            ),
                                            Div(
                                                "Pro: $29/month - Advanced features",
                                                cls="py-1",
                                            ),
                                            Div(
                                                "Enterprise: Custom - Full access",
                                                cls="py-1",
                                            ),
                                        ),
                                    ),
                                    value="pricing",
                                ),
                                value="pricing",
                            ),
                            type="multiple",
                            default_value=["getting-started"],
                            signal="accordion_multiple",
                            cls="w-full",
                        ),
                        cls="mb-6",
                    ),
                    cls="mb-8 space-y-4",
                ),
            ),
            # Avatar examples
            Div(
                H2("Avatars", cls="mb-4 text-2xl font-semibold"),
                Div(
                    # Basic Avatar with image
                    Div(
                        H3("Basic Avatar", cls="mb-2 text-lg font-medium"),
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
                            cls="flex items-center gap-4"
                        ),
                        cls="mb-6",
                    ),
                    # Different sizes (composition example)
                    Div(
                        H3("Avatar Sizes", cls="mb-2 text-lg font-medium"),
                        P("Use size classes to customize:", cls="mb-2 text-sm text-muted-foreground"),
                        Div(
                            Avatar(AvatarFallback("XS"), cls="size-6"),
                            Avatar(AvatarFallback("SM"), cls="size-8"),
                            Avatar(AvatarFallback("MD")),  # default size-10
                            Avatar(AvatarFallback("LG"), cls="size-12"),
                            Avatar(AvatarFallback("XL"), cls="size-16"),
                            Avatar(AvatarFallback("2X"), cls="size-20"),
                            cls="flex items-center gap-4"
                        ),
                        cls="mb-6",
                    ),
                    # Avatar with automatic fallback
                    Div(
                        H3("Automatic Fallback", cls="mb-2 text-lg font-medium"),
                        P("The second avatar will show fallback as the image URL is invalid:", cls="mb-2 text-sm text-muted-foreground"),
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
                            cls="flex items-center gap-4"
                        ),
                        cls="mb-6",
                    ),
                    # Avatar Group (composition example)
                    Div(
                        H3("Avatar Group", cls="mb-2 text-lg font-medium"),
                        P("Compose avatars with overlapping styles:", cls="mb-2 text-sm text-muted-foreground"),
                        Div(
                            Div(
                                Avatar(AvatarFallback("JD")),
                                Avatar(AvatarFallback("AS")),
                                Avatar(AvatarFallback("PQ")),
                                Avatar(AvatarFallback("+2", cls="text-xs font-medium")),
                                cls="flex -space-x-2 [&>*[data-slot=avatar]]:ring-2 [&>*[data-slot=avatar]]:ring-background"
                            ),
                            cls="mb-2"
                        ),
                        cls="mb-6",
                    ),
                    # Avatar with Badge (composition example)
                    Div(
                        H3("Avatar with Badge", cls="mb-2 text-lg font-medium"),
                        P("Compose with absolute positioning:", cls="mb-2 text-sm text-muted-foreground"),
                        Div(
                            # Green status badge
                            Div(
                                Avatar(AvatarFallback("JD")),
                                Span(cls="absolute right-0 bottom-0 size-3 rounded-full bg-green-500 ring-2 ring-background"),
                                cls="relative inline-block"
                            ),
                            # Red status badge
                            Div(
                                Avatar(AvatarFallback("AS")),
                                Span(cls="absolute right-0 bottom-0 size-3 rounded-full bg-red-500 ring-2 ring-background"),
                                cls="relative inline-block"
                            ),
                            # Badge with count
                            Div(
                                Avatar(AvatarFallback("MN")),
                                Span("5", cls="absolute right-0 bottom-0 flex size-4 items-center justify-center rounded-full bg-red-500 text-[8px] font-bold text-white ring-2 ring-background"),
                                cls="relative inline-block"
                            ),
                            cls="flex items-center gap-4"
                        ),
                        cls="mb-6",
                    ),
                    # Avatar from Initials (composition example)
                    Div(
                        H3("Avatar from Initials", cls="mb-2 text-lg font-medium"),
                        P("Use colored backgrounds for initials:", cls="mb-2 text-sm text-muted-foreground"),
                        Div(
                            Avatar(AvatarFallback("JD", cls="bg-red-600 font-semibold text-white dark:bg-red-500")),
                            Avatar(AvatarFallback("AS", cls="bg-blue-600 font-semibold text-white dark:bg-blue-500")),
                            Avatar(AvatarFallback("PQ", cls="bg-green-600 font-semibold text-white dark:bg-green-500")),
                            Avatar(AvatarFallback("MN", cls="bg-purple-600 font-semibold text-white dark:bg-purple-500")),
                            Avatar(AvatarFallback("XY", cls="bg-orange-600 font-semibold text-white dark:bg-orange-500")),
                            cls="flex items-center gap-4"
                        ),
                        cls="mb-6",
                    ),
                    cls="mb-8 space-y-4",
                ),
            ),
            # Separator examples
            Div(
                H2("Separators", cls="mb-4 text-2xl font-semibold"),
                Div(
                    Div(
                        P("Content above separator", cls="mb-4"),
                        Separator(),
                        P("Content below separator", cls="mt-4"),
                        cls="mb-6",
                    ),
                    Div(
                        H3("Vertical Separators", cls="mb-2 text-lg font-medium"),
                        Div(
                            Span("Left content"),
                            Separator(orientation="vertical", cls="mx-4"),
                            Span("Right content"),
                            cls="flex h-8 items-center",
                        ),
                        cls="mb-6",
                    ),
                    Div(
                        H3("Custom Styling", cls="mb-2 text-lg font-medium"),
                        Div(
                            P("Custom colored separator below:", cls="mb-2"),
                            Separator(cls="h-0.5 bg-red-500"),
                            P("Thicker separator with different color:", cls="mt-4 mb-2"),
                            Separator(cls="h-1 bg-blue-500"),
                        ),
                    ),
                    cls="mb-8 space-y-4",
                ),
            ),
            # Skeleton examples
            Div(
                H2("Skeleton", cls="mb-4 text-2xl font-semibold"),
                Div(
                    # Basic skeleton shapes
                    Div(
                        H3("Basic Shapes", cls="mb-2 text-lg font-medium"),
                        Div(
                            Skeleton(cls="h-4 w-64"),  # Text line
                            Skeleton(cls="h-4 w-48"),  # Shorter text line
                            Skeleton(cls="h-4 w-56"),  # Another text line
                            cls="mb-4 space-y-2",
                        ),
                        cls="mb-6",
                    ),
                    # Card skeleton
                    Div(
                        H3("Card Skeleton", cls="mb-2 text-lg font-medium"),
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
                            Skeleton(cls="mt-4 h-32 w-full"),  # Content area
                            Skeleton(cls="mt-4 h-4 w-full"),  # Footer line
                            cls="rounded-lg border p-4",
                        ),
                        cls="mb-6",
                    ),
                    # Article skeleton
                    Div(
                        H3("Article Skeleton", cls="mb-2 text-lg font-medium"),
                        Div(
                            Skeleton(cls="mb-4 h-8 w-3/4"),  # Title
                            Skeleton(cls="mb-6 h-3 w-32"),  # Date
                            Div(
                                Skeleton(cls="h-4 w-full"),
                                Skeleton(cls="h-4 w-full"),
                                Skeleton(cls="h-4 w-2/3"),
                                cls="mb-4 space-y-2",
                            ),
                            Skeleton(cls="h-40 w-full"),  # Image placeholder
                            cls="rounded-lg border p-4",
                        ),
                        cls="mb-6",
                    ),
                    # Interactive skeleton toggle
                    Div(
                        H3("Loading State Toggle", cls="mb-2 text-lg font-medium"),
                        Div(
                            Button(
                                ds_text("$loading ? 'Stop Loading' : 'Start Loading'"),
                                ds_on_click(toggle_signal("loading")),
                                variant="outline",
                                cls="mb-4",
                            ),
                            # Content that toggles based on loading state
                            Div(
                                Skeleton(cls="mb-2 h-6 w-48"),
                                Skeleton(cls="mb-4 h-4 w-64"),
                                Skeleton(cls="h-20 w-full"),
                                ds_show("$loading"),
                            ),
                            Div(
                                H4("Content Loaded!", cls="mb-2 text-lg font-semibold"),
                                P("This content appears when loading is complete.", cls="mb-4"),
                                Div(
                                    "This is the actual content that would load.",
                                    cls="rounded-lg bg-muted p-4",
                                ),
                                ds_show("!$loading"),
                            ),
                            ds_signals(loading=True),
                            cls="rounded-lg border p-4",
                        ),
                        cls="mb-6",
                    ),
                    cls="mb-8 space-y-4",
                ),
            ),
            # Progress examples
            Div(
                H2("Progress", cls="mb-4 text-2xl font-semibold"),
                Div(
                    # Basic examples
                    Div(
                        H3("Basic Examples", cls="mb-2 text-lg font-medium"),
                        Div(
                            P("Default (25%):", cls="mb-2"),
                            Progress(progress_value=25),
                            P("Half-way (50%):", cls="mt-4 mb-2"),
                            Progress(progress_value=50),
                            P("Complete (100%):", cls="mt-4 mb-2"),
                            Progress(progress_value=100),
                        ),
                        cls="mb-6",
                    ),
                    # Reactive progress with signals
                    Div(
                        H3("Interactive Progress", cls="mb-2 text-lg font-medium"),
                        Div(
                            Progress(progress_value=35, signal="demo_progress"),
                            Div(
                                Button("Increase", ds_on_click("$demo_progress = Math.min(100, $demo_progress + 10)")),
                                Button("Decrease", ds_on_click("$demo_progress = Math.max(0, $demo_progress - 10)")),
                                Button("Reset", ds_on_click("$demo_progress = 0")),
                                cls="mt-4 flex gap-2",
                            ),
                            P(
                                Span("Current: "),
                                Span(ds_text("$demo_progress"), cls="font-bold"),
                                Span("%"),
                                cls="mt-2 text-sm text-muted-foreground",
                            ),
                        ),
                        cls="mb-6",
                    ),
                    # Auto-incrementing progress
                    Div(
                        H3("Auto-incrementing Progress", cls="mb-2 text-lg font-medium"),
                        Div(
                            Progress(progress_value=0, signal="auto_progress"),
                            Div(
                                Button(
                                    "Start", 
                                    ds_on_click("""
                                        if (!window.autoProgressInterval) {
                                            $auto_progress = 0;
                                            window.autoProgressInterval = setInterval(() => {
                                                if ($auto_progress < 100) {
                                                    $auto_progress += 2;
                                                } else {
                                                    clearInterval(window.autoProgressInterval);
                                                    window.autoProgressInterval = null;
                                                }
                                            }, 100);
                                        }
                                    """),
                                    variant="default"
                                ),
                                Button(
                                    "Stop", 
                                    ds_on_click("""
                                        if (window.autoProgressInterval) {
                                            clearInterval(window.autoProgressInterval);
                                            window.autoProgressInterval = null;
                                        }
                                    """),
                                    variant="destructive"
                                ),
                                Button(
                                    "Reset", 
                                    ds_on_click("""
                                        if (window.autoProgressInterval) {
                                            clearInterval(window.autoProgressInterval);
                                            window.autoProgressInterval = null;
                                        }
                                        $auto_progress = 0;
                                    """),
                                    variant="secondary"
                                ),
                                cls="mt-4 flex gap-2",
                            ),
                            P(
                                Span("Progress: "),
                                Span(ds_text("$auto_progress"), cls="font-bold"),
                                Span("%"),
                                cls="mt-2 text-sm text-muted-foreground",
                            ),
                        ),
                        cls="mb-6",
                    ),
                    # Custom styling
                    Div(
                        H3("Custom Styling", cls="mb-2 text-lg font-medium"),
                        Div(
                            P("Large progress bar:", cls="mb-2"),
                            Progress(progress_value=60, cls="h-4"),
                            P("Custom color:", cls="mt-4 mb-2"),
                            Progress(progress_value=80, class_name="bg-green-200", cls="[&>div]:bg-green-500"),
                        ),
                    ),
                    cls="mb-8 space-y-4",
                ),
            ),
            # Interactive counter with Datastar
            Div(
                H2("Interactive Counter (Datastar)", cls="mb-4 text-2xl font-semibold"),
                Div(
                    Div(
                        Span("Count: ", cls="font-semibold"),
                        Span(ds_text("$count")),
                        cls="mb-4 text-xl",
                    ),
                    Div(
                        Button("-", ds_on_click("$count--"), variant="outline"),
                        Button("Reset", ds_on_click("$count = 0"), variant="secondary"),
                        Button("+", ds_on_click("$count++"), variant="outline"),
                        cls="flex gap-2",
                    ),
                    ds_signals(count=0),
                    cls="mb-8 rounded-lg border p-4",
                ),
            ),
            # Table examples
            Div(
                H2("Tables", cls="mb-4 text-2xl font-semibold"),
                Div(
                    # Basic table
                    Div(
                        H3("Basic Table", cls="mb-2 text-lg font-medium"),
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
                            cls="mb-6",
                        ),
                        cls="mb-8",
                    ),
                    # Table with selection
                    Div(
                        H3("Table with Selection", cls="mb-2 text-lg font-medium"),
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
                                    TableCell(Checkbox(signal="user_1")),
                                    TableCell("John Doe"),
                                    TableCell("john@example.com"),
                                    TableCell(Badge("Admin")),
                                    TableCell(
                                        Button("Edit", variant="ghost", size="sm"),
                                        cls="space-x-2",
                                    ),
                                ),
                                TableRow(
                                    TableCell(Checkbox(signal="user_2", checked=True)),
                                    TableCell("Jane Smith"),
                                    TableCell("jane@example.com"),
                                    TableCell(Badge("User", variant="secondary")),
                                    TableCell(
                                        Button("Edit", variant="ghost", size="sm"),
                                        cls="space-x-2",
                                    ),
                                    selected=True,
                                ),
                                TableRow(
                                    TableCell(Checkbox(signal="user_3")),
                                    TableCell("Bob Johnson"),
                                    TableCell("bob@example.com"),
                                    TableCell(Badge("User", variant="secondary")),
                                    TableCell(
                                        Button("Edit", variant="ghost", size="sm"),
                                        cls="space-x-2",
                                    ),
                                ),
                            ),
                            cls="mb-6",
                        ),
                        cls="mb-8",
                    ),
                    # Compact table
                    Div(
                        H3("Compact Table", cls="mb-2 text-lg font-medium"),
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
                            ),
                            cls="text-xs [&_td]:p-1 [&_th]:h-8 [&_th]:p-1",
                        ),
                        cls="mb-8",
                    ),
                    cls="mb-8 space-y-4",
                ),
            ),
            # Date Picker examples
            Div(
                H2("Date Picker", cls="mb-4 text-2xl font-semibold"),
                Div(
                    # Single date picker
                    Div(
                        H3("Single Date", cls="mb-2 text-lg font-medium"),
                        DatePicker(
                            signal="single_date",
                            mode="single",
                            placeholder="Pick a date",
                        ),
                        cls="mb-4",
                    ),
                    # Date range picker
                    Div(
                        H3("Date Range", cls="mb-2 text-lg font-medium"),
                        DateRangePicker(
                            signal="date_range",
                            placeholder="Pick a date range",
                        ),
                        cls="mb-4",
                    ),
                    # Date picker with presets
                    Div(
                        H3("With Presets", cls="mb-2 text-lg font-medium"),
                        DatePickerWithPresets(
                            signal="date_presets",
                            placeholder="Select a date",
                        ),
                        cls="mb-4",
                    ),
                    # Multiple date selection
                    Div(
                        H3("Multiple Dates", cls="mb-2 text-lg font-medium"),
                        DatePicker(
                            signal="multiple_dates",
                            mode="multiple",
                            placeholder="Select multiple dates",
                        ),
                        cls="mb-4",
                    ),
                    # Date and time picker
                    Div(
                        H3("Date & Time", cls="mb-2 text-lg font-medium"),
                        DateTimePicker(
                            signal="datetime",
                            placeholder="Select date and time",
                        ),
                        cls="mb-4",
                    ),
                    # Date picker with input
                    Div(
                        H3("With Input Field", cls="mb-2 text-lg font-medium"),
                        DatePickerWithInput(
                            signal="date_input",
                            placeholder="YYYY-MM-DD",
                        ),
                        cls="mb-4",
                    ),
                    cls="mb-8 grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3",
                ),
            ),
            # Command examples
            Div(
                H2("Command", cls="mb-4 text-2xl font-semibold"),
                Div(
                    # Basic Command palette
                    Div(
                        H3("Basic Command Palette", cls="mb-2 text-lg font-medium"),
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
                                        data_index=0,
                                    ),
                                    CommandItem(
                                        Icon("lucide:folder"),
                                        Span("New Folder", cls="ml-2"),
                                        value="new-folder",
                                        onclick="console.log('New folder')",
                                        data_index=1,
                                    ),
                                    CommandItem(
                                        Icon("lucide:save"),
                                        Span("Save", cls="ml-2"),
                                        CommandShortcut("⌘S"),
                                        value="save",
                                        onclick="console.log('Save')",
                                        data_index=2,
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
                                        data_index=3,
                                    ),
                                    CommandItem(
                                        Icon("lucide:user"),
                                        Span("Profile", cls="ml-2"),
                                        value="profile",
                                        onclick="console.log('Profile')",
                                        data_index=4,
                                    ),
                                    CommandItem(
                                        Icon("lucide:log-out"),
                                        Span("Log Out", cls="ml-2"),
                                        value="logout",
                                        onclick="console.log('Logout')",
                                        data_index=5,
                                    ),
                                    heading="User",
                                ),
                            ),
                            signal="basic_command",
                            size="md",
                            cls="max-w-md",
                        ),
                        cls="mb-6",
                    ),
                    # Command Dialog
                    Div(
                        H3("Command Dialog", cls="mb-2 text-lg font-medium"),
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
                                            onclick="console.log('Copy'); document.getElementById('cmd_dialog_dialog').close()",
                                            data_index=0,
                                        ),
                                        CommandItem(
                                            Icon("lucide:clipboard"),
                                            Span("Paste", cls="ml-2"),
                                            CommandShortcut("⌘V"),
                                            value="paste",
                                            onclick="console.log('Paste'); document.getElementById('cmd_dialog_dialog').close()",
                                            data_index=1,
                                        ),
                                        CommandItem(
                                            Icon("lucide:scissors"),
                                            Span("Cut", cls="ml-2"),
                                            CommandShortcut("⌘X"),
                                            value="cut",
                                            onclick="console.log('Cut'); document.getElementById('cmd_dialog_dialog').close()",
                                            data_index=2,
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
                                            onclick="console.log('Toggle sidebar'); document.getElementById('cmd_dialog_dialog').close()",
                                            data_index=3,
                                        ),
                                        CommandItem(
                                            Icon("lucide:moon"),
                                            Span("Toggle Theme", cls="ml-2"),
                                            CommandShortcut("⌘T"),
                                            value="toggle-theme",
                                            onclick="console.log('Toggle theme'); document.getElementById('cmd_dialog_dialog').close()",
                                            data_index=4,
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
                                            onclick="console.log('Help'); document.getElementById('cmd_dialog_dialog').close()",
                                            data_index=5,
                                        ),
                                        CommandItem(
                                            Icon("lucide:keyboard"),
                                            Span("Keyboard Shortcuts", cls="ml-2"),
                                            value="shortcuts",
                                            onclick="console.log('Shortcuts'); document.getElementById('cmd_dialog_dialog').close()",
                                            data_index=6,
                                        ),
                                        heading="Help",
                                    ),
                                ),
                            ],
                            signal="cmd_dialog",
                        ),
                        cls="mb-6",
                    ),
                    # Command with search example
                    Div(
                        H3("Searchable Command Palette", cls="mb-2 text-lg font-medium"),
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
                                        data_index=0,
                                    ),
                                    CommandItem(
                                        "Vue",
                                        value="vue",
                                        keywords="javascript frontend",
                                        onclick="alert('Selected: Vue')",
                                        data_index=1,
                                    ),
                                    CommandItem(
                                        "Angular",
                                        value="angular",
                                        keywords="typescript frontend",
                                        onclick="alert('Selected: Angular')",
                                        data_index=2,
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
                                        data_index=3,
                                    ),
                                    CommandItem(
                                        "FastAPI",
                                        value="fastapi",
                                        keywords="python backend api",
                                        onclick="alert('Selected: FastAPI')",
                                        data_index=4,
                                    ),
                                    CommandItem(
                                        "Express",
                                        value="express",
                                        keywords="javascript nodejs backend",
                                        onclick="alert('Selected: Express')",
                                        data_index=5,
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
                                        data_index=6,
                                    ),
                                    CommandItem(
                                        "Nuxt",
                                        value="nuxt",
                                        keywords="vue fullstack",
                                        onclick="alert('Selected: Nuxt')",
                                        data_index=7,
                                    ),
                                    CommandItem(
                                        "SvelteKit",
                                        value="sveltekit",
                                        keywords="svelte fullstack",
                                        onclick="alert('Selected: SvelteKit')",
                                        data_index=8,
                                    ),
                                    heading="Full Stack",
                                ),
                            ),
                            signal="framework_command",
                            size="lg",
                            cls="max-w-md",
                        ),
                        cls="mb-6",
                    ),
                    # Command with disabled items
                    Div(
                        H3("Command with Disabled Items", cls="mb-2 text-lg font-medium"),
                        Command(
                            CommandInput(placeholder="Search actions..."),
                            CommandList(
                                CommandEmpty("No action found."),
                                CommandItem(
                                    Icon("lucide:check"),
                                    Span("Available Action", cls="ml-2"),
                                    value="available",
                                    onclick="alert('Action executed')",
                                    data_index=0,
                                ),
                                CommandItem(
                                    Icon("lucide:lock"),
                                    Span("Premium Feature", cls="ml-2"),
                                    Badge("Pro", variant="secondary", cls="ml-auto"),
                                    value="premium",
                                    disabled=True,
                                    data_index=1,
                                ),
                                CommandItem(
                                    Icon("lucide:shield"),
                                    Span("Admin Only", cls="ml-2"),
                                    value="admin",
                                    disabled=True,
                                    data_index=2,
                                ),
                                CommandItem(
                                    Icon("lucide:play"),
                                    Span("Run Task", cls="ml-2"),
                                    value="run",
                                    onclick="alert('Task started')",
                                    data_index=3,
                                ),
                            ),
                            signal="disabled_command",
                            size="sm",
                            cls="max-w-md",
                        ),
                        cls="mb-6",
                    ),
                    cls="mb-8 space-y-4",
                ),
            ),
            # Toast examples
            Div(
                H2("Toast Notifications", cls="mb-4 text-2xl font-semibold"),
                Div(
                    # Basic toast triggers
                    Div(
                        H3("Basic Toast Types", cls="mb-2 text-lg font-medium"),
                        Div(
                            Button(
                                "Default Toast",
                                ds_on_click(toast('Event has been created', 'Your event is now live')),
                                variant="outline"
                            ),
                            Button(
                                "Success Toast",
                                ds_on_click(success_toast('Success!', 'Operation completed successfully')),
                                variant="outline"
                            ),
                            Button(
                                "Error Toast",
                                ds_on_click(error_toast('Error!', 'Something went wrong')),
                                variant="outline"
                            ),
                            Button(
                                "Warning Toast",
                                ds_on_click(warning_toast('Warning!', 'Please be careful')),
                                variant="outline"
                            ),
                            Button(
                                "Info Toast",
                                ds_on_click(info_toast('Info', 'Here is some information')),
                                variant="outline"
                            ),
                            cls="flex flex-wrap gap-2"
                        ),
                        cls="mb-6",
                    ),
                    # Toast with different durations
                    Div(
                        H3("Custom Duration", cls="mb-2 text-lg font-medium"),
                        Div(
                            Button(
                                "Quick Toast (1s)",
                                ds_on_click(toast('Quick!', 'This disappears fast', duration=1000)),
                                variant="secondary"
                            ),
                            Button(
                                "Long Toast (10s)",
                                ds_on_click(toast('Long Toast', 'This stays for 10 seconds', duration=10000)),
                                variant="secondary"
                            ),
                            Button(
                                "Persistent Toast",
                                ds_on_click(toast('Persistent', 'Click X to dismiss', duration=0)),
                                variant="secondary"
                            ),
                            cls="flex flex-wrap gap-2"
                        ),
                        cls="mb-6",
                    ),
                    # Multiple toasts
                    Div(
                        H3("Multiple Toasts", cls="mb-2 text-lg font-medium"),
                        Div(
                            Button(
                                "Spam Toasts",
                                ds_on_click(f"""
                                    {info_toast('First toast', 'This is the first one')}
                                    setTimeout(() => {{ {success_toast('Second toast', 'This is the second one')} }}, 500);
                                    setTimeout(() => {{ {warning_toast('Third toast', 'This is the third one')} }}, 1000);
                                """),
                                variant="destructive"
                            ),
                            cls="flex gap-2"
                        ),
                        cls="mb-6",
                    ),
                    
                    # Position examples with different toasters
                    Div(
                        H3("Different Positions", cls="mb-2 text-lg font-medium"),
                        P("Note: In a real app, you'd have separate toasters for different positions", cls="mb-4 text-sm text-muted-foreground"),
                        Div(
                            Button(
                                "Promise Toast",
                                ds_on_click(f"""
                                    {toast('Loading...', 'Please wait...')}
                                    setTimeout(() => {{ {success_toast('Hello John Doe', 'Promise resolved successfully')} }}, 2000);
                                """),
                                variant="outline"
                            ),
                            Button(
                                "Rich Colors Demo",
                                ds_on_click(success_toast('Rich Colors', 'Notice the rich background colors when enabled')),
                                variant="outline"
                            ),
                            cls="flex gap-2"
                        ),
                        cls="mb-6",
                    ),
                    cls="mb-8 space-y-4",
                ),
            ),
            # Form with validation example
            Div(
                H2(
                    "Form with Validation (Datastar)", cls="mb-4 text-2xl font-semibold"
                ),
                Form(
                    Div(
                        Label("Name", for_="name"),
                        Input(
                            id="name", 
                            placeholder="Enter your name",
                            signal="name"
                        ),
                        Span(
                            "Name is required",
                            ds_show("$submitted && !$name"),
                            cls="text-sm text-destructive",
                        ),
                        cls="space-y-2",
                    ),
                    Div(
                        Label("Email", for_="email"),
                        Input(
                            id="email",
                            type="email",
                            placeholder="email@example.com",
                            signal="email"
                        ),
                        Span(
                            "Invalid email",
                            ds_show("$email && !$email.includes('@')"),
                            cls="text-sm text-destructive",
                        ),
                        cls="space-y-2",
                    ),
                    Button(
                        "Submit",
                        ds_on_click("$submitted = true"),
                        ds_class(
                            opacity_50="!$name || !$email || !$email.includes('@')"
                        ),
                        type="submit",
                    ),
                    ds_signals(name=expr(""), email=expr(""), submitted=False),
                    ds_on_submit(
                        "event.preventDefault(); if($name && $email.includes('@')) alert('Form submitted!')"
                    ),
                    cls="max-w-md space-y-4",
                ),
            ),
            cls="container mx-auto p-8",
        ),
        cls="relative min-h-screen",
    )


@rt("/dropdown-width-debug")
def dropdown_width_debug():
    """Debug dropdown width matching issues."""
    return Div(
        # Theme toggle in top-right corner
        Div(ThemeToggle(), cls="absolute top-4 right-4"),
        # Main content
        Div(
            H1("Dropdown Width Matching Debug", cls="mb-8 text-3xl font-bold"),
            
            Div(
                H2("WORKING: Select Component", cls="mb-4 text-xl font-semibold text-green-600"),
                Select(
                    SelectTrigger(
                        SelectValue(placeholder="Choose option")
                    ),
                    SelectContent(
                        SelectItem("Option 1", "opt1"),
                        SelectItem("Option 2", "opt2"),
                        SelectItem("Option 3", "opt3")
                    )
                ),
                cls="mb-8"
            ),
            
            Div(
                H2("FAILING: Hero Dropdown (Open Menu)", cls="mb-4 text-xl font-semibold text-red-600"),
                DropdownMenu(
                    DropdownMenuTrigger(
                        "Open Menu",
                        Icon("lucide:chevron-down", cls="ml-2 h-4 w-4")
                    ),
                    DropdownMenuContent(
                        DropdownMenuItem(
                            Icon("lucide:plus", cls="mr-2 h-4 w-4"),
                            "New File"
                        ),
                        DropdownMenuItem(
                            Icon("lucide:download", cls="mr-2 h-4 w-4"),
                            "Download"
                        ),
                        DropdownMenuSeparator(),
                        DropdownMenuItem(
                            Icon("lucide:trash", cls="mr-2 h-4 w-4"),
                            "Delete",
                            variant="destructive"
                        )
                    )
                ),
                cls="mb-8"
            ),
            
            Div(
                H2("FAILING: Checkbox Dropdown (View Options)", cls="mb-4 text-xl font-semibold text-red-600"),
                DropdownMenu(
                    DropdownMenuTrigger(
                        Icon("lucide:eye", cls="mr-2 h-4 w-4"),
                        "View Options"
                    ),
                    DropdownMenuContent(
                        DropdownMenuLabel("Display Settings"),
                        DropdownMenuSeparator(),
                        DropdownMenuCheckboxItem(
                            "Show Grid",
                            signal="show_grid"
                        ),
                        DropdownMenuCheckboxItem(
                            "Show Rulers", 
                            signal="show_rulers"
                        ),
                        DropdownMenuCheckboxItem(
                            "Show Guides",
                            signal="show_guides"
                        )
                    )
                ),
                cls="mb-8"
            ),
            
            Div(
                H2("WORKING: Simple Dropdown (Settings)", cls="mb-4 text-xl font-semibold text-green-600"),
                DropdownMenu(
                    DropdownMenuTrigger("Settings"),
                    DropdownMenuContent(
                        DropdownMenuItem("Profile"),
                        DropdownMenuItem("Billing"),
                        DropdownMenuItem("Settings"),
                        DropdownMenuItem("Log out")
                    )
                ),
                cls="mb-8"
            ),
            
            # CSS Debug Tools Section
            Div(
                H1("🔧 CSS Debug Tools", cls="mb-6 text-3xl font-bold text-blue-600"),
                P(
                    "Advanced CSS debugging tools for analyzing dropdown width conflicts. "
                    "These tools help identify why some dropdowns are narrower than their triggers "
                    "despite having reactive min-width properties.",
                    cls="mb-8 text-lg text-gray-600"
                ),
                
                # CSS Debug Agent
                Div(
                    CSSDebugAgent(),
                    cls="mb-8"
                ),
                
                # CSS Cascade Analyzer
                Div(
                    CSSCascadeAnalyzer(),
                    cls="mb-8"
                ),
                
                # Width Conflict Detector
                Div(
                    WidthConflictDetector(),
                    cls="mb-8"
                ),
                
                cls="container mx-auto max-w-7xl p-8"
            ),
            
            cls="container mx-auto max-w-2xl p-8"
        ),
        ds_signals(show_grid=True, show_rulers=False, show_guides=True),
        Script("""
            // Debug dropdown width calculations
            setTimeout(() => {
                console.log('=== DROPDOWN WIDTH DEBUG V2 ===');
                
                // Find all triggers and their associated dropdowns
                document.querySelectorAll('button[id*="-trigger"]').forEach((trigger, i) => {
                    const triggerWidth = trigger.offsetWidth;
                    const triggerId = trigger.id;
                    const signal = triggerId.replace('-trigger', '');
                    const isSelect = trigger.getAttribute('role') === 'combobox';
                    const contentId = signal + '-content';
                    const content = document.getElementById(contentId);
                    
                    console.log(`\\n--- ${isSelect ? 'SELECT' : 'DROPDOWN'} ${i}: ${trigger.textContent.trim()} ---`);
                    console.log('Trigger ID:', triggerId);
                    console.log('Signal:', signal);
                    console.log('Trigger width:', triggerWidth + 'px');
                    console.log('Trigger data-ref:', trigger.getAttribute('data-ref'));
                    
                    // Check for signal references
                    const triggerRef = window[signal + '_trigger'];
                    console.log('Window trigger ref exists:', !!triggerRef);
                    if (triggerRef) {
                        console.log('Trigger ref offsetWidth:', triggerRef.offsetWidth);
                    }
                    
                    if (content) {
                        const contentWidth = content.offsetWidth;
                        const computedStyles = getComputedStyle(content);
                        const cssMinWidth = computedStyles.minWidth;
                        const inlineMinWidth = content.style.minWidth;
                        
                        console.log('Content width:', contentWidth + 'px');
                        console.log('CSS min-width:', cssMinWidth);
                        console.log('Inline min-width:', inlineMinWidth);
                        
                        // Check the computed signal attributes
                        const computedAttr = content.getAttribute('data-computed-' + signal + '_content_min_width');
                        const styleAttr = content.getAttribute('data-style-min-width');
                        
                        console.log('data-computed attr:', computedAttr);
                        console.log('data-style attr:', styleAttr);
                        
                        // Check parent for signals
                        const parent = content.closest('[data-signals]');
                        if (parent) {
                            const signals = parent.getAttribute('data-signals');
                            console.log('Parent signals:', signals);
                            
                            // Check if our computed signal is there
                            if (signals && signals.includes(signal + '_content_min_width')) {
                                console.log('✓ Found content_min_width in parent signals');
                            } else {
                                console.log('✗ content_min_width NOT in parent signals');
                            }
                        }
                        
                        // Check for the computed value
                        const computedValue = window[signal + '_content_min_width'];
                        console.log('Window computed value exists:', !!computedValue);
                        console.log('Window computed value:', computedValue);
                        
                        // Calculate what the width SHOULD be
                        const shouldBeWidth = Math.max(triggerWidth, 128); // 8rem = 128px
                        console.log('Expected width (max of trigger/8rem):', shouldBeWidth + 'px');
                        
                        // Check if the width mismatch is happening
                        const widthMismatch = Math.abs(contentWidth - shouldBeWidth) > 5; // Allow 5px tolerance
                        if (widthMismatch) {
                            console.log('⚠️  WIDTH MISMATCH DETECTED!');
                            console.log('Content is:', contentWidth + 'px');
                            console.log('Should be:', shouldBeWidth + 'px');
                            console.log('Difference:', (contentWidth - shouldBeWidth) + 'px');
                        } else {
                            console.log('✅ Width correct (within tolerance)');
                        }
                    } else {
                        console.log('❌ Content element not found!');
                    }
                });
                
                console.log('\\n=== CHECKING DATASTAR STATE ===');
                // Check if DataStar is initialized and what signals exist
                if (window.ds && window.ds.store) {
                    console.log('DataStar store signals:', Object.keys(window.ds.store).filter(k => k.includes('_')));
                } else {
                    console.log('DataStar store not accessible');
                }
                
                console.log('\\n=== END DEBUG ===');
            }, 1500); // Wait longer for datastar to fully initialize
        """),
        cls="relative min-h-screen"
    )


if __name__ == "__main__":
    serve(port=5004)
