# Local Development Guide

## Without Docker

This guide shows how to run the system without Docker containers.

## Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+
- OKX API credentials

## 1. Setup Backend

### Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file in the backend directory:

```bash
DATABASE_URL=postgresql://trader:traderpassword@localhost:5432/crypto_trading
REDIS_URL=redis://localhost:6379/0
OKX_API_KEY=your_okx_api_key
OKX_SECRET_KEY=your_okx_secret_key
OKX_PASSPHRASE=your_okx_passphrase
```

### Setup Database

```bash
# Install PostgreSQL client (if not installed)
brew install postgresql@15  # macOS
# or
sudo apt-get install postgresql-15  # Ubuntu

# Start PostgreSQL
brew services start postgresql@15  # macOS
# or
sudo systemctl start postgresql  # Ubuntu

# Create database
psql -U postgres
CREATE DATABASE crypto_trading;
\q
```

### Setup Redis

```bash
# Install Redis
brew install redis  # macOS
# or
sudo apt-get install redis-server  # Ubuntu

# Start Redis
brew services start redis  # macOS
# or
sudo systemctl start redis-server  # Ubuntu
```

### Run Database Migrations

```bash
cd backend
python -c "from app.core.database import init_db; init_db()"
```

### Run Backend

```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Backend will be available at http://localhost:8000

## 2. Setup Frontend

### Install Node Dependencies

```bash
cd frontend
npm install
```

### Run Frontend

```bash
cd frontend
npm run dev
```

Frontend will be available at http://localhost:3000

## 3. Start Development

### Terminal 1 - Backend

```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Terminal 2 - Frontend

```bash
cd frontend
npm run dev
```

### Terminal 3 - Database (optional)

```bash
# For development, you might want to monitor the database
pgAdmin or DBeaver connected to localhost:5432
```

### Terminal 4 - Redis (optional)

```bash
# For development, you might want to monitor Redis
redis-cli MONITOR
```

## 4. Verify Setup

### Check Backend Health

```bash
curl http://localhost:8000/health
```

### Check API Documentation

Open browser: http://localhost:8000/docs

### Check Frontend

Open browser: http://localhost:3000

## 5. Common Issues

### Port Already in Use

If port 8000 or 3000 is already in use:

```bash
# Backend on port 8001
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload

# Frontend on port 3001
npm run dev -- --port 3001
```

### Database Connection Issues

```bash
# Check PostgreSQL is running
brew services list | grep postgresql

# Test connection
psql -U postgres -d crypto_trading -h localhost

# Restart PostgreSQL if needed
brew services restart postgresql@15
```

### Redis Connection Issues

```bash
# Check Redis is running
redis-cli ping

# Restart Redis if needed
brew services restart redis
```

### Python Module Issues

```bash
# Clear Python cache
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# Reinstall dependencies
cd backend
pip install -r requirements.txt --force-reinstall
```

## 6. Database Management

### Connect to Database

```bash
psql -U trader -d crypto_trading -h localhost
```

### View Tables

```sql
\dt
```

### View Orders

```sql
SELECT * FROM orders;
```

### View Strategies

```sql
SELECT * FROM strategies;
```

### Clear All Data

```sql
TRUNCATE TABLE orders, trades, positions, strategies RESTART IDENTITY CASCADE;
```

## 7. Testing

### Test API Endpoints

```bash
# Get health check
curl http://localhost:8000/health

# Get balance (requires API keys)
curl http://localhost:8000/api/balance

# Get orders
curl http://localhost:8000/api/orders
```

### Test WebSocket Connection

```bash
# Using wscat (install with: npm install -g wscat)
wscat -c ws://localhost:8000/ws
```

## 8. Production Considerations

### Environment Variables

```bash
# Production .env
DATABASE_URL=postgresql://trader:password@db-host:5432/crypto_trading
REDIS_URL=redis://redis-host:6379/0
OKX_API_KEY=your_produced_api_key
OKX_SECRET_KEY=your_produced_secret_key
OKX_PASSPHRASE=your_produced_passphrase
```

### Security

1. **Never commit `.env` files**
2. **Use strong passwords**
3. **Enable HTTPS in production**
4. **Restrict API key permissions**
5. **Use environment-specific configs**

### Performance

1. **Use production build**:
   ```bash
   cd backend
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

2. **Use production build**:
   ```bash
   cd frontend
   npm run build
   npm start
   ```

### Database Backups

```bash
# Backup database
pg_dump -U trader crypto_trading > backup_$(date +%Y%m%d).sql

# Restore database
psql -U trader crypto_trading < backup_20240101.sql
```

## 9. Monitoring

### Backend Logs

Check terminal output for backend logs

### Database Logs

```bash
# PostgreSQL logs (check log file location)
tail -f /usr/local/var/log/postgresql/postgresql@15.log
```

### Redis Logs

```bash
# Redis logs
tail -f /usr/local/var/log/redis.log
```

## 10. Troubleshooting Docker Build Issues

If you encounter Docker build issues, remember that the `package-lock.json` file is now included. The Dockerfile has been updated to use `npm install` instead of `npm ci`.

To rebuild the Docker image:

```bash
cd /Users/totb/Desktop/test
docker compose build
docker compose up -d
```

## Support

If you encounter issues:
1. Check the error messages in the terminal
2. Verify all services are running
3. Check environment variables are set correctly
4. Review logs from each service
5. Ensure ports are not already in use
