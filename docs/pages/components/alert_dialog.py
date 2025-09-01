"""
AlertDialog component documentation - Convention-based functional approach.
Clean, minimal, and easy to extend.
"""

# Component metadata for auto-discovery
TITLE = "Alert Dialog"
DESCRIPTION = "A modal dialog that interrupts the user with important content and expects a response."
CATEGORY = "overlay"
ORDER = 45
STATUS = "stable"

from starhtml import Div, P, Icon, Span, H3, Code, Ul, Li
from starhtml.datastar import (
    ds_on_click, ds_show, ds_text, ds_signals, value,
    ds_bind, ds_disabled, ds_on_change, ds_effect, ds_class, ds_style
)
from starui.registry.components.alert_dialog import (
    AlertDialog, AlertDialogTrigger, AlertDialogContent,
    AlertDialogHeader, AlertDialogFooter, AlertDialogTitle,
    AlertDialogDescription, AlertDialogAction, AlertDialogCancel
)
from starui.registry.components.button import Button
from starui.registry.components.card import Card, CardHeader, CardContent, CardTitle, CardDescription
from starui.registry.components.badge import Badge
from starui.registry.components.input import InputWithLabel
from starui.registry.components.checkbox import CheckboxWithLabel
from utils import auto_generate_page
from widgets.component_preview import ComponentPreview


