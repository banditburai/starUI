"""
AlertDialog component documentation - Convention-based functional approach.
Clean, minimal, and easy to extend.
"""

TITLE = "Alert Dialog"
DESCRIPTION = "A modal dialog that interrupts the user with important content and expects a response."
CATEGORY = "overlay"
ORDER = 45
STATUS = "stable"

from starhtml import Div, P, Icon, Span, Ul, Li, Signal, js
from starui.registry.components.alert_dialog import (
    AlertDialog, AlertDialogTrigger, AlertDialogContent,
    AlertDialogHeader, AlertDialogFooter, AlertDialogTitle,
    AlertDialogDescription, AlertDialogAction, AlertDialogCancel
)
from starui.registry.components.button import Button
from starui.registry.components.card import Card, CardHeader, CardContent, CardTitle, CardDescription
from starui.registry.components.input import InputWithLabel
from starui.registry.components.checkbox import CheckboxWithLabel
from utils import auto_generate_page, with_code, Prop, Component, build_api_reference




@with_code
def hero_alert_dialog_example():
    return AlertDialog(
        AlertDialogTrigger("Delete Item", variant="destructive"),
        AlertDialogContent(
            AlertDialogHeader(
                AlertDialogTitle("Are you absolutely sure?"),
                AlertDialogDescription(
                    "This action cannot be undone. This will permanently delete your item and remove it from our servers."
                )
            ),
            AlertDialogFooter(
                AlertDialogCancel("Cancel"),
                AlertDialogAction("Delete", variant="destructive")
            )
        )
    )



@with_code
def destructive_alert_dialog_example():
        deletion_items = [
            "All source code and version history",
            "Issues, pull requests, and comments",
            "Wiki pages and project settings",
            "All collaborator associations"
        ]
        
        danger_info = Div(
            P("Delete Repository", cls="font-medium"),
            P("Once deleted, it will be gone forever",
              cls="text-sm text-muted-foreground mt-1"),
            cls="flex-1"
        )

        dialog_content = AlertDialogContent(
            AlertDialogHeader(
                AlertDialogTitle(
                    Icon("lucide:alert-triangle", cls="h-6 w-6 mr-2 text-destructive"),
                    "Delete Repository"
                ),
                AlertDialogDescription(
                    "This action cannot be undone. This will permanently delete the repository and all of its contents."
                )
            ),
            Div(
                P("The following will be deleted:", cls="text-sm font-medium mb-2"),
                Ul(
                    *[Li(item, cls="text-sm text-muted-foreground") for item in deletion_items],
                    cls="list-disc list-inside space-y-1"
                ),
                cls="py-4"
            ),
            AlertDialogFooter(
                AlertDialogCancel("Cancel"),
                AlertDialogAction("Delete Repository", variant="destructive")
            )
        )

        return Card(
            CardHeader(
                CardTitle("Danger Zone"),
                CardDescription("Irreversible actions")
            ),
            CardContent(
                Div(
                    danger_info,
                    AlertDialog(
                        AlertDialogTrigger(
                            Icon("lucide:trash-2", cls="h-4 w-4 mr-2"),
                            "Delete",
                            variant="destructive",
                            size="sm"
                        ),
                        dialog_content
                    ),
                    cls="flex items-end justify-between gap-6 p-6 border rounded-lg"
                )
            ),
            cls="max-w-lg"
        )


