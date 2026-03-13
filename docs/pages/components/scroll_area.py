TITLE = "Scroll Area"
DESCRIPTION = "Scrollable viewport with custom styled scrollbars."
CATEGORY = "layout"
ORDER = 15
STATUS = "stable"

from starhtml import Div, P, Span, Icon, Code
from components.scroll_area import ScrollArea
from components.separator import Separator
from components.badge import Badge
from utils import with_code, Prop, build_api_reference, auto_generate_page


@with_code
def default_example():
    notifications = [  #: hide
        ("lucide:mail", "New deployment succeeded", "api-server v3.1.2 deployed to production", "2 min ago"),
        ("lucide:message-square", "Emma commented on PR #42", "Looks good, just one nit on the error handling", "18 min ago"),
        ("lucide:git-pull-request", "PR #39 merged", "feat: add scroll-area component", "1 hr ago"),
        ("lucide:alert-triangle", "Build failed on staging", "Test suite: 3 failures in auth module", "2 hr ago"),
        ("lucide:user-plus", "New team member", "Anika joined the project", "3 hr ago"),
        ("lucide:git-branch", "Branch protection updated", "main now requires 2 approvals", "5 hr ago"),
        ("lucide:package", "Dependency update available", "fasthtml 1.2.0 → 1.3.0", "6 hr ago"),
        ("lucide:check-circle", "Security scan passed", "0 vulnerabilities found", "8 hr ago"),
        ("lucide:message-square", "Review requested", "Marcus requested your review on PR #44", "12 hr ago"),
        ("lucide:zap", "Performance alert resolved", "p99 latency back under 200ms", "1 day ago"),
    ]
    return ScrollArea(  #: hide
        Div(
            P("Notifications", cls="mb-1 text-sm font-semibold"),
            Span("You have 3 unread messages", cls="text-xs text-muted-foreground"),
            Separator(cls="my-3"),
            *[
                Div(
                    Div(
                        Icon(icon, cls="mt-0.5 h-4 w-4 shrink-0 text-muted-foreground"),
                        Div(
                            P(title, cls="text-sm leading-tight font-medium"),
                            P(desc, cls="mt-0.5 line-clamp-1 text-xs text-muted-foreground"),
                        ),
                        Span(time, cls="ml-auto shrink-0 text-[11px] text-muted-foreground"),
                        cls="flex gap-3",
                    ),
                    cls="py-2.5",
                )
                for icon, title, desc, time in notifications
            ],
            cls="p-4",
        ),
        cls="h-80 w-80 rounded-md border",
        aria_label="Notifications",
    )


@with_code
def horizontal_example():
    members = [  #: hide
        ("lucide:shield", "Anika Patel", "Lead", "bg-violet-100 text-violet-700 dark:bg-violet-900 dark:text-violet-300"),
        ("lucide:code", "Marcus Chen", "Backend", "bg-sky-100 text-sky-700 dark:bg-sky-900 dark:text-sky-300"),
        ("lucide:palette", "Ines Moreau", "Design", "bg-rose-100 text-rose-700 dark:bg-rose-900 dark:text-rose-300"),
        ("lucide:server", "Kwame Asante", "Infra", "bg-amber-100 text-amber-700 dark:bg-amber-900 dark:text-amber-300"),
        ("lucide:test-tube", "Yuki Tanaka", "QA", "bg-emerald-100 text-emerald-700 dark:bg-emerald-900 dark:text-emerald-300"),
        ("lucide:smartphone", "Lena Vogt", "Mobile", "bg-fuchsia-100 text-fuchsia-700 dark:bg-fuchsia-900 dark:text-fuchsia-300"),
        ("lucide:database", "Ravi Sharma", "Data", "bg-orange-100 text-orange-700 dark:bg-orange-900 dark:text-orange-300"),
        ("lucide:lock", "Sofia Rivera", "Security", "bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-300"),
    ]
    return ScrollArea(  #: hide
        Div(
            *[
                Div(
                    Div(
                        Icon(icon, cls=f"h-5 w-5 {color_cls}"),
                        cls=f"flex items-center justify-center rounded-full h-12 w-12 {color_cls.split()[0]} dark:{color_cls.split()[2]}",
                    ),
                    Span(name, cls="mt-2 text-center text-sm font-medium"),
                    Badge(role, variant="outline", cls="mt-1"),
                    cls="flex w-28 shrink-0 flex-col items-center",
                )
                for icon, name, role, color_cls in members
            ],
            cls="flex gap-4 p-4",
        ),
        orientation="horizontal",
        cls="w-full max-w-md rounded-md border",
        aria_label="Team members",
    )


