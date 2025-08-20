#!/usr/bin/env python3
# Import all registry components at once
from registry_loader import *
from starhtml import *

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
