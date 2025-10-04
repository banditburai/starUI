# StarUI Component Architecture Patterns

This document defines the architectural patterns for StarUI components, providing clear guidance on when to use closures, slots, or direct kwargs.

## Three Core Patterns

### 1. Closures Pattern (Stateful Components)
### 2. Slots Pattern (Structural Components)
### 3. Direct Pattern (Simple Components)

---

## Pattern 1: Closures (Stateful Components)

### When to Use

Use closures when your component needs to:
- Pass Signal objects between parent and child components
- Maintain reactive state that children need programmatic access to
- Provide Signal methods like `.set()`, `.toggle()`, `.if_()` to children
- Have dynamic/flexible structure (variable number of items)

### Characteristics

- ✅ Type-safe state passing
- ✅ Signal objects available in children
- ✅ IDE autocomplete for state
- ✅ Explicit data flow
- ❌ More verbose than slots
- ❌ Fixed contract between parent/child

### Examples

Accordion, Tabs, AlertDialog, DropdownMenu, Select, RadioGroup, ToggleGroup

### Implementation Pattern

```python
# Parent component creates Signal and passes to children
def Accordion(
    *children: Any,
    type: AccordionType = "single",
    collapsible: bool = False,
    default_value: str | list[str] | None = None,
    signal: str = "",
    cls: str = "",
    **kwargs: Any,
) -> FT:
    sig_name = ensure_signal(signal, "accordion")
    initial = default_value or "" if type == "single" else (default_value or [])

    return Div(
        (sig := Signal(sig_name, initial)),
        # Children can be callables that receive state
        *[child(sig, type, collapsible) if callable(child) else child for child in children],
        cls=cn("w-full", cls),
        **kwargs,
    )


# Child component returns closure that receives state
def AccordionItem(
    *children: Any,
    value: str,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    # Returns function that will receive state from parent
    def _(sig, type="single", collapsible=False):
        return Div(
            # Passes state further down the tree
            *[child(sig, type, collapsible, value) if callable(child) else child for child in children],
            data_value=value,
            cls=cn("border-b", cls),
            **kwargs,
        )

    return _


# Leaf component uses state
def AccordionTrigger(
    *children: Any,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    def _(sig, type="single", collapsible=False, item_value=None):
        if not item_value:
            raise ValueError("AccordionTrigger must be used inside AccordionItem")

        # Can use Signal object methods directly!
        is_open = (sig == item_value) if type == "single" else sig.contains(item_value)
        click_action = sig.toggle(item_value, "") if collapsible else sig.set(item_value)

        return Button(
            *children,
            data_on_click=click_action,  # Using Signal methods
            data_attr_state=is_open.if_("open", "closed"),  # Using Signal expressions
            cls=cn("flex w-full items-center justify-between", cls),
            **kwargs,
        )

    return _
```

### Key Points

1. **Parent creates Signal**: `(sig := Signal(sig_name, initial))`
2. **Children return closures**: `def _(sig, ...): return Element(...)`
3. **Parent invokes closures**: `child(sig, type, collapsible) if callable(child) else child`
4. **Unused params prefixed with underscore**: `def _(_sig, _ref_id):` when state not needed
5. **Children can use Signal methods**: `sig.set()`, `sig.toggle()`, `sig.if_()`, etc.

### Usage Example

```python
# User code
Accordion(
    AccordionItem(
        AccordionTrigger("Section 1"),
        AccordionContent("Content 1"),
        value="item-1"
    ),
    AccordionItem(
        AccordionTrigger("Section 2"),
        AccordionContent("Content 2"),
        value="item-2"
    ),
    type="single",
    default_value="item-1"
)
```

---

## Pattern 2: Slots (Structural Components)

### When to Use

Use slots when your component:
- Has a fixed structural layout (header/body/footer)
- Doesn't need to pass Signal objects to children
- Needs runtime customization of structural elements
- Has presentational nested elements users might want to customize

### Characteristics

- ✅ Runtime flexibility
- ✅ Declarative API
- ✅ Users can apply reactive attrs to structural elements
- ❌ No Signal object access
- ❌ String-based slot matching
- ❌ Less type safety

### Examples

Card, Panel, Modal (layout only, not behavior), SplitPane, Drawer (structure)

### Implementation Pattern

