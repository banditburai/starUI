"""
Dialog component documentation - Convention-based functional approach.
Clean, minimal, and easy to extend.
"""

# Component metadata for auto-discovery
TITLE = "Dialog"
DESCRIPTION = "A modal dialog component using the native HTML dialog element for accessibility and performance."
CATEGORY = "overlay"
ORDER = 40
STATUS = "stable"

from starhtml import Div, P, Input, Label, Icon, Span, H2, H3, Form, Code, Ul, Li, Style
from starhtml.datastar import (
    ds_on_click, ds_show, ds_text, ds_signals, value,
    ds_bind, ds_disabled, ds_on_change, ds_effect, ds_class, ds_style
)
from starui.registry.components.dialog import (
    Dialog, DialogTrigger, DialogContent, DialogHeader, DialogFooter,
    DialogTitle, DialogDescription, DialogClose
)
from starui.registry.components.button import Button
from starui.registry.components.input import Input as UIInput, InputWithLabel
from starui.registry.components.textarea import TextareaWithLabel
from starui.registry.components.card import Card, CardHeader, CardContent, CardTitle, CardDescription
from starui.registry.components.badge import Badge
from starui.registry.components.separator import Separator
from starui.registry.components.select import SelectWithLabel
from starui.registry.components.checkbox import CheckboxWithLabel
from utils import auto_generate_page
from widgets.component_preview import ComponentPreview


