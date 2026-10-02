# LegalInsight AI - Frontend

React + Vite single-page application for LegalInsight AI.

## Getting Started

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Start the development server:**
   ```bash
   npm run dev
   ```

3. **Build for production:**
   ```bash
   npm run build
   ```

4. **Lint code:**
   ```bash
   npm run lint
   ```

## Architecture
- `src/api.js`: Central Axios instance with JWT interceptor.
- `src/context/AuthContext.jsx`: Multi-tenant authentication context provider.
- `src/components/AuthScreen.jsx`: Login & registration view.
- `src/components/UploadForm.next.jsx`: Document ingestion with drag-and-drop.
- `src/components/Dashboard.compact.jsx`: Risk analysis report and PDF export generator.
- `src/components/ProfileSection.jsx`: User profile, password management, and private clause library.
- `src/components/GlobalSearch.jsx`: Semantic search across all indexed contracts.
