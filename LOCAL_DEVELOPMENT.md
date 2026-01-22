# Local Quartz Development Guide

## Quick Start

### 1. Install Dependencies
```bash
npm install
```

### 2. Test Build (Before Pushing)
```bash
./test-build.sh
```

This script will:
- Build the Quartz site
- Show any build errors
- Confirm if the build is successful

### 3. Preview Locally with Live Reload
```bash
npx quartz build --serve -d .
```

Then open your browser to `http://localhost:8080`

The server will:
- Watch for file changes
- Rebuild automatically
- Refresh the browser

**Important:** The `-d .` flag tells Quartz to use the current directory as the content source (same as GitHub Actions).

## Common Commands

### Build Only
```bash
npx quartz build -d .
```

### Build and Serve
```bash
npx quartz build --serve -d .
```

### Format Code
```bash
npm run format
```

## Workflow

### Before Pushing to GitHub

1. Make your changes
2. Run the test build:
   ```bash
   ./test-build.sh
   ```
3. If successful, commit and push
4. GitHub Actions will build and deploy automatically

### Active Development

1. Start the development server:
   ```bash
   npx quartz build --serve
   ```
2. Make changes to your files
3. Check the browser for updates (auto-refreshes)
4. Check the terminal for any build errors

## Troubleshooting

### Node Version Warning
You may see warnings about Node version (requires Node 22, you have Node 20). This is usually fine for development, but if you encounter issues, consider upgrading Node.

### Build Errors
- Check the terminal output for specific error messages
- Most errors will point to the file and line number
- Common issues:
  - Syntax errors in TypeScript/JavaScript files
  - Invalid frontmatter in markdown files
  - Missing files or broken links

### Port Already in Use
If port 8080 is already in use:
```bash
npx quartz build --serve --port 3000
```

## Files Modified

### Recent Changes
- `quartz/plugins/transformers/frontmatter.ts` - Now extracts H1 titles for display in Explorer
- `80-Tools/update_lesson_navigation.py` - Updated with fancy icons and next lesson links
- `test-build.sh` - Quick build verification script

## Notes

- The build output goes to the `public/` directory
- GitHub Actions uses the same build command: `npx quartz build`
- If it builds locally, it will build in CI/CD
