#!/bin/bash

echo "🔍 TypeScript Error Scanner"
echo "==========================="
echo ""

# Check all TypeScript files for potential issues
echo "1. Checking for unexported types..."
grep -r "interface\|type" /Users/totb/Desktop/test/frontend/components/*.tsx 2>/dev/null | grep -v "export" | grep "interface" | head -10

echo ""
echo "2. Checking for incorrect imports..."
grep -r "from.*types" /Users/totb/Desktop/test/frontend/components/*.tsx 2>/dev/null | grep -v "export" | head -10

echo ""
echo "3. Checking for undefined types..."
for file in /Users/totb/Desktop/test/frontend/components/*.tsx; do
    if [ -f "$file" ]; then
        basename=$(basename "$file")
        # Check if file imports from types
        if grep -q "from.*types" "$file" 2>/dev/null; then
            imports=$(grep "from.*types" "$file" 2>/dev/null)
            echo "   $basename: $imports"
        fi
    fi
done

echo ""
echo "4. Verifying type exports..."
grep "^export interface\|^export type" /Users/totb/Desktop/test/frontend/types/index.ts

echo ""
echo "==========================="
echo "✅ Scan Complete"
echo "==========================="