```python
def Card(
    *children: Any,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    """Card with header, body, and footer slots."""

    return Div(
        Div(data_slot="header"),
        Div(*children, data_slot="body"),
        Div(data_slot="footer"),

        # Users can customize structural elements
        slot_header=dict(
            cls="card-header",
            # Users can add: data_show=condition, data_attr_class=reactive, etc.
        ),
        slot_body=dict(
            cls="card-body",
        ),
        slot_footer=dict(
            cls="card-footer",
        ),
        cls=cn("rounded-lg border bg-card text-card-foreground shadow-sm", cls),
        **kwargs,
    )
```

### Key Points

1. **Fixed structure**: Elements with `data_slot="name"` mark positions
2. **Snake_case → kebab-case**: `slot_header` targets `data-slot="header"`
3. **Dict syntax**: `slot_name=dict(attrs=values)`
4. **Same attrs as components**: Can use all Datastar attrs
5. **No Signal objects**: Can only use signal names as strings

### Usage Example

```python
# User code
Card(
    H3("Card Title"),
    P("Card content here"),

    # Customize structural elements
    slot_header=dict(
        cls="bg-primary text-primary-foreground p-4",
        data_show=is_header_visible,
        data_attr_class=is_highlighted.if_("border-accent", "")
    ),
    slot_footer=dict(
        cls="p-4 border-t",
        data_show=has_actions
    )
)
```

---

## Pattern 3: Direct (Simple Components)

### When to Use

Use direct kwargs when your component:
- Is simple/presentational
- Has no nested structure to customize
- Doesn't manage state
- All customization happens at the root element level

### Characteristics

- ✅ Simplest pattern
- ✅ Direct and obvious
- ✅ No ceremony
- ❌ Can't customize nested elements
- ❌ Limited to root element attrs

### Examples

Button, Badge, Avatar, Icon, Label, Separator, Skeleton

### Implementation Pattern

```python
def Button(
    *children: Any,
    variant: ButtonVariant = "default",
    size: ButtonSize = "default",
    cls: str = "",
    **kwargs: Any,
) -> FT:
    """Simple button component - all customization via kwargs."""

    return HTMLButton(
        *children,
        type="button",
        cls=cn(button_variants(variant=variant, size=size), cls),
        **kwargs,  # All Datastar attrs passed directly
    )
```

### Key Points

1. **No closures**: Returns element directly
2. **No slots**: No nested structure to customize
3. **All kwargs pass through**: `**kwargs` goes to root element
4. **Variant/size props**: Use typed props for built-in variations

### Usage Example

```python
# User code - all attrs go directly to button
Button(
    "Click me",
    variant="destructive",
    data_on_click=counter.add(1),
    data_attr_disabled=is_loading,
    cls="custom-class"
)
```

---

## Decision Tree

Use this flowchart to choose the right pattern:

```
Does component manage reactive state (Signals)?
├─ YES → Does it need to pass Signal objects to children?
│         ├─ YES → Use CLOSURES pattern
│         └─ NO → Does it have fixed nested structure to customize?
│                  ├─ YES → Use SLOTS pattern
│                  └─ NO → Use DIRECT pattern
└─ NO → Does it have fixed nested structure to customize?
         ├─ YES → Use SLOTS pattern
         └─ NO → Use DIRECT pattern
```

### Quick Reference Table

| Component Type | State? | Nested Structure? | Pattern |
|----------------|--------|-------------------|---------|
| Accordion | ✅ Signal passed to children | Dynamic items | **CLOSURES** |
| Tabs | ✅ Signal passed to children | Dynamic tabs | **CLOSURES** |
| AlertDialog | ✅ Signal passed to children | Fixed but stateful | **CLOSURES** |
| Card | ❌ No state | Fixed header/body/footer | **SLOTS** |
| Panel | ❌ No state | Fixed header/body | **SLOTS** |
| Button | ❌ No state | No nested structure | **DIRECT** |
| Badge | ❌ No state | No nested structure | **DIRECT** |
| Select | ✅ Signal for selection | Dynamic options | **CLOSURES** |
| Modal | ✅ Signal for open/closed | Fixed but stateful | **CLOSURES** |
| Drawer | 🤔 Depends | Fixed structure | **SLOTS** if just layout<br>**CLOSURES** if stateful |

---

## Anti-Patterns to Avoid

### ❌ Using Slots for Stateful Components

```python
# WRONG - Can't pass Signal objects through slots
def Accordion(*children, **kwargs):
    return Div(
        Div(data_slot="trigger"),
        Div(data_slot="content"),

        # ❌ Can't do this - no Signal object!
        slot_trigger=dict(
            data_on_click=sig.toggle()  # sig doesn't exist here!
        )
    )
```