@with_code
def unsaved_changes_alert_dialog_example():
    return Card(
        (doc_title := Signal("doc_title", "My Document")),
        (doc_author := Signal("doc_author", "John Doe")),

        CardHeader(
            CardTitle("Document Editor"),
            CardDescription("Edit your document details")
        ),
        CardContent(
            Div(
                InputWithLabel(
                    label="Document Title",
                    value="My Document",
                    signal=doc_title
                ),
                InputWithLabel(
                    label="Author",
                    value="John Doe",
                    signal=doc_author,
                    cls="mt-4"
                ),
                P("Make changes to the document fields above and try to save.",
                  cls="text-sm text-muted-foreground italic mt-4")
            ),
            Div(
                AlertDialog(
                    AlertDialogTrigger("Save & Exit"),
                    AlertDialogContent(
                        AlertDialogHeader(
                            AlertDialogTitle("Save changes?"),
                            AlertDialogDescription("You have unsaved changes. What would you like to do?")
                        ),
                        Div(
                            Div(
                                Icon("lucide:save", cls="h-4 w-4 mr-2 text-blue-500"),
                                P("Your changes:", cls="text-sm font-medium"),
                                cls="flex items-center mb-2"
                            ),
                            Div(
                                P("Title: ", Span(data_text=doc_title, cls="font-mono"), cls="text-sm"),
                                P("Author: ", Span(data_text=doc_author, cls="font-mono"), cls="text-sm"),
                                cls="space-y-1 p-3 bg-muted rounded-md"
                            ),
                            cls="py-6"
                        ),
                        AlertDialogFooter(
                            AlertDialogAction(
                                "Discard Changes",
                                variant="destructive",
                                action=[
                                    doc_title.set("My Document"),
                                    doc_author.set("John Doe")
                                ]
                            ),
                            AlertDialogCancel("Keep Editing"),
                            AlertDialogAction("Save & Exit")
                        )
                    )
                ),
                cls="mt-4"
            )
        ),
        cls="max-w-md"
    )


@with_code
def session_timeout_alert_dialog_example():
    countdown = Signal("countdown", 10)
    active = Signal("active", False)

    timeout_dialog = AlertDialog(
        AlertDialogContent(
            AlertDialogHeader(
                AlertDialogTitle("Session Expiring"),
                AlertDialogDescription(
                    "Your session expires in ",
                    Span(data_text=countdown, cls="font-bold text-orange-500"),
                    " seconds."
                )
            ),
            AlertDialogFooter(
                AlertDialogAction("Logout", variant="destructive", action=active.set(False)),
                AlertDialogAction("Stay Logged In", action=countdown.set(10))
            )
        ),
        signal="timeout_dialog"
    )

    timer = Div(data_effect=js("""
        if ($active) {
            const id = setInterval(() => {
                if (!$active) { clearInterval(id); return }
                $countdown--
                if ($countdown === 5) $timeout_dialog?.showModal()
                if ($countdown <= 0) { clearInterval(id); $active = false; $countdown = 10 }
            }, 1000)
            return () => clearInterval(id)
        }
    """))

    return Card(
        countdown, active,
        CardHeader(
            CardTitle("Session Demo"),
            CardDescription("Programmatic dialog open via signal prop")
        ),
        CardContent(
            Div(
                Button("Start Session", data_on_click=[active.set(True), countdown.set(10)]),
                data_show=~active
            ),
            Div(
                P("Session expires in: ",
                  Span(data_text=countdown, cls="font-mono font-bold text-lg"), " seconds",
                  cls="text-sm"),
                Button("Logout", data_on_click=active.set(False), variant="outline", size="sm", cls="mt-3"),
                data_show=active, cls="space-y-2"
            ),
            timer, timeout_dialog
        ),
        cls="max-w-md"
    )


