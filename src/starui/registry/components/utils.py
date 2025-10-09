from collections.abc import Callable
from typing import Any
from uuid import uuid4
from starhtml import Div, Signal
from starhtml.datastar import Expr, _JSRaw, _ensure_expr

try:
    from starmerge import merge
except ImportError:
    def merge(*classes: str) -> str:
        return " ".join(c for c in classes if c)


def with_signals(component, **signals):
    """
    Attach signals as attributes to a component for IDE autocomplete and type hints.

    Usage:
        return with_signals(
            Div(...),
            selected=selected_sig,
            month=month_sig,
        )

    This allows users to access component.selected, component.month, etc.
    """
    for name, signal in signals.items():
        setattr(component, name, signal)
    return component

# Theme configuration
DEFAULT_THEME = "light"
ALT_THEME = "dark"


def cn(*classes: Any) -> str:
    """Merge Tailwind classes intelligently, resolving conflicts."""
    processed: list[str] = []

    for cls in classes:
        if not cls:
            continue

        if isinstance(cls, str):
            processed.append(cls)
        elif isinstance(cls, dict):
            for class_name, condition in cls.items():
                if condition:
                    processed.append(str(class_name))
        elif isinstance(cls, list | tuple):
            processed.append(cn(*cls))
        else:
            processed.append(str(cls))

    return merge(*processed) if processed else ""


def cva(base: str = "", config: dict[str, Any] | None = None) -> Callable[..., str]:
    if config is None:
        config = {}

    variants = config.get("variants", {})
    compound_variants = config.get("compoundVariants", [])
    default_variants = config.get("defaultVariants", {})

    def variant_function(**props: Any) -> str:
        classes = [base] if base else []

        # Merge defaults with props
        final_props = {**default_variants, **props}

        # Apply variants
        for variant_key, variant_values in variants.items():
            prop_value = final_props.get(variant_key)
            if prop_value and prop_value in variant_values:
                classes.append(variant_values[prop_value])

        # Apply compound variants
        for compound in compound_variants:
            compound_class = compound.get("class", "")
            if not compound_class:
                continue

            matches = True
            for key, value in compound.items():
                if key == "class":
                    continue
                if final_props.get(key) != value:
                    matches = False
                    break

            if matches:
                classes.append(compound_class)

        return cn(*classes)

    return variant_function

def gen_id(prefix: str) -> str:
    """Generate a short, unique id with a given prefix."""
    return f"{prefix}_{uuid4().hex[:8]}"


def ensure_signal(signal: str | None, prefix: str) -> str:
    """Return the provided signal or generate one with the prefix."""
    return signal or gen_id(prefix)


def inject_context(element, **context):
    """Recursively inject context into callable children, preserving structure.

    Allows arbitrary HTML wrappers while ensuring context flows to nested callables.
    """
    if callable(element):
        result = element(**context)
        if hasattr(result, 'children') and result.children:
            result.children = tuple(inject_context(c, **context) for c in result.children)
        return result

    if hasattr(element, 'children') and element.children:
        element.children = tuple(inject_context(c, **context) for c in element.children)

    return element


# Timer utilities - generate JavaScript setTimeout/clearTimeout expressions
def _timer_ref(timer: Signal, window: bool = False) -> str:
    """Generate JavaScript reference for a timer Signal.

    Args:
        timer: Signal containing timer ID
        window: If True, use window._ prefix (persists across DOM updates)

    Returns:
        String reference: $timer or window._timer
    """
    timer_id = timer.id if hasattr(timer, 'id') else timer
    return f"window._{timer_id}" if window else f"${timer_id}"


def set_timeout(action: Any, ms: int | Expr, *, store: Signal | None = None, window: bool = False) -> _JSRaw:
    """Generate setTimeout JavaScript expression.

    Args:
        action: Expression or list of expressions to execute after delay
        ms: Delay in milliseconds (can be Signal or int)
        store: Optional Signal to store timer ID for later cancellation
        window: If True, store timer as window property (persists across DOM updates)

    Returns:
        _JSRaw expression: setTimeout(() => { action }, ms)
        or with store: $timer = setTimeout(() => { action }, ms)

    Examples:
        # Fire-and-forget timer
        set_timeout(copied.set(False), 2000)
        # → setTimeout(() => { $copied = false }, 2000)

        # Store timer ID for cancellation (component-scoped)
        set_timeout(open_state.set(True), 700, store=timer_sig)
        # → $timer = setTimeout(() => { $open_state = true }, 700)

        # Store as window property (persists across element replacement)
        set_timeout(selected.set(0), 50, store=timer_sig, window=True)
        # → window._timer = setTimeout(() => { $selected = 0 }, 50)

        # Multiple actions
        set_timeout([step.set(2), progress.set(40)], 1000)
        # → setTimeout(() => { $step = 2; $progress = 40 }, 1000)
    """
    action_js = _ensure_expr(action).to_js() if not isinstance(action, list) \
                else "; ".join(_ensure_expr(a).to_js() for a in action)
    ms_js = _ensure_expr(ms).to_js()
    timeout_expr = f"setTimeout(() => {{ {action_js} }}, {ms_js})"

    if store:
        timer_ref = _timer_ref(store, window)
        return _JSRaw(f"{timer_ref} = {timeout_expr}")
    return _JSRaw(timeout_expr)


