#!/usr/bin/env python3
# Import starhtml first, then override with our custom components
from starhtml import *

# Import all registry components at once (this will override starhtml components)
from registry_loader import *

styles = Link(rel="stylesheet", href="/static/css/starui.css", type="text/css")

app, rt = star_app(
    hdrs=(
        fouc_script(use_data_theme=True),
        styles,
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
                    ds_signals(name="", email="", submitted=False),
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
