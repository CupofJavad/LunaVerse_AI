# Quick Start Guide - Lunaverse Show Brain

**For users who already have Docker and basic tools installed.**

## Prerequisites Check

Run these commands to verify you have everything:

```bash
docker --version          # Should show version
docker compose version    # Should show version
python3 --version         # Should show Python 3.x
git --version            # Should show version
```

If any fail, see `docs/complete-setup-guide.md` Part 1.

## 5-Minute Setup

### 1. Configure Environment (2 minutes)

```bash
cd ~/PycharmProjects/LunaVerse_AI

# Generate JWT secret
python3 -c "import secrets; print(secrets.token_urlsafe(64))"
# Copy the output

# Edit .env file
nano .env  # or code .env, or open in your editor
```

**Fill in these 3 values:**
- `HF_API_KEY` - Get from https://huggingface.co/settings/tokens
- `JWT_SECRET_KEY` - Paste the generated secret
- `HF_API_URL` - Use: `https://api-inference.huggingface.co/models/meta-llama/Llama-3-8b-instruct`

Save and close.

### 2. Start Services (2 minutes)

```bash
cd infrastructure
docker compose up -d
```

Wait for all services to start (check with `docker compose ps`).

### 3. Initialize Database (30 seconds)

```bash
docker compose exec db psql -U postgres -d lunaverse -f /docker-entrypoint-initdb.d/schema.sql
```

### 4. Create User (30 seconds)

```bash
cd ..
./scripts/create_user.sh
```

Or manually:
```bash
docker compose -f infrastructure/docker-compose.yml exec api python3 scripts/create_user.py
```

### 5. Access Application

- **Frontend**: http://localhost:4173
- **API Docs**: http://localhost:8000/docs
- **Login** with the user you created

## Common Commands

```bash
# Start services
cd infrastructure && docker compose up -d

# Stop services
docker compose down

# View logs
docker compose logs -f api

# Restart a service
docker compose restart api

# Check status
docker compose ps
```

## Troubleshooting

**Services won't start?**
- Check Docker is running
- Check ports 8000, 5432, 4173 are free
- See `docs/complete-setup-guide.md` Part 9

**Can't login?**
- Verify user was created: `docker compose exec db psql -U postgres -d lunaverse -c "SELECT email FROM users;"`
- Check API logs: `docker compose logs api`

**Plan generation fails?**
- Verify HF_API_KEY in .env is correct
- Check API logs for LLM errors
- Test HF endpoint manually

## Full Details

For complete step-by-step instructions, see: `docs/complete-setup-guide.md`

