# StarMerge Usage Guide

StarMerge is a Python port of [tailwind-merge](https://github.com/dcastil/tailwind-merge) - it intelligently merges Tailwind CSS classes without style conflicts.

## Installation

```bash
pip install starmerge
```

## Basic Usage

```python
from starmerge import merge

# Later classes override earlier ones
merge("px-2 py-1 bg-red hover:bg-dark-red", "p-3 bg-[#B91C1C]")
# → 'hover:bg-dark-red p-3 bg-[#B91C1C]'

# Conflicts are resolved intelligently
merge("h-10 h-min")
# → 'h-min'

merge("text-sm text-lg")
# → 'text-lg'
```

## Usage in Component Libraries (shadcn-style)

StarMerge works **identically** to how you'd use `tailwind-merge` in JavaScript/TypeScript component libraries.

### Component Pattern

```python
from starmerge import merge

def button(variant="default", size="default", class_name=None):
    """shadcn-style button component."""

    base = "inline-flex items-center justify-center rounded-md font-medium transition-colors"

    variants = {
        "default": "bg-primary text-primary-foreground hover:bg-primary/90",
        "destructive": "bg-destructive text-destructive-foreground hover:bg-destructive/90",
        "outline": "border border-input bg-background hover:bg-accent hover:text-accent-foreground",
        "ghost": "hover:bg-accent hover:text-accent-foreground",
    }

    sizes = {
        "default": "h-10 px-4 py-2",
        "sm": "h-9 rounded-md px-3",
        "lg": "h-11 rounded-md px-8",
        "icon": "h-10 w-10",
    }

    classes = merge(
        base,
        variants.get(variant, variants["default"]),
        sizes.get(size, sizes["default"]),
        class_name or ""
    )

    return f'<button class="{classes}">Button</button>'

# Usage
button(variant="outline", size="lg", class_name="w-full")
# → class="inline-flex items-center justify-center rounded-md font-medium transition-colors border border-input bg-background hover:bg-accent hover:text-accent-foreground h-11 px-8 w-full"
```

### With FastHTML/StarHTML

```python
from starhtml import *
from starmerge import merge

def Button(*children, variant="default", size="default", **kwargs):
    """Button component with variant support."""

    base = "inline-flex items-center justify-center rounded-md font-medium transition-colors"

    variants = {
        "default": "bg-primary text-primary-foreground hover:bg-primary/90",
        "outline": "border border-input hover:bg-accent",
    }

    sizes = {
        "default": "h-10 px-4 py-2",
        "sm": "h-9 px-3",
        "lg": "h-11 px-8",
    }

    # Merge base classes with variant, size, and any custom classes
    class_name = merge(
        base,
        variants.get(variant, variants["default"]),
        sizes.get(size, sizes["default"]),
        kwargs.pop("cls", "")  # Custom classes from user
    )

    return button(*children, cls=class_name, **kwargs)

# Usage
Button("Click me", variant="outline", size="lg", cls="w-full mt-4")
```

### Card Component Example

```python
from starmerge import merge

def card(class_name=None):
    """shadcn-style card component."""
    return merge(
        "rounded-lg border bg-card text-card-foreground shadow-sm",
        class_name or ""
    )

def card_header(class_name=None):
    return merge("flex flex-col space-y-1.5 p-6", class_name or "")

def card_title(class_name=None):
    return merge(
        "text-2xl font-semibold leading-none tracking-tight",
        class_name or ""
    )

def card_content(class_name=None):
    return merge("p-6 pt-0", class_name or "")

# Usage - override default padding
card_content("p-4")
# → 'p-4'  (not 'p-6 pt-0 p-4')
```

## Advanced Features

### Arbitrary Values

```python
merge("m-[2px] m-[10px]")
# → 'm-[10px]'

merge("text-[12px] text-[14px]")
# → 'text-[14px]'
```

### Modifiers (hover, focus, responsive, etc.)

```python
merge("hover:px-2 hover:p-3")
# → 'hover:p-3'

merge("md:px-2 lg:px-3")
# → 'md:px-2 lg:px-3'  (different modifiers, no conflict)

merge("hover:focus:m-2 focus:hover:m-4")
# → 'focus:hover:m-4'  (same modifiers, different order)
```

### Important Modifier

```python
merge("!font-medium !font-bold")
# → '!font-bold'
```

### Custom Configuration

```python
from starmerge import extend_tailwind_merge

# Add custom class groups
custom_merge = extend_tailwind_merge({
    "class_groups": {
        "custom-spacing": [{"custom": ["1", "2", "3"]}]
    }
})

custom_merge("custom-1 custom-2")
# → 'custom-2'
```

## Key Differences from JavaScript tailwind-merge

The API is **identical**, with these Python-specific adjustments:

1. **Import name**:
   - JS: `import { twMerge } from 'tailwind-merge'`
   - Python: `from starmerge import merge`

2. **Function name**:
   - JS: `twMerge(...)`
   - Python: `merge(...)`
   - (Alias `tailwind_merge()` also available)

3. **Configuration keys**:
   - Use snake_case: `class_groups`, `conflicting_class_groups`
   - (camelCase also supported for compatibility)

## When to Use StarMerge

✅ **Use StarMerge when you need to:**
- Build component libraries with variant support
- Accept custom classes that override defaults
- Merge classes from multiple sources without conflicts
- Build shadcn-style components in Python

❌ **Don't need StarMerge when:**
- Just concatenating static classes (use f-strings)
- No conflicting classes to merge
- Not accepting user-provided class overrides

## Complete Example: shadcn Badge Component

```python
from starmerge import merge

def badge(variant="default", class_name=None):
    """Badge component with variants."""

    base = "inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors"

    variants = {
        "default": "border-transparent bg-primary text-primary-foreground hover:bg-primary/80",
        "secondary": "border-transparent bg-secondary text-secondary-foreground hover:bg-secondary/80",
        "destructive": "border-transparent bg-destructive text-destructive-foreground hover:bg-destructive/80",
        "outline": "text-foreground",
    }

    return merge(
        base,
        variants.get(variant, variants["default"]),
        class_name or ""
    )

# Usage
badge("New")
# → 'inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors border-transparent bg-primary text-primary-foreground hover:bg-primary/80'

badge(variant="outline", class_name="border-green-500")
# → Custom border color overrides default
```

## Resources

- **GitHub**: https://github.com/banditburai/starmerge
- **PyPI**: https://pypi.org/project/starmerge/
- **Original tailwind-merge**: https://github.com/dcastil/tailwind-merge
- **Tailwind CSS**: https://tailwindcss.com

## License

MIT - Same as the original tailwind-merge
