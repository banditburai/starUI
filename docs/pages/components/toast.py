"""
Toast component documentation — Brief notifications that appear temporarily.
"""

TITLE = "Toast"
DESCRIPTION = "A brief notification that appears temporarily."
CATEGORY = "ui"
ORDER = 93
STATUS = "stable"

from starhtml import Div, get, js, set_timeout
from starui.registry.components.toast import Toaster, toast
from starui.registry.components.button import Button
from utils import auto_generate_page, with_code, Prop, Component, build_api_reference


USAGE_CODE = '''\
from starui.registry.components.toast import Toaster, toast

# Place Toaster once in your layout
Toaster()

# Client-side — trigger from any button
Button("Save", data_on_click=toast.success("Profile updated", "Name and email saved."))

# Server-side — trigger from an SSE route
from starui.registry.components.toast import ToastQueue

@rt("/process")
@sse
async def process():
    t = ToastQueue()
    yield t.success("Done", "Report generated successfully")
'''

USAGE_DESCRIPTION = "Place the Toaster component once in your root layout. Use toast() for instant client-side feedback, or ToastQueue in SSE routes for server-driven notifications."


@with_code
def default_example():
    return Div(
        Toaster(),
        Button(
            "Save changes",
            data_on_click=toast.success("Profile updated", "Display name and email saved."),
        ),
        cls="flex items-center justify-center py-6",
    )


@with_code
def variants_example():
    buttons = [
        Button("Success", variant="outline", data_on_click=toast.success("Invoice #1042 sent", "Emailed to billing@acme.com")),
        Button("Error", variant="outline", data_on_click=toast.error("Upload failed", "Image exceeds the 10 MB limit")),
        Button("Warning", variant="outline", data_on_click=toast.warning("Storage almost full", "48 MB remaining on your plan")),
        Button("Info", variant="outline", data_on_click=toast.info("Tip", "Press Ctrl+K to open the command palette")),
        Button("Default", variant="outline", data_on_click=toast("Meeting moved to 3:00 PM")),
        Button("Destructive", variant="outline", data_on_click=toast.destructive("Repository deleted", "'acme-api' has been permanently removed")),
    ]
    return Div(
        Toaster(),
        Div(*buttons, cls="flex flex-wrap items-center justify-center gap-2"),
        cls="py-6",
    )


@with_code
def duration_example():
    return Div(
        Toaster(),
        Button(
            "Quick confirmation",
            variant="outline",
            data_on_click=toast("Copied to clipboard", duration=1500),
        ),
        Button(
            "Persistent error",
            variant="outline",
            data_on_click=toast.error("Connection lost", "Check your network and try again.", duration=0),
        ),
        cls="flex items-center justify-center gap-3 py-6",
    )


@with_code
def stacking_example():
    return Div(
        Toaster(),
        Button(
            "Run 5 notifications",
            variant="outline",
            data_on_click=[
                js(toast.info('Downloading assets', '3 files remaining')),
                set_timeout(js(toast('Compiling sources')), 800),
                set_timeout(js(toast.success('Assets ready', 'Bundle size: 142 KB')), 1600),
                set_timeout(js(toast.warning('Cache expired', 'Rebuilding indexes')), 2400),
                set_timeout(js(toast.success('Build complete', 'All 12 tasks passed')), 3200),
            ],
        ),
        cls="flex items-center justify-center py-6",
    )


@with_code
def position_example():
    return Div(
        Toaster(position="top-right"),
        Button(
            "Top right toast",
            data_on_click=toast.info("Sync complete", "3 files updated from remote."),
        ),
        cls="flex items-end justify-center min-h-[250px] pb-6",
    )


def _sse_route_code():
    @rt("/deploy")
    @sse
    async def deploy():
        t = ToastQueue()
        yield t.info("Deploying...", "Building from main branch")
        await asyncio.sleep(1.5)
        yield t.success("Deployed", "v2.4.1 is live on production")
        await asyncio.sleep(4)
        yield t.clear()


@with_code
def server_side_example():
    #: include _sse_route_code()
    return Div(
        Toaster(),
        Button(
            "Deploy to production",
            variant="outline",
            data_on_click=get("/component-preview-iframe/toast-sse-demo"),  #: hide
        ),
        cls="flex items-center justify-center py-6",
    )


EXAMPLES_DATA = [
    {"fn": default_example, "title": "Default", "description": "Realistic form-save feedback using toast.success() with a title and description.", "use_iframe": True, "iframe_height": "300px", "preview_class": "!min-h-0 !p-4"},
    {"fn": variants_example, "title": "Variants", "description": "All six visual styles — success, error, warning, info, default, and destructive — with realistic microcopy.", "use_iframe": True, "iframe_height": "300px", "preview_class": "!min-h-0 !p-4"},
    {"fn": duration_example, "title": "Duration", "description": "Control how long toasts stay visible. Set duration=0 for errors that require acknowledgment.", "use_iframe": True, "iframe_height": "300px", "preview_class": "!min-h-0 !p-4"},
    {"fn": stacking_example, "title": "Stacking", "description": "Toasts queue automatically — the oldest is replaced when the stack is full.", "use_iframe": True, "iframe_height": "300px", "preview_class": "!min-h-0 !p-4"},
    {"fn": position_example, "title": "Position", "description": "Use the position prop on Toaster to control where toasts appear.", "use_iframe": True, "iframe_height": "300px", "preview_class": "!min-h-0 !p-4"},
    {"fn": server_side_example, "title": "Server-Side (SSE)", "description": "Trigger toasts from Python server code using ToastQueue — ideal for background tasks, deployments, and form processing.", "use_iframe": True, "iframe_height": "300px", "preview_class": "!min-h-0 !p-4"},
]

API_REFERENCE = build_api_reference(
    main_props=[
        Prop("position", "ToastPosition", "Where toasts appear on screen", "'bottom-right'"),
        Prop("max_visible", "int", "Maximum number of toasts shown at once", "3"),
        Prop("cls", "str", "Additional CSS classes for the toast container", "''"),
        Prop("duration", "int", "Auto-dismiss delay in milliseconds (0 to disable)", "4000"),
        Prop("variant", "ToastVariant", "Visual style — 'default', 'success', 'error', 'warning', 'info', 'destructive'", "'default'"),
    ],
    components=[
        Component("Toaster", "Fixed-position container — place once in your layout"),
        Component("toast", "Client-side helper — returns JS expressions for data_on_click"),
        Component("toast.success / .error / .warning / .info / .destructive", "Variant shortcuts — toast.success(title, description, duration)"),
        Component("ToastQueue", "Server-side toast manager for SSE routes — call .show() and return the result"),
    ],
)


def create_toast_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE, usage_code=USAGE_CODE, usage_description=USAGE_DESCRIPTION)
