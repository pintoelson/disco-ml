---
trigger: always_on
---

# Project Rules (DISCO-ML)

This file defines the rules and standards for the DISCO-ML project.

## General AI Rules
- **Stack Consistency**: Always adhere to the established tech stack. Do NOT suggest or introduce new libraries without explicit user permission.
- **Atomic Commits**: Suggest changes in small, logical increments.


---

## [Frontend] Rules
The frontend is a prototype for a research thesis. It focuses on visualization and clear, academic aesthetics.

### Tech Stack
- **Framework**: Next.js 16 (App Router)
- **React**: version 19
- **Styling**: Tailwind CSS 4 (using CSS variables and theme tokens)
- **Components**: shadcn/ui (Radix-UI)
- **Graphing**: React Flow
- **Icons**: Lucide React
- **Language**: TypeScript (Strict Mode)


### Architectural Patterns
- **Composable UI**: Prefer small, reusable components over large, monolithic files.
- **Logic Separation**: Keep complex business logic (e.g., graph processing) in the `lib/` directory or dedicated hooks.
- **Component Placement**: 
  - `components/ui/`: Low-level shadcn primitives.
  - `components/[feature]/`: Feature-specific components (e.g., `components/dashboard/`).
  - `components/layout/`: Global layout elements.
- **Documentation**: Keep `frontend/changelog.md` updated with new features and architectural changes.

### Styling & Aesthetics
- **Neutral & Academic**: UI must be minimal, clean, and use a neutral color palette (grays, subtle accents).
- **No Custom CSS**: Use Tailwind utility classes for all styling. External `.css` files are allowed only if strictly required by a library.
- **No Inline Styles**: Use Tailwind classes instead of the `style={{}}` prop.
- **Responsive**: Ensure all views are responsive and work well on standard laptop/desktop resolutions.

### Type Safety
- **Strict Types**: Avoid `any`. Define interfaces/types for all props and data structures in a central `types/` folder or at the top of the component file.
- **Zod**: Use Zod for any data validation if introduced.

---

## [Backend] Rules
*The backend plan is not yet finalized. Rules will be added once the backend implementation starts.*
- **Placeholder**: Currently Frontend-only.
