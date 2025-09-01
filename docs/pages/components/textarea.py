"""
Textarea component documentation - Convention-based functional approach.
Clean, minimal, and easy to extend.
"""

# Component metadata for auto-discovery
TITLE = "Textarea"
DESCRIPTION = "A multi-line text input field for longer content like comments, messages, and descriptions."
CATEGORY = "form"
ORDER = 25
STATUS = "stable"

from starhtml import Div, P, Input, Label, Icon, Span, H2, H3, Form, Code, Button as HTMLButton
from starhtml.datastar import (
    ds_on_click, ds_show, ds_text, ds_signals, value,
    ds_bind, ds_disabled, ds_on_input, ds_effect, ds_class, toggle, ds_style
)
from starui.registry.components.textarea import Textarea, TextareaWithLabel
from starui.registry.components.button import Button
from starui.registry.components.card import Card, CardHeader, CardContent, CardTitle, CardDescription
from starui.registry.components.badge import Badge
from starui.registry.components.separator import Separator
from utils import auto_generate_page
from widgets.component_preview import ComponentPreview


def examples():
    """Generate textarea examples using ComponentPreview with tabs."""
    
    # Basic usage
    yield ComponentPreview(
        Div(
            Textarea(placeholder="Type your message here..."),
            Textarea(
                placeholder="With initial value",
                value="This textarea starts with content that you can edit.",
                cls="mt-4"
            ),
            Textarea(
                placeholder="Disabled textarea",
                disabled=True,
                cls="mt-4"
            ),
            cls="space-y-4 max-w-md mx-auto"
        ),
        '''Textarea(placeholder="Type your message here...")
Textarea(
    placeholder="With initial value",
    value="This textarea starts with content that you can edit."
)
Textarea(placeholder="Disabled textarea", disabled=True)''',
        title="Basic Textarea",
        description="Simple textarea with different states"
    )
    
    # Size variations
    yield ComponentPreview(
        Div(
            TextareaWithLabel(
                label="Compact (2 rows)",
                placeholder="Brief input...",
                rows=2,
                signal="compact"
            ),
            TextareaWithLabel(
                label="Standard (4 rows)",
                placeholder="Regular input...",
                rows=4,
                signal="standard"
            ),
            TextareaWithLabel(
                label="Extended (8 rows)",
                placeholder="Detailed input...",
                rows=8,
                signal="extended"
            ),
            cls="space-y-4 max-w-md mx-auto"
        ),
        '''TextareaWithLabel(
    label="Compact (2 rows)",
    placeholder="Brief input...",
    rows=2
)
TextareaWithLabel(
    label="Standard (4 rows)",
    placeholder="Regular input...",
    rows=4
)
TextareaWithLabel(
    label="Extended (8 rows)",
    placeholder="Detailed input...",
    rows=8
)''',
        title="Size Variations",
        description="Different row heights for various use cases"
    )
    
    # Character counter
    yield ComponentPreview(
        Card(
            CardHeader(
                CardTitle("Bio"),
                CardDescription("Tell us about yourself")
            ),
            CardContent(
                TextareaWithLabel(
                    label="Your Bio",
                    placeholder="Share your background, interests, and expertise...",
                    rows=4,
                    maxlength=280,
                    signal="bio",
                    helper_text="Max 280 characters"
                ),
                Div(
                    Div(
                        Div(
                            ds_style(width="min(100%, calc(($bio || '').length / 280 * 100%))"),
                            cls="h-1 bg-primary rounded-full transition-all duration-300"
                        ),
                        cls="w-full bg-secondary rounded-full h-1"
                    ),
                    P(
                        Span(ds_text("($bio || '').length"), cls="font-mono font-medium"),
                        " / 280 characters",
                        ds_class(**{
                            "text-muted-foreground": "($bio || '').length < 250",
                            "text-orange-500": "($bio || '').length >= 250 && ($bio || '').length < 280",
                            "text-destructive": "($bio || '').length >= 280"
                        }),
                        cls="text-sm text-right"
                    ),
                    cls="space-y-2 mt-3"
                ),
                Button(
                    "Save Bio",
                    ds_disabled("($bio || '').length === 0"),
                    ds_on_click="alert('Bio saved!')",
                    cls="w-full mt-4"
                ),
                ds_signals(bio=value(""))
            ),
            cls="max-w-md"
        ),
        '''Card(
    CardContent(
        TextareaWithLabel(
            label="Your Bio",
            placeholder="Share your background...",
            maxlength=280,
            signal="bio"
        ),
        Div(
            // Progress bar
            Div(
                ds_style(width="min(100%, calc(($bio || '').length / 280 * 100%))"),
                cls="h-1 bg-primary rounded-full"
            ),
            // Character count
            P(
                Span(ds_text("($bio || '').length")),
                " / 280 characters",
                ds_class({
                    "text-muted-foreground": "($bio || '').length < 250",
                    "text-orange-500": "($bio || '').length >= 250",
                    "text-destructive": "($bio || '').length >= 280"
                })
            )
        ),
        ds_signals(bio=value(""))
    )
)''',
        title="Character Counter",
        description="Track character count with visual feedback"
    )
    
    # Comment box with formatting hints
    yield ComponentPreview(
        Card(
            CardHeader(
                CardTitle("Add Comment"),
                CardDescription("Share your thoughts with the community")
            ),
            CardContent(
                Form(
                    TextareaWithLabel(
                        label="Your Comment",
                        placeholder="What are your thoughts?",
                        rows=4,
                        signal="comment",
                        helper_text="Markdown formatting is supported"
                    ),
                    Div(
                        HTMLButton(
                            Icon("lucide:bold", cls="h-4 w-4"),
                            type="button",
                            ds_on_click="$comment = $comment + '**bold**'",
                            cls="p-1.5 rounded hover:bg-accent"
                        ),
                        HTMLButton(
                            Icon("lucide:italic", cls="h-4 w-4"),
                            type="button",
                            ds_on_click="$comment = $comment + '*italic*'",
                            cls="p-1.5 rounded hover:bg-accent"
                        ),
                        HTMLButton(
                            Icon("lucide:link", cls="h-4 w-4"),
                            type="button",
                            ds_on_click="$comment = $comment + '[link](url)'",
                            cls="p-1.5 rounded hover:bg-accent"
                        ),
                        HTMLButton(
                            Icon("lucide:code", cls="h-4 w-4"),
                            type="button",
                            ds_on_click="$comment = $comment + '`code`'",
                            cls="p-1.5 rounded hover:bg-accent"
                        ),
                        HTMLButton(
                            Icon("lucide:list", cls="h-4 w-4"),
                            type="button",
                            ds_on_click="$comment = $comment + '\\n- Item'",
                            cls="p-1.5 rounded hover:bg-accent"
                        ),
                        cls="flex gap-1 p-1 border rounded-md"
                    ),
                    Div(
                        Button(
                            "Cancel",
                            variant="outline",
                            type="button",
                            ds_on_click="$comment = ''"
                        ),
                        Button(
                            "Post Comment",
                            type="submit",
                            ds_disabled="($comment || '').trim().length === 0",
                            ds_on_click="event.preventDefault(); alert('Comment posted!')"
                        ),
                        cls="flex gap-2 justify-end mt-4"
                    ),
                    ds_signals(comment=value(""))
                )
            ),
            cls="max-w-lg"
        ),
        '''Card(
    CardContent(
        Form(
            TextareaWithLabel(
                label="Your Comment",
                placeholder="What are your thoughts?",
                signal="comment",
                helper_text="Markdown formatting is supported"
            ),
            Div(  // Formatting toolbar
                Button(Icon("lucide:bold"), ds_on_click="$comment += '**bold**'"),
                Button(Icon("lucide:italic"), ds_on_click="$comment += '*italic*'"),
                Button(Icon("lucide:link"), ds_on_click="$comment += '[link](url)'"),
                Button(Icon("lucide:code"), ds_on_click="$comment += '`code`'"),
                cls="flex gap-1"
            ),
            Button(
                "Post Comment",
                ds_disabled="($comment || '').trim().length === 0"
            ),
            ds_signals(comment=value(""))
        )
    )
)''',
        title="Comment Box",
        description="Rich text comment with formatting toolbar"
    )
    
    # Auto-expanding textarea
    yield ComponentPreview(
        Card(
            CardHeader(
                CardTitle("Auto-Expanding"),
                CardDescription("Grows with your content")
            ),
            CardContent(
                TextareaWithLabel(
                    label="Message",
                    placeholder="Start typing and watch it grow...",
                    signal="auto_expand",
                    helper_text="This textarea expands as you type",
                    cls="[&_textarea]:field-sizing-content [&_textarea]:min-h-[60px] [&_textarea]:max-h-[300px]"
                ),
                P(
                    "Lines: ",
                    Span(
                        ds_text("(($auto_expand || '').match(/\\n/g) || []).length + 1"),
                        cls="font-mono font-medium"
                    ),
                    cls="text-sm text-muted-foreground mt-2"
                ),
                ds_signals(auto_expand=value(""))
            ),
            cls="max-w-md"
        ),
        '''TextareaWithLabel(
    label="Message",
    placeholder="Start typing and watch it grow...",
    signal="auto_expand",
    cls="[&_textarea]:field-sizing-content [&_textarea]:min-h-[60px] [&_textarea]:max-h-[300px]"
)
// The field-sizing-content CSS property makes it auto-expand''',
        title="Auto-Expanding",
        description="Textarea that grows with content"
    )
    
    # Feedback form with validation
    yield ComponentPreview(
        Card(
            CardHeader(
                CardTitle("Feedback Form"),
                CardDescription("Help us improve our service")
            ),
            CardContent(
                Form(
                    TextareaWithLabel(
                        label="How was your experience?",
                        placeholder="Tell us what you think...",
                        required=True,
                        rows=4,
                        signal="feedback",
                        error_text=ds_show("$feedback_submitted && ($feedback || '').length < 10") and "Feedback must be at least 10 characters" or None,
                        helper_text="Minimum 10 characters required"
                    ),
                    TextareaWithLabel(
                        label="Suggestions for improvement",
                        placeholder="Any ideas to make things better? (optional)",
                        rows=3,
                        signal="suggestions"
                    ),
                    Div(
                        Badge(
                            "Draft",
                            variant="secondary",
                            ds_show="($feedback || '').length > 0 && ($feedback || '').length < 10"
                        ),
                        Badge(
                            "Ready to submit",
                            variant="default",
                            ds_show="($feedback || '').length >= 10"
                        ),
                        cls="flex gap-2 mb-4"
                    ),
                    Button(
                        "Submit Feedback",
                        type="submit",
                        ds_on_click="""
                            event.preventDefault();
                            $feedback_submitted = true;
                            if (($feedback || '').length >= 10) {
                                alert('Thank you for your feedback!');
                                $feedback = '';
                                $suggestions = '';
                                $feedback_submitted = false;
                            }
                        """,
                        cls="w-full"
                    ),
                    ds_signals(feedback=value(""), suggestions=value(""), feedback_submitted=False)
                )
            ),
            cls="max-w-md"
        ),
        '''Card(
    CardContent(
        Form(
            TextareaWithLabel(
                label="How was your experience?",
                required=True,
                signal="feedback",
                error_text=ds_show("$feedback_submitted && $feedback.length < 10") 
                    and "Minimum 10 characters" or None,
                helper_text="Minimum 10 characters required"
            ),
            TextareaWithLabel(
                label="Suggestions for improvement",
                placeholder="Any ideas? (optional)",
                signal="suggestions"
            ),
            Badge(
                "Ready to submit",
                ds_show="$feedback.length >= 10"
            ),
            Button(
                "Submit Feedback",
                ds_on_click="validateAndSubmit()"
            ),
            ds_signals(feedback="", suggestions="", feedback_submitted=False)
        )
    )
)''',
        title="Feedback Form",
        description="Multi-field form with validation"
    )
    
    # Code editor style
    yield ComponentPreview(
        Card(
            CardHeader(
                CardTitle("Code Editor"),
                CardDescription("Write and format code")
            ),
            CardContent(
                Div(
                    Div(
                        P("Language: ", cls="text-sm text-muted-foreground"),
                        Badge("Python", variant="outline"),
                        cls="flex items-center justify-between mb-2"
                    ),
                    Textarea(
                        placeholder="# Enter your code here...",
                        signal="code_editor",
                        rows=8,
                        cls="font-mono text-sm",
                        resize="vertical"
                    ),
                    Div(
                        P(
                            "Lines: ",
                            Span(
                                ds_text("(($code_editor || '').match(/\\n/g) || []).length + 1"),
                                cls="font-mono"
                            ),
                            " | Characters: ",
                            Span(
                                ds_text("($code_editor || '').length"),
                                cls="font-mono"
                            ),
                            cls="text-xs text-muted-foreground"
                        ),
                        Button(
                            Icon("lucide:copy", cls="h-4 w-4 mr-2"),
                            "Copy",
                            size="sm",
                            variant="outline",
                            ds_on_click="navigator.clipboard.writeText($code_editor); alert('Copied!')"
                        ),
                        cls="flex items-center justify-between mt-2"
                    ),
                    ds_signals(code_editor=value("def hello_world():\n    print('Hello, World!')\n    return True"))
                )
            ),
            cls="max-w-lg"
        ),
        '''Textarea(
    placeholder="# Enter your code here...",
    signal="code_editor",
    rows=8,
    cls="font-mono text-sm",
    resize="vertical"
)
// With line/char count and copy button
Div(
    P("Lines: ", Span(ds_text("lines")), " | Characters: ", Span(ds_text("chars"))),
    Button(Icon("lucide:copy"), "Copy", ds_on_click="copyCode()")
)''',
        title="Code Editor",
        description="Code input with monospace font and utilities"
    )


