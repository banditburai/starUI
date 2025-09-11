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
from utils import auto_generate_page, with_code, Prop, Component, build_api_reference
from widgets.component_preview import ComponentPreview


def examples():
    """Generate alert dialog examples using ComponentPreview with tabs."""
    
    # Basic alert dialog
    @with_code
    def basic_alert_dialog_example():
        return AlertDialog(
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
        )
    
    yield ComponentPreview(
        basic_alert_dialog_example(),
        basic_alert_dialog_example.code,
        title="Basic Alert",
        description="Simple alert dialog with cancel and action buttons"
    )
    
    # Destructive confirmation
    @with_code
    def destructive_alert_dialog_example():
        return Card(
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
                                AlertDialogHeader(
                                    AlertDialogTitle(
                                        Icon("lucide:alert-triangle", width="24", height="24", cls="mr-2 text-destructive"),
                                        "Delete Repository"
                                    ),
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
                                        action="console.log('Repository deleted')"
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
        )
    
    yield ComponentPreview(
        destructive_alert_dialog_example(),
        destructive_alert_dialog_example.code,
        title="Destructive Action",
        description="High-risk action with clear warnings and consequences"
    )
    
    # Unsaved changes warning
    @with_code
    def unsaved_changes_alert_dialog_example():
        return Card(
            CardHeader(
                CardTitle("Document Editor"),
                CardDescription("Edit your document details")
            ),
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
                        Div(
                            P("Make changes to the document fields above and try to save.", cls="text-sm text-muted-foreground italic mb-2")
                        ),
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
                                        action="$doc_title='My Document'; $doc_author='John Doe'; console.log('Changes discarded')"
                                    ),
                                    AlertDialogCancel("Keep Editing", ref_id="unsaved_dialog"),
                                    AlertDialogAction(
                                        "Save & Exit",
                                        ref_id="unsaved_dialog",
                                        action="console.log('Document saved')"
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
        )
    
    yield ComponentPreview(
        unsaved_changes_alert_dialog_example(),
        unsaved_changes_alert_dialog_example.code,
        title="Unsaved Changes",
        description="Three-option dialog for handling unsaved work"
    )
    
    # Session timeout warning
    @with_code
    def session_timeout_alert_dialog_example():
        return Div(
            Card(
                CardHeader(
                CardTitle("Session Management"),
                CardDescription("Login and auto-logout demonstration")
            ),
            CardContent(
                Div(
                    ds_signals(session_time=15, timeout_dialog_open=False, timer_started=False, logged_in=False),
                    Div(
                        Button(
                            "Login",
                            ds_on_click("console.log('Login button clicked!', {before: $logged_in}); $logged_in = true; $session_time = 15; $timer_started = true; console.log('After click:', {logged_in: $logged_in, timer: $timer_started})"),
                            variant="default"
                        ),
                        ds_show("!$logged_in")
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
                                ds_style(width="`${Math.max(0, ($session_time / 15 * 100))}%`"),
                                cls="h-2 bg-orange-500 rounded-full transition-all duration-1000"
                            ),
                            cls="w-full bg-secondary rounded-full h-2 mt-2"
                        ),
                        Button(
                            "Logout",
                            ds_on_click("console.log('Logout clicked'); $logged_in = false; $timer_started = false; $session_time = 15"),
                            variant="outline",
                            size="sm",
                            cls="mt-4"
                        ),
                        ds_show("$logged_in"),
                        cls="space-y-2"
                    ),
                    Div(
                        ds_effect("""
                            if ($timer_started && $logged_in) {
                                console.log('Starting session timer...');
                                const timer = setInterval(() => {
                                    if (!$logged_in || !$timer_started) {
                                        console.log('Timer stopped - user logged out');
                                        clearInterval(timer);
                                        return;
                                    }
                                    
                                    if ($session_time > 0) {
                                        $session_time = $session_time - 1;
                                        console.log('Session time:', $session_time);
                                        
                                        // Show dialog at 5 seconds
                                        if ($session_time === 5 && !$timeout_dialog_open) {
                                            console.log('Showing timeout warning dialog');
                                            setTimeout(() => {
                                                const dialog = document.getElementById('timeout_dialog');
                                                if (dialog) {
                                                    dialog.showModal();
                                                    $timeout_dialog_open = true;
                                                } else {
                                                    console.error('Could not find timeout dialog with id timeout_dialog');
                                                }
                                            }, 0);
                                        }
                                        
                                        // Auto logout at 0 seconds
                                        if ($session_time === 0) {
                                            console.log('Session expired - logging out');
                                            clearInterval(timer);
                                            if ($timeout_dialog_open) {
                                                const dialog = document.getElementById('timeout_dialog');
                                                if (dialog) {
                                                    dialog.close();
                                                }
                                                $timeout_dialog_open = false;
                                            }
                                            $logged_in = false;
                                            $session_time = 15;
                                            $timer_started = false;
                                        }
                                    }
                                }, 1000);
                                
                                // Cleanup function
                                return () => {
                                    console.log('Cleaning up session timer');
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
                                    "Logout Now",
                                    ref_id="timeout_dialog",
                                    variant="destructive",
                                    action="$logged_in = false; $timer_started = false; $session_time = 15; $timeout_dialog_open = false"
                                ),
                                AlertDialogAction(
                                    "Continue Session",
                                    ref_id="timeout_dialog",
                                    action="$session_time = 15; $timeout_dialog_open = false"
                                )
                            )
                        ),
                        ref_id="timeout_dialog"
                    )
                )
            ),
            cls="w-full max-w-lg"
        ),
        cls="w-full max-w-2xl"
    )
    
    yield ComponentPreview(
        session_timeout_alert_dialog_example(),
        session_timeout_alert_dialog_example.code,
        title="Session Timeout",
        description="Auto-triggered alert with countdown timer"
    )
    
    # Batch operation confirmation
    @with_code
    def batch_operation_alert_dialog_example():
        return Card(
            CardHeader(
                CardTitle("Batch Operations"),
                CardDescription("Confirm actions on multiple items")
            ),
            CardContent(
                Div(
                    Div(
                        Div(
                            CheckboxWithLabel(label="file1.txt", signal="file1", checked=True),
                            ds_show("$file1_exists")
                        ),
                        Div(
                            CheckboxWithLabel(label="file2.pdf", signal="file2", checked=True),
                            ds_show("$file2_exists")
                        ),
                        Div(
                            CheckboxWithLabel(label="file3.jpg", signal="file3"),
                            ds_show("$file3_exists")
                        ),
                        Div(
                            CheckboxWithLabel(label="file4.doc", signal="file4", checked=True),
                            ds_show("$file4_exists")
                        ),
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
                                        Li("file1.txt", ds_show("$file1"), cls="text-sm text-muted-foreground"),
                                        Li("file2.pdf", ds_show("$file2"), cls="text-sm text-muted-foreground"),
                                        Li("file3.jpg", ds_show("$file3"), cls="text-sm text-muted-foreground"),
                                        Li("file4.doc", ds_show("$file4"), cls="text-sm text-muted-foreground"),
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
                                        action="console.log('Action executing', $batch_dialog); if($file1) $file1_exists=false; if($file2) $file2_exists=false; if($file3) $file3_exists=false; if($file4) $file4_exists=false"
                                    )
                                )
                            ),
                            ref_id="batch_dialog"
                        ),
                        cls="flex items-center gap-4 mt-4"
                    ),
                    ds_signals(file1=True, file2=True, file3=False, file4=True, file1_exists=True, file2_exists=True, file3_exists=True, file4_exists=True, batch_dialog_open=False),
                    cls="space-y-2"
                )
            ),
            cls="max-w-md"
        )
    
    yield ComponentPreview(
        batch_operation_alert_dialog_example(),
        batch_operation_alert_dialog_example.code,
        title="Batch Operations",
        description="Confirm actions on multiple selected items"
    )
    
    # Payment confirmation
    @with_code
    def payment_confirmation_alert_dialog_example():
        return Card(
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
                                    Icon("lucide:shield-check", width="24", height="24", cls="mr-2 text-green-500"),
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
                                    action="console.log('Payment successful! Order #12345')"
                                )
                            )
                        ),
                        ref_id="payment_dialog"
                    ),
                    ds_signals(payment_dialog_open=False)
                )
            ),
            cls="max-w-sm"
        )
    
    yield ComponentPreview(
        payment_confirmation_alert_dialog_example(),
        payment_confirmation_alert_dialog_example.code,
        title="Payment Confirmation",
        description="Secure payment confirmation with trust indicators"
    )


def create_alert_dialog_docs():
    """Create alert dialog documentation page using convention-based approach."""
    
    # For AlertDialog, users need to understand the building blocks (sub-components)
    # rather than the main props, since examples show usage patterns clearly
    api_reference = build_api_reference(
        components=[
            Component("AlertDialog", "Main container component that manages dialog state"),
            Component("AlertDialogTrigger", "Button that opens the alert dialog"),
            Component("AlertDialogContent", "Container for all dialog content"),
            Component("AlertDialogHeader", "Container for title and description"),
            Component("AlertDialogTitle", "Primary heading text for the alert"),
            Component("AlertDialogDescription", "Supporting description text"),
            Component("AlertDialogFooter", "Container for action buttons"),
            Component("AlertDialogAction", "Primary action button (confirms/proceeds)"),
            Component("AlertDialogCancel", "Secondary button (dismisses dialog)"),
        ]
    )
    
    # Hero example
    @with_code
    def hero_alert_dialog_example():
        return AlertDialog(
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
                        action="console.log('Item deleted')"
                    )
                )
            ),
            ref_id="hero_alert"
        )
    
    hero_example = ComponentPreview(
        hero_alert_dialog_example(),
        hero_alert_dialog_example.code,
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