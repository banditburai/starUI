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

from starhtml import Div, P, Input, Label, Icon, Span, H2, H3, Form, Code, Button as HTMLButton, Script
from starhtml.datastar import (
    ds_on_click, ds_show, ds_text, ds_signals, value,
    ds_bind, ds_disabled, ds_on_input, ds_effect, ds_class, ds_style,
    ds_on_mouseenter, ds_on_mouseleave
)
from starui.registry.components.textarea import Textarea, TextareaWithLabel
from starui.registry.components.button import Button
from starui.registry.components.card import Card, CardHeader, CardContent, CardTitle, CardDescription
from starui.registry.components.badge import Badge
from starui.registry.components.separator import Separator
from utils import auto_generate_page, with_code, Prop, build_api_reference
from widgets.component_preview import ComponentPreview


def examples():
    
    # Basic usage
    @with_code
    def basic_textarea_example():
        return Div(
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
            cls="space-y-4 w-full max-w-3xl mx-auto"
        )

    yield ComponentPreview(
        basic_textarea_example(),
        basic_textarea_example.code,
        title="Basic Textarea",
        description="Simple textarea with different states"
    )
    
    # Contextual usage examples
    @with_code
    def contextual_textarea_examples():
        return Div(
            Card(
                CardHeader(
                    CardTitle("Quick Note"),
                    CardDescription("Brief message or reminder")
                ),
                CardContent(
                    TextareaWithLabel(
                        label="Note",
                        placeholder="Jot down your thoughts...",
                        rows=2,
                        signal="quick_note",
                        helper_text="Perfect for short messages"
                    ),
                    Button(
                        Icon("lucide:save", cls="h-4 w-4 mr-2"),
                        "Save Note",
                        ds_on_click("alert('Note saved!')"),
                        size="sm",
                        ds_disabled="($quick_note || '').trim().length === 0",                        
                        cls="mt-3"
                    ),
                    ds_signals(quick_note=value(""))
                ),
                cls="w-full"
            ),
            Card(
                CardHeader(
                    CardTitle("Article Summary"),
                    CardDescription("Summarize the key points")
                ),
                CardContent(
                    TextareaWithLabel(
                        label="Summary",
                        placeholder="Write a concise summary of the main ideas...",
                        rows=4,
                        signal="article_summary",
                        helper_text="Aim for 2-3 sentences"
                    ),
                    Div(
                        Badge(
                            ds_text("($article_summary || '').split(' ').length + ' words'"),
                            variant="secondary"
                        ),
                        ds_show="($article_summary || '').trim().length > 0",
                        cls="mt-2"
                    ),
                    ds_signals(article_summary=value(""))
                ),
                cls="w-full"
            ),
            Card(
                CardHeader(
                    CardTitle("Essay Draft"),
                    CardDescription("Long-form writing space")
                ),
                CardContent(
                    TextareaWithLabel(
                        label="Content",
                        placeholder="Begin writing your essay or long-form content here...",
                        rows=8,
                        signal="essay_draft",
                        helper_text="Take your time to develop your ideas"
                    ),
                    Div(
                        P(
                            "Words: ",
                            Span(
                                ds_text("($essay_draft || '').trim() ? ($essay_draft || '').trim().split(/\\s+/).length : 0"),
                                cls="font-medium"
                            ),
                            " | Characters: ",
                            Span(
                                ds_text("($essay_draft || '').length"),
                                cls="font-medium"
                            ),
                            cls="text-sm text-muted-foreground"
                        ),
                        ds_show="($essay_draft || '').trim().length > 0",
                        cls="mt-2"
                    ),
                    ds_signals(essay_draft=value(""))
                ),
                cls="w-full"
            ),
            cls="grid grid-cols-1 md:grid-cols-3 gap-4 w-full max-w-6xl mx-auto"
        )

    yield ComponentPreview(
        contextual_textarea_examples(),
        contextual_textarea_examples.code,
        title="Contextual Usage",
        description="Textarea sizes matched to specific use cases"
    )
    
    # Character counter
    @with_code
    def character_counter_example():
        return Card(
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
                            ds_style(width="`${Math.min(100, ($bio || '').length / 280 * 100)}%`"),
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
                    ds_on_click("alert('Bio saved!')"),
                    cls="w-full mt-4"
                ),
                ds_signals(bio=value(""))
            ),
            cls="w-full max-w-3xl"
        )

    yield ComponentPreview(
        character_counter_example(),
        character_counter_example.code,
        title="Character Counter",
        description="Track character count with visual feedback"
    )
    
    # Comment box with live markdown preview
    @with_code
    def comment_box_live_preview_example():
        def create_format_button(icon, action, title):
            return HTMLButton(
                Icon(icon, cls="h-4 w-4"),
                ds_on_click(action),
                type="button",
                title=title,
                cls="p-2 rounded-md hover:bg-accent transition-colors border"
            )
        return Div(
            Card(
                CardHeader(
                    CardTitle("Comment Box with Live Preview"),
                    CardDescription("Rich text editor with real-time preview")
                ),
            CardContent(
                # Markdown renderer and formatting functions
                Script(r"""
                    window.renderMarkdown = function(text) {
                        if (!text) return '';
                        let html = text
                            .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')  // Bold
                            .replace(/\*(.+?)\*/g, '<em>$1</em>')  // Italic
                            .replace(/`([^`]+)`/g, '<code class="bg-gray-100 dark:bg-gray-800 px-1 rounded">$1</code>')  // Inline code
                            .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" class="text-primary underline">$1</a>')  // Links
                            .replace(/^> (.*$)/gim, '<blockquote class="border-l-4 border-gray-300 pl-4 italic">$1</blockquote>')  // Quotes
                            .replace(/^- (.*$)/gim, '<li>$1</li>')  // Lists
                            .replace(/\n/g, '<br>');  // Line breaks
                        // Wrap list items
                        return html.replace(/(<li>.*<\/li>(<br>)?)+/g, m => '<ul class="list-disc pl-5">' + m.replace(/<br>/g, '') + '</ul>');
                    };
                    
                    window.applyFormatting = function(prefix, suffix, defaultText, cursorPos) {
                        const textarea = document.querySelector('[data-bind="comment_text"]');
                        if (!textarea) return;
                        
                        const start = textarea.selectionStart;
                        const end = textarea.selectionEnd;
                        const selectedText = textarea.value.substring(start, end);
                        const replacement = selectedText ? 
                            prefix + selectedText + suffix : 
                            prefix + defaultText + suffix;
                        const newValue = textarea.value.substring(0, start) + replacement + textarea.value.substring(end);
                        
                        // Update the textarea value directly
                        textarea.value = newValue;
                        
                        // Trigger input event for Datastar binding and preview update
                        const updateEvent = new Event('input', { bubbles: true });
                        textarea.dispatchEvent(updateEvent);
                        
                        setTimeout(() => {
                            textarea.focus();
                            if (cursorPos === 'link') {
                                const linkStart = start + replacement.indexOf('](') + 2;
                                const linkEnd = start + replacement.lastIndexOf(')');
                                textarea.setSelectionRange(linkStart, linkEnd);
                            } else {
                                const newPos = start + replacement.length;
                                textarea.setSelectionRange(newPos, newPos);
                            }
                        }, 10);
                    };
                    
                    window.applyListFormatting = function(linePrefix, defaultText) {
                        const textarea = document.querySelector('[data-bind="comment_text"]');
                        if (!textarea) return;
                        
                        const start = textarea.selectionStart;
                        const end = textarea.selectionEnd;
                        const selectedText = textarea.value.substring(start, end);
                        const lines = selectedText ? selectedText.split('\\n') : [defaultText || ''];
                        const replacement = lines.map(line => linePrefix + line).join('\\n');
                        const newValue = textarea.value.substring(0, start) + replacement + textarea.value.substring(end);
                        
                        // Update the textarea value directly
                        textarea.value = newValue;
                        
                        // Trigger input event for Datastar binding and preview update
                        const updateEvent = new Event('input', { bubbles: true });
                        textarea.dispatchEvent(updateEvent);
                        
                        setTimeout(() => {
                            textarea.focus();
                            const newPos = start + replacement.length;
                            textarea.setSelectionRange(newPos, newPos);
                        }, 10);
                    };
                    
                    // Set up reactive markdown rendering after DOM loads
                    document.addEventListener('DOMContentLoaded', () => {
                        const updatePreview = () => {
                            const preview = document.getElementById('preview-area');
                            const textarea = document.querySelector('[data-bind="comment_text"]');
                            if (preview && textarea) {
                                const rendered = window.renderMarkdown(textarea.value);
                                preview.innerHTML = rendered || '<span class="text-muted-foreground">Start typing to see a preview...</span>';
                            }
                        };
                        
                        // Listen for changes
                        const textarea = document.querySelector('[data-bind="comment_text"]');
                        if (textarea) {
                            textarea.addEventListener('input', updatePreview);
                            // Initial render
                            setTimeout(updatePreview, 100);
                        }
                    });
                """),
                Form(
                    # Stacked layout
                    Div(
                        # Editor section
                        Div(
                            # Formatting toolbar
                            Div(
                                Div(
                                    create_format_button("lucide:bold", "applyFormatting('**', '**', 'bold text')", "Bold (Ctrl+B)"),
                                    create_format_button("lucide:italic", "applyFormatting('*', '*', 'italic text')", "Italic (Ctrl+I)"),
                                    create_format_button("lucide:link", "applyFormatting('[', '](https://example.com)', 'link text', 'link')", "Insert Link"),
                                    create_format_button("lucide:code", "applyFormatting('`', '`', 'code')", "Inline Code"),
                                    create_format_button("lucide:list", "applyListFormatting('- ')", "Bullet List"),
                                    create_format_button("lucide:quote", "applyListFormatting('> ', 'Quote text')", "Quote"),
                                    cls="flex gap-1"
                                ),
                                P(
                                    ds_class(**{
                                        "text-muted-foreground": "($comment_text || '').length < 500",
                                        "text-orange-500": "($comment_text || '').length >= 500 && ($comment_text || '').length < 1000",
                                        "text-destructive": "($comment_text || '').length >= 1000"
                                    }),
                                    ds_text="($comment_text || '').length + ' characters'",                                    
                                    cls="text-xs font-mono"
                                ),
                                cls="flex items-center justify-between p-3 border rounded-t-md bg-muted/30 border-b-0"
                            ),
                            
                            # Textarea with custom style override
                            Textarea(
                                placeholder="What are your thoughts? Supports **bold**, *italic*, `code`, [links](url), lists, and > quotes",
                                rows=6,
                                signal="comment_text",
                                style="outline: none !important; box-shadow: none !important; border: none !important;",
                                cls="rounded-t-none border-t-0 min-h-[150px] resize-none focus:outline-none focus:ring-0 focus:border-input focus-visible:outline-none focus-visible:ring-0 focus-visible:border-input !border-none"
                            ),
                            cls="flex-1"
                        ),
                        
                        # Live preview section 
                        Div(
                            Div(
                                P("Live Preview", cls="text-sm font-semibold mb-2"),
                                Div(
                                    Div(
                                        # Preview area - will be populated by JavaScript
                                        "Start typing to see a preview...",
                                        cls="whitespace-pre-wrap leading-relaxed prose-content",
                                        id="preview-area"
                                    ),
                                    cls="min-h-[150px] p-4 border rounded-md bg-background/50 prose prose-sm max-w-none overflow-auto"
                                )
                            ),
                            cls="w-full"
                        ),
                        cls="flex flex-col gap-4"
                    ),
                    
                    # Action buttons
                    Div(
                        Button(
                            Icon("lucide:x", cls="h-4 w-4 mr-2"),
                            "Cancel",
                            ds_on_click="$comment_text = ''",
                            variant="outline",
                            type="button",
                            ds_disabled="($comment_text || '').trim().length === 0"
                        ),
                        Button(
                            Icon("lucide:send", cls="h-4 w-4 mr-2"),
                            "Post Comment",
                            type="submit",
                            ds_disabled="($comment_text || '').trim().length === 0",
                            ds_on_click="""
                                evt.preventDefault(); 
                                if (($comment_text || '').trim().length > 0) {
                                    alert('Comment posted successfully!');
                                    $comment_text = '';
                                }
                            """
                        ),
                        cls="flex gap-3 justify-end mt-6"
                    ),
                    ds_signals(comment_text=value(""))
                )
            ),
            cls="w-full max-w-6xl"
        ),
        cls="w-full"
    )

    yield ComponentPreview(
        comment_box_live_preview_example(),
        comment_box_live_preview_example.code,
        title="Comment Box with Live Preview", 
        description="Rich text editor with real-time preview and formatting toolbar"
    )
    
    # Auto-expanding textarea
    @with_code
    def auto_expanding_textarea_example():
        return Card(
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
            cls="w-full max-w-3xl"
        )

    yield ComponentPreview(
        auto_expanding_textarea_example(),
        auto_expanding_textarea_example.code,
        title="Auto-Expanding",
        description="Textarea that grows with content"
    )
    
    # Enhanced feedback form with advanced validation
    @with_code
    def enhanced_feedback_form_example():
        return Card(
            CardHeader(
                CardTitle("Customer Feedback"),
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
                        error_text=None,
                        helper_text="Share your honest thoughts (10-1000 characters)"
                    ),
                    # Validation messages
                    Div(
                        P(
                            "Feedback is required",
                            cls="text-sm text-destructive"
                        ),
                        ds_show("$feedback_submitted && ($feedback || '').trim().length === 0")
                    ),
                    Div(
                        P(
                            "Please provide at least 10 characters",
                            cls="text-sm text-destructive"
                        ),
                        ds_show("$feedback_submitted && ($feedback || '').trim().length > 0 && ($feedback || '').length < 10")
                    ),
                    Div(
                        P(
                            "Feedback cannot exceed 1000 characters",
                            cls="text-sm text-destructive"
                        ),
                        ds_show("($feedback || '').length > 1000")
                    ),
                    Div(
                        P(
                            "Rate your experience",
                            cls="text-sm font-medium mb-3"
                        ),
                        Div(
                            *[
                                HTMLButton(
                                    "★",
                                    ds_class(**{
                                        "text-yellow-500": f"($feedback_rating && $feedback_rating >= {i+1}) || ($hover_rating && $hover_rating >= {i+1})",
                                        "text-gray-300": f"(!$feedback_rating || $feedback_rating < {i+1}) && (!$hover_rating || $hover_rating < {i+1})"
                                    }),
                                    ds_on_click(f"$feedback_rating = $feedback_rating === {i+1} ? null : {i+1}"),
                                    ds_on_mouseenter(f"$hover_rating = {i+1}"),
                                    ds_on_mouseleave("$hover_rating = null"),
                                    type="button",
                                    cls="text-3xl transition-colors"
                                )
                                for i in range(5)
                            ],
                            cls="flex gap-1 mb-2"
                        ),
                        P(
                            "Rating: ",
                            Span(
                                ds_text("$feedback_rating || 'Not selected'"),
                                cls="font-medium"
                            ),
                            cls="text-sm text-muted-foreground"
                        ),
                        cls="border rounded-lg p-4 bg-muted/30 my-6"
                    ),
                    TextareaWithLabel(
                        label="Additional suggestions",
                        placeholder="Any specific improvements you'd like to see? (optional)",
                        rows=3,
                        signal="suggestions",
                        helper_text="This helps us prioritize improvements"
                    ),
                    Div(
                        # Status indicators
                        Badge(
                            Icon("lucide:clock", cls="h-3 w-3 mr-1"),                            
                            "Draft",
                            ds_show("($feedback || '').trim().length > 0 && ($feedback || '').length < 10"),
                            variant="secondary",                            
                        ),
                        Badge(
                            Icon("lucide:check-circle", cls="h-3 w-3 mr-1"),
                            "Ready to submit",
                            ds_show("($feedback || '').length >= 10 && ($feedback || '').length <= 1000 && !$feedback_rating"),
                            variant="default",                            
                        ),
                        Badge(
                            Icon("lucide:star", cls="h-3 w-3 mr-1"),
                            "Complete",
                            ds_show("($feedback || '').length >= 10 && $feedback_rating"),
                            variant="default",                            
                        ),
                        cls="flex flex-wrap gap-2 mb-4"
                    ),
                    Div(
                        Button(
                            "Clear Form",
                            variant="outline",
                            type="button",
                            ds_on_click="""
                                $feedback = '';
                                $suggestions = '';
                                $feedback_rating = null;
                                $hover_rating = null;
                                $feedback_submitted = false;
                            """,
                            ds_disabled="($feedback || '').length === 0 && ($suggestions || '').length === 0 && !$feedback_rating"
                        ),
                        Button(
                            Icon("lucide:send", cls="h-4 w-4 mr-2"),
                            "Submit Feedback",
                            type="submit",
                            ds_disabled="($feedback || '').length < 10 || !$feedback_rating || ($feedback || '').length > 1000",
                            ds_on_click="""
                                evt.preventDefault();
                                $feedback_submitted = true;
                                if (($feedback || '').length >= 10 && $feedback_rating && ($feedback || '').length <= 1000) {
                                    alert(`Thank you for your ${$feedback_rating}-star feedback!`);
                                    $feedback = '';
                                    $suggestions = '';
                                    $feedback_rating = null;
                                    $feedback_submitted = false;
                                }
                            """
                        ),
                        cls="flex gap-2 justify-end"
                    ),
                    ds_signals(
                        feedback=value(""), 
                        suggestions=value(""), 
                        feedback_rating=value(None),
                        hover_rating=value(None),
                        feedback_submitted=False
                    )
                )
            ),
            cls="w-full max-w-3xl"
        )

    yield ComponentPreview(
        enhanced_feedback_form_example(),
        enhanced_feedback_form_example.code,
        title="Feedback Form",
        description="Multi-field form with validation"
    )
    
    # Code editor style
    @with_code
    def code_editor_textarea_example():
        return Card(
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
                            Span(Icon("lucide:check", cls="h-4 w-4 mr-2"), ds_show("$code_copied")),
                            Span(Icon("lucide:copy", cls="h-4 w-4 mr-2"), ds_show("!$code_copied")),
                            Span("Copied!", ds_show("$code_copied")),
                            Span("Copy", ds_show("!$code_copied")),
                            ds_on_click("@clipboard($code_editor || '', 'code_copied', 2000)"),
                            size="sm",
                            variant="outline",                            
                        ),
                        cls="flex items-center justify-between mt-2"
                    ),
                    ds_signals(
                        code_editor=value("def hello_world():\n    print('Hello, World!')\n    return True"),
                        code_copied=False
                    )
                )
            ),
            cls="w-full max-w-3xl"
        )

    yield ComponentPreview(
        code_editor_textarea_example(),
        code_editor_textarea_example.code,
        title="Code Editor",
        description="Code input with monospace font and utilities"
    )
    
    # Email template composer
    @with_code
    def email_template_composer_example():
        def create_variable_button(var_name):
            return HTMLButton(
                f"{{{{{{var_name}}}}}}",
                ds_on_click(f"insertVariable('{var_name}')"),
                type="button",
                cls="px-2 py-1 text-xs bg-muted hover:bg-accent rounded border"
            )
        return Card(
            CardHeader(
                CardTitle("Email Template Composer"),
                CardDescription("Create professional email templates with variables")
            ),
            CardContent(
                Form(
                    Div(
                        TextareaWithLabel(
                            label="Subject Line",
                            placeholder="Welcome to {{company_name}}, {{first_name}}!",
                            rows=1,
                            signal="email_subject",
                            helper_text="Use {{variable}} syntax for dynamic content"
                        ),
                        cls="mb-4"
                    ),
                    TextareaWithLabel(
                        label="Email Body",
                        placeholder="Hi {{first_name}},\n\nWelcome to {{company_name}}! We're excited to have you on board.\n\nBest regards,\n{{sender_name}}",
                        rows=8,
                        signal="email_body",
                        helper_text="Available variables: {{first_name}}, {{last_name}}, {{company_name}}, {{sender_name}}"
                    ),
                    
                    # Variable insertion toolbar with script for cursor position
                    Script(r"""
                        // Track last focused textarea
                        let lastFocusedTextarea = null;
                        
                        // Set up focus tracking after DOM loads
                        document.addEventListener('DOMContentLoaded', () => {
                            const bodyTextarea = document.querySelector('[data-bind="email_body"]');
                            const subjectTextarea = document.querySelector('[data-bind="email_subject"]');
                            
                            if (bodyTextarea) {
                                bodyTextarea.addEventListener('focus', () => {
                                    lastFocusedTextarea = bodyTextarea;
                                });
                            }
                            
                            if (subjectTextarea) {
                                subjectTextarea.addEventListener('focus', () => {
                                    lastFocusedTextarea = subjectTextarea;
                                });
                            }
                            
                            // Default to body textarea
                            lastFocusedTextarea = bodyTextarea;
                        });
                        
                        window.insertVariable = function(varName) {
                            // Use the last focused textarea, or fall back to body
                            const bodyTextarea = document.querySelector('[data-bind="email_body"]');
                            let targetTextarea = lastFocusedTextarea || bodyTextarea;
                            
                            if (!targetTextarea) return;
                            
                            const start = targetTextarea.selectionStart;
                            const end = targetTextarea.selectionEnd;
                            const text = targetTextarea.value;
                            const variable = '{{' + varName + '}}';
                            
                            // Insert at cursor position
                            const newValue = text.substring(0, start) + variable + text.substring(end);
                            targetTextarea.value = newValue;
                            
                            // No need to manually update signal - the input event will handle it
                            
                            // Trigger input evt for reactivity
                            targetTextarea.dispatchEvent(new Event('input', { bubbles: true }));
                            
                            // Set cursor after inserted variable
                            setTimeout(() => {
                                targetTextarea.focus();
                                const newPos = start + variable.length;
                                targetTextarea.setSelectionRange(newPos, newPos);
                            }, 10);
                        };
                    """),
                    Div(
                        P("Quick Variables:", cls="text-sm font-medium mb-2"),
                        Div(
                            create_variable_button("first_name"),
                            create_variable_button("last_name"),
                            create_variable_button("company_name"),
                            create_variable_button("sender_name"),
                            cls="flex flex-wrap gap-2"
                        ),
                        cls="p-3 border rounded-md bg-muted/30 mb-4"
                    ),
                    
                    # Preview section
                    Div(
                        P("Preview", cls="text-sm font-medium mb-2"),
                        Div(
                            Div(
                                P("Subject:", cls="text-xs text-muted-foreground"),
                                P(
                                    ds_text("($email_subject || 'No subject').replace(/{{([^}]+)}}/g, function(m,p1){return '[' + p1 + ']'})"),
                                    cls="font-medium text-sm mb-2"
                                ),
                                Separator(cls="my-2"),
                                P(
                                    ds_text("($email_body || 'No content').replace(/{{([^}]+)}}/g, function(m,p1){return '[' + p1 + ']'})"),
                                    cls="text-sm whitespace-pre-wrap"
                                )
                            ),
                            cls="p-3 bg-background border rounded-md min-h-[120px]"
                        ),
                        P("Variables will be replaced with actual values when sent", cls="text-xs text-muted-foreground mt-1"),
                        ds_show="($email_subject || '').length > 0 || ($email_body || '').length > 0",
                        cls="mb-4"
                    ),
                    
                    # Actions
                    Div(
                        Button(
                            Icon("lucide:eye", cls="h-4 w-4 mr-2"),
                            "Test Send",
                            ds_on_click("alert('Test email sent to your address!')"),
                            variant="outline",
                            type="button",
                            ds_disabled="($email_subject || '').length === 0 || ($email_body || '').length === 0",                            
                        ),
                        Button(
                            Icon("lucide:save", cls="h-4 w-4 mr-2"),
                            "Save Template",
                            type="submit",
                            ds_disabled="($email_subject || '').length === 0 || ($email_body || '').length === 0",
                            ds_on_click="""
                                evt.preventDefault();
                                if (($email_subject || '').length > 0 && ($email_body || '').length > 0) {
                                    alert('Template saved successfully!');
                                }
                            """
                        ),
                        cls="flex gap-2 justify-end"
                    ),
                    
                    ds_signals(
                        email_subject=value("Welcome to {{company_name}}, {{first_name}}!"),
                        email_body=value("Hi {{first_name}},\n\nWelcome to {{company_name}}! We're excited to have you on board.\n\nBest regards,\n{{sender_name}}")
                    )
                )
            ),
            cls="max-w-3xl"
        )

    yield ComponentPreview(
        email_template_composer_example(),
        email_template_composer_example.code,
        title="Email Template Composer",
        description="Professional template system with variable substitution"
    )


