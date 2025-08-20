# Changelog

All notable changes to StarUI will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed
- **🚀 Tailwind v4 `@source` Directive Resolution**
  - Fixed critical issue where `star build` and `star dev` couldn't scan Python CVA component definitions
  - Resolved subprocess working directory (`cwd`) handling in CSS builder
  - Fixed `input.css` path resolution to preserve relative `@source` directives
  - Ensures all component CSS classes are properly generated without manual workarounds
- **🎨 Button Component Shadcn Parity**
  - Completely overhauled Button component to match Shadcn UI pixel-perfectly
  - Fixed icon button sizing, alignment, and visual consistency
  - Added proper `has-[>svg]` conditional padding for all size variants
  - Implemented all Shadcn size variants (`default`, `sm`, `lg`, `icon`) with exact styling
  - Enhanced Iconify icon support with proper CSS targeting (`[&_iconify-icon]`)
  - Fixed CVA variant/size conflicts and compound variant handling

### Changed
- **🧪 Improved Test Quality**
  - Refactored metadata tests to focus on behavior rather than implementation details
  - Removed brittle string assertions that tested internal documentation
  - Enhanced test robustness for component metadata extraction
- **📦 Cleaner Public API**
  - Removed unused `component_classes` export from main package
  - Streamlined `__init__.py` imports for better maintainability

### Added
- **🛠️ Development Infrastructure**
  - Added comprehensive test sandbox (`test_sandbox/`) with component preview app
  - Added Pyright configuration (`pyrightconfig.json`) for consistent type checking
  - Enhanced `.gitignore` with development artifacts (`.sesskey`)

## [0.1.4] - 2025-08-19

### Added
- **🛡️ FOUC Prevention in App Starter**
  - Integrated `fouc_script` from StarHTML for flash-free theme loading
  - Supports both `.dark` class and `data-theme` attribute approaches
  - Automatic system preference detection on initial load

### Changed
- **🎨 Enhanced ThemeToggle Component**
  - Simplified to work seamlessly with `fouc_script`
  - Support for arbitrary theme names (not just dark/light)
  - Cleaner reactive patterns using `ds_effect`
  - Renamed signal from `$isDark` to `$isAlt` for generic theme toggling
- **📦 First-class Component Exports**
  - `Button` and `ThemeToggle` now available as direct imports from `starui`
  - Enables `from starui import Button, ThemeToggle` for convenience

### Fixed
- **📁 CSS Path Detection in Init Command**
  - Fixed critical issue where CSS output path was determined before directory creation
  - Now correctly detects and uses `static/css/starui.css` path
  - Ensures app starter template references correct CSS location
- **🔧 Datastar Variable Scoping**
  - Resolved duplicate variable declaration errors in ThemeToggle
  - Fixed scope conflicts between `ds_on_load` and `ds_effect`

## [0.1.3] - 2025-08-18

### Added
- **🎨 Optimized Template System**
  - 57% CSS reduction with hybrid theming support
  - Enhanced ThemeToggle component with smart .dark class and data-theme detection
  - WCAG AA compliant OKLCH colors for better accessibility
  - Default theme system included in `star init` for immediate productivity

### Changed
- **🔧 Modern, Idiomatic Codebase**
  - Refactored CLI commands (add.py, init.py) for concise, Pythonic patterns
  - Enhanced app starter template with semantic color system
  - Improved ThemeToggle to intelligently handle both Tailwind and semantic approaches
  - Updated dependency resolution system with comprehensive test coverage

### Fixed
- **✨ Enhanced Developer Experience**
  - Removed CSS reset (Tailwind v4 handles it automatically)
  - Fixed StarHTML DatastarAttr type compatibility (no more type: ignore needed)
  - Enhanced component dependency system with theme_toggle → button resolution
  - Improved code formatting and linting compliance across all files

### Technical
- Updated StarHTML dependency to use latest GitHub version with DatastarAttr type fixes
- Added comprehensive test suite for dependency resolution system
- Enhanced ThemeToggle to support both `.dark` class and `data-theme` attribute approaches

## [0.1.2] - 2025-08-18

### Changed
- Updated default theme to use modern `oklch` color space matching shadcn v2 with Tailwind v4
- Modernized type hints to use Python 3.10+ union syntax (`X | None` instead of `Optional[X]`)
- Improved code quality with more Pythonic patterns (dict comprehensions, walrus operator)

### Fixed
- Fixed CSS template generation - removed double curly braces that were causing Tailwind v4 errors
- Fixed component import transformation - components now correctly import utilities from starui instead of relative imports

## [0.1.1] - 2025-08-17

### Fixed
- Fixed create-release workflow to correctly update only the project version
- Fixed create-release workflow version extraction to use grep instead of tomli
- Fixed GitHub Actions to use `uv pip install` instead of `python -m pip install`

## [0.1.0] - 2025-08-17

### Added
- 🎨 **Core Component Library**
  - Button component with shadcn/ui variants (default, destructive, outline, secondary, ghost, link)
  - Alert component with title and description support
  - Badge component with clickable variants
  - Card component with header, content, and footer sections
  - Input component with comprehensive form support
  - Label component with accessibility features

- 🔧 **CLI Tools**
  - `star init` - Initialize new StarUI projects
  - `star add <component>` - Add components to existing projects  
  - `star dev <app.py>` - Development server with hot reloading
  - `star build` - Build production CSS
  - `star list` - List available components

- ⚡ **Modern Development Experience**
  - Zero-configuration setup with sensible defaults
  - Automatic Tailwind CSS v4 integration
  - shadcn/ui color scheme and design tokens
  - CSS reset and dark mode support
  - File watching and hot reloading

- 🎯 **StarHTML Integration**
  - Native StarHTML component compatibility
  - Type-safe component APIs with pragmatic flexibility
  - Proper FT return types and HTML attribute support
  - StarHTML dependency with type stubs

- 📦 **Build System & Quality**
  - Modern Python packaging with pyproject.toml
  - Comprehensive GitHub Actions CI/CD
  - Code quality enforcement (ruff, pyright, pytest)
  - Automated PyPI publishing with manual version selection
  - 25% test coverage with behavior-focused testing

### Technical Details
- **Dependencies**: StarHTML, Typer, Watchdog, Requests, Pydantic, Rich
- **Python Support**: 3.12+
- **Package Size**: ~34KB wheel
- **Type Safety**: 0 pyright errors with pragmatic configuration
- **Code Quality**: 100% ruff compliance


[0.1.0]: https://github.com/banditburai/starui/releases/tag/v0.1.0
[0.1.1]: https://github.com/banditburai/starui/releases/tag/v0.1.1
[0.1.2]: https://github.com/banditburai/starUI/releases/tag/v0.1.2

[0.1.3]: https://github.com/banditburai/starUI/releases/tag/v0.1.3

[0.1.4]: https://github.com/banditburai/starUI/releases/tag/v0.1.4
