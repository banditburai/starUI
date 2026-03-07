TITLE = "Drawer"
DESCRIPTION = "A panel that slides from any screen edge with optional drag-to-dismiss."
CATEGORY = "overlay"
ORDER = 152
STATUS = "stable"

from starhtml import Div, P, Span, Signal, Icon

from components.button import Button
from components.drawer import (
    Drawer,
    DrawerClose,
    DrawerContent,
    DrawerDescription,
    DrawerFooter,
    DrawerHeader,
    DrawerTitle,
    DrawerTrigger,
)
from components.slider import SliderWithLabel
from utils import Component, Prop, auto_generate_page, build_api_reference, with_code


@with_code
def default_example():
    return Drawer(
        DrawerTrigger("Set Timer"),
        DrawerContent(
            DrawerHeader(
                DrawerTitle("Focus timer"),
                DrawerDescription("How long do you want to focus?"),
            ),
            Div(
                SliderWithLabel(
                    label="Duration",
                    default_value=25,
                    min=5,
                    max=60,
                    step=5,
                    value_text=" min",
                ),
                cls="px-4",
            ),
            DrawerFooter(
                Button("Start", cls="w-full"),
                DrawerClose("Cancel", variant="outline", cls="w-full"),
            ),
        ),
    )


@with_code
def direction_example():
    demos = [
        ("bottom", "Share", "Send this to a friend or save for later."),
        ("right", "Filters", "Narrow down your search results."),
        ("top", "Updates", "2 items need your attention."),
        ("left", "Menu", "Jump to a different section."),
    ]

    def make_drawer(d, title, desc):
        return Drawer(
            DrawerTrigger(title, variant="outline"),
            DrawerContent(
                DrawerHeader(
                    DrawerTitle(title),
                    DrawerDescription(desc),
                ),
                DrawerFooter(DrawerClose("Close", variant="outline")),
                direction=d,
            ),
        )

    return Div(
        *[make_drawer(*demo) for demo in demos],
        cls="flex flex-wrap gap-2 justify-center",
    )


@with_code
def reactive_example():
    items = [
        ("Espresso", "$4.50", Signal("dr_esp", True)),
        ("Almond croissant", "$3.00", Signal("dr_croi", True)),
        ("Fresh juice", "$5.50", Signal("dr_oj", False)),
    ]
    sigs = [s for _, _, s in items]
    count = sum(sigs)

    return Div(
        sigs,
        Drawer(
            DrawerTrigger(
                Icon("lucide:shopping-bag", cls="size-4"),
                Span(data_text=count, cls="text-xs"),
                variant="outline",
            ),
            DrawerContent(
                DrawerHeader(
                    DrawerTitle("Your order"),
                    DrawerDescription(
                        Span(data_text=count), " items",
                    ),
                ),
                Div(
                    *[
                        Div(
                            Div(
                                P(name, cls="text-sm font-medium"),
                                P(price, cls="text-xs text-muted-foreground"),
                            ),
                            Button(
                                Icon("lucide:x", cls="size-3"),
                                variant="ghost", size="icon",
                                cls="size-7 shrink-0",
                                data_on_click=sig.set(False),
                                aria_label=f"Remove {name}",
                            ),
                            data_show=sig,
                            cls="flex items-center justify-between p-2 rounded-md border",
                        )
                        for name, price, sig in items
                    ],
                    P(
                        "Your order is empty",
                        data_show=count.eq(0),
                        cls="text-sm text-muted-foreground text-center py-4",
                    ),
                    cls="space-y-2 px-4",
                ),
                DrawerFooter(
                    Button(
                        "Checkout", cls="w-full",
                        data_attr_disabled=count.eq(0),
                    ),
                    Button(
                        "Reset order", variant="ghost", cls="w-full",
                        data_on_click=[s.set(True) for s in sigs],
                    ),
                ),
            ),
        ),
    )