def examples():
    """Generate dialog examples using ComponentPreview with tabs."""
    
    # Basic dialog
    yield ComponentPreview(
        Dialog(
            DialogTrigger("Open Dialog", ref_id="basic_dialog"),
            DialogContent(
                DialogHeader(
                    DialogTitle("Welcome to StarUI"),
                    DialogDescription(
                        "This is a simple dialog demonstrating the basic structure and functionality."
                    )
                ),
                P("Dialog content goes here. You can include any content you need.", cls="py-4"),
                DialogFooter(
                    DialogClose("Got it", ref_id="basic_dialog")
                )
            ),
            ref_id="basic_dialog"
        ),
        '''Dialog(
    DialogTrigger("Open Dialog", ref_id="basic_dialog"),
    DialogContent(
        DialogHeader(
            DialogTitle("Welcome to StarUI"),
            DialogDescription("This is a simple dialog...")
        ),
        P("Dialog content goes here."),
        DialogFooter(
            DialogClose("Got it", ref_id="basic_dialog")
        )
    ),
    ref_id="basic_dialog"
)''',
        title="Basic Dialog",
        description="Simple dialog with title, description, and close button"
    )
    
    # Confirmation dialog
    yield ComponentPreview(
        Dialog(
            DialogTrigger(
                Icon("lucide:trash-2", cls="h-4 w-4 mr-2"),
                "Delete Account",
                ref_id="confirm_dialog",
                variant="destructive"
            ),
            DialogContent(
                DialogHeader(
                    DialogTitle("Are you absolutely sure?"),
                    DialogDescription(
                        "This action cannot be undone. This will permanently delete your "
                        "account and remove your data from our servers."
                    )
                ),
                Div(
                    Div(
                        Icon("lucide:alert-triangle", cls="h-6 w-6 text-destructive flex-shrink-0 mt-0.5"),
                        Div(
                            P(
                                "Warning: ",
                                Span("This action is irreversible", cls="font-semibold"),
                                cls="text-sm"
                            ),
                            Ul(
                                Li("All your projects will be deleted", cls="text-sm"),
                                Li("Your subscription will be cancelled", cls="text-sm"),
                                Li("You will lose access to all shared resources", cls="text-sm"),
                                cls="list-disc list-inside mt-2 space-y-1 text-muted-foreground"
                            ),
                        ),
                        cls="flex gap-3"
                    ),
                    cls="py-4"
                ),
                DialogFooter(
                    DialogClose("Cancel", ref_id="confirm_dialog", variant="outline"),
                    DialogClose(
                        "Delete Account",
                        ref_id="confirm_dialog",
                        variant="destructive",
                        value="delete",
                        onclick="alert('Account deleted!')"
                    )
                )
            ),
            ref_id="confirm_dialog"
        ),
        '''Dialog(
    DialogTrigger(
        Icon("lucide:trash-2"),
        "Delete Account",
        ref_id="confirm_dialog",
        variant="destructive"
    ),
    DialogContent(
        DialogHeader(
            DialogTitle("Are you absolutely sure?"),
            DialogDescription("This action cannot be undone...")
        ),
        Div(
            P(Icon("lucide:alert-triangle"), "Warning: This is irreversible"),
            Ul(
                Li("All projects will be deleted"),
                Li("Subscription will be cancelled"),
                Li("Access will be revoked")
            )
        ),
        DialogFooter(
            DialogClose("Cancel", variant="outline"),
            DialogClose("Delete Account", variant="destructive", value="delete")
        )
    ),
    ref_id="confirm_dialog"
)''',
        title="Confirmation Dialog",
        description="Destructive action confirmation with warnings"
    )
    
    # Form dialog
    yield ComponentPreview(
        Dialog(
            DialogTrigger(
                Icon("lucide:user-plus", cls="h-4 w-4 mr-2"),
                "Add Team Member",
                ref_id="form_dialog"
            ),
            DialogContent(
                DialogHeader(
                    DialogTitle("Invite Team Member"),
                    DialogDescription("Add a new member to your team and assign their role")
                ),
                Form(
                    # Personal Information Section
                    Div(
                        P(
                            Icon("lucide:user", cls="h-4 w-4 inline mr-2"),
                            "Personal Information",
                            cls="text-sm font-semibold text-foreground mb-3 flex items-center"
                        ),
                        InputWithLabel(
                            label="Full Name",
                            placeholder="Enter full name",
                            signal="member_name",
                            required=True,
                            helper_text="This will be displayed in the team directory"
                        ),
                        InputWithLabel(
                            label="Email Address",
                            type="email",
                            placeholder="Enter email address",
                            signal="member_email",
                            required=True,
                            helper_text="Invitation will be sent to this email"
                        ),
                        cls="space-y-4"
                    ),
                    
                    Separator(cls="my-6"),
                    
                    # Access & Permissions Section
                    Div(
                        P(
                            Icon("lucide:shield-check", cls="h-4 w-4 inline mr-2"),
                            "Access & Permissions",
                            cls="text-sm font-semibold text-foreground mb-3 flex items-center"
                        ),
                        SelectWithLabel(
                            label="Role",
                            options=[
                                ("viewer", "Viewer - Can view projects and files"),
                                ("editor", "Editor - Can edit projects and collaborate"),
                                ("admin", "Admin - Full administrative access")
                            ],
                            value="viewer",
                            signal="member_role",
                            helper_text="Choose the appropriate permission level for this user"
                        ),
                        # Role preview card
                        Div(
                            Div(
                                Icon("lucide:eye", cls="h-5 w-5 text-blue-500"),
                                Div(
                                    P("Viewer Access", cls="font-medium text-sm"),
                                    P("Can view and comment on projects", cls="text-xs text-muted-foreground"),
                                    cls="ml-3"
                                ),
                                ds_show("$member_role_value === 'viewer'"),
                                cls="flex items-center p-3 bg-blue-50 dark:bg-blue-950/20 rounded-md border border-blue-200 dark:border-blue-800"
                            ),
                            Div(
                                Icon("lucide:edit-3", cls="h-5 w-5 text-green-500"),
                                Div(
                                    P("Editor Access", cls="font-medium text-sm"),
                                    P("Can edit, create, and manage projects", cls="text-xs text-muted-foreground"),
                                    cls="ml-3"
                                ),
                                ds_show("$member_role_value === 'editor'"),
                                cls="flex items-center p-3 bg-green-50 dark:bg-green-950/20 rounded-md border border-green-200 dark:border-green-800"
                            ),
                            Div(
                                Icon("lucide:crown", cls="h-5 w-5 text-amber-500"),
                                Div(
                                    P("Admin Access", cls="font-medium text-sm"),
                                    P("Full control including user and billing management", cls="text-xs text-muted-foreground"),
                                    cls="ml-3"
                                ),
                                ds_show("$member_role_value === 'admin'"),
                                cls="flex items-center p-3 bg-amber-50 dark:bg-amber-950/20 rounded-md border border-amber-200 dark:border-amber-800"
                            ),
                            cls="mt-3"
                        ),
                        cls="space-y-4"
                    ),
                    
                    Separator(cls="my-6"),
                    
                    # Notification Settings
                    Div(
                        P(
                            Icon("lucide:mail", cls="h-4 w-4 inline mr-2"),
                            "Notification Settings",
                            cls="text-sm font-semibold text-foreground mb-3 flex items-center"
                        ),
                        CheckboxWithLabel(
                            label="Send invitation email immediately",
                            checked=True,
                            signal="send_invite",
                            helper_text="The team member will receive an email invitation to join"
                        ),
                        CheckboxWithLabel(
                            label="Send welcome email with getting started guide",
                            checked=True,
                            signal="send_welcome",
                            helper_text="Include helpful resources for new team members"
                        ),
                        cls="space-y-3"
                    ),
                    
                    DialogFooter(
                        DialogClose("Cancel", ref_id="form_dialog", variant="outline"),
                        Button(
                            Icon("lucide:send", cls="h-4 w-4 mr-2"),
                            "Send Invitation",
                            ds_disabled("!$member_name || !$member_email"),
                            ds_on_click("""
                                event.preventDefault();
                                if ($member_name && $member_email) {
                                    const roleLabel = $member_role === 'viewer' ? 'Viewer' : 
                                                     $member_role === 'editor' ? 'Editor' : 'Admin';
                                    alert(`✅ Invitation sent to ${$member_email} as ${roleLabel}`);
                                    $form_dialog.close();
                                    // Reset form
                                    $member_name = '';
                                    $member_email = '';
                                    $member_role = 'viewer';
                                    $send_invite = true;
                                    $send_welcome = true;
                                }
                            """),
                            type="submit",
                            cls="bg-primary hover:bg-primary/90"
                        )
                    ),
                    ds_signals(
                        member_name=value(""),
                        member_email=value(""),
                        member_role_value=value("viewer"),
                        member_role_label=value("Viewer - Can view projects and files"),
                        member_role_open=False,
                        send_invite=True,
                        send_welcome=True
                    ),
                    cls="space-y-6 py-4"
                )
            ),
            ref_id="form_dialog",
            size="lg"
        ),
        '''Dialog(
    DialogTrigger("Add Team Member", ref_id="form_dialog"),
    DialogContent(
        DialogHeader(
            DialogTitle("Invite Team Member"),
            DialogDescription("Add a new member to your team")
        ),
        Form(
            InputWithLabel(label="Name", signal="member_name", required=True),
            InputWithLabel(label="Email", type="email", signal="member_email", required=True),
            SelectWithLabel(
                label="Role",
                options=[("viewer", "Viewer"), ("editor", "Editor"), ("admin", "Admin")],
                signal="member_role"
            ),
            CheckboxWithLabel(label="Send invitation email", signal="send_invite"),
            DialogFooter(
                DialogClose("Cancel", variant="outline"),
                Button("Send Invitation", type="submit", ds_on_click="submitForm()")
            ),
            ds_signals(member_name="", member_email="", member_role="viewer")
        )
    ),
    ref_id="form_dialog"
)''',
        title="Form Dialog",
        description="Complex form with multiple input types in a dialog"
    )
    
    # Scrollable content dialog
    yield ComponentPreview(
        Dialog(
            DialogTrigger("View Terms", ref_id="scroll_dialog"),
            DialogContent(
                DialogHeader(
                    DialogTitle("Terms of Service"),
                    DialogDescription("Please review our terms and conditions")
                ),
                Div(
                    Div(
                        H3("1. Acceptance of Terms", cls="font-semibold mb-2"),
                        P("By accessing and using this service, you accept and agree to be bound by the terms and provision of this agreement.", cls="text-sm text-muted-foreground mb-4"),
                        
                        H3("2. Use License", cls="font-semibold mb-2"),
                        P("Permission is granted to temporarily download one copy of the materials for personal, non-commercial transitory viewing only.", cls="text-sm text-muted-foreground mb-4"),
                        
                        H3("3. Disclaimer", cls="font-semibold mb-2"),
                        P("The materials on this service are provided on an 'as is' basis. We make no warranties, expressed or implied, and hereby disclaim and negate all other warranties including, without limitation, implied warranties or conditions of merchantability, fitness for a particular purpose, or non-infringement of intellectual property or other violation of rights.", cls="text-sm text-muted-foreground mb-4"),
                        
                        H3("4. Limitations", cls="font-semibold mb-2"),
                        P("In no event shall our company or its suppliers be liable for any damages (including, without limitation, damages for loss of data or profit, or due to business interruption) arising out of the use or inability to use the materials on our service.", cls="text-sm text-muted-foreground mb-4"),
                        
                        H3("5. Privacy Policy", cls="font-semibold mb-2"),
                        P("Your privacy is important to us. Our privacy policy explains how we collect, use, and protect your data.", cls="text-sm text-muted-foreground mb-4"),
                        
                        H3("6. Account Termination", cls="font-semibold mb-2"),
                        P("We reserve the right to terminate accounts that violate our terms of service.", cls="text-sm text-muted-foreground"),
                        
                        cls="py-4 px-4"
                    ),
                    cls="max-h-[300px] overflow-y-auto my-4 border rounded-md"
                ),
                CheckboxWithLabel(
                    label="I have read and agree to the terms",
                    signal="terms_accepted"
                ),
                DialogFooter(
                    DialogClose("Decline", ref_id="scroll_dialog", variant="outline"),
                    DialogClose(
                        "Accept",
                        ds_disabled("!$terms_accepted"),
                        ref_id="scroll_dialog",
                        onclick="alert('Terms accepted!')"
                    )
                ),
                ds_signals(terms_accepted=False)
            ),
            ref_id="scroll_dialog",
            size="lg"
        ),
        '''Dialog(
    DialogTrigger("View Terms", ref_id="scroll_dialog"),
    DialogContent(
        DialogHeader(
            DialogTitle("Terms of Service"),
            DialogDescription("Please review our terms")
        ),
        Div(
            // Long scrollable content
            H3("1. Acceptance of Terms"),
            P("By accessing this service..."),
            // ... more sections
            cls="max-h-[300px] overflow-y-auto"
        ),
        CheckboxWithLabel(label="I agree to the terms", signal="terms_accepted"),
        DialogFooter(
            DialogClose("Decline", variant="outline"),
            Button("Accept", ds_disabled="!$terms_accepted")
        ),
        ds_signals(terms_accepted=False)
    ),
    ref_id="scroll_dialog",
    size="lg"
)''',
        title="Scrollable Content",
        description="Dialog with scrollable content and conditional actions"
    )
    
    # Loading/async dialog
    yield ComponentPreview(
        Dialog(
            DialogTrigger(
                Icon("lucide:cloud-upload", cls="h-4 w-4 mr-2"),
                "Upload File",
                ref_id="upload_dialog"
            ),
            DialogContent(
                DialogHeader(
                    DialogTitle("Upload Document"),
                    DialogDescription("Upload and process your document")
                ),
                # Upload form (shown when not uploading)
                Div(
                    InputWithLabel(
                        label="Document Title",
                        placeholder="Enter a title for your document",
                        signal="doc_title",
                        required=True,
                        helper_text="Required - give your document a descriptive name"
                    ),
                    Div(
                        P("Choose file to upload:", cls="text-sm font-medium mb-2"),
                        Div(
                            Span(
                                Icon("lucide:file-text", cls="w-8 h-8 text-muted-foreground mb-2 [&>svg]:w-full [&>svg]:h-full", style="font-size: 32px;"),
                                ds_show("!$file_selected")
                            ),
                            Span(
                                Icon("lucide:file-check", cls="w-8 h-8 text-green-500 mb-2 [&>svg]:w-full [&>svg]:h-full", style="font-size: 32px;"),
                                ds_show("$file_selected")
                            ),
                            P(
                                ds_text("$file_selected ? $selected_file_name : 'Click to select file or drag and drop'"),
                                ds_style(color="$file_selected ? 'hsl(var(--foreground))' : 'hsl(var(--muted-foreground))'"),
                                cls="text-sm font-medium mb-1",                                
                            ),
                            P(
                                ds_text("$file_selected ? `${$selected_file_size} MB` : 'PDF, DOC, TXT up to 10MB'"),
                                cls="text-xs text-muted-foreground"
                            ),
                            ds_on_click("""
                                if (!$file_selected) {
                                    $file_selected = true;
                                    $selected_file_name = 'project-proposal.pdf';
                                    $selected_file_size = '2.4';
                                }
                            """),
                             ds_style(
                                border_color="$file_selected ? 'hsl(var(--border))' : 'hsl(var(--muted))'",
                                background_color="$file_selected ? 'hsl(var(--muted)/0.3)' : 'transparent'"
                            ),
                            cls="border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-all duration-200",
                           
                        ),
                        cls="mb-4"
                    ),
                    ds_show("!$uploading && !$upload_complete"),
                    cls="py-4 space-y-4"
                ),
                # Loading state (shown during upload)
                Div(
                    Div(
                        Div(
                            Icon(
                                "lucide:loader", 
                                cls="text-primary [&>svg]:w-full [&>svg]:h-full",
                                style="font-size: 32px;"
                            ),
                            cls="w-8 h-8 flex items-center justify-center animate-spin mx-auto mb-4"
                        ),
                        P("Uploading document...", cls="text-center font-medium mb-2"),
                        P(ds_text("`${$upload_progress}% complete`"), cls="text-center text-sm text-muted-foreground mb-4"),
                        # Progress bar
                        Div(
                            Div(
                                ds_style(width="`${$upload_progress}%`"),
                                cls="h-2 bg-primary rounded-full transition-all duration-300",                                
                            ),
                            cls="w-full bg-muted rounded-full h-2"
                        ),
                        cls="py-8"
                    ),
                    ds_show("$uploading && !$upload_complete"),
                    cls="text-center"
                ),
                # Success state
                Div(
                    Div(
                        Icon("lucide:check-circle", cls="w-8 h-8 text-green-500 mx-auto mb-4 [&>svg]:w-full [&>svg]:h-full", style="font-size: 32px;"),
                        P("Upload Complete!", cls="text-center font-medium text-green-600 mb-2"),
                        P(ds_text("`Successfully uploaded: ${$doc_title || 'Document'}`"), cls="text-center text-sm text-muted-foreground"),
                        cls="py-8"
                    ),
                    ds_show("$upload_complete"),
                    cls="text-center"
                ),
                DialogFooter(
                    DialogClose("Cancel", ds_show("!$uploading"), ref_id="upload_dialog", variant="outline"),
                    Button(
                        "Start Upload",
                        ds_disabled("!$doc_title || !$file_selected"),
                        ds_show("!$uploading && !$upload_complete"),
                        ds_on_click("""
                            if ($doc_title && $file_selected) {
                                $uploading = true;
                                $upload_progress = 0;
                                const interval = setInterval(() => {
                                    $upload_progress += 10;
                                    if ($upload_progress >= 100) {
                                        clearInterval(interval);
                                        setTimeout(() => {
                                            $upload_complete = true;
                                        }, 500);
                                    }
                                }, 200);
                            }
                        """)
                    ),
                    Button(
                        "Done",
                        ds_show("$upload_complete"),
                        ds_on_click("""
                            $upload_dialog.close();
                            // Reset all state
                            $uploading = false;
                            $upload_complete = false;
                            $upload_progress = 0;
                            $file_selected = false;
                            $selected_file_name = '';
                            $selected_file_size = '';
                            $doc_title = '';
                        """)
                    )
                ),
                ds_signals(
                    uploading=False,
                    upload_complete=False,
                    upload_progress=0,
                    file_selected=False,
                    selected_file_name=value(""),
                    selected_file_size=value(""),
                    doc_title=value("")
                )
            ),
            ref_id="upload_dialog"
        ),
        '''Dialog(
    DialogTrigger("Upload File", ref_id="upload_dialog"),
    DialogContent(
        DialogHeader(
            DialogTitle("Upload Document"),
            DialogDescription("Upload and process your document")
        ),
        // Upload form
        Div(
            InputWithLabel(label="Document Title", signal="doc_title", required=True),
            // File upload area
            Div(/* file upload UI */),
            ds_show="!$uploading"
        ),
        // Loading state
        Div(
            Icon("lucide:loader", cls="w-8 h-8 animate-spin [&>svg]:w-full [&>svg]:h-full", style="font-size: 32px;"),
            P("Uploading document..."),
            P(ds_text="`${$upload_progress}% complete`"),
            // Progress bar
            Div(/* progress bar */),
            ds_show="$uploading && !$upload_complete"
        ),
        // Success state
        Div(
            Icon("lucide:check-circle", cls="w-8 h-8 text-green-500 [&>svg]:w-full [&>svg]:h-full", style="font-size: 32px;"),
            P("Upload Complete!", cls="text-green-600"),
            ds_show="$upload_complete"
        ),
        DialogFooter(
            Button("Start Upload", ds_disabled="!$doc_title", ds_on_click="startUpload()"),
            Button("Done", ds_show="$upload_complete")
        ),
        ds_signals(uploading=False, upload_complete=False, upload_progress=0)
    )
)''',
        title="Loading/Async Dialog",
        description="Dialog with loading states, progress tracking, and async operations"
    )
    
    # Multi-step dialog
    yield ComponentPreview(
        Dialog(
            DialogTrigger(
                Icon("lucide:rocket", cls="h-4 w-4 mr-2"),
                "Start Setup",
                ref_id="wizard_dialog"
            ),
            DialogContent(
                DialogHeader(
                    DialogTitle("Project Setup"),
                    DialogDescription(
                        ds_text("$step === 1 ? 'Choose your project type' : $step === 2 ? 'Configure settings' : 'Review and confirm'")
                    )
                ),
                # Step progress indicator
                Div(
                    # Background line with rounded ends
                    Div(cls="absolute top-3 left-0 w-full h-1 bg-muted rounded-full"),
                    # Progress bar with rounded ends
                    Div(
                        ds_style(
                            width="$step === 1 ? '0%' : $step === 2 ? '50%' : '100%'"
                        ),
                        cls="absolute top-3 left-0 h-1 bg-primary rounded-full transition-all duration-500"
                    ),
                    # Steps container
                    Div(
                        # Step 1
                        Div(
                            Div(
                                Span(
                                    Icon("lucide:check", cls="w-3 h-3 text-white"),
                                    ds_show("$step > 1")
                                ),
                                Span("1", ds_show("$step <= 1")),
                                ds_style(
                                    background_color="$step >= 1 ? 'rgb(59, 130, 246)' : 'rgb(203, 213, 225)'",
                                    color="$step >= 1 ? 'white' : 'rgb(71, 85, 105)'"
                                ),
                                cls="w-6 h-6 rounded-full flex items-center justify-center text-xs font-semibold"
                            ),
                            P("Project Type",
                                ds_style(color="$step >= 1 ? 'hsl(var(--foreground))' : 'hsl(var(--muted-foreground))'"),
                                cls="text-xs font-medium mt-2 text-center"
                            ),
                            cls="flex flex-col items-center"
                        ),
                        # Step 2
                        Div(
                            Div(
                                Span(
                                    Icon("lucide:check", cls="w-3 h-3 text-white"),
                                    ds_show("$step > 2")
                                ),
                                Span("2", ds_show("$step <= 2")),
                                ds_style(
                                    background_color="$step >= 2 ? 'rgb(59, 130, 246)' : 'rgb(203, 213, 225)'",
                                    color="$step >= 2 ? 'white' : 'rgb(71, 85, 105)'"
                                ),
                                cls="w-6 h-6 rounded-full flex items-center justify-center text-xs font-semibold"
                            ),
                            P("Configuration",
                                ds_style(color="$step >= 2 ? 'hsl(var(--foreground))' : 'hsl(var(--muted-foreground))'"),
                                cls="text-xs font-medium mt-2 text-center"
                            ),
                            cls="flex flex-col items-center"
                        ),
                        # Step 3
                        Div(
                            Div(
                                Span(
                                    Icon("lucide:check", cls="w-3 h-3 text-white"),
                                    ds_show("$step > 3")
                                ),
                                Span("3", ds_show("$step <= 3")),
                                ds_style(
                                    background_color="$step >= 3 ? 'rgb(59, 130, 246)' : 'rgb(203, 213, 225)'",
                                    color="$step >= 3 ? 'white' : 'rgb(71, 85, 105)'"
                                ),
                                cls="w-6 h-6 rounded-full flex items-center justify-center text-xs font-semibold"
                            ),
                            P("Review",
                                ds_style(color="$step >= 3 ? 'hsl(var(--foreground))' : 'hsl(var(--muted-foreground))'"),
                                cls="text-xs font-medium mt-2 text-center"
                            ),
                            cls="flex flex-col items-center"
                        ),
                        cls="flex justify-between items-start relative z-10"
                    ),
                    cls="relative w-full mb-8 px-8"
                ),
                # Step 1: Project Type
                Div(
                    Div(
                        Button(
                            Icon("lucide:globe", cls="h-8 w-8 mb-2"),
                            P("Web Application", cls="font-semibold"),
                            P("React, Vue, or vanilla JS", cls="text-xs text-muted-foreground"),
                            ds_on_click("$project_type = 'web'; $step = 2"),
                            variant="outline",                            
                            cls="h-auto flex-col p-4 w-full"
                        ),
                        Button(
                            Icon("lucide:smartphone", cls="h-8 w-8 mb-2"),
                            P("Mobile App", cls="font-semibold"),
                            P("iOS or Android", cls="text-xs text-muted-foreground"),
                            ds_on_click("$project_type = 'mobile'; $step = 2"),
                            variant="outline",                            
                            cls="h-auto flex-col p-4 w-full"
                        ),
                        Button(
                            Icon("lucide:server", cls="h-8 w-8 mb-2"),
                            P("API Service", cls="font-semibold"),
                            P("REST or GraphQL", cls="text-xs text-muted-foreground"),
                            ds_on_click("$project_type = 'api'; $step = 2"),
                            variant="outline",                            
                            cls="h-auto flex-col p-4 w-full"
                        ),
                        cls="grid grid-cols-3 gap-3"
                    ),
                    ds_show("$step === 1"),
                    cls="py-4"
                ),
                # Step 2: Configuration
                Div(
                    InputWithLabel(
                        label="Project Name",
                        placeholder="my-awesome-project",
                        signal="project_name",
                        required=True
                    ),
                    TextareaWithLabel(
                        label="Description",
                        placeholder="Describe your project...",
                        rows=3,
                        signal="project_desc"
                    ),
                    ds_show("$step === 2"),
                    cls="space-y-4 py-4"
                ),
                # Step 3: Review
                Div(
                    Div(
                        P("Project Type: ", Span(ds_text("$project_type"), cls="font-semibold")),
                        P("Name: ", Span(ds_text("$project_name || 'Not specified'"), cls="font-semibold")),
                        P("Description: ", Span(ds_text("$project_desc || 'Not specified'"), cls="font-semibold")),
                        cls="space-y-2 p-4 bg-muted rounded-md"
                    ),
                    ds_show("$step === 3"),
                    cls="py-4"
                ),
                DialogFooter(
                    Button(
                        "Previous",
                        ds_on_click("$step = Math.max(1, $step - 1)"),
                        ds_disabled("$step === 1"),
                        variant="outline",                        
                    ),
                    Button(
                        ds_text("$step === 3 ? 'Create Project' : 'Next'"),
                        ds_on_click("""
                            if ($step === 1 && $project_type) $step = 2;
                            else if ($step === 2 && $project_name) $step = 3;
                            else if ($step === 3) {
                                $step = 4; // Show checkmark on step 3
                                setTimeout(() => {
                                    alert(`Creating ${$project_type} project: ${$project_name}`);
                                    $wizard_dialog.close();
                                    $step = 1;
                                    $project_type = '';
                                    $project_name = '';
                                    $project_desc = '';
                                }, 100);
                            }
                        """),
                        ds_disabled("($step === 1 && !$project_type) || ($step === 2 && !$project_name)")
                    )
                ),
                ds_signals(
                    step=1,
                    project_type=value(""),
                    project_name=value(""),
                    project_desc=value("")
                )
            ),
            ref_id="wizard_dialog",
            size="lg"
        ),
    '''Dialog(
    DialogTrigger("Start Setup", ref_id="wizard_dialog"),
    DialogContent(
        DialogHeader(
            DialogTitle("Project Setup"),
            DialogDescription(ds_text("Step description based on $step"))
        ),
        // Step indicators
        Div(/* step bubbles and progress bars */),
        // Step 1
        Div(/* project type selection */, ds_show="$step === 1"),
        // Step 2
        Div(/* configuration form */, ds_show="$step === 2"),
        // Step 3
        Div(/* review and confirm */, ds_show="$step === 3"),
        DialogFooter(
            Button("Previous", ds_on_click="$step--", ds_disabled="$step === 1"),
            Button(
                ds_text("$step === 3 ? 'Create' : 'Next'"),
                ds_on_click="handleStep()"
            )
        ),
        ds_signals(step=1, project_type="", project_name="")
    ),
    ref_id="wizard_dialog"
)''',
    title="Multi-Step Wizard",
    description="Complex wizard flow with step indicators and validation"
    )
    
    # Settings dialog with tabs
    yield ComponentPreview(
        Dialog(
            DialogTrigger(
                Icon("lucide:settings", cls="h-4 w-4 mr-2"),
                "Settings",
                ref_id="settings_dialog"
            ),
            DialogContent(
                DialogHeader(
                    DialogTitle("Settings"),
                    DialogDescription("Manage your account and application preferences")
                ),
                # Tab navigation
                Div(
                    Button(
                        Icon("lucide:user", cls="h-4 w-4 mr-2"),
                        "Profile",
                        ds_on_click("$settings_tab = 'profile'; console.log('Profile clicked, settings_tab:', $settings_tab)"),
                        ds_style(
                            background_color="$settings_tab === 'profile' ? '#f1f5f9' : 'transparent'",
                            color="$settings_tab === 'profile' ? '#0f172a' : '#71717a'",
                            box_shadow="$settings_tab === 'profile' ? '0 1px 2px rgba(0,0,0,0.1)' : 'none'"
                        ),
                        variant="ghost",
                        size="sm",
                        
                        cls="flex-1"
                    ),
                    Button(
                        Icon("lucide:bell", cls="h-4 w-4 mr-2"),
                        "Notifications",
                        ds_on_click("$settings_tab = 'notifications'; console.log('Notifications clicked, settings_tab:', $settings_tab)"),
                        ds_style(
                            background_color="$settings_tab === 'notifications' ? '#f1f5f9' : 'transparent'",
                            color="$settings_tab === 'notifications' ? '#0f172a' : '#71717a'",
                            box_shadow="$settings_tab === 'notifications' ? '0 1px 2px rgba(0,0,0,0.1)' : 'none'"
                        ),
                        variant="ghost",
                        size="sm",
                        
                        cls="flex-1"
                    ),
                    Button(
                        Icon("lucide:shield", cls="h-4 w-4 mr-2"),
                        "Security",
                        ds_on_click("$settings_tab = 'security'; console.log('Security clicked, settings_tab:', $settings_tab)"),
                        ds_style(
                            background_color="$settings_tab === 'security' ? '#f1f5f9' : 'transparent'",
                            color="$settings_tab === 'security' ? '#0f172a' : '#71717a'",
                            box_shadow="$settings_tab === 'security' ? '0 1px 2px rgba(0,0,0,0.1)' : 'none'"
                        ),
                        variant="ghost",
                        size="sm",
                        
                        cls="flex-1"
                    ),
                    cls="flex gap-1 mb-6 p-1 bg-muted/30 rounded-lg"
                ),
                # Profile tab
                Div(
                    InputWithLabel(
                        label="Display Name",
                        placeholder="John Doe",
                        value="John Doe",
                        signal="profile_name"
                    ),
                    InputWithLabel(
                        label="Email",
                        type="email",
                        placeholder="john@example.com",
                        value="john@example.com",
                        signal="profile_email"
                    ),
                    TextareaWithLabel(
                        label="Bio",
                        placeholder="Tell us about yourself...",
                        rows=3,
                        signal="profile_bio"
                    ),
                    SelectWithLabel(
                        label="Time Zone",
                        options=[
                            ("utc", "UTC"),
                            ("pst", "Pacific Standard Time"),
                            ("est", "Eastern Standard Time"),
                            ("cet", "Central European Time")
                        ],
                        value="utc",
                        signal="profile_timezone"
                    ),
                    ds_show("$settings_tab === 'profile'"),
                    cls="space-y-4"
                ),
                # Notifications tab
                Div(
                    CheckboxWithLabel(
                        label="Email notifications",
                        helper_text="Receive updates and announcements via email",
                        checked=True,
                        signal="notify_email"
                    ),
                    CheckboxWithLabel(
                        label="Push notifications",
                        helper_text="Get notified about important events",
                        checked=False,
                        signal="notify_push"
                    ),
                    CheckboxWithLabel(
                        label="Marketing emails",
                        helper_text="Receive product updates and promotional content",
                        checked=False,
                        signal="notify_marketing"
                    ),
                    Separator(cls="my-4"),
                    P("Notification Frequency", cls="text-sm font-medium mb-2"),
                    SelectWithLabel(
                        label="Email Digest",
                        options=[
                            ("never", "Never"),
                            ("daily", "Daily"),
                            ("weekly", "Weekly"),
                            ("monthly", "Monthly")
                        ],
                        value="weekly",
                        signal="notify_frequency",
                        helper_text="How often you'd like to receive summary emails"
                    ),
                    ds_show("$settings_tab === 'notifications'"),
                    cls="space-y-4"
                ),
                # Security tab
                Div(
                    P("Password", cls="text-sm font-medium mb-2"),
                    Div(
                        P("Last changed: 2 months ago", cls="text-sm text-muted-foreground mb-2"),
                        Button(
                            "Change Password",
                            ds_on_click("alert('Password change dialog would open')"),
                            variant="outline",
                            size="sm",
                            
                        ),
                        cls="mb-4"
                    ),
                    CheckboxWithLabel(
                        label="Two-factor authentication",
                        helper_text="Add an extra layer of security to your account",
                        checked=False,
                        signal="security_2fa"
                    ),
                    CheckboxWithLabel(
                        label="Login notifications",
                        helper_text="Get notified when someone signs into your account",
                        checked=True,
                        signal="security_login_notify"
                    ),
                    Separator(cls="my-4"),
                    P("Session Management", cls="text-sm font-medium mb-2"),
                    Div(
                        P("Active sessions: 3 devices", cls="text-sm text-muted-foreground mb-2"),
                        Button(
                            "View All Sessions",
                            ds_on_click("alert('Sessions dialog would open')"),
                            variant="outline",
                            size="sm",
                            
                        ),
                        cls="mb-4"
                    ),
                    ds_show("$settings_tab === 'security'"),
                    cls="space-y-4"
                ),
                DialogFooter(
                    DialogClose("Cancel", ref_id="settings_dialog", variant="outline"),
                    Button(
                        "Save Changes",
                        ds_on_click("""
                            alert('Settings saved successfully!');
                            $settings_dialog.close();
                        """)
                    )
                ),
                ds_signals(
                    settings_tab=value("profile"),
                    profile_name=value("John Doe"),
                    profile_email=value("john@example.com"),
                    profile_bio=value(""),
                    profile_timezone=value("utc"),
                    notify_email=True,
                    notify_push=False,
                    notify_marketing=False,
                    notify_frequency=value("weekly"),
                    security_2fa=False,
                    security_login_notify=True
                ),
                cls="pb-2"
            ),
            ref_id="settings_dialog",
            size="lg"
        ),
        '''Dialog(
    DialogTrigger("Settings", ref_id="settings_dialog"),
    DialogContent(
        DialogHeader(
            DialogTitle("Settings"),
            DialogDescription("Manage your preferences")
        ),
        // Tab navigation
        Div(
            Button("Profile", ds_on_click("$settings_tab = 'profile'")),
            Button("Notifications", ds_on_click("$settings_tab = 'notifications'")),
            Button("Security", ds_on_click("$settings_tab = 'security'")),
            cls="flex gap-1 p-1 bg-muted/30 rounded-lg"
        ),
        // Profile tab
        Div(
            InputWithLabel(label="Display Name", signal="profile_name"),
            InputWithLabel(label="Email", signal="profile_email"),
            TextareaWithLabel(label="Bio", signal="profile_bio"),
            ds_show="$settings_tab === 'profile'"
        ),
        // Notifications tab
        Div(
            CheckboxWithLabel(label="Email notifications", signal="notify_email"),
            CheckboxWithLabel(label="Push notifications", signal="notify_push"),
            SelectWithLabel(label="Frequency", signal="notify_frequency"),
            ds_show="$settings_tab === 'notifications'"
        ),
        // Security tab
        Div(
            Button("Change Password"),
            CheckboxWithLabel(label="Two-factor auth", signal="security_2fa"),
            ds_show="$settings_tab === 'security'"
        ),
        DialogFooter(
            DialogClose("Cancel"),
            Button("Save Changes")
        ),
        ds_signals(settings_tab="profile", ...)
    ),
    size="lg"
)''',
        title="Settings Dialog",
        description="Tabbed interface for managing different categories of settings"
    )
    
    # Custom styled dialog with sizes
    yield ComponentPreview(
        Div(
            Dialog(
                DialogTrigger("Small", ref_id="small_dialog", variant="outline", cls="mr-2"),
                DialogContent(
                    DialogHeader(
                        DialogTitle("Small Dialog"),
                        DialogDescription("This is a small dialog (max-width: sm)")
                    ),
                    P("Compact content area.", cls="py-4"),
                    DialogFooter(DialogClose("Close", ref_id="small_dialog"))
                ),
                ref_id="small_dialog",
                size="sm"
            ),
            Dialog(
                DialogTrigger("Medium", ref_id="medium_dialog", variant="outline", cls="mr-2"),
                DialogContent(
                    DialogHeader(
                        DialogTitle("Medium Dialog"),
                        DialogDescription("This is a medium dialog (max-width: lg)")
                    ),
                    P("Standard content area.", cls="py-4"),
                    DialogFooter(DialogClose("Close", ref_id="medium_dialog"))
                ),
                ref_id="medium_dialog",
                size="md"
            ),
            Dialog(
                DialogTrigger("Large", ref_id="large_dialog", variant="outline", cls="mr-2"),
                DialogContent(
                    DialogHeader(
                        DialogTitle("Large Dialog"),
                        DialogDescription("This is a large dialog (max-width: 2xl)")
                    ),
                    P("Spacious content area for complex forms or content.", cls="py-4"),
                    DialogFooter(DialogClose("Close", ref_id="large_dialog"))
                ),
                ref_id="large_dialog",
                size="lg"
            ),
            cls="flex flex-wrap"
        ),
        '''// Different dialog sizes
Dialog(DialogTrigger("Small"), DialogContent(...), ref_id="small", size="sm")
Dialog(DialogTrigger("Medium"), DialogContent(...), ref_id="medium", size="md")
Dialog(DialogTrigger("Large"), DialogContent(...), ref_id="large", size="lg")
Dialog(DialogTrigger("XL"), DialogContent(...), ref_id="xl", size="xl")''',
        title="Dialog Sizes",
        description="Different dialog sizes for various content needs"
    )