@with_code
def log_viewer_example():
    log_lines = [  #: hide
        ("[INFO]  2026-03-06 09:14:01  server.startup       Listening on 0.0.0.0:8000                                    pid=1842"),
        ("[INFO]  2026-03-06 09:14:01  db.pool              Pool initialized                    min=5  max=20  timeout=30s"),
        ("[INFO]  2026-03-06 09:14:02  cache.redis           Connected to redis://localhost:6379/0                         latency=2ms"),
        ("[DEBUG] 2026-03-06 09:14:15  http.request          GET /api/v1/users                   200  12ms   user_agent=curl/8.4"),
        ("[DEBUG] 2026-03-06 09:14:15  db.query              SELECT * FROM users LIMIT 50        rows=23  duration=4ms"),
        ("[INFO]  2026-03-06 09:14:22  auth.login            Login succeeded                     user=anika@example.com  ip=10.0.1.42"),
        ("[WARN]  2026-03-06 09:15:03  rate_limit            Approaching limit                   endpoint=/api/v1/search  count=847/1000"),
        ("[DEBUG] 2026-03-06 09:15:04  http.request          POST /api/v1/deployments            201  340ms  body_size=2.1KB"),
        ("[INFO]  2026-03-06 09:15:04  deploy.trigger        Deployment started                  service=api-server  version=3.1.2  env=staging"),
        ("[DEBUG] 2026-03-06 09:15:08  deploy.build          Image built                         tag=api-server:3.1.2  size=142MB  duration=4.2s"),
        ("[INFO]  2026-03-06 09:15:12  deploy.rollout        Rolling update 1/3                  pod=api-server-7d4b9  status=running"),
        ("[INFO]  2026-03-06 09:15:18  deploy.rollout        Rolling update 2/3                  pod=api-server-8e5c1  status=running"),
        ("[INFO]  2026-03-06 09:15:24  deploy.rollout        Rolling update 3/3                  pod=api-server-9f6d2  status=running"),
        ("[INFO]  2026-03-06 09:15:25  deploy.complete       Deployment succeeded                service=api-server  version=3.1.2  duration=21s"),
        ("[ERROR] 2026-03-06 09:16:41  http.request          GET /api/v1/reports/export           500  2.4s   error=QueryTimeout"),
        ("[ERROR] 2026-03-06 09:16:41  db.query              Query exceeded timeout               query=report_aggregate  limit=5000ms  actual=5002ms"),
        ("[WARN]  2026-03-06 09:16:42  circuit_breaker       Circuit opened                      service=report-export  failures=3/3  cooldown=30s"),
        ("[INFO]  2026-03-06 09:17:12  circuit_breaker       Circuit half-open                   service=report-export  next_attempt=1"),
        ("[DEBUG] 2026-03-06 09:17:13  http.request          GET /api/v1/reports/export           200  890ms  retry=true"),
        ("[INFO]  2026-03-06 09:17:13  circuit_breaker       Circuit closed                      service=report-export  recovered=true"),
    ]
    return ScrollArea(  #: hide
        Div(
            *[
                Code(line, cls="block py-px text-[11px] leading-5 whitespace-pre")
                for line in log_lines
            ],
            cls="w-max p-3",
        ),
        orientation="both",
        cls="h-64 w-full max-w-2xl rounded-md border bg-muted/30 font-mono",
        aria_label="Application logs",
    )


@with_code
def auto_hide_example():
    changelog = [  #: hide
        ("3.1.2", "Patch", "Fix connection pool leak under high concurrency"),
        ("3.1.1", "Patch", "Correct timezone handling in scheduled tasks"),
        ("3.1.0", "Minor", "Add WebSocket support for real-time notifications"),
        ("3.0.2", "Patch", "Fix rate limiter not resetting after window expiry"),
        ("3.0.1", "Patch", "Handle graceful shutdown on SIGTERM"),
        ("3.0.0", "Major", "Migrate from REST to GraphQL API layer"),
        ("2.9.4", "Patch", "Pin dependency versions for reproducible builds"),
        ("2.9.3", "Patch", "Fix CSV export truncating Unicode characters"),
        ("2.9.2", "Patch", "Resolve deadlock in batch processing queue"),
        ("2.9.1", "Patch", "Correct pagination offset for filtered queries"),
        ("2.9.0", "Minor", "Introduce role-based access control"),
        ("2.8.0", "Minor", "Add audit log for admin actions"),
    ]
    badge_variant = {"Major": "destructive", "Minor": "default", "Patch": "secondary"}  #: hide
    return ScrollArea(  #: hide
        Div(
            *[
                Div(
                    Div(
                        Span(f"v{version}", cls="font-mono text-sm font-medium"),
                        Badge(kind, variant=badge_variant[kind]),
                        cls="flex items-center gap-2",
                    ),
                    P(desc, cls="mt-0.5 text-xs text-muted-foreground"),
                    cls="py-2.5",
                )
                for version, kind, desc in changelog
            ],
            cls="p-4",
        ),
        auto_hide=True,
        cls="h-72 w-72 rounded-md border",
        aria_label="Changelog",
    )


EXAMPLES_DATA = [
    {
        "fn": default_example,
        "title": "Notifications",
        "description": "Vertical scroll with mixed content — icons, text, and timestamps",
    },
    {
        "fn": horizontal_example,
        "title": "Horizontal",
        "description": "Team members overflow naturally along the x-axis while the y-axis stays locked",
    },
    {
        "fn": log_viewer_example,
        "title": "Log Viewer",
        "description": "Two-axis scrolling for wide, tall content like logs or data tables",
    },
    {
        "fn": auto_hide_example,
        "title": "Auto-Hide Scrollbar",
        "description": "Scrollbar hides when idle and reveals on hover, scroll, or keyboard focus",
    },
]

API_REFERENCE = build_api_reference(
    main_props=[
        Prop(
            "orientation",
            "Literal['vertical', 'horizontal', 'both']",
            "Scroll direction. Controls which axes overflow",
            "'vertical'",
        ),
        Prop("dir", "Literal['ltr', 'rtl']", "Text direction for RTL support", "'ltr'"),
        Prop("auto_hide", "bool", "Hide scrollbar when not interacting", "False"),
        Prop(
            "scroll_hide_delay",
            "int",
            "Delay in ms before hiding scrollbar (requires auto_hide=True)",
            "600",
        ),
        Prop(
            "aria_label", "str", "ARIA label for accessibility", "'Scrollable content'"
        ),
        Prop("cls", "str", "Additional CSS classes on the outer wrapper", "''"),
    ]
)


def create_scroll_area_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)
