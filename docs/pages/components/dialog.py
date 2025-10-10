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

from starhtml import Div, P, Input, Label, Icon, Span, H2, H3, Form, Code, Ul, Li, Style, Signal, js
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
from utils import auto_generate_page, with_code, Prop, Component, build_api_reference
from widgets.component_preview import ComponentPreview


# ============================================================================
# EXAMPLE FUNCTIONS (decorated with @with_code for markdown generation)
# ============================================================================

# Basic dialog
@with_code
def basic_dialog_example():
    return Dialog(
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
    )


# Confirmation dialog
@with_code
def confirmation_dialog_example():
    return Dialog(
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
    )


# Form dialog
@with_code
def form_dialog_example():
    def create_role_preview(role, icon, title, description, color):
        return Div(
            Icon(icon, cls=f"h-5 w-5 text-{color}-500"),
            Div(
                P(title, cls="font-medium text-sm"),
                P(description, cls="text-xs text-muted-foreground"),
                cls="ml-3"
            ),
            data_show=js(f"$member_role_value === '{role}'"),
            cls=f"flex items-center p-3 bg-{color}-50 dark:bg-{color}-950/20 rounded-md border border-{color}-200 dark:border-{color}-800"
        )

    def create_section_header(icon, title):
        return P(
            Icon(icon, cls="h-4 w-4 inline mr-2"),
            title,
            cls="text-sm font-semibold text-foreground mb-3 flex items-center"
        )

    member_name = Signal("member_name", "")
    member_email = Signal("member_email", "")
    member_role_value = Signal("member_role_value", "viewer")
    member_role_label = Signal("member_role_label", "Viewer - Can view projects and files")
    member_role_open = Signal("member_role_open", False)
    send_invite = Signal("send_invite", True)
    send_welcome = Signal("send_welcome", True)

    return Dialog(
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
                member_name,
                member_email,
                member_role_value,
                member_role_label,
                member_role_open,
                send_invite,
                send_welcome,
                Div(
                    create_section_header("lucide:user", "Personal Information"),
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

                Div(
                    create_section_header("lucide:shield-check", "Access & Permissions"),
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
                    Div(
                        create_role_preview("viewer", "lucide:eye", "Viewer Access", "Can view and comment on projects", "blue"),
                        create_role_preview("editor", "lucide:edit-3", "Editor Access", "Can edit, create, and manage projects", "green"),
                        create_role_preview("admin", "lucide:crown", "Admin Access", "Full control including user and billing management", "amber"),
                        cls="mt-3"
                    ),
                    cls="space-y-4"
                ),

                Separator(cls="my-6"),

                Div(
                    create_section_header("lucide:mail", "Notification Settings"),
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
                        data_attr_disabled=member_name.not_().or_(member_email.not_()),
                        data_on_click=js("""
                            evt.preventDefault();
                            if ($member_name && $member_email) {
                                const roleLabel = $member_role_value === 'viewer' ? 'Viewer' :
                                                 $member_role_value === 'editor' ? 'Editor' : 'Admin';
                                alert(`✅ Invitation sent to ${$member_email} as ${roleLabel}`);
                                $form_dialog.close();
                                // Reset form
                                $member_name = '';
                                $member_email = '';
                                $member_role_value = 'viewer';
                                $send_invite = true;
                                $send_welcome = true;
                            }
                        """),
                        type="submit",
                        cls="bg-primary hover:bg-primary/90"
                    )
                ),
                cls="space-y-6 py-4"
            )
        ),
        ref_id="form_dialog",
        size="lg"
    )


# Scrollable content dialog
@with_code
def scrollable_content_example():
    terms_accepted = Signal("terms_accepted", False)

    return Dialog(
        DialogTrigger("View Terms", ref_id="scroll_dialog"),
        DialogContent(
            terms_accepted,
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
                    data_attr_disabled=terms_accepted.not_(),
                    ref_id="scroll_dialog",
                    variant="default",
                    onclick="alert('Terms accepted!')"
                )
            )
        ),
        ref_id="scroll_dialog",
        size="lg"
    )