def examples():
    """Generate alert dialog examples using ComponentPreview with tabs."""
    
    # Basic alert dialog
    yield ComponentPreview(
        AlertDialog(
            AlertDialogTrigger("Show Alert", ref_id="basic_alert"),
            AlertDialogContent(
                AlertDialogHeader(
                    AlertDialogTitle("Heads up!"),
                    AlertDialogDescription(
                        "This is an important message that requires your attention."
                    )
                ),
                AlertDialogFooter(
                    AlertDialogCancel("Dismiss", ref_id="basic_alert"),
                    AlertDialogAction("Understood", ref_id="basic_alert")
                )
            ),
            ref_id="basic_alert"
        ),
        '''AlertDialog(
    AlertDialogTrigger("Show Alert", ref_id="basic_alert"),
    AlertDialogContent(
        AlertDialogHeader(
            AlertDialogTitle("Heads up!"),
            AlertDialogDescription("This is an important message...")
        ),
        AlertDialogFooter(
            AlertDialogCancel("Dismiss", ref_id="basic_alert"),
            AlertDialogAction("Understood", ref_id="basic_alert")
        )
    ),
    ref_id="basic_alert"
)''',
        title="Basic Alert",
        description="Simple alert dialog with cancel and action buttons"
    )
    
    # Destructive confirmation
    yield ComponentPreview(
        Card(
            CardHeader(
                CardTitle("Danger Zone"),
                CardDescription("Irreversible actions")
            ),
            CardContent(
                Div(
                    Div(
                        Div(
                            P("Delete Repository", cls="font-medium"),
                            P("Once deleted, it will be gone forever", cls="text-sm text-muted-foreground mt-1"),
                            cls="flex-1"
                        ),
                        AlertDialog(
                            AlertDialogTrigger(
                                Icon("lucide:trash-2", cls="h-4 w-4 mr-2"),
                                "Delete",
                                ref_id="delete_repo",
                                variant="destructive",
                                size="sm"
                            ),
                            AlertDialogContent(
                                Icon("lucide:alert-triangle", cls="h-12 w-12 text-destructive mx-auto mb-4"),
                                AlertDialogHeader(
                                    AlertDialogTitle("Delete Repository"),
                                    AlertDialogDescription(
                                        "This action cannot be undone. This will permanently delete the repository and all of its contents."
                                    )
                                ),
                                Div(
                                    P("The following will be deleted:", cls="text-sm font-medium mb-2"),
                                    Ul(
                                        Li("All source code and version history", cls="text-sm text-muted-foreground"),
                                        Li("Issues, pull requests, and comments", cls="text-sm text-muted-foreground"),
                                        Li("Wiki pages and project settings", cls="text-sm text-muted-foreground"),
                                        Li("All collaborator associations", cls="text-sm text-muted-foreground"),
                                        cls="list-disc list-inside space-y-1"
                                    ),
                                    cls="py-4"
                                ),
                                AlertDialogFooter(
                                    AlertDialogCancel("Cancel", ref_id="delete_repo"),
                                    AlertDialogAction(
                                        "Delete Repository",
                                        ref_id="delete_repo",
                                        variant="destructive",
                                        action="alert('Repository deleted!')"
                                    )
                                )
                            ),
                            ref_id="delete_repo"
                        ),
                        cls="flex items-end justify-between gap-6 p-6 border rounded-lg"
                    ),
                    cls="space-y-3"
                )
            ),
            cls="max-w-lg"
        ),
        '''AlertDialog(
    AlertDialogTrigger(
        Icon("lucide:trash-2"),
        "Delete",
        ref_id="delete_repo",
        variant="destructive"
    ),
    AlertDialogContent(
        Icon("lucide:alert-triangle", cls="h-12 w-12 text-destructive"),
        AlertDialogHeader(
            AlertDialogTitle("Delete Repository"),
            AlertDialogDescription("This action cannot be undone...")
        ),
        Ul(
            Li("All source code will be deleted"),
            Li("Issues and PRs will be lost"),
            Li("Wiki pages will be removed")
        ),
        AlertDialogFooter(
            AlertDialogCancel("Cancel", ref_id="delete_repo"),
            AlertDialogAction(
                "Delete Repository",
                ref_id="delete_repo",
                variant="destructive",
                action="deleteRepo()"
            )
        )
    ),
    ref_id="delete_repo"
)''',
        title="Destructive Action",
        description="High-risk action with clear warnings and consequences"
    )
    
    # Unsaved changes warning
    yield ComponentPreview(
        Card(
            CardContent(
                Div(
                    Div(
                        InputWithLabel(
                            label="Document Title",
                            value="My Document",
                            signal="doc_title"
                        ),
                        cls="mb-4"
                    ),
                    Div(
                        InputWithLabel(
                            label="Author",
                            value="John Doe",
                            signal="doc_author"
                        ),
                        cls="mb-4"
                    ),
                    Div(
                        Button(
                            "Cancel",
                            ds_on_click("$changes_made = true"),
                            variant="outline"
                        ),
                        AlertDialog(
                            AlertDialogTrigger(
                                "Save & Exit",
                                ref_id="unsaved_dialog"
                            ),
                            AlertDialogContent(
                                AlertDialogHeader(
                                    AlertDialogTitle("Save changes?"),
                                    AlertDialogDescription(
                                        "You have unsaved changes. What would you like to do?"
                                    )
                                ),
                                Div(
                                    Div(
                                        Icon("lucide:save", cls="h-4 w-4 mr-2 text-blue-500"),
                                        P("Your changes:", cls="text-sm font-medium"),
                                        cls="flex items-center mb-2"
                                    ),
                                    Div(
                                        P("Title: ", Span(ds_text("$doc_title"), cls="font-mono"), cls="text-sm"),
                                        P("Author: ", Span(ds_text("$doc_author"), cls="font-mono"), cls="text-sm"),
                                        cls="space-y-1 p-3 bg-muted rounded-md"
                                    ),
                                    cls="py-6"
                                ),
                                AlertDialogFooter(
                                    AlertDialogAction(
                                        "Discard Changes",
                                        ref_id="unsaved_dialog",
                                        variant="destructive",
                                        action="$doc_title=''; $doc_author=''; alert('Changes discarded')"
                                    ),
                                    AlertDialogCancel("Keep Editing", ref_id="unsaved_dialog"),
                                    AlertDialogAction(
                                        "Save & Exit",
                                        ref_id="unsaved_dialog",
                                        action="alert('Document saved!')"
                                    )
                                )
                            ),
                            ref_id="unsaved_dialog"
                        ),
                        cls="flex gap-2 mt-4"
                    ),
                    ds_signals(
                        doc_title=value("My Document"),
                        doc_author=value("John Doe"),
                        changes_made=False
                    )
                ),
                cls="space-y-4"
            ),
            cls="max-w-md"
        ),
        '''AlertDialog(
    Button("Save & Exit", /* trigger */),
    AlertDialogContent(
        AlertDialogHeader(
            AlertDialogTitle("Save changes?"),
            AlertDialogDescription("You have unsaved changes...")
        ),
        Div(
            P("Your changes:"),
            Div(/* display changes */)
        ),
        AlertDialogFooter(
            AlertDialogAction("Discard Changes", variant="destructive"),
            AlertDialogCancel("Keep Editing"),
            AlertDialogAction("Save & Exit")
        )
    ),
    ref_id="unsaved_dialog"
)''',
        title="Unsaved Changes",
        description="Three-option dialog for handling unsaved work"
    )
    
    # Session timeout warning
    yield ComponentPreview(
        Card(
            CardHeader(
                CardTitle("Session Management"),
                CardDescription("Login and auto-logout demonstration")
            ),
            CardContent(
                Div(
                    Div(
                        Div(
                            Button(
                                "Login",
                                ds_on_click("$logged_in = true; $session_time = 15; $timer_started = true"),
                                variant="default",
                                cls="w-full"
                            ),
                            ds_show="!$logged_in"
                        ),
                        Div(
                            P(
                                "Logged in as: user@example.com",
                                cls="text-sm font-medium mb-2"
                            ),
                            P(
                                "Session expires in: ",
                                Span(ds_text("$session_time"), cls="font-mono font-bold text-lg"),
                                " seconds",
                                cls="text-sm"
                            ),
                            Div(
                                Div(
                                    ds_style(width="`${((15 - $session_time) / 15 * 100)}%`"),
                                    cls="h-2 bg-primary rounded-full transition-all duration-1000"
                                ),
                                cls="w-full bg-secondary rounded-full h-2 mt-2"
                            ),
                            Button(
                                "Logout",
                                ds_on_click("$logged_in = false; $timer_started = false; $session_time = 15"),
                                variant="outline",
                                size="sm",
                                cls="mt-4"
                            ),
                            ds_show="$logged_in",
                            cls="space-y-2"
                        )
                    ),
                    Div(
                        ds_effect("""
                            if ($timer_started && $logged_in) {
                                const timer = setInterval(() => {
                                    $session_time--;
                                    if ($session_time === 5 && !$timeout_dialog_open) {
                                        document.getElementById('timeout_dialog').showModal();
                                        $timeout_dialog_open = true;
                                    }
                                    if ($session_time === 0) {
                                        clearInterval(timer);
                                        if ($timeout_dialog_open) {
                                            document.getElementById('timeout_dialog').close();
                                            $timeout_dialog_open = false;
                                        }
                                        alert('Session expired - logged out');
                                        $logged_in = false;
                                        $session_time = 15;
                                        $timer_started = false;
                                    }
                                }, 1000);
                                return () => {
                                    clearInterval(timer);
                                };
                            }
                        """)
                    ),
                    AlertDialog(
                        Div(),
                        AlertDialogContent(
                            Icon("lucide:clock", cls="h-12 w-12 text-orange-500 mx-auto mb-4"),
                            AlertDialogHeader(
                                AlertDialogTitle("Session Expiring Soon"),
                                AlertDialogDescription(
                                    Span("Your session will expire in "),
                                    Span(ds_text("$session_time"), cls="font-bold text-orange-500"),
                                    Span(" seconds. Do you want to continue?")
                                )
                            ),
                            AlertDialogFooter(
                                AlertDialogAction(
                                    "Logout",
                                    ref_id="timeout_dialog",
                                    variant="destructive",
                                    action="$session_time = 0; $logged_in = false; alert('Logged out')"
                                ),
                                AlertDialogAction(
                                    "Continue Session",
                                    ref_id="timeout_dialog",
                                    action="$session_time = 15; $timeout_dialog_open = false; alert('Session extended')"
                                )
                            )
                        ),
                        ref_id="timeout_dialog"
                    ),
                    ds_signals(session_time=15, timeout_dialog_open=False, timer_started=False, logged_in=False)
                )
            ),
            cls="max-w-md"
        ),
        '''// Auto-show alert when session is about to expire
AlertDialog(
    Div(ds_effect("""
        const timer = setInterval(() => {
            $session_time--;
            if ($session_time === 10) {
                $timeout_dialog.showModal();
            }
        }, 1000);
    """)),
    AlertDialogContent(
        Icon("lucide:clock"),
        AlertDialogTitle("Session Expiring Soon"),
        AlertDialogDescription(
            "Your session will expire in ",
            Span(ds_text("$session_time")),
            " seconds"
        ),
        AlertDialogFooter(
            AlertDialogAction("Logout", variant="destructive"),
            AlertDialogAction("Continue Session")
        )
    ),
    ref_id="timeout_dialog"
)''',
        title="Session Timeout",
        description="Auto-triggered alert with countdown timer"
    )
    
    # Batch operation confirmation
    yield ComponentPreview(
        Card(
            CardHeader(
                CardTitle("Batch Operations"),
                CardDescription("Confirm actions on multiple items")
            ),
            CardContent(
                Div(
                    Div(
                        CheckboxWithLabel(label="file1.txt", signal="file1", checked=True),
                        CheckboxWithLabel(label="file2.pdf", signal="file2", checked=True),
                        CheckboxWithLabel(label="file3.jpg", signal="file3"),
                        CheckboxWithLabel(label="file4.doc", signal="file4", checked=True),
                        cls="space-y-2"
                    ),
                    Div(
                        P(
                            Span(ds_text("[$file1, $file2, $file3, $file4].filter(Boolean).length"), cls="font-bold"),
                            " items selected",
                            cls="text-sm text-muted-foreground"
                        ),
                        AlertDialog(
                            AlertDialogTrigger(
                                Icon("lucide:trash-2", cls="h-4 w-4 mr-2"),
                                "Delete Selected",
                                variant="destructive",
                                ref_id="batch_dialog",
                                ds_disabled="!$file1 && !$file2 && !$file3 && !$file4"
                            ),
                            AlertDialogContent(
                                AlertDialogHeader(
                                    AlertDialogTitle("Delete Multiple Items"),
                                    AlertDialogDescription(
                                        Span("You are about to delete "),
                                        Span(
                                            ds_text("[$file1, $file2, $file3, $file4].filter(Boolean).length"),
                                            cls="font-bold text-destructive"
                                        ),
                                        Span(" items. This action cannot be undone.")
                                    )
                                ),
                                Div(
                                    P("The following items will be deleted:", cls="text-sm font-medium mb-2"),
                                    Ul(
                                        Li("file1.txt", ds_show="$file1", cls="text-sm text-muted-foreground"),
                                        Li("file2.pdf", ds_show="$file2", cls="text-sm text-muted-foreground"),
                                        Li("file3.jpg", ds_show="$file3", cls="text-sm text-muted-foreground"),
                                        Li("file4.doc", ds_show="$file4", cls="text-sm text-muted-foreground"),
                                        cls="list-disc list-inside space-y-1"
                                    ),
                                    cls="py-4"
                                ),
                                AlertDialogFooter(
                                    AlertDialogCancel("Cancel", ref_id="batch_dialog"),
                                    AlertDialogAction(
                                        ds_text("'Delete ' + [$file1, $file2, $file3, $file4].filter(Boolean).length + ' Items'"),
                                        ref_id="batch_dialog",
                                        variant="destructive",
                                        action="alert('Items deleted'); $file1=false; $file2=false; $file3=false; $file4=false"
                                    )
                                )
                            ),
                            ref_id="batch_dialog"
                        ),
                        cls="flex items-center gap-4 mt-4"
                    ),
                    ds_signals(file1=True, file2=True, file3=False, file4=True, batch_dialog_open=False),
                    cls="space-y-2"
                )
            ),
            cls="max-w-md"
        ),
        '''AlertDialog(
    Button(
        "Delete Selected",
        ds_disabled="!hasSelection",
        variant="destructive"
    ),
    AlertDialogContent(
        AlertDialogTitle("Delete Multiple Items"),
        AlertDialogDescription(
            "You are about to delete ",
            Span(ds_text("selectedCount")),
            " items"
        ),
        Ul(/* list selected items */),
        AlertDialogFooter(
            AlertDialogCancel("Cancel"),
            AlertDialogAction(
                ds_text("'Delete ' + selectedCount + ' Items'"),
                variant="destructive"
            )
        )
    ),
    ref_id="batch_dialog"
)''',
        title="Batch Operations",
        description="Confirm actions on multiple selected items"
    )
    
    # Payment confirmation
    yield ComponentPreview(
        Card(
            CardHeader(
                CardTitle("Complete Purchase"),
                CardDescription("Review your order")
            ),
            CardContent(
                Div(
                    Div(
                        P("Product:", cls="text-sm text-muted-foreground"),
                        P("Premium Plan", cls="font-medium"),
                        cls="flex justify-between py-2"
                    ),
                    Div(
                        P("Price:", cls="text-sm text-muted-foreground"),
                        P("$99.00", cls="font-medium"),
                        cls="flex justify-between py-2"
                    ),
                    Div(
                        P("Tax:", cls="text-sm text-muted-foreground"),
                        P("$9.90", cls="font-medium"),
                        cls="flex justify-between py-2 border-b"
                    ),
                    Div(
                        P("Total:", cls="font-medium"),
                        P("$108.90", cls="text-xl font-bold"),
                        cls="flex justify-between py-2"
                    ),
                    AlertDialog(
                        AlertDialogTrigger(
                            Icon("lucide:credit-card", cls="h-4 w-4 mr-2"),
                            "Complete Purchase",
                            ref_id="payment_dialog",
                            cls="w-full"
                        ),
                        AlertDialogContent(
                            AlertDialogHeader(
                                AlertDialogTitle(
                                    Icon("lucide:shield-check", cls="h-5 w-5 text-green-500 inline mr-2"),
                                    "Confirm Payment"
                                ),
                                AlertDialogDescription("Please review and confirm your purchase")
                            ),
                            Div(
                                Div(
                                    Div(
                                        Icon("lucide:lock", cls="h-4 w-4 text-green-500"),
                                        P("Secure Payment", cls="text-sm font-medium"),
                                        cls="flex items-center gap-2"
                                    ),
                                    P("Your payment information is encrypted and secure", cls="text-xs text-muted-foreground mt-1"),
                                    cls="p-3 bg-green-50 dark:bg-green-950/20 rounded-md mb-4"
                                ),
                                Div(
                                    P("Amount to charge: ", Span("$108.90", cls="font-bold text-lg")),
                                    P("Card ending in: ", Span("****4242", cls="font-mono")),
                                    cls="space-y-2"
                                ),
                                cls="py-4"
                            ),
                            AlertDialogFooter(
                                AlertDialogCancel("Cancel", ref_id="payment_dialog"),
                                AlertDialogAction(
                                    "Confirm Payment",
                                    ref_id="payment_dialog",
                                    action="alert('Payment successful! Order #12345')"
                                )
                            )
                        ),
                        ref_id="payment_dialog"
                    ),
                    ds_signals(payment_dialog_open=False)
                )
            ),
            cls="max-w-sm"
        ),
        '''AlertDialog(
    Button("Complete Purchase"),
    AlertDialogContent(
        Icon("lucide:shield-check", cls="text-green-500"),
        AlertDialogTitle("Confirm Payment"),
        Div(
            Div(
                Icon("lucide:lock"),
                P("Secure Payment")
            ),
            P("Amount: $108.90"),
            P("Card: ****4242")
        ),
        AlertDialogFooter(
            AlertDialogCancel("Cancel"),
            AlertDialogAction("Confirm Payment")
        )
    ),
    ref_id="payment_dialog"
)''',
        title="Payment Confirmation",
        description="Secure payment confirmation with trust indicators"
    )


