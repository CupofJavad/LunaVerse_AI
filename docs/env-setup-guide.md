# Complete .env Configuration Guide

This guide provides step-by-step instructions for filling in every placeholder in your `.env` file.

## Prerequisites

- A Hugging Face account (free tier is fine)
- Terminal/command line access
- Text editor

---

## Step 1: Open Your .env File

1. Navigate to your project directory: `/Users/Javad/PycharmProjects/LunaVerse_AI`
2. Open the `.env` file in your text editor (VS Code, PyCharm, nano, vim, etc.)
   - In terminal: `nano .env` or `code .env`
   - In PyCharm: Right-click `.env` → Open

---

## Step 2: Configure Hugging Face API (Required)

### 2.1 Get Your Hugging Face API Key

1. **Open your web browser**
2. **Go to**: https://huggingface.co/
3. **Sign in** (or create a free account if you don't have one)
   - Click "Sign Up" in top right if needed
   - Use email or GitHub/Google to sign up
4. **Navigate to your profile settings**:
   - Click your profile picture/avatar in top right
   - Click "Settings" from dropdown menu
5. **Go to Access Tokens**:
   - In left sidebar, click "Access Tokens"
   - Or go directly to: https://huggingface.co/settings/tokens
6. **Create a new token**:
   - Click "New token" button
   - **Name**: Enter "Lunaverse Show Brain" (or any name you prefer)
   - **Type**: Select "Read" (sufficient for inference endpoints)
   - Click "Generate token"
7. **Copy the token**:
   - **IMPORTANT**: Copy the token immediately (it shows only once)
   - It will look like: `hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - Paste it somewhere safe temporarily

### 2.2 Set Up Hugging Face Inference Endpoint

**Option A: Use Hugging Face's Free Inference API (Easiest)**

1. **Go to**: https://huggingface.co/models
2. **Search for**: "meta-llama/Llama-3-8b-instruct" or "meta-llama/Llama-3-70b-instruct"
3. **Click on the model** you want to use
4. **Click "Deploy" tab** at the top
5. **Select "Inference Endpoints"**
6. **Click "New Endpoint"**:
   - **Name**: "lunaverse-llm" (or any name)
   - **Compute**: Select "CPU Basic" (free tier) or "GPU" (paid)
   - **Region**: Choose closest to you
   - **Task**: Select "Text Generation"
   - Click "Create Endpoint"
7. **Wait for deployment** (5-10 minutes)
8. **Copy the endpoint URL**:
   - Once deployed, you'll see a URL like: `https://xxxxx.us-east-1.aws.endpoints.huggingface.cloud`
   - Copy this entire URL

**Option B: Use Hugging Face Inference API (No Endpoint Setup)**

If you don't want to set up an endpoint, use the direct API:

1. **Use this URL**: `https://api-inference.huggingface.co/models/meta-llama/Llama-3-8b-instruct`
   - Note: Free tier has rate limits and may queue requests

### 2.3 Fill in .env File

In your `.env` file, find these lines and replace:

```bash
HF_API_URL=https://api-inference.huggingface.co/models/meta-llama/Llama-3-8b-instruct
```

**Replace with**:
- **If using Inference Endpoint**: Your endpoint URL from Step 2.2 (Option A)
- **If using direct API**: Keep as is, or use: `https://api-inference.huggingface.co/models/meta-llama/Llama-3-8b-instruct`

```bash
HF_API_KEY=your-hf-api-key-here
```

**Replace with**: The token you copied in Step 2.1
- Example: `HF_API_KEY=hf_AbCdEf1234567890XyZ`

---

## Step 3: Generate JWT Secret Key (Required)

### 3.1 Generate a Secure Random String

**Option A: Using Python (Recommended)**

1. **Open terminal**
2. **Run this command**:
   ```bash
   python3 -c "import secrets; print(secrets.token_urlsafe(64))"
   ```
3. **Copy the output** (it will be a long random string)

**Option B: Using OpenSSL**

1. **Open terminal**
2. **Run this command**:
   ```bash
   openssl rand -hex 32
   ```
3. **Copy the output**

**Option C: Using Online Generator**

1. **Go to**: https://randomkeygen.com/
2. **Find "CodeIgniter Encryption Keys"** section
3. **Copy any 64-character key**

### 3.2 Fill in .env File

In your `.env` file, find:

```bash
JWT_SECRET_KEY=change-me-in-production-use-long-random-string
```

**Replace with**: The random string you generated
- Example: `JWT_SECRET_KEY=K8mN2pQ5rT9vW1xY3zA6bC4dE7fG0hI2jK4lM6nO8pQ0rS2tU4vW6xY8zA`

---

## Step 4: Database Configuration (Optional - Defaults Work)

The default database URL should work with Docker Compose:

```bash
DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/lunaverse
```

**Only change if**:
- You're running PostgreSQL locally (not in Docker)
- You want to use a different database name
- You want to use different credentials

**If running locally**:
```bash
DATABASE_URL=postgresql+psycopg2://postgres:your_password@localhost:5432/lunaverse
```

---

## Step 5: CORS Origins (Optional - Defaults Work)

```bash
CORS_ORIGINS=http://localhost:4173,http://localhost:3000
```

**Only change if**:
- Your frontend runs on a different port
- You're deploying to a domain

**For production**, add your domain:
```bash
CORS_ORIGINS=http://localhost:4173,http://localhost:3000,https://yourdomain.com
```

---

## Step 6: Vector DB Configuration (Optional - Not Required for v1)

```bash
VECTOR_DB_URL=http://vector-db:8000
VECTOR_DB_API_KEY=
VECTOR_DB_TYPE=chroma
```

**Leave as is** for now. The system uses PostgreSQL for embeddings in v1.

---

## Step 7: LLM Model Configuration (Optional)

```bash
HF_MODEL_NAME=meta-llama/Llama-3-8b-instruct
HF_TEMPERATURE=0.3
HF_MAX_NEW_TOKENS=2000
```

**Only change if**:
- You want to use a different model (e.g., `meta-llama/Llama-3-70b-instruct`)
- You want different generation parameters
  - `HF_TEMPERATURE`: Lower (0.1-0.3) = more deterministic, Higher (0.7-1.0) = more creative
  - `HF_MAX_NEW_TOKENS`: Maximum tokens in response (2000 is good for plans)

---

## Step 8: RAG Settings (Optional - Defaults Work)

```bash
INVENTORY_TOP_K=40
HISTORIC_TOP_K=10
TEMPLATES_TOP_K=10
```

**Leave as is** unless you want to:
- Retrieve more/fewer inventory items (increase/decrease `INVENTORY_TOP_K`)
- Include more/fewer historic events (increase/decrease `HISTORIC_TOP_K`)

---

## Step 9: Current RMS Integration (Optional - v2 Feature)

```bash
CURRENT_RMS_SUBDOMAIN=
CURRENT_RMS_API_KEY=
```

**Leave empty** for v1. These are for future Current RMS API integration.

---

## Step 10: Verify Your Configuration

### 10.1 Check Your .env File

Your `.env` should now have at minimum:

```bash
HF_API_URL=<your-endpoint-url>
HF_API_KEY=<your-token>
JWT_SECRET_KEY=<your-random-string>
```

### 10.2 Test Configuration (After Starting Services)

1. **Start services**: `cd infrastructure && docker compose up -d`
2. **Check logs**: `docker compose logs api`
3. **Look for errors** related to:
   - "HF_API_KEY" → Token might be invalid
   - "Connection refused" → Endpoint URL might be wrong
   - "JWT" → Secret key format issue

---

## Quick Reference: Minimum Required Changes

**You MUST change these 3 values:**

1. ✅ `HF_API_KEY` - Your Hugging Face token
2. ✅ `JWT_SECRET_KEY` - A random secure string
3. ✅ `HF_API_URL` - Your endpoint URL (if using custom endpoint)

**Everything else can use defaults for local development.**

---

## Troubleshooting

### "Invalid API Key" Error
- Verify your HF token is correct (no extra spaces)
- Check token hasn't expired
- Ensure token has "Read" permissions

### "Connection Refused" to HF Endpoint
- Verify endpoint URL is correct
- Check endpoint is deployed and running
- Try using direct API URL instead

### "JWT Error"
- Ensure JWT_SECRET_KEY is at least 32 characters
- No spaces or special characters that need escaping
- Use the exact format from generation command

---

## Example Complete .env File

```bash
# Backend Environment Variables
APP_ENV=development
APP_HOST=0.0.0.0
APP_PORT=8000

DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/lunaverse

VECTOR_DB_URL=http://vector-db:8000
VECTOR_DB_API_KEY=
VECTOR_DB_TYPE=chroma

# Hugging Face - FILLED IN
HF_API_URL=https://xxxxx.us-east-1.aws.endpoints.huggingface.cloud
HF_API_KEY=hf_AbCdEf1234567890XyZ
HF_MODEL_NAME=meta-llama/Llama-3-8b-instruct
HF_TEMPERATURE=0.3
HF_MAX_NEW_TOKENS=2000

# JWT - FILLED IN
JWT_SECRET_KEY=K8mN2pQ5rT9vW1xY3zA6bC4dE7fG0hI2jK4lM6nO8pQ0rS2tU4vW6xY8zA
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=1440

# CORS
CORS_ORIGINS=http://localhost:4173,http://localhost:3000

# Logging
LOG_LEVEL=INFO

# RAG Settings
INVENTORY_TOP_K=40
HISTORIC_TOP_K=10
TEMPLATES_TOP_K=10

# Current RMS (v2+)
CURRENT_RMS_SUBDOMAIN=
CURRENT_RMS_API_KEY=
```

---

## Next Steps

After completing this configuration:

1. Save your `.env` file
2. Start services: `cd infrastructure && docker compose up -d`
3. Initialize database (see `docs/dev-setup.md`)
4. Create admin user
5. Test the application!