### ❌ Using Closures for Simple Components

```python
# WRONG - Unnecessary complexity for simple component
def Badge(*children, **kwargs):
    def _():  # ❌ Why?
        return Span(*children, **kwargs)
    return _

# RIGHT - Keep it simple
def Badge(*children, **kwargs):
    return Span(*children, **kwargs)
```

### ❌ Mixing Patterns Inconsistently

```python
# WRONG - Some children use closures, some don't
def Parent(*children, **kwargs):
    (sig := Signal("sig", 0))
    return Div(
        sig,
        *children,  # ❌ Not calling children with sig
    )

def Child1(*children, **kwargs):
    def _(sig):  # ❌ Expects sig but parent doesn't pass it
        return Div(*children, data_on_click=sig.add(1))
    return _

def Child2(*children, **kwargs):
    return Div(*children, **kwargs)  # ❌ Inconsistent with Child1

# RIGHT - Be consistent
def Parent(*children, **kwargs):
    (sig := Signal("sig", 0))
    return Div(
        sig,
        *[child(sig) if callable(child) else child for child in children],
    )
```

### ❌ Forgetting to Handle Non-Callable Children

```python
# WRONG - Assumes all children are callables
def Parent(*children, **kwargs):
    (sig := Signal("sig", 0))
    return Div(sig, *[child(sig) for child in children])  # ❌ Crashes on non-callable

# RIGHT - Handle both callables and static content
def Parent(*children, **kwargs):
    (sig := Signal("sig", 0))
    return Div(
        sig,
        *[child(sig) if callable(child) else child for child in children]
    )
```

---

## Pattern Evolution

If you find yourself needing to change patterns:

### Closures → Slots
When state management moves entirely to backend/SSE and children only need declarative customization.

### Direct → Closures
When you add state management (e.g., Button becomes ToggleButton with active state).

### Slots → Closures
When you realize you need to pass Signal objects to customize behavior, not just appearance.

---

## Testing Pattern Compliance

When reviewing a component, ask:

1. **Does it pass Signal objects to children?**
   - YES → Should use closures
   - NO → Continue

2. **Does it have fixed structural positions users might customize?**
   - YES → Should use slots
   - NO → Continue

3. **Is it simple with no nested customization?**
   - YES → Should use direct kwargs
   - NO → Reconsider architecture

---

## Examples from Codebase

### Closures: Accordion (accordion.py:10-111)

```python
def Accordion(*children, signal="", **kwargs):
    sig = ensure_signal(signal, "accordion")
    return Div(
        (sig := Signal(sig, initial)),
        *[child(sig, type, collapsible) if callable(child) else child for child in children],
    )

def AccordionItem(*children, value, **kwargs):
    def _(sig, type, collapsible):
        return Div(*[child(sig, type, collapsible, value) if callable(child) else child for child in children])
    return _
```

### Closures: AlertDialog (alert_dialog.py:13-42)

```python
def AlertDialog(trigger, content, ref_id, **kwargs):
    trigger_element = trigger((open_sig := Signal(f"{ref_id}_open", False)), ref_id) if callable(trigger) else trigger
    content_element = content(open_sig, ref_id) if callable(content) else content
    return Div(trigger_element, dialog_element, scroll_lock)

def AlertDialogTrigger(*children, **kwargs):
    def _(open_sig, ref_id):
        return Button(*children, data_on_click=[js(f"${ref_id}.showModal()"), open_sig.set(True)])
    return _
```

### Slots: (Future Card component)

```python
def Card(*children, **kwargs):
    return Div(
        Div(data_slot="header"),
        Div(*children, data_slot="body"),
        Div(data_slot="footer"),
        slot_header=dict(cls="card-header"),
        slot_body=dict(cls="card-body"),
        **kwargs,
    )
```

### Direct: Button (button.py)

```python
def Button(*children, variant="default", size="default", cls="", **kwargs):
    return HTMLButton(
        *children,
        type="button",
        cls=cn(button_variants(variant=variant, size=size), cls),
        **kwargs,
    )
```

---

## Naming Standards

### Minimal HTML: No Unnecessary Attributes (Shadcn Philosophy)

**StarUI follows shadcn's minimalist philosophy: Don't add attributes speculatively.**