def clear_timeout(timer: Signal, *actions: Any, window: bool = False) -> _JSRaw:
    """Generate clearTimeout JavaScript expression with optional actions.

    Args:
        timer: Signal containing timer ID to cancel
        *actions: Optional expressions to execute after clearing timer
        window: If True, clear timer from window property (persists across DOM updates)

    Returns:
        _JSRaw expression: clearTimeout($timer); [actions]

    Examples:
        # Just cancel timer
        clear_timeout(timer_sig)
        # → clearTimeout($timer)

        # Cancel window timer
        clear_timeout(timer_sig, window=True)
        # → clearTimeout(window._timer)

        # Cancel timer and execute action
        clear_timeout(timer_sig, open_state.set(False))
        # → clearTimeout($timer); $open_state = false

        # Cancel timer and execute multiple actions
        clear_timeout(timer_sig, open_state.set(False), loading.set(False))
        # → clearTimeout($timer); $open_state = false; $loading = false
    """
    timer_ref = _timer_ref(timer, window)
    clear = f"clearTimeout({timer_ref})"
    if not actions:
        return _JSRaw(clear)

    action_js = "; ".join(_ensure_expr(a).to_js() for a in actions)
    return _JSRaw(f"{clear}; {action_js}")


def reset_timeout(timer: Signal, ms: int | Expr, *actions: Any, window: bool = False) -> _JSRaw:
    """Generate clearTimeout + setTimeout pattern (most common).

    Cancels existing timer and schedules new one. This is the standard
    pattern for debounced actions like tooltips, auto-save, etc.

    Args:
        timer: Signal containing timer ID to cancel and reuse
        ms: Delay in milliseconds for new timer
        *actions: Expressions to execute after delay
        window: If True, use window property (persists across DOM updates)

    Returns:
        _JSRaw expression: clearTimeout($timer); $timer = setTimeout(() => { actions }, ms)

    Examples:
        # Tooltip hover delay (component-scoped)
        reset_timeout(timer_sig, 700, open_state.set(True))
        # → clearTimeout($timer); $timer = setTimeout(() => { $open_state = true }, 700)

        # Global search debounce (persists across DOM updates)
        reset_timeout(timer_sig, 50, selected.set(0), window=True)
        # → clearTimeout(window._timer); window._timer = setTimeout(() => { $selected = 0 }, 50)

        # Multiple actions with delay
        reset_timeout(timer_sig, 1000, step.set(2), progress.set(40))
        # → clearTimeout($timer); $timer = setTimeout(() => { $step = 2; $progress = 40 }, 1000)
    """
    timer_ref = _timer_ref(timer, window)
    action_js = "; ".join(_ensure_expr(a).to_js() for a in actions)
    ms_js = _ensure_expr(ms).to_js()
    return _JSRaw(
        f"clearTimeout({timer_ref}); "
        f"{timer_ref} = setTimeout(() => {{ {action_js} }}, {ms_js})"
    )


def set_interval(action: Any, ms: int | Expr, *, store: Signal | None = None, window: bool = False) -> _JSRaw:
    """Generate setInterval JavaScript expression for repeating actions.

    Args:
        action: Expression or list of expressions to execute repeatedly
        ms: Interval in milliseconds (can be Signal or int)
        store: Optional Signal to store interval ID for later cancellation
        window: If True, store interval as window property (persists across DOM updates)

    Returns:
        _JSRaw expression: setInterval(() => { action }, ms)
        or with store: $interval = setInterval(() => { action }, ms)

    Examples:
        # Countdown timer (component-scoped)
        set_interval(counter.add(-1), 1000, store=interval_sig)
        # → $interval = setInterval(() => { $counter-- }, 1000)

        # Global polling (persists across DOM updates)
        set_interval(fetch_updates(), 5000, store=interval_sig, window=True)
        # → window._interval = setInterval(() => { ... }, 5000)

        # Multiple actions repeating
        set_interval([time.add(1), progress.set(time * 10)], 100)
        # → setInterval(() => { $time++; $progress = $time * 10 }, 100)
    """
    action_js = _ensure_expr(action).to_js() if not isinstance(action, list) \
                else "; ".join(_ensure_expr(a).to_js() for a in action)
    ms_js = _ensure_expr(ms).to_js()
    interval_expr = f"setInterval(() => {{ {action_js} }}, {ms_js})"

    if store:
        timer_ref = _timer_ref(store, window)
        return _JSRaw(f"{timer_ref} = {interval_expr}")
    return _JSRaw(interval_expr)