def create_textarea_docs():
    
    # For Textarea, users need the key props they will set most often.
    api_reference = build_api_reference(
        main_props=[
            Prop("placeholder", "str | None", "Placeholder text shown when empty", "None"),
            Prop("value", "str | None", "Initial text value", "None"),
            Prop("signal", "str | None", "Datastar signal for two-way binding", "None"),
            Prop("rows", "int | None", "Number of visible text rows", "None"),
            Prop("maxlength", "int | None", "Maximum number of characters", "None"),
            Prop("resize", "Literal['none','both','horizontal','vertical'] | None", "Controls textarea resizing behavior", "None"),
            Prop("disabled", "bool", "Whether the textarea is disabled", "False"),
            Prop("required", "bool", "Whether the textarea is required", "False"),
            Prop("cls", "str", "Additional CSS classes", "''"),
        ]
    )
    
    # Hero example
    @with_code
    def hero_textarea_example():
        return Div(
            TextareaWithLabel(
                label="Description",
                placeholder="Enter a detailed description...",
                rows=4,
                signal="hero_textarea",
                helper_text="Provide as much detail as needed"
            ),
            cls="w-full max-w-4xl mx-auto"
        )

    hero_example = ComponentPreview(
        hero_textarea_example(),
        hero_textarea_example.code,
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