# Loading/async dialog
@with_code
def loading_async_dialog_example():
    uploading = Signal("uploading", False)
    upload_complete = Signal("upload_complete", False)
    upload_progress = Signal("upload_progress", 0)
    file_selected = Signal("file_selected", False)
    selected_file_name = Signal("selected_file_name", "")
    selected_file_size = Signal("selected_file_size", "")
    doc_title = Signal("doc_title", "")

    return Dialog(
        DialogTrigger(
            Icon("lucide:cloud-upload", cls="h-4 w-4 mr-2"),
            "Upload File",
            ref_id="upload_dialog"
        ),
        DialogContent(
            uploading,
            upload_complete,
            upload_progress,
            file_selected,
            selected_file_name,
            selected_file_size,
            doc_title,
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
                            data_show=js("!$file_selected")
                        ),
                        Span(
                            Icon("lucide:file-check", cls="w-8 h-8 text-green-500 mb-2 [&>svg]:w-full [&>svg]:h-full", style="font-size: 32px;"),
                            data_show=file_selected
                        ),
                        P(
                            data_text=js("$file_selected ? $selected_file_name : 'Click to select file or drag and drop'"),
                            data_style_color=js("$file_selected ? 'hsl(var(--foreground))' : 'hsl(var(--muted-foreground))'"),
                            cls="text-sm font-medium mb-1",
                        ),
                        P(
                            data_text=js("$file_selected ? `${$selected_file_size} MB` : 'PDF, DOC, TXT up to 10MB'"),
                            cls="text-xs text-muted-foreground"
                        ),
                        data_on_click=js("""
                            if (!$file_selected) {
                                $file_selected = true;
                                $selected_file_name = 'project-proposal.pdf';
                                $selected_file_size = '2.4';
                            }
                        """),
                        data_style_border_color=js("$file_selected ? 'hsl(var(--border))' : 'hsl(var(--muted))'"),
                        data_style_background_color=js("$file_selected ? 'hsl(var(--muted)/0.3)' : 'transparent'"),
                        cls="border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-all duration-200",

                    ),
                    cls="mb-4"
                ),
                data_show=js("!$uploading && !$upload_complete"),
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
                    P(data_text=js("`${$upload_progress}% complete`"), cls="text-center text-sm text-muted-foreground mb-4"),
                    # Progress bar
                    Div(
                        Div(
                            data_style_width=js("`${$upload_progress}%`"),
                            cls="h-2 bg-primary rounded-full transition-all duration-300",
                        ),
                        cls="w-full bg-muted rounded-full h-2"
                    ),
                    cls="py-8"
                ),
                data_show=js("$uploading && !$upload_complete"),
                cls="text-center"
            ),
            # Success state
            Div(
                Div(
                    Icon("lucide:check-circle", cls="w-8 h-8 text-green-500 mx-auto mb-4 [&>svg]:w-full [&>svg]:h-full", style="font-size: 32px;"),
                    P("Upload Complete!", cls="text-center font-medium text-green-600 mb-2"),
                    P(data_text=js("`Successfully uploaded: ${$doc_title || 'Document'}`"), cls="text-center text-sm text-muted-foreground"),
                    cls="py-8"
                ),
                data_show=upload_complete,
                cls="text-center"
            ),
            DialogFooter(
                DialogClose("Cancel", data_show=js("!$uploading"), ref_id="upload_dialog", variant="outline"),
                Button(
                    "Start Upload",
                    data_attr_disabled=js("!$doc_title || !$file_selected"),
                    data_show=js("!$uploading && !$upload_complete"),
                    data_on_click=js("""
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
                    data_show=upload_complete,
                    data_on_click=js("""
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
            )
        ),
        ref_id="upload_dialog"
    )


