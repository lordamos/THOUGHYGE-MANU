# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

Project summary
- Tech stack: Astro (v5.x) with optional React islands, custom CSS, deployed on Netlify using the @astrojs/netlify adapter.
- Source layout (canonical):
  - src/pages, src/components, src/layouts, src/styles
  - public/ for static assets (images/, videos/)
  - netlify/functions/ for serverless functions (when added)
- Important docs in this repo:
  - Thoughtlyfe Astro Website - Final Project Report.md (canonical architecture, deployment details)
  - Guide to Implementing Backend Functionality with Netlify Functions for Thoughtlyfe Website.md (how backend functions are structured and configured)
  - database_schema.sql (future Supabase schema; not wired into the site yet)
  - Multiple PRDs outlining the planned feature set and future phases

Essential commands
Prerequisites
- Node.js: Use Node 20.x (as deployed on Netlify per the project report).
- Package manager: npm.

Install dependencies
- npm install

Local development
- Preferred: npm run dev
- If no script is present: npx astro dev

Build
- npm run build
- Output directory: dist/

Preview the production build
- If a preview script exists: npm run preview
- Otherwise: npx astro preview --host

Netlify deployment
- Netlify builds with: npm run build
- Netlify publishes: dist
- Node version on Netlify: 20.x
- Functions (when added) should live in: netlify/functions/ and be configured in netlify.toml under [functions].

Netlify CLI (local)
- Install CLI: npm install -g netlify-cli
  - Without a global install: npx netlify --version
- Authenticate: netlify login
- Link this repo to an existing site: netlify link
  - Or initialize a new site: netlify init --manual
- Run locally (serves site, proxies functions, loads env): netlify dev
- Deploy a preview build: netlify deploy --build --message "preview"
- Deploy to production: netlify deploy --build --prod --message "release"
- Manage environment variables:
  - List: netlify env:list
  - Set: netlify env:set NAME VALUE

Linting and tests
- Linting: No lint configuration or lint scripts are present in this repository.
- Tests: No test runner or tests are present. Running a single test is not applicable at this time.

High-level architecture and structure
Frontend (Astro + Islands)
- Pages: Content pages live under src/pages (e.g., index.astro as the homepage). Pages import shared components and layouts.
- Layouts: src/layouts/Layout.astro defines the outer HTML shell and metadata for pages.
- Components: src/components contains presentational units such as Header.astro, Footer.astro, and VideoHero.astro. Interactive islands can be implemented with React (e.g., AuraSyncPage.tsx) and hydrated where needed.
- Styling: src/styles/global.css provides the site-wide theme (Crystal Design: deep purple, teal, gold). Components use semantic, accessible markup and minimal JS.

Key homepage composition (from index.astro)
- Video hero section (VideoHero) at the top.
- Book feature section with CTA to shop.
- Author section (Meet Darwin) with CTA to About.
- Aura Sync readings preview with tiered offerings and CTAs to readings.
- Courses preview with CTAs to courses.
- Testimonials.
- Newsletter signup form (client-side handler; backend integration is planned but not yet wired).

Deployment model (Netlify)
- The site is built with Astro and deployed to Netlify via the @astrojs/netlify adapter.
- Static assets are served from the CDN; SSR capabilities are available if enabled by the adapter.
- Build artefacts are written to dist/ and served by Netlify.

Backend plan (serverless-first)
- Serverless functions: The repo is prepared for Netlify Functions in netlify/functions with esbuild bundling, configured via netlify.toml. Core planned functions include:
  - booking (Aura Sync bookings)
  - newsletter (email subscriptions)
  - contact (form submissions)
- Frontend calls functions via /.netlify/functions/<name> using fetch.

Data layer (future)
- Supabase (PostgreSQL) is the planned database. The provided database_schema.sql defines tables for profiles, products, courses, bookings, content, analytics, etc., plus RLS policies and helper triggers.
- Environment variables for Supabase (SUPABASE_URL, SUPABASE_ANON_KEY) must be set in Netlify when the data layer is introduced. Do not commit secrets.

Repository notes
- If you do not see the canonical src/ structure, the complete Astro project is also included in the repository as a packaged archive (e.g., thoughtlyfe_astro_complete.zip). Extracting that archive will reveal the standard Astro layout described above.
- netlify.toml exists in the repo and should declare at minimum:
  - [build] command = "npm run build" and publish = "dist"
  - [functions] directory = "netlify/functions" and node_bundler = "esbuild"

Operational guidance for Warp in this repo
- Prefer npm run dev for local development; fall back to npx astro dev if scripts are missing.
- Use npm run build to generate dist prior to deployment or preview.
- Treat Netlify as the source of truth for production builds; align Node version and build settings with the report and netlify.toml.
- When adding backend features, create functions under netlify/functions and wire frontend calls to /.netlify/functions/<name>. Keep secrets in Netlify environment variables.