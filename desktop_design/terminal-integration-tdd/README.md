# terminal-integration-tdd

TDD implementation of terminal integration for Stigmergy desktop app

## Project Structure

```
src/
├── main/              # Main process code (Electron)
│   ├── terminal/      # Terminal management
│   ├── ipc/          # IPC handlers
│   └── utils/        # Utility functions
├── renderer/          # Renderer process code (React)
│   ├── components/    # React components
│   ├── services/      # Business logic services
│   └── utils/        # Utility functions
├── shared/           # Shared code between main and renderer
│   └── types/        # TypeScript types
test/
├── unit/             # Unit tests
├── integration/      # Integration tests
└── e2e/             # End-to-end tests
```

## Setup

1. Install dependencies:
   ```bash
   npm install
   ```

2. Run tests:
   ```bash
   npm test
   ```

3. Run tests in watch mode:
   ```bash
   npm run test:watch
   ```

4. Build project:
   ```bash
   npm run build
   ```

5. Start development server:
   ```bash
   npm run dev
   ```

## TDD Workflow

1. Write failing test
2. Run test to confirm it fails
3. Write minimal code to make test pass
4. Run test to confirm it passes
5. Refactor if needed
6. Repeat