def clear_interval(interval: Signal, *actions: Any, window: bool = False) -> _JSRaw:
    """Generate clearInterval JavaScript expression with optional actions.

    Args:
        interval: Signal containing interval ID to cancel
        *actions: Optional expressions to execute after clearing interval
        window: If True, clear interval from window property (persists across DOM updates)

    Returns:
        _JSRaw expression: clearInterval($interval); [actions]

    Examples:
        # Just cancel interval
        clear_interval(interval_sig)
        # → clearInterval($interval)

        # Cancel window interval
        clear_interval(interval_sig, window=True)
        # → clearInterval(window._interval)

        # Cancel interval and reset state
        clear_interval(interval_sig, counter.set(0), running.set(False))
        # → clearInterval($interval); $counter = 0; $running = false
    """
    timer_ref = _timer_ref(interval, window)
    clear = f"clearInterval({timer_ref})"
    if not actions:
        return _JSRaw(clear)

    action_js = "; ".join(_ensure_expr(a).to_js() for a in actions)
    return _JSRaw(f"{clear}; {action_js}")


def reset_interval(interval: Signal, ms: int | Expr, *actions: Any, window: bool = False) -> _JSRaw:
    """Generate clearInterval + setInterval pattern.

    Cancels existing interval and schedules new one. Useful for
    restarting repeating timers with new intervals.

    Args:
        interval: Signal containing interval ID to cancel and reuse
        ms: Interval in milliseconds for new repeating timer
        *actions: Expressions to execute repeatedly
        window: If True, use window property (persists across DOM updates)

    Returns:
        _JSRaw expression: clearInterval($interval); $interval = setInterval(() => { actions }, ms)

    Examples:
        # Restart countdown with new speed (component-scoped)
        reset_interval(interval_sig, 500, counter.add(-1))
        # → clearInterval($interval); $interval = setInterval(() => { $counter-- }, 500)

        # Restart global polling (persists across DOM updates)
        reset_interval(interval_sig, 1000, fetch_data(), window=True)
        # → clearInterval(window._interval); window._interval = setInterval(() => { ... }, 1000)
    """
    timer_ref = _timer_ref(interval, window)
    action_js = "; ".join(_ensure_expr(a).to_js() for a in actions)
    ms_js = _ensure_expr(ms).to_js()
    return _JSRaw(
        f"clearInterval({timer_ref}); "
        f"{timer_ref} = setInterval(() => {{ {action_js} }}, {ms_js})"
    )


def managed_interval(
    condition: Expr | bool,
    action: Any,
    ms: int | Expr,
    *,
    interval: Signal,
    window: bool = False,
) -> _JSRaw:
    """Generate a self-cleaning interval that starts/stops based on condition.

    This creates the full pattern: if (condition) { start interval; return cleanup }
    Datastar will automatically call the cleanup function when the effect re-runs or
    the element is removed.

    Args:
        condition: Expression that controls when interval should run
        action: Expression or list of expressions to execute repeatedly
        ms: Interval in milliseconds
        interval: Signal to store interval ID
        window: If True, use window property (persists across DOM updates)

    Returns:
        _JSRaw expression with automatic cleanup pattern

    Examples:
        # Session timeout with auto cleanup (component-scoped)
        managed_interval(
            timer_active & logged_in,
            session_time.add(-1),
            1000,
            interval=interval_sig
        )
        # → if ($timer_active && $logged_in) {
        #      const timer = setInterval(() => { $session_time-- }, 1000);
        #      $interval = timer;
        #      return () => clearInterval(timer);
        #    }

        # Global polling with condition (persists across DOM updates)
        managed_interval(
            is_connected,
            fetch_updates(),
            5000,
            interval=interval_sig,
            window=True
        )

        # Multiple actions with condition
        managed_interval(
            is_playing,
            [current_time.add(1), progress.set(current_time / duration * 100)],
            100,
            interval=player_interval
        )
    """
    timer_ref = _timer_ref(interval, window)
    condition_js = _ensure_expr(condition).to_js()
    action_js = _ensure_expr(action).to_js() if not isinstance(action, list) \
                else "; ".join(_ensure_expr(a).to_js() for a in action)
    ms_js = _ensure_expr(ms).to_js()

    return _JSRaw(
        f"if ({condition_js}) {{ "
        f"const timer = setInterval(() => {{ {action_js} }}, {ms_js}); "
        f"{timer_ref} = timer; "
        f"return () => clearInterval(timer); "
        f"}}"
    )