def create_dialog_docs():
    """Create dialog documentation page using convention-based approach."""
    
    api_reference = {
        "props": [
            {
                "name": "trigger",
                "type": "FT",
                "description": "The trigger element (usually DialogTrigger)"
            },
            {
                "name": "content",
                "type": "FT",
                "description": "The dialog content (usually DialogContent)"
            },
            {
                "name": "ref_id",
                "type": "str",
                "description": "Unique identifier for the dialog instance"
            },
            {
                "name": "modal",
                "type": "bool",
                "default": "True",
                "description": "Whether dialog is modal (blocks interaction with rest of page)"
            },
            {
                "name": "size",
                "type": "Literal['sm', 'md', 'lg', 'xl', 'full']",
                "default": "'md'",
                "description": "Size of the dialog"
            }
        ],
        "sub_components": [
            {
                "name": "DialogTrigger",
                "description": "Button that opens the dialog",
                "props": [
                    {
                        "name": "ref_id",
                        "type": "str",
                        "description": "Must match the Dialog's ref_id"
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
                "name": "DialogContent",
                "description": "Container for dialog content",
                "props": [
                    {
                        "name": "show_close_button",
                        "type": "bool",
                        "default": "True",
                        "description": "Whether to show the X close button"
                    }
                ]
            },
            {
                "name": "DialogHeader",
                "description": "Container for title and description"
            },
            {
                "name": "DialogTitle",
                "description": "The dialog's title"
            },
            {
                "name": "DialogDescription",
                "description": "Subtitle or description text"
            },
            {
                "name": "DialogFooter",
                "description": "Container for action buttons"
            },
            {
                "name": "DialogClose",
                "description": "Button that closes the dialog",
                "props": [
                    {
                        "name": "ref_id",
                        "type": "str",
                        "description": "Must match the Dialog's ref_id"
                    },
                    {
                        "name": "value",
                        "type": "str",
                        "default": "''",
                        "description": "Return value when dialog closes"
                    }
                ]
            }
        ]
    }
    
    # Hero example
    hero_example = ComponentPreview(
        Dialog(
            DialogTrigger("Open Dialog", ref_id="hero_dialog"),
            DialogContent(
                DialogHeader(
                    DialogTitle("Edit Profile"),
                    DialogDescription("Make changes to your profile here. Click save when you're done.")
                ),
                Div(
                    InputWithLabel(
                        label="Username",
                        placeholder="@username",
                        signal="username"
                    ),
                    InputWithLabel(
                        label="Email",
                        type="email",
                        placeholder="email@example.com",
                        signal="email"
                    ),
                    ds_signals(username=value(""), email=value("")),
                    cls="space-y-4 py-4"
                ),
                DialogFooter(
                    DialogClose("Cancel", ref_id="hero_dialog", variant="outline"),
                    DialogClose(
                        "Save Changes", 
                        ref_id="hero_dialog",
                        onclick="alert('Profile saved!')"
                    )
                )
            ),
            ref_id="hero_dialog"
        ),
        '''Dialog(
    DialogTrigger("Open Dialog", ref_id="hero_dialog"),
    DialogContent(
        DialogHeader(
            DialogTitle("Edit Profile"),
            DialogDescription("Make changes to your profile...")
        ),
        Div(
            InputWithLabel(label="Username", signal="username"),
            InputWithLabel(label="Email", type="email", signal="email")
        ),
        DialogFooter(
            DialogClose("Cancel", variant="outline"),
            DialogClose("Save Changes")
        )
    ),
    ref_id="hero_dialog"
)''',
        copy_button=True
    )
    
    return auto_generate_page(
        TITLE,
        DESCRIPTION,
        list(examples()),
        cli_command="star add dialog",
        api_reference=api_reference,
        hero_example=hero_example,
        component_slug="dialog"
    )