```python
# ✅ CORRECT - Minimal, clean HTML
def Alert(*children, variant="default", **kwargs):
    return Div(
        *children,
        role="alert",  # Only semantic/a11y attributes
        cls=cn(alert_variants(variant=variant), cls),
    )

def AlertDescription(*children, cls="", **kwargs):
    return Div(
        *children,
        cls=cn("text-muted-foreground col-start-2 ...", cls),
    )

# Children inherit variant styling naturally
"destructive": "text-destructive bg-card [&>iconify-icon]:text-destructive"
```

```python
# ❌ WRONG - Speculative attributes "just in case"
def Badge(*children, **kwargs):
    return Span(
        *children,
        data_slot="badge",  # ❌ Nothing targets this
        data_component="badge",  # ❌ Unnecessary metadata
        cls=cn(base_classes, cls),
    )
```

**Shadcn's approach:**
- Only semantic attributes (`role`, `aria-*`, etc.)
- Let children inherit styling naturally
- Use structural selectors when needed (`[&>svg]`, `[&_p]`)
- No parent-context child targeting for micro-optimizations

**Exception for `data-slot`:**
ONLY use `data-slot` if actively implementing the **Slots Pattern** (not for CSS targeting):
- Component has fixed structure with customizable positions
- Using `slot_*=dict()` kwargs to pass attributes to slots
- See Slots Pattern section for proper usage

**Key principle:** If you're not sure you need it, you don't need it.

---

## Backend Response Patterns

### Returning Partial HTML Updates with Datastar

When creating endpoints that return HTML fragments to be morphed into specific elements (not full page replacements), use this pattern:

```python
# Response and to_xml are already available from starhtml
# from starhtml import *

@rt("/api/data")
async def api_data():
    content = Div(
        P("✓ Data fetched successfully!"),
        id="api-response",  # ID must match selector
        cls="mt-2 p-2"
    )

    return Response(
        content=to_xml(content),       # Convert FT to HTML string
        media_type="text/html",         # Tell browser it's HTML
        headers={
            "datastar-selector": "#api-response",  # CSS selector for target
            "datastar-mode": "outer"               # How to patch element
        }
    )
```

### Key Points

1. **Use `to_xml()`** - Converts FT objects to HTML strings (not `str()`)
2. **Use `Response`** - With `media_type="text/html"` (not `HTMLResponse`)
3. **Set `datastar-selector`** - CSS selector for the target element (`#id`, `.class`, etc.)
4. **Set `datastar-mode`** - Patching strategy:
   - `outer` (default) - Replace entire element including tag
   - `inner` - Replace only innerHTML
   - `prepend`/`append` - Add before/after existing content
   - `before`/`after` - Add as sibling
   - `replace` - Replace with new element(s)
   - `remove` - Remove matched elements

### Common Modes

```python
# Replace entire element (default)
headers={"datastar-selector": "#result", "datastar-mode": "outer"}

# Replace only inner content
headers={"datastar-selector": "#container", "datastar-mode": "inner"}

# Append to list
headers={"datastar-selector": "#list", "datastar-mode": "append"}

# Insert before element
headers={"datastar-selector": "#target", "datastar-mode": "before"}
```

### Without Headers (ID-based morphing)

If you don't set headers, Datastar will try to morph by matching element IDs:

```python
# Simple case - Datastar finds matching ID automatically
return Div(
    P("New content"),
    id="my-element"  # Must match existing element's ID
)
```

**⚠️ Warning:** Without `datastar-selector` header, full page replacement may occur if ID match isn't found.

### Frontend Pattern

Button triggering backend update:

```python
Button(
    Icon("lucide:loader-2", data_show="$fetching"),
    Icon("lucide:download", data_show="!$fetching"),
    data_on_click=get("/api/data"),
    data_indicator_fetching=True,  # Creates $fetching signal
    data_attr_disabled="$fetching",
)

# Target element
Div(
    P("Response will appear here..."),
    id="api-response"
)
```

---

## Summary

- **Closures** = Stateful components that pass Signal objects
- **Slots** = Structural components with fixed, customizable positions (via `slot_*` kwargs)
- **Direct** = Simple components with no nested structure
- **HTML Minimalism** = No speculative attributes; only semantic/functional attributes needed NOW
- **Backend Responses** = Use `to_xml()` + `Response` + Datastar headers for partial updates

Choose based on: Does it pass Signals? → Closures. Does it have fixed structure? → Slots. Otherwise? → Direct.

**Golden Rule:** If you're not using it right now, don't add it. Users can extend components when they need to.

When in doubt, start with Direct and evolve to Closures/Slots as needed.