# Multi-step wizard dialog
@with_code
def multi_step_wizard_example():
    def create_step_indicator(number, label, step):
        return Div(
            Div(
                Span(
                    Icon("lucide:check", cls="w-3 h-3 text-white"),
                    data_show=js(f"$step > {number}")
                ),
                Span(str(number), data_show=js(f"$step <= {number}")),
                data_style_background_color=js(f"$step >= {number} ? 'rgb(59, 130, 246)' : 'rgb(203, 213, 225)'"),
                data_style_color=js(f"$step >= {number} ? 'white' : 'rgb(71, 85, 105)'"),
                cls="w-6 h-6 rounded-full flex items-center justify-center text-xs font-semibold"
            ),
            P(label,
                data_style_color=js(f"$step >= {number} ? 'hsl(var(--foreground))' : 'hsl(var(--muted-foreground))'"),
                cls="text-xs font-medium mt-2 text-center"
            ),
            cls="flex flex-col items-center"
        )

    def create_project_type_button(icon, title, description, type_value):
        return Button(
            Icon(icon, cls="h-8 w-8 mb-2"),
            P(title, cls="font-semibold"),
            P(description, cls="text-xs text-muted-foreground"),
            data_on_click=js(f"$project_type = '{type_value}'; $step = 2"),
            variant="outline",
            cls="h-auto flex-col p-4 w-full"
        )

    step = Signal("step", 1)
    project_type = Signal("project_type", "")
    project_name = Signal("project_name", "")
    project_desc = Signal("project_desc", "")

    return Dialog(
        DialogTrigger(
            Icon("lucide:rocket", cls="h-4 w-4 mr-2"),
            "Start Setup",
            ref_id="wizard_dialog"
        ),
        DialogContent(
            step,
            project_type,
            project_name,
            project_desc,
            DialogHeader(
                DialogTitle("Project Setup"),
                DialogDescription(
                    data_text=js("$step === 1 ? 'Choose your project type' : $step === 2 ? 'Configure settings' : 'Review and confirm'")
                )
            ),
            Div(
                Div(cls="absolute top-3 left-0 w-full h-1 bg-muted rounded-full"),
                Div(
                    data_style_width=js("$step === 1 ? '0%' : $step === 2 ? '50%' : '100%'"),
                    cls="absolute top-3 left-0 h-1 bg-primary rounded-full transition-all duration-500"
                ),
                Div(
                    create_step_indicator(1, "Project Type", step),
                    create_step_indicator(2, "Configuration", step),
                    create_step_indicator(3, "Review", step),
                    cls="flex justify-between items-start relative z-10"
                ),
                cls="relative w-full mb-8 px-8"
            ),
            Div(
                Div(
                    create_project_type_button("lucide:globe", "Web Application", "React, Vue, or vanilla JS", "web"),
                    create_project_type_button("lucide:smartphone", "Mobile App", "iOS or Android", "mobile"),
                    create_project_type_button("lucide:server", "API Service", "REST or GraphQL", "api"),
                    cls="grid grid-cols-3 gap-3"
                ),
                data_show=js("$step === 1"),
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
                data_show=js("$step === 2"),
                cls="space-y-4 py-4"
            ),
            # Step 3: Review
            Div(
                Div(
                    P("Project Type: ", Span(data_text=project_type, cls="font-semibold")),
                    P("Name: ", Span(data_text=js("$project_name || 'Not specified'"), cls="font-semibold")),
                    P("Description: ", Span(data_text=js("$project_desc || 'Not specified'"), cls="font-semibold")),
                    cls="space-y-2 p-4 bg-muted rounded-md"
                ),
                data_show=js("$step === 3"),
                cls="py-4"
            ),
            DialogFooter(
                Button(
                    "Previous",
                    data_on_click=js("$step = Math.max(1, $step - 1)"),
                    data_attr_disabled=js("$step === 1"),
                    variant="outline",
                ),
                Button(
                    data_text=js("$step === 3 ? 'Create Project' : 'Next'"),
                    data_on_click=js("""
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
                    data_attr_disabled=js("($step === 1 && !$project_type) || ($step === 2 && !$project_name)")
                )
            )
        ),
        ref_id="wizard_dialog",
        size="lg"
    )


# Settings dialog with tabs
@with_code
def settings_dialog_example():
    def create_tab_button(icon, label, tab_id):
        return Button(
            Icon(icon, cls="h-4 w-4 mr-2"),
            label,
            data_on_click=js(f"$settings_tab = '{tab_id}'; console.log('{label} clicked, settings_tab:', $settings_tab)"),
            data_style_background_color=js(f"$settings_tab === '{tab_id}' ? '#f1f5f9' : 'transparent'"),
            data_style_color=js(f"$settings_tab === '{tab_id}' ? '#0f172a' : '#71717a'"),
            data_style_box_shadow=js(f"$settings_tab === '{tab_id}' ? '0 1px 2px rgba(0,0,0,0.1)' : 'none'"),
            variant="ghost",
            size="sm",
            cls="flex-1"
        )

    settings_tab = Signal("settings_tab", "profile")
    profile_name = Signal("profile_name", "John Doe")
    profile_email = Signal("profile_email", "john@example.com")
    profile_bio = Signal("profile_bio", "")
    profile_timezone = Signal("profile_timezone", "utc")
    notify_email = Signal("notify_email", True)
    notify_push = Signal("notify_push", False)
    notify_marketing = Signal("notify_marketing", False)
    notify_frequency = Signal("notify_frequency", "weekly")
    security_2fa = Signal("security_2fa", False)
    security_login_notify = Signal("security_login_notify", True)

    return Dialog(
        DialogTrigger(
            Icon("lucide:settings", cls="h-4 w-4 mr-2"),
            "Settings",
            ref_id="settings_dialog"
        ),
        DialogContent(
            settings_tab,
            profile_name,
            profile_email,
            profile_bio,
            profile_timezone,
            notify_email,
            notify_push,
            notify_marketing,
            notify_frequency,
            security_2fa,
            security_login_notify,
            DialogHeader(
                DialogTitle("Settings"),
                DialogDescription("Manage your account and application preferences")
            ),
            Div(
                create_tab_button("lucide:user", "Profile", "profile"),
                create_tab_button("lucide:bell", "Notifications", "notifications"),
                create_tab_button("lucide:shield", "Security", "security"),
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
                data_show=js("$settings_tab === 'profile'"),
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
                data_show=js("$settings_tab === 'notifications'"),
                cls="space-y-4"
            ),
            # Security tab
            Div(
                P("Password", cls="text-sm font-medium mb-2"),
                Div(
                    P("Last changed: 2 months ago", cls="text-sm text-muted-foreground mb-2"),
                    Button(
                        "Change Password",
                        data_on_click=js("alert('Password change dialog would open')"),
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
                        data_on_click=js("alert('Sessions dialog would open')"),
                        variant="outline",
                        size="sm",

                    ),
                    cls="mb-4"
                ),
                data_show=js("$settings_tab === 'security'"),
                cls="space-y-4"
            ),
            DialogFooter(
                DialogClose("Cancel", ref_id="settings_dialog", variant="outline"),
                Button(
                    "Save Changes",
                    data_on_click=js("""
                        alert('Settings saved successfully!');
                        $settings_dialog.close();
                    """)
                )
            ),
            cls="pb-2"
        ),
        ref_id="settings_dialog",
        size="lg"
    )


# Dialog sizes example
@with_code
def dialog_sizes_example():
    return Div(
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
    )


# ============================================================================
# MODULE-LEVEL DATA (for markdown API)
# ============================================================================

EXAMPLES_DATA = [
    {"title": "Basic Dialog", "description": "Simple dialog with title, description, and close button", "fn": basic_dialog_example},
    {"title": "Confirmation Dialog", "description": "Destructive action confirmation with warnings", "fn": confirmation_dialog_example},
    {"title": "Form Dialog", "description": "Complex form with multiple input types in a dialog", "fn": form_dialog_example},
    {"title": "Scrollable Content", "description": "Dialog with scrollable content and conditional actions", "fn": scrollable_content_example},
    {"title": "Loading/Async Dialog", "description": "Dialog with loading states, progress tracking, and async operations", "fn": loading_async_dialog_example},
    {"title": "Multi-Step Wizard", "description": "Complex wizard flow with step indicators and validation", "fn": multi_step_wizard_example},
    {"title": "Settings Dialog", "description": "Tabbed interface for managing different categories of settings", "fn": settings_dialog_example},
    {"title": "Dialog Sizes", "description": "Different dialog sizes for various content needs", "fn": dialog_sizes_example},
]

API_REFERENCE = build_api_reference(
    components=[
        Component("Dialog", "The main dialog container with modal behavior and backdrop"),
        Component("DialogTrigger", "Button that opens the dialog when clicked"),
        Component("DialogContent", "Container for all dialog content with proper styling and positioning"),
        Component("DialogHeader", "Header section containing title and description"),
        Component("DialogTitle", "Main heading for the dialog"),
        Component("DialogDescription", "Supporting text that describes the dialog purpose"),
        Component("DialogFooter", "Footer section for action buttons and controls"),
        Component("DialogClose", "Button that closes the dialog and optionally returns a value"),
    ]
)


def examples():
    """Generate dialog examples."""

    # Basic dialog
    yield ComponentPreview(
        basic_dialog_example(),
        basic_dialog_example.code,
        title="Basic Dialog",
        description="Simple dialog with title, description, and close button"
    )

    # Confirmation dialog
    yield ComponentPreview(
        confirmation_dialog_example(),
        confirmation_dialog_example.code,
        title="Confirmation Dialog",
        description="Destructive action confirmation with warnings"
    )

    # Form dialog
    yield ComponentPreview(
        form_dialog_example(),
        form_dialog_example.code,
        title="Form Dialog",
        description="Complex form with multiple input types in a dialog"
    )

    # Scrollable content dialog
    yield ComponentPreview(
        scrollable_content_example(),
        scrollable_content_example.code,
        title="Scrollable Content",
        description="Dialog with scrollable content and conditional actions"
    )

    # Loading/async dialog
    yield ComponentPreview(
        loading_async_dialog_example(),
        loading_async_dialog_example.code,
        title="Loading/Async Dialog",
        description="Dialog with loading states, progress tracking, and async operations"
    )

    # Multi-step wizard
    yield ComponentPreview(
        multi_step_wizard_example(),
        multi_step_wizard_example.code,
        title="Multi-Step Wizard",
        description="Complex wizard flow with step indicators and validation"
    )

    # Settings dialog
    yield ComponentPreview(
        settings_dialog_example(),
        settings_dialog_example.code,
        title="Settings Dialog",
        description="Tabbed interface for managing different categories of settings"
    )

    # Dialog sizes
    yield ComponentPreview(
        dialog_sizes_example(),
        dialog_sizes_example.code,
        title="Dialog Sizes",
        description="Different dialog sizes for various content needs"
    )


def create_dialog_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)