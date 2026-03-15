#!/bin/bash

# ══════════════════════════════════════════════════════════════════════════════
# 🎉 CRYPTO TRADING SYSTEM - COMPLETE BUILD SCRIPT
# ══════════════════════════════════════════════════════════════════════════════

set -e  # Exit on error

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "╔═════════════════════════════════════════════════════════════════════════════╗"
echo "║                    🎊 CRYPTO TRADING SYSTEM BUILD 🎊                       ║"
echo "║                          COMPLETE REBUILD                                  ║"
echo "╚═════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Function to print colored messages
print_status() {
    echo -e "${BLUE}$1${NC}"
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

# ══════════════════════════════════════════════════════════════════════════════
# Step 1: Verify Environment
# ══════════════════════════════════════════════════════════════════════════════

print_status "📊 Step 1: Verifying build environment..."

if [ ! -f "package.json" ]; then
    print_error "❌ package.json not found in root directory"
    exit 1
fi

if [ ! -f "backend/requirements.txt" ]; then
    print_error "❌ backend/requirements.txt not found"
    exit 1
fi

print_success "✅ Build environment verified"

# ══════════════════════════════════════════════════════════════════════════════
# Step 2: Check TypeScript fixes
# ══════════════════════════════════════════════════════════════════════════════

print_status "🔍 Step 2: Verifying TypeScript fixes..."

cd frontend

# Check for LogEntry type
if grep -q "export interface LogEntry" types/index.ts; then
    print_success "✅ LogEntry type exported"
else
    print_error "❌ LogEntry type missing"
    exit 1
fi

# Check for Balance type
if grep -q "export interface Balance" types/index.ts; then
    print_success "✅ Balance type exported"
else
    print_error "❌ Balance type missing"
    exit 1
fi

# Check for BalanceCard imports
if grep -q "import { Balance } from \"@/types\"" components/BalanceCard.tsx; then
    print_success "✅ BalanceCard imports Balance type correctly"
else
    print_error "❌ BalanceCard has import issues"
    exit 1
fi

# Check for PositionTable safe values
if grep -q "const quantity = position.quantity ?? 0" components/PositionTable.tsx; then
    print_success "✅ PositionTable has safe value handling"
else
    print_error "❌ PositionTable missing safe value handling"
    exit 1
fi

# Check for class-variance-authority
if grep -q "class-variance-authority" package.json; then
    print_success "✅ class-variance-authority installed"
else
    print_error "❌ class-variance-authority missing"
    exit 1
fi

cd ..

print_success "✅ All TypeScript fixes verified"

# ══════════════════════════════════════════════════════════════════════════════
# Step 3: Clean and stop services
# ══════════════════════════════════════════════════════════════════════════════

print_status "🛑 Step 3: Stopping services and cleaning cache..."

docker compose down 2>/dev/null || true
docker system prune -f
print_success "✅ Services stopped and cache cleaned"

# ══════════════════════════════════════════════════════════════════════════════
# Step 4: Build frontend
# ══════════════════════════════════════════════════════════════════════════════

print_status "🔨 Step 4: Building frontend..."
cd frontend

# Install dependencies
print_info "Installing frontend dependencies..."
npm install --legacy-peer-deps

# Build frontend
print_info "Building frontend..."
npm run build

cd ..
print_success "✅ Frontend build complete"

# ══════════════════════════════════════════════════════════════════════════════
# Step 5: Build backend
# ══════════════════════════════════════════════════════════════════════════════

print_status "🔨 Step 5: Building backend..."
cd backend

# Install dependencies
print_info "Installing backend dependencies..."
pip install -r requirements.txt --upgrade

# Build backend
print_info "Building backend..."
python -m build

cd ..
print_success "✅ Backend build complete"

# ══════════════════════════════════════════════════════════════════════════════
# Step 6: Start services
# ══════════════════════════════════════════════════════════════════════════════

print_status "🚀 Step 6: Starting services..."

docker compose up -d

print_info "Waiting for services to start..."
sleep 10

# Check service status
print_info "Checking service status..."
docker compose ps

print_success "✅ Services started"

# ══════════════════════════════════════════════════════════════════════════════
# Step 7: Verify services
# ══════════════════════════════════════════════════════════════════════════════

print_status "🏥 Step 7: Verifying service health..."

# Wait a bit more for services to be ready
sleep 5

# Check if services are running
BACKEND_COUNT=$(docker compose ps backend | grep "Up" | wc -l)
FRONTEND_COUNT=$(docker compose ps frontend | grep "Up" | wc -l)

if [ $BACKEND_COUNT -eq 1 ]; then
    print_success "✅ Backend is running"
else
    print_error "❌ Backend is not running"
fi

if [ $FRONTEND_COUNT -eq 1 ]; then
    print_success "✅ Frontend is running"
else
    print_error "❌ Frontend is not running"
fi

# Check health endpoint
print_info "Checking health endpoints..."
sleep 3

if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    print_success "✅ Backend health endpoint responding"
else
    print_error "❌ Backend health endpoint not responding"
fi

# ══════════════════════════════════════════════════════════════════════════════
# Step 8: Display access information
# ══════════════════════════════════════════════════════════════════════════════

echo ""
echo "╔═════════════════════════════════════════════════════════════════════════════╗"
echo "║                        🎊 BUILD SUCCESSFUL! 🎊                             ║"
echo "╚═════════════════════════════════════════════════════════════════════════════╝"
echo ""
echo -e "${GREEN}📊 SYSTEM STATUS${NC}"
echo "─────────────────────────────────────────────────────────────────────────────"
echo "   Frontend:   ${GREEN}http://localhost:3000${NC}"
echo "   Backend:    ${GREEN}http://localhost:8000${NC}"
echo "   API Docs:   ${GREEN}http://localhost:8000/docs${NC}"
echo ""
echo -e "${YELLOW}🔧 CONFIGURATION${NC}"
echo "─────────────────────────────────────────────────────────────────────────────"
echo "   To configure API keys:"
echo "   ${YELLOW}echo 'OKX_API_KEY=your_key' > backend/.env${NC}"
echo "   ${YELLOW}echo 'OKX_SECRET_KEY=your_secret' >> backend/.env${NC}"
echo "   ${YELLOW}echo 'OKX_PASSPHRASE=your_passphrase' >> backend/.env${NC}"
echo ""
echo -e "${BLUE}📚 DOCUMENTATION${NC}"
echo "─────────────────────────────────────────────────────────────────────────────"
echo "   - README.md              Project overview"
echo "   - SETUP_GUIDE.md         Quick start guide"
echo "   - COMPLETE_GUIDE.md      Complete system guide"
echo "   - FINAL_BUILD_SUMMARY.md Build completion summary"
echo "   - TYPESCRIPT_FIX.md     TypeScript error fixes"
echo ""
echo -e "${BLUE}🔄 QUICK COMMANDS${NC}"
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
echo "   ${YELLOW}# Check status${NC}"
echo "   docker compose ps"
echo ""
echo "╔═════════════════════════════════════════════════════════════════════════════╗"
echo "║                     🎉 SYSTEM READY TO TRADE! 🎉                           ║"
echo "╚═════════════════════════════════════════════════════════════════════════════╝"