def create_alert_dialog_docs():
    """Create alert dialog documentation page using convention-based approach."""
    
    api_reference = {
        "props": [
            {
                "name": "trigger",
                "type": "FT",
                "description": "The trigger element (usually AlertDialogTrigger)"
            },
            {
                "name": "content",
                "type": "FT",
                "description": "The dialog content (usually AlertDialogContent)"
            },
            {
                "name": "ref_id",
                "type": "str",
                "description": "Unique identifier for the alert dialog instance"
            }
        ],
        "sub_components": [
            {
                "name": "AlertDialogTrigger",
                "description": "Button that opens the alert dialog",
                "props": [
                    {
                        "name": "ref_id",
                        "type": "str",
                        "description": "Must match the AlertDialog's ref_id"
                    },
                    {
                        "name": "variant",
                        "type": "str",
                        "default": "'default'",
                        "description": "Button variant"
                    }
                ]
            },
            {
                "name": "AlertDialogContent",
                "description": "Container for alert dialog content"
            },
            {
                "name": "AlertDialogHeader",
                "description": "Container for title and description"
            },
            {
                "name": "AlertDialogTitle",
                "description": "The alert's title"
            },
            {
                "name": "AlertDialogDescription",
                "description": "Subtitle or description text"
            },
            {
                "name": "AlertDialogFooter",
                "description": "Container for action buttons"
            },
            {
                "name": "AlertDialogAction",
                "description": "Primary action button",
                "props": [
                    {
                        "name": "ref_id",
                        "type": "str",
                        "description": "Must match the AlertDialog's ref_id"
                    },
                    {
                        "name": "action",
                        "type": "str",
                        "default": "''",
                        "description": "JavaScript to execute before closing"
                    },
                    {
                        "name": "variant",
                        "type": "Literal['default', 'destructive']",
                        "default": "'default'",
                        "description": "Button variant"
                    }
                ]
            },
            {
                "name": "AlertDialogCancel",
                "description": "Cancel button",
                "props": [
                    {
                        "name": "ref_id",
                        "type": "str",
                        "description": "Must match the AlertDialog's ref_id"
                    }
                ]
            }
        ]
    }
    
    # Hero example
    hero_example = ComponentPreview(
        AlertDialog(
            AlertDialogTrigger(
                "Delete Item",
                ref_id="hero_alert",
                variant="destructive"
            ),
            AlertDialogContent(
                AlertDialogHeader(
                    AlertDialogTitle("Are you absolutely sure?"),
                    AlertDialogDescription(
                        "This action cannot be undone. This will permanently delete your item and remove it from our servers."
                    )
                ),
                AlertDialogFooter(
                    AlertDialogCancel("Cancel", ref_id="hero_alert"),
                    AlertDialogAction(
                        "Delete",
                        ref_id="hero_alert",
                        variant="destructive",
                        action="alert('Item deleted!')"
                    )
                )
            ),
            ref_id="hero_alert"
        ),
        '''AlertDialog(
    AlertDialogTrigger("Delete Item", ref_id="hero_alert", variant="destructive"),
    AlertDialogContent(
        AlertDialogHeader(
            AlertDialogTitle("Are you absolutely sure?"),
            AlertDialogDescription("This action cannot be undone...")
        ),
        AlertDialogFooter(
            AlertDialogCancel("Cancel", ref_id="hero_alert"),
            AlertDialogAction("Delete", ref_id="hero_alert", variant="destructive")
        )
    ),
    ref_id="hero_alert"
)''',
        copy_button=True
    )
    
    return auto_generate_page(
        TITLE,
        DESCRIPTION,
        list(examples()),
        cli_command="star add alert-dialog",
        api_reference=api_reference,
        hero_example=hero_example,
        component_slug="alert-dialog"
    )