def create_textarea_docs():
    """Create textarea documentation page using convention-based approach."""
    
    api_reference = {
        "props": [
            {
                "name": "placeholder",
                "type": "str | None",
                "default": "None",
                "description": "Placeholder text when empty"
            },
            {
                "name": "value",
                "type": "str | None",
                "default": "None",
                "description": "Initial text value"
            },
            {
                "name": "signal",
                "type": "str | None",
                "default": "None",
                "description": "Datastar signal for two-way binding"
            },
            {
                "name": "name",
                "type": "str | None",
                "default": "None",
                "description": "Name attribute for form submission"
            },
            {
                "name": "disabled",
                "type": "bool",
                "default": "False",
                "description": "Whether textarea is disabled"
            },
            {
                "name": "readonly",
                "type": "bool",
                "default": "False",
                "description": "Whether textarea is read-only"
            },
            {
                "name": "required",
                "type": "bool",
                "default": "False",
                "description": "Whether textarea is required"
            },
            {
                "name": "rows",
                "type": "int | None",
                "default": "None",
                "description": "Number of visible text rows"
            },
            {
                "name": "cols",
                "type": "int | None",
                "default": "None",
                "description": "Visible width in character columns"
            },
            {
                "name": "maxlength",
                "type": "int | None",
                "default": "None",
                "description": "Maximum number of characters"
            },
            {
                "name": "resize",
                "type": "Literal['none', 'both', 'horizontal', 'vertical'] | None",
                "default": "None",
                "description": "Controls textarea resizing behavior"
            },
            {
                "name": "cls",
                "type": "str",
                "default": "''",
                "description": "Additional CSS classes"
            }
        ],
        "helper_components": [
            {
                "name": "TextareaWithLabel",
                "description": "Textarea with integrated label and helper/error text",
                "props": [
                    {
                        "name": "label",
                        "type": "str",
                        "description": "Label text for the textarea"
                    },
                    {
                        "name": "helper_text",
                        "type": "str | None",
                        "description": "Helper text displayed below the textarea"
                    },
                    {
                        "name": "error_text",
                        "type": "str | None",
                        "description": "Error message displayed below the textarea"
                    },
                    {
                        "name": "label_cls",
                        "type": "str",
                        "description": "Additional CSS classes for the label"
                    },
                    {
                        "name": "textarea_cls",
                        "type": "str",
                        "description": "Additional CSS classes for the textarea itself"
                    }
                ]
            }
        ]
    }
    
    # Hero example
    hero_example = ComponentPreview(
        Div(
            TextareaWithLabel(
                label="Description",
                placeholder="Enter a detailed description...",
                rows=4,
                signal="hero_textarea",
                helper_text="Provide as much detail as needed"
            ),
            cls="max-w-md mx-auto"
        ),
        '''TextareaWithLabel(
    label="Description",
    placeholder="Enter a detailed description...",
    rows=4,
    signal="description",
    helper_text="Provide as much detail as needed"
)''',
        copy_button=True
    )
    
    return auto_generate_page(
        TITLE,
        DESCRIPTION,
        list(examples()),
        cli_command="star add textarea",
        api_reference=api_reference,
        hero_example=hero_example,
        component_slug="textarea"
    )