@with_code
def no_handle_example():
    return Drawer(
        DrawerTrigger("Cookie Settings", variant="outline"),
        DrawerContent(
            DrawerHeader(
                DrawerTitle("Cookie preferences"),
                DrawerDescription(
                    "We use cookies to keep things running and improve your experience."
                ),
            ),
            Div(
                P(
                    "Essential cookies are always active. "
                    "Accept all to enable analytics and personalization.",
                    cls="text-sm text-muted-foreground",
                ),
                cls="px-4",
            ),
            DrawerFooter(
                DrawerClose("Accept all", variant="default", cls="w-full"),
                DrawerClose("Essential only", variant="outline", cls="w-full"),
            ),
            show_handle=False,
        ),
        dismissible=False,
    )


@with_code
def non_modal_example():
    return Drawer(
        DrawerTrigger(
            Icon("lucide:music", cls="size-4"),
            "Now Playing",
            variant="outline",
        ),
        DrawerContent(
            DrawerHeader(
                DrawerTitle("Now playing"),
                DrawerDescription("Chet Baker — Almost Blue"),
            ),
            Div(
                Div(cls="aspect-square w-48 mx-auto rounded-md bg-muted"),
                Div(
                    Button(
                        Icon("lucide:skip-back", cls="size-4"),
                        variant="ghost", size="icon",
                    ),
                    Button(
                        Icon("lucide:play", cls="size-5"),
                        variant="outline", size="icon", cls="size-10",
                    ),
                    Button(
                        Icon("lucide:skip-forward", cls="size-4"),
                        variant="ghost", size="icon",
                    ),
                    cls="flex items-center justify-center gap-4",
                ),
                cls="space-y-4 px-4",
            ),
            DrawerFooter(
                DrawerClose("Dismiss", variant="ghost", cls="w-full"),
            ),
            direction="right",
            show_close=True,
        ),
        modal=False,
    )


API_REFERENCE = build_api_reference(
    components=[
        Component("Drawer", "Root container managing open state and drag signals"),
        Component("DrawerTrigger", "Button that opens the drawer"),
        Component(
            "DrawerContent",
            "Panel container; supports direction, show_handle, and show_close",
        ),
        Component("DrawerHeader", "Header layout for title and description"),
        Component("DrawerTitle", "Accessible title linked to content"),
        Component("DrawerDescription", "Supplementary description text"),
        Component("DrawerFooter", "Footer area for actions"),
        Component("DrawerClose", "Action that closes the drawer"),
    ],
    main_props=[
        Prop("signal", "str | Signal", "Signal name for open state", "auto-generated"),
        Prop("modal", "bool", "Use showModal() for focus trapping and backdrop", "True"),
        Prop("dismissible", "bool", "Allow dismissing via click-outside and drag", "True"),
        Prop(
            "direction",
            "Literal['top','right','bottom','left']",
            "Edge the drawer slides from",
            "'bottom'",
        ),
        Prop(
            "show_handle",
            "bool | None",
            "Show the drag handle for swipe-to-dismiss (defaults to True for bottom, False otherwise)",
            "None",
        ),
        Prop("show_close", "bool", "Show the default close button", "False"),
    ],
)


EXAMPLES_DATA = [
    {
        "fn": default_example,
        "title": "Default",
        "description": "Bottom drawer with drag handle and a focus timer slider",
    },
    {
        "fn": direction_example,
        "title": "Direction",
        "description": "Drawers from all four edges — bottom gets a drag handle by default",
    },
    {
        "fn": reactive_example,
        "title": "Reactive",
        "description": "Order cart with per-item dismiss, running count, and empty state",
    },
    {
        "fn": no_handle_example,
        "title": "No Handle",
        "description": "Cookie consent with show_handle=False and dismissible=False",
    },
    {
        "fn": non_modal_example,
        "title": "Non-modal",
        "description": "Now-playing panel that doesn't trap focus or show a backdrop",
    },
]


def create_drawer_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)
