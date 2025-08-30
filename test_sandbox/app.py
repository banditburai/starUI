#!/usr/bin/env python3
# Import starhtml first, then override with our custom components
from starhtml import *
from starhtml.datastar import value

# Import all registry components at once (this will override starhtml components)
from registry_loader import *

styles = Link(rel="stylesheet", href="/static/css/starui.css", type="text/css")

app, rt = star_app(
    live=True,
    hdrs=(        
        fouc_script(use_data_theme=True),
        styles,        
        position_handler(),  # Enhanced handler is now built-in
    ),
    htmlkw=dict(lang="en", dir="ltr"),
    bodykw=dict(cls="min-h-screen bg-background text-foreground"),
)


@rt("/")
def index():
    return Div(
        # Theme toggle in top-right corner
        Div(ThemeToggle(), cls="absolute top-4 right-4"),
        # Main content container
        Div(
            H1("StarUI Component Test", cls="text-4xl font-bold mb-8"),
            # Button variants
            Div(
                H2("Buttons", cls="text-2xl font-semibold mb-4"),
                Div(
                    Button("Default"),
                    Button("Destructive", variant="destructive"),
                    Button("Outline", variant="outline"),
                    Button("Secondary", variant="secondary"),
                    Button("Ghost", variant="ghost"),
                    Button("Link", variant="link"),
                    Button(Icon("lucide:settings"), variant="secondary", size="icon"),
                    Button("Disabled", disabled=True),
                    cls="flex flex-wrap gap-2 mb-8",
                ),
            ),
            # Badge variants
            Div(
                H2("Badges", cls="text-2xl font-semibold mb-4"),
                Div(
                    Badge("Default"),
                    Badge("Secondary", variant="secondary"),
                    Badge("Destructive", variant="destructive"),
                    Badge("Outline", variant="outline"),
                    Badge("Clickable", ds_on_click("alert('Badge clicked!')")),
                    cls="flex flex-wrap gap-2 mb-8",
                ),
            ),
            # Input types
            Div(
                H2("Inputs", cls="text-2xl font-semibold mb-4"),
                Div(
                    Div(
                        Label("Text Input", for_="text-input"),
                        Input(
                            ds_bind("name"),
                            id="text-input",
                            placeholder="Enter text...",
                        ),
                        cls="space-y-2",
                    ),
                    Div(
                        Label("Email Input", for_="email-input"),
                        Input(
                            ds_bind("email"),
                            id="email-input",
                            type="email",
                            placeholder="email@example.com",
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
                    cls="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8",
                ),
            ),
            # Card example
            Div(
                H2("Card", cls="text-2xl font-semibold mb-4"),
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
                    cls="max-w-md mb-8",
                ),
            ),
            # Alert variants
            Div(
                H2("Alerts", cls="text-2xl font-semibold mb-4"),
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
                    cls="space-y-4 mb-8",
                ),
            ),
            # Breadcrumb
            Div(
                H2("Breadcrumb", cls="text-2xl font-semibold mb-4"),
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
                H2("Tabs - Default Variant", cls="text-2xl font-semibold mb-4"),
                Tabs(
                    TabsList(
                        TabsTrigger("Preview", value="preview"),
                        TabsTrigger("Code", value="code"),
                        TabsTrigger("Settings", value="settings"),
                    ),
                    TabsContent(
                        Div(
                            H3("Preview Content", cls="text-lg font-semibold mb-2"),
                            P(
                                "This is the preview tab content with the default boxed style."
                            ),
                            Button(
                                "Action in Preview", variant="secondary", cls="mt-4"
                            ),
                        ),
                        value="preview",
                    ),
                    TabsContent(
                        Div(
                            H3("Code Content", cls="text-lg font-semibold mb-2"),
                            Pre(
                                Code(
                                    "# Example code\ndef hello_world():\n    print('Hello, World!')",
                                    cls="block p-4 bg-muted rounded",
                                )
                            ),
                        ),
                        value="code",
                    ),
                    TabsContent(
                        Div(
                            H3("Settings Content", cls="text-lg font-semibold mb-2"),
                            P("Configure your preferences here."),
                            Div(
                                Label("Enable notifications", for_="notifications"),
                                Input(type="checkbox", id="notifications", cls="ml-2"),
                                cls="flex items-center gap-2 mt-4",
                            ),
                        ),
                        value="settings",
                    ),
                    default_value="preview",
                    variant="default",
                    cls="mb-8",
                ),
            ),
            # Tabs example - Plain variant (text style)
            Div(
                H2("Tabs - Plain Variant", cls="text-2xl font-semibold mb-4"),
                Tabs(
                    TabsList(
                        TabsTrigger("Account", value="account"),
                        TabsTrigger("Password", value="password"),
                        TabsTrigger("Team", value="team"),
                        TabsTrigger("Billing", value="billing"),
                    ),
                    TabsContent(
                        Div(
                            H3("Account Settings", cls="text-lg font-semibold mb-2"),
                            P("Manage your account settings and preferences."),
                            Div(
                                Label("Username", for_="username"),
                                Input(
                                    id="username",
                                    placeholder="Enter username",
                                    cls="max-w-sm",
                                ),
                                cls="space-y-2 mt-4",
                            ),
                        ),
                        value="account",
                    ),
                    TabsContent(
                        Div(
                            H3("Password & Security", cls="text-lg font-semibold mb-2"),
                            P("Update your password and security settings."),
                            Button("Change Password", variant="outline", cls="mt-4"),
                        ),
                        value="password",
                    ),
                    TabsContent(
                        Div(
                            H3("Team Members", cls="text-lg font-semibold mb-2"),
                            P("Manage your team and collaborate with others."),
                        ),
                        value="team",
                    ),
                    TabsContent(
                        Div(
                            H3("Billing Information", cls="text-lg font-semibold mb-2"),
                            P("View and manage your subscription and payment methods."),
                        ),
                        value="billing",
                    ),
                    default_value="account",
                    variant="plain",
                    cls="mb-8",
                ),
            ),
            # Sheet example
            Div(
                H2("Sheet (Modal Drawer)", cls="text-2xl font-semibold mb-4"),
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
                            cls="p-6 space-y-4",
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
                ),
                cls="mb-8",
            ),
            # Dialog example
            Div(
                H2("Dialog (Modal)", cls="text-2xl font-semibold mb-4"),
                Dialog(
                    trigger=DialogTrigger("Edit Profile", ref_id="edit-profile-dialog"),
                    content=DialogContent(
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
                    ref_id="edit-profile-dialog",
                    size="md",
                ),
                cls="mb-8",
            ),
            # Dialog with different size and content
            Div(
                H2("Alert Dialog", cls="text-2xl font-semibold mb-4"),
                Dialog(
                    trigger=DialogTrigger(
                        "Delete Account", ref_id="delete-dialog", variant="destructive"
                    ),
                    content=DialogContent(
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
                    ref_id="delete-dialog",
                    size="sm",
                ),
                cls="mb-8",
            ),
            # Radio Group examples
            Div(
                H2("Radio Groups", cls="text-2xl font-semibold mb-4"),
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
                            cls="text-sm font-medium mb-2",
                        ),
                        RadioGroup(
                            RadioGroupItem("small", "Small"),
                            RadioGroupItem("medium", "Medium"),
                            RadioGroupItem("large", "Large"),
                            value="medium",
                        ),
                        cls="p-4 border rounded-lg",
                    ),
                    Div(
                        P(
                            "Custom styled radio group (blue indicator):",
                            cls="text-sm font-medium mb-2",
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
                        cls="p-4 border rounded-lg",
                    ),
                    cls="space-y-6 mb-8",
                ),
            ),
            # Switch examples
            Div(
                H2("Switches", cls="text-2xl font-semibold mb-4"),
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
                        P("Simple switches:", cls="text-sm font-medium mb-2"),
                        Div(
                            Switch(signal="simple1", checked=True),
                            Switch(signal="simple2"),
                            Switch(disabled=True),
                            cls="flex gap-4",
                        ),
                        cls="p-4 border rounded-lg",
                    ),
                    cls="space-y-4 mb-8",
                ),
            ),
            # Textarea examples
            Div(
                H2("Textareas", cls="text-2xl font-semibold mb-4"),
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
                        P("Simple textarea:", cls="text-sm font-medium mb-2"),
                        Textarea(
                            placeholder="Type something...",
                            signal="simple_textarea",
                            resize="vertical",
                        ),
                        cls="p-4 border rounded-lg",
                    ),
                    cls="space-y-4 mb-8",
                ),
            ),
            # Select examples
            Div(
                H2("Select", cls="text-2xl font-semibold mb-4"),
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
                        P("Simple select:", cls="text-sm font-medium mb-2"),
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
                        cls="p-4 border rounded-lg",
                    ),
                    cls="space-y-4 mb-8",
                ),
            ),
            # Popover examples
            Div(
                H2("Popovers", cls="text-2xl font-semibold mb-4"),
                Div(
                    # Basic popover
                    Popover(
                        PopoverTrigger("Open Popover"),
                        PopoverContent(
                            Div(
                                H3("About this feature", cls="font-semibold mb-2"),
                                P("This is a popover component that displays rich content in a floating panel.", cls="text-sm text-muted-foreground mb-3"),
                                PopoverClose("✕"),
                            ),
                        ),
                    ),
                    # Popover with different positioning
                    Popover(
                        PopoverTrigger("Top Popover", variant="outline"),
                        PopoverContent(
                            Div(
                                H3("Top positioned", cls="font-semibold mb-2"),
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
                                H3("Quick Settings", cls="font-semibold mb-3"),
                                Div(
                                    Label("Theme", cls="text-sm font-medium"),
                                    Button("Toggle", variant="outline", size="sm"),
                                    cls="flex justify-between items-center mb-2",
                                ),
                                Div(
                                    Label("Notifications", cls="text-sm font-medium"),
                                    Switch(signal="notif_setting"),
                                    cls="flex justify-between items-center",
                                ),
                                PopoverClose("Done", variant="ghost"),
                            ),
                        ),
                    ),
                    cls="flex flex-wrap gap-4 mb-8",
                ),
            ),
            # HoverCard examples
            Div(
                H2("Hover Cards", cls="text-2xl font-semibold mb-4"),
                Div(
                    # Basic hover card
                    HoverCard(
                        HoverCardTrigger(
                            Span("@username", cls="text-blue-600 underline cursor-pointer"),
                            signal="user_hover",
                        ),
                        HoverCardContent(
                            Div(
                                Div(
                                    Div("👤", cls="w-12 h-12 bg-muted rounded-full flex items-center justify-center text-2xl mb-3"),
                                    H3("John Doe", cls="font-semibold mb-1"),
                                    P("@username", cls="text-sm text-muted-foreground mb-2"),
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
                                H3("Quick Info", cls="font-semibold mb-2"),
                                P("This hover card appears when you hover over the trigger element.", cls="text-sm text-muted-foreground mb-2"),
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
                            ),
                            signal="product_hover",
                            side="left",
                        ),
                        signal="product_hover",
                    ),
                    cls="flex flex-wrap gap-4 mb-8",
                ),
            ),
            # Checkbox examples
            Div(
                H2("Checkboxes", cls="text-2xl font-semibold mb-4"),
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
                            checkbox_cls="checked:!bg-blue-600 checked:!border-blue-600 dark:checked:!bg-blue-700 dark:checked:!border-blue-700",
                            indicator_cls="!text-white",
                        ),
                        cls="p-4 border rounded-lg",
                    ),
                    cls="space-y-4 mb-8",
                ),
            ),
            # Toggle examples
            Div(
                H2("Toggles", cls="text-2xl font-semibold mb-4"),
                Div(
                    # Basic toggles
                    Div(
                        P("Basic toggles:", cls="text-sm font-medium mb-2"),
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
                        P("Outline variant:", cls="text-sm font-medium mb-2"),
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
                        P("Different sizes:", cls="text-sm font-medium mb-2"),
                        Div(
                            Toggle("Small", size="sm", variant="outline", signal="size_sm"),
                            Toggle("Default", size="default", variant="outline", signal="size_default"),
                            Toggle("Large", size="lg", variant="outline", signal="size_lg"),
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
                    cls="space-y-4 mb-8",
                ),
            ),
            # Toggle Group examples
            Div(
                H2("Toggle Groups", cls="text-2xl font-semibold mb-4"),
                Div(
                    # Single selection toggle group
                    Div(
                        P("Text formatting (single selection):", cls="text-sm font-medium mb-2"),
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
                        P("Text options (multiple selection):", cls="text-sm font-medium mb-2"),
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
                        P("Text alignment:", cls="text-sm font-medium mb-2"),
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
                        P("Size selection:", cls="text-sm font-medium mb-2"),
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
                        P("View mode:", cls="text-sm font-medium mb-2"),
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
                        P("Disabled group:", cls="text-sm font-medium mb-2"),
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
                    cls="space-y-4 mb-8",
                ),
            ),
            # Accordion examples
            Div(
                H2("Accordion", cls="text-2xl font-semibold mb-4"),
                Div(
                    # Single accordion with collapsible
                    Div(
                        P(
                            "Single selection (collapsible):",
                            cls="text-sm font-medium mb-2",
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
                        P("Multiple selection:", cls="text-sm font-medium mb-2"),
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
                    cls="space-y-4 mb-8",
                ),
            ),
            # Interactive counter with Datastar
            Div(
                H2("Interactive Counter (Datastar)", cls="text-2xl font-semibold mb-4"),
                Div(
                    Div(
                        Span("Count: ", cls="font-semibold"),
                        Span(ds_text("$count")),
                        cls="text-xl mb-4",
                    ),
                    Div(
                        Button("-", ds_on_click("$count--"), variant="outline"),
                        Button("Reset", ds_on_click("$count = 0"), variant="secondary"),
                        Button("+", ds_on_click("$count++"), variant="outline"),
                        cls="flex gap-2",
                    ),
                    ds_signals(count=0),
                    cls="p-4 border rounded-lg mb-8",
                ),
            ),
            # Form with validation example
            Div(
                H2(
                    "Form with Validation (Datastar)", cls="text-2xl font-semibold mb-4"
                ),
                Form(
                    Div(
                        Label("Name", for_="name"),
                        Input(
                            ds_bind("name"), id="name", placeholder="Enter your name"
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
                            ds_bind("email"),
                            id="email",
                            type="email",
                            placeholder="email@example.com",
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
                    ds_signals(name=value(""), email=value(""), submitted=False),
                    ds_on_submit(
                        "event.preventDefault(); if($name && $email.includes('@')) alert('Form submitted!')"
                    ),
                    cls="space-y-4 max-w-md",
                ),
            ),
            cls="container mx-auto p-8",
        ),
        cls="min-h-screen relative",
    )


if __name__ == "__main__":
    serve(port=5004)