@with_code
def batch_operation_alert_dialog_example():
    files = [
        {"name": "file1.txt", "checked": True},
        {"name": "file2.pdf", "checked": True},
        {"name": "file3.jpg", "checked": False},
        {"name": "file4.doc", "checked": True},
    ]

    selected = Signal("batch_selected", [i for i, f in enumerate(files) if f["checked"]])
    visible = Signal("batch_visible", list(range(len(files))))

    file_checkboxes = [
        Div(
            CheckboxWithLabel(
                label=f["name"],
                checked=f["checked"],
                data_on_change=selected.toggle_in(i)
            ),
            data_show=visible.contains(i)
        )
        for i, f in enumerate(files)
    ]

    dialog_items = [
        Li(f["name"], data_show=selected.contains(i), cls="text-sm text-muted-foreground")
        for i, f in enumerate(files)
    ]

    delete_action = js("$batch_visible = $batch_visible.filter(v => !$batch_selected.includes(v)); $batch_selected = []")

    selection_count = P(
        Span(data_text=selected.length, cls="font-bold"),
        " items selected",
        cls="text-sm text-muted-foreground"
    )

    delete_dialog = AlertDialog(
        AlertDialogTrigger(
            Icon("lucide:trash-2", cls="h-4 w-4 mr-2"),
            "Delete Selected",
            variant="destructive",
            data_attr_disabled=selected.length.eq(0)
        ),
        AlertDialogContent(
            AlertDialogHeader(
                AlertDialogTitle("Delete Multiple Items"),
                AlertDialogDescription(
                    "You are about to delete ",
                    Span(data_text=selected.length, cls="font-bold text-destructive"),
                    " items. This action cannot be undone."
                )
            ),
            Div(
                P("The following items will be deleted:", cls="text-sm font-medium mb-2"),
                Ul(*dialog_items, cls="list-disc list-inside space-y-1"),
                cls="py-4"
            ),
            AlertDialogFooter(
                AlertDialogCancel("Cancel"),
                AlertDialogAction(
                    data_text="Delete " + selected.length + " Items",
                    variant="destructive",
                    action=delete_action
                )
            )
        )
    )

    return Card(
        selected,
        visible,
        CardHeader(
            CardTitle("Batch Operations"),
            CardDescription("Confirm actions on multiple items")
        ),
        CardContent(
            Div(*file_checkboxes, cls="space-y-2"),
            Div(selection_count, delete_dialog, cls="flex items-center gap-4 mt-4")
        ),
        cls="max-w-md"
    )


EXAMPLES_DATA = [
    {"fn": hero_alert_dialog_example, "title": "Destructive Confirmation", "description": "Basic confirm/cancel pattern with a destructive action"},
    {"fn": destructive_alert_dialog_example, "title": "Rich Content", "description": "Icons, consequence lists, and Card composition for a danger zone pattern"},
    {"fn": unsaved_changes_alert_dialog_example, "title": "Reactive Content", "description": "Using action callbacks to reset signals — multi-button footer with live data preview"},
    {"fn": session_timeout_alert_dialog_example, "title": "Programmatic Open", "description": "Opening the dialog from JavaScript via the signal prop — no trigger click needed"},
    {"fn": batch_operation_alert_dialog_example, "title": "Batch Operations", "description": "Reactive selection state with dynamic button labels and conditional content"},
]

API_REFERENCE = build_api_reference(
    main_props=[
        Prop("signal", "str | Signal", "Named signal for programmatic open/close. Creates a DOM ref accessible as $name in Datastar expressions", "auto-generated"),
        Prop("cls", "str", "Additional CSS classes for the dialog element", "''"),
    ],
    components=[
        Component("AlertDialog", "Root container that manages dialog open/close state"),
        Component("AlertDialogTrigger", "Button that opens the dialog. Props: variant ('default' | 'destructive'), size, and all Button props are passed through"),
        Component("AlertDialogContent", "Dialog content container rendered inside the native <dialog> element"),
        Component("AlertDialogHeader", "Flex column layout for title and description"),
        Component("AlertDialogTitle", "Dialog title — rendered as <h2> with aria-labelledby linkage"),
        Component("AlertDialogDescription", "Dialog description — rendered as <p> with aria-describedby linkage"),
        Component("AlertDialogFooter", "Footer layout — stacks vertically on mobile, horizontal on sm+"),
        Component("AlertDialogAction", "Confirm button. Props: action (Any) — signal setters or js() to run before close; variant ('default' | 'destructive')"),
        Component("AlertDialogCancel", "Cancel button — always renders with variant='outline'. Closes the dialog with no additional action"),
    ]
)



def create_alert_dialog_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)