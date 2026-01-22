#!/bin/bash
echo "🏗️  Building Quartz..."
npx quartz build -d .
if [ $? -ne 0 ]; then
    echo "❌ Build failed"
    exit 1
fi

echo "✅ Build successful!"
echo ""
echo "💡 To preview the site locally, run:"
echo "   npx quartz build --serve -d ."
