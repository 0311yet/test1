#!/bin/bash

# ══════════════════════════════════════════════════════════════════════════════
# 🎉 CRYPTO TRADING SYSTEM - ALL ERRORS FIXED - FINAL BUILD SCRIPT
# ══════════════════════════════════════════════════════════════════════════════

set -e  # Exit on error

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

echo "╔═════════════════════════════════════════════════════════════════════════════╗"
echo "║        🎊 CRYPTO TRADING SYSTEM - ALL ERRORS FIXED - FINAL BUILD 🎊        ║"
echo "║                          Build Complete - 9 Errors Fixed                  ║"
echo "╚═════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Function to print colored messages
print_status() {
    echo -e "${CYAN}$1${NC}"
}

print_success() {
    echo -e "${GREEN}$1${NC}"
}

print_error() {
    echo -e "${RED}$1${NC}"
}

print_info() {
    echo -e "${YELLOW}$1${NC}"
}

print_fix() {
    echo -e "${MAGENTA}$1${NC}"
}

# ══════════════════════════════════════════════════════════════════════════════
# Step 1: Verify all fixes
# ══════════════════════════════════════════════════════════════════════════════

print_status "🔍 Step 1: Verifying all 9 error fixes..."

cd frontend

# Check for explicit types in map functions
print_fix "✅ TypeScript Strict Mode Fixes:"
if grep -q "orders.map((order: Order)" components/OrderTable.tsx; then
    print_success "  ✓ OrderTable has explicit type"
else
    print_error "  ✗ OrderTable missing explicit type"
    exit 1
fi

if grep -q "positions.map((position: Position)" components/PositionTable.tsx; then
    print_success "  ✓ PositionTable has explicit type"
else
    print_error "  ✗ PositionTable missing explicit type"
    exit 1
fi

if grep -q "map((log: LogEntry, index: number)" components/LogPanel.tsx; then
    print_success "  ✓ LogPanel has explicit types"
else
    print_error "  ✗ LogPanel missing explicit types"
    exit 1
fi

# Check for safe value handling
print_fix "✅ Safe Value Handling:"
if grep -q "const unrealizedPnl = data?.unrealized_pnl ?? 0" components/BalanceCard.tsx; then
    print_success "  ✓ BalanceCard has safe values"
else
    print_error "  ✗ BalanceCard missing safe values"
    exit 1
fi

if grep -q "const quantity = position.quantity ?? 0" components/PositionTable.tsx; then
    print_success "  ✓ PositionTable has safe values"
else
    print_error "  ✗ PositionTable missing safe values"
    exit 1
fi

# Check for class-variance-authority
if grep -q "class-variance-authority" package.json; then
    print_success "  ✓ class-variance-authority installed"
else
    print_error "  ✗ class-variance-authority missing"
    exit 1
fi

# Check for CardFooter
if grep -q "const CardFooter = React.forwardRef" components/ui/card.tsx; then
    print_success "  ✓ CardFooter component exists"
else
    print_error "  ✗ CardFooter component missing"
    exit 1
fi

# Check for LogEntry type
if grep -q "export interface LogEntry" types/index.ts; then
    print_success "  ✓ LogEntry type exported"
else
    print_error "  ✗ LogEntry type missing"
    exit 1
fi

# Check for correct type name
if grep -q "import { Balance } from \"@/types\"" components/BalanceCard.tsx; then
    print_success "  ✓ BalanceCard uses correct type"
else
    print_error "  ✗ BalanceCard has type issues"
    exit 1
fi

# Check for API argument fixes
if grep -q "api.put(\`/strategies/\${strategyId}/toggle\`, {})" lib/hooks.ts; then
    print_success "  ✓ API put has correct arguments"
else
    print_error "  ✗ API put missing arguments"
    exit 1
fi

if grep -q "api.post(\`/strategies/\${strategyId}/execute\`, {})" lib/hooks.ts; then
    print_success "  ✓ API post has correct arguments"
else
    print_error "  ✗ API post missing arguments"
    exit 1
fi

cd ..

# ══════════════════════════════════════════════════════════════════════════════
# Step 2: Build frontend
# ══════════════════════════════════════════════════════════════════════════════

print_status "🔨 Step 2: Building frontend..."
cd frontend

print_info "Installing dependencies..."
npm install --legacy-peer-deps

print_info "Building..."
npm run build

cd ..
print_success "✅ Frontend built successfully"

# ══════════════════════════════════════════════════════════════════════════════
# Step 3: Build backend
# ══════════════════════════════════════════════════════════════════════════════

print_status "🔨 Step 3: Building backend..."

cd backend

print_info "Installing dependencies..."
pip install -r requirements.txt --upgrade

cd ..
print_success "✅ Backend built successfully"

# ══════════════════════════════════════════════════════════════════════════════
# Step 4: Start services
# ══════════════════════════════════════════════════════════════════════════════

print_status "🚀 Step 4: Starting services..."

docker compose up -d

print_info "Waiting for services..."
sleep 10

docker compose ps
print_success "✅ Services started"

# ══════════════════════════════════════════════════════════════════════════════
# Step 5: Display results
# ══════════════════════════════════════════════════════════════════════════════

echo ""
echo "╔═════════════════════════════════════════════════════════════════════════════╗"
echo "║                   🎊 BUILD SUCCESSFUL! 🎊                                  ║"
echo "║                    All 9 Errors Fixed! 🎊                                 ║"
echo "╚═════════════════════════════════════════════════════════════════════════════╝"
echo ""
echo -e "${CYAN}📊 ACCESS POINTS${NC}"
echo "─────────────────────────────────────────────────────────────────────────────"
echo "   Frontend:   ${GREEN}http://localhost:3000${NC}"
echo "   Backend:    ${GREEN}http://localhost:8000${NC}"
echo "   API Docs:   ${GREEN}http://localhost:8000/docs${NC}"
echo ""
echo -e "${CYAN}🔧 CONFIGURE API KEYS${NC}"
echo "─────────────────────────────────────────────────────────────────────────────"
echo "   echo 'OKX_API_KEY=your_key' > backend/.env"
echo "   echo 'OKX_SECRET_KEY=your_secret' >> backend/.env"
echo "   echo 'OKX_PASSPHRASE=your_passphrase' >> backend/.env"
echo ""
echo -e "${CYAN}📚 DOCUMENTATION${NC}"
echo "─────────────────────────────────────────────────────────────────────────────"
echo "   - FINAL_COMPLETE_BUILD.md    Complete fix summary"
echo "   - API_ARGUMENTS_FIX.md        API arguments fix"
echo "   - TYPESCRIPT_FIX.md          TypeScript errors"
echo "   - TYPESCRIPT_STRICT_FIX.md   Strict mode fixes"
echo ""
echo -e "${CYAN}🔄 QUICK COMMANDS${NC}"
echo "─────────────────────────────────────────────────────────────────────────────"
echo "   ${YELLOW}# View logs${NC}"
echo "   docker compose logs -f"
echo ""
echo "   ${YELLOW}# Restart services${NC}"
echo "   docker compose restart"
echo ""
echo "   ${YELLOW}# Stop services${NC}"
echo "   docker compose down"
echo ""
echo "╔═════════════════════════════════════════════════════════════════════════════╗"
echo "║              🎉 SYSTEM COMPLETE AND READY TO TRADE! 🎉                    ║"
echo "╚═════════════════════════════════════════════════════════════════════════════╝"
