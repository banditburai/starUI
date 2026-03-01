TITLE = "Sheet"
DESCRIPTION = "A side panel component that slides in from the screen edge. Perfect for navigation menus, filter panels, settings drawers, and detail views."
CATEGORY = "overlay"
ORDER = 150
STATUS = "stable"

from starhtml import Div, P, Span, Icon, Signal
from starui.registry.components.sheet import (
    Sheet, SheetTrigger, SheetContent, SheetClose,
    SheetHeader, SheetFooter, SheetTitle, SheetDescription
)
from starui.registry.components.input import InputWithLabel
from starui.registry.components.button import Button
from utils import auto_generate_page, with_code, Prop, Component, build_api_reference


@with_code
def default_example():
    return Sheet(
        SheetTrigger("Edit Profile"),
        SheetContent(
            SheetHeader(
                SheetTitle("Edit profile"),
                SheetDescription("Make changes to your profile here. Click save when you're done.")
            ),
            Div(
                InputWithLabel(label="Name", value="Pedro Duarte", autofocus=True, onfocus="this.select()"),
                InputWithLabel(label="Username", value="@peduarte"),
                cls="space-y-4 px-4"
            ),
            SheetFooter(
                SheetClose("Save changes", variant="default")
            ),
        ),
    )


@with_code
def side_positioning_example():
    sides = ["top", "right", "bottom", "left"]

    def create_side_demo(side):
        return Sheet(
            SheetTrigger(side.capitalize(), variant="outline"),
            SheetContent(
                SheetHeader(
                    SheetTitle(f"{side.capitalize()} sheet"),
                    SheetDescription(f"This sheet slides in from the {side} edge.")
                ),
                SheetFooter(
                    SheetClose("Close", variant="outline")
                ),
                side=side,
            ),
        )

    return Div(
        *[create_side_demo(s) for s in sides],
        cls="flex flex-wrap gap-2 justify-center"
    )


@with_code
def sizes_example():
    sheet_configs = [
        {"button": "Small", "size": "sm", "title": "Small Sheet", "description": "Compact size for simple content",
         "content": "This is a small sheet (max-w-sm) — perfect for simple forms and quick actions."},
        {"button": "Medium", "size": "md", "title": "Medium Sheet", "description": "Standard size for most content",
         "content": "This is a medium sheet (max-w-md) — the default size for forms and settings."},
        {"button": "Large", "size": "lg", "title": "Large Sheet", "description": "More space for complex content",
         "content": "This is a large sheet (max-w-lg) — great for detailed forms and data views."},
        {"button": "Extra Large", "size": "xl", "title": "Extra Large Sheet", "description": "Maximum width for extensive content",
         "content": "This is an extra large sheet (max-w-xl) — ideal for dashboards and data tables."},
    ]

    def create_size_demo(config):
        return Sheet(
            SheetTrigger(config["button"], variant="outline", size="sm"),
            SheetContent(
                SheetHeader(
                    SheetTitle(config["title"]),
                    SheetDescription(config["description"])
                ),
                Div(P(config["content"], cls="text-sm"), cls="px-4"),
                side="right",
                size=config["size"]
            ),
        )

    return Div(
        *[create_size_demo(config) for config in sheet_configs],
        cls="flex flex-wrap gap-2 justify-center"
    )


@with_code
def no_close_button_example():
    return Sheet(
        SheetTrigger("Open Sheet", variant="outline"),
        SheetContent(
            SheetHeader(
                SheetTitle("Custom close"),
                SheetDescription("This sheet hides the default close button. Use the button below to dismiss.")
            ),
            SheetFooter(
                SheetClose("Done", variant="default")
            ),
            show_close=False,
        ),
    )


@with_code
def notifications_example():
    notifications = [
        {"title": "Deployment complete", "desc": "v2.4.1 deployed to production", "icon": "lucide:rocket",
         "sig": Signal("notif_deploy", True)},
        {"title": "New comment", "desc": "Priya commented on PR #417", "icon": "lucide:message-circle",
         "sig": Signal("notif_comment", True)},
        {"title": "Build failed", "desc": "CI pipeline timed out on staging", "icon": "lucide:alert-triangle",
         "sig": Signal("notif_build", True)},
    ]

    sigs = [n["sig"] for n in notifications]
    count = sum(sigs)

    return Div(
        sigs,
        Sheet(
            SheetTrigger(
                Icon("lucide:bell", cls="h-4 w-4"),
                Span(data_text=count, cls="text-xs"),
                variant="outline",
            ),
            SheetContent(
                SheetHeader(
                    SheetTitle("Notifications"),
                    SheetDescription(
                        Span(data_text=count),
                        " unread",
                    ),
                ),
                Div(
                    *[
                        Div(
                            Icon(n["icon"], cls="h-4 w-4 shrink-0 mt-0.5"),
                            Div(
                                P(n["title"], cls="text-sm font-medium"),
                                P(n["desc"], cls="text-xs text-muted-foreground"),
                            ),
                            Button(
                                Icon("lucide:x", cls="h-3 w-3"),
                                size="icon", variant="ghost", cls="h-6 w-6 ml-auto shrink-0",
                                data_on_click=n["sig"].set(False),
                                aria_label="Dismiss",
                            ),
                            data_show=n["sig"],
                            cls="flex items-start gap-3 p-3 rounded-md border",
                        )
                        for n in notifications
                    ],
                    cls="space-y-2 px-4",
                ),
                SheetFooter(
                    Button(
                        "Clear all", variant="outline", size="sm",
                        data_on_click=[s.set(False) for s in sigs],
                        data_attr_disabled=count.eq(0),
                    ),
                ),
            ),
        ),
    )


API_REFERENCE = build_api_reference(
    components=[
        Component("Sheet", "Root container managing open state via Datastar signal"),
        Component("SheetTrigger", "Button that opens the sheet"),
        Component("SheetContent", "Panel container; supports side and size"),
        Component("SheetHeader", "Header layout for title and description"),
        Component("SheetTitle", "Accessible title linked to content"),
        Component("SheetDescription", "Supplementary description text"),
        Component("SheetFooter", "Footer area for actions"),
        Component("SheetClose", "Action that closes the sheet"),
    ],
    main_props=[
        Prop("signal", "str | Signal", "Signal name for open state", "auto-generated"),
        Prop("modal", "bool", "Use showModal() for focus trapping and backdrop", "True"),
        Prop("side", "Literal['top','right','bottom','left']", "Edge the sheet slides from", "'right'"),
        Prop("size", "Literal['sm','md','lg','xl','full']", "Width constraint for left/right sheets", "'sm'"),
        Prop("show_close", "bool", "Show the default close button", "True"),
    ]
)


EXAMPLES_DATA = [
    {"fn": default_example, "title": "Default", "description": "Simple edit profile sheet showing all core sub-components"},
    {"fn": side_positioning_example, "title": "Side", "description": "Sheets sliding from all four screen edges"},
    {"fn": sizes_example, "title": "Sizes", "description": "Width variants from small to extra large"},
    {"fn": no_close_button_example, "title": "No Close Button", "description": "Custom close with show_close=False"},
    {"fn": notifications_example, "title": "Notifications", "description": "Per-item dismiss with reactive unread count and Clear all [Signal, data_show, sum(), data_text]"},
]


def create_sheet_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)
