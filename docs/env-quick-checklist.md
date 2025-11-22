# .env Configuration Quick Checklist

## ✅ Step-by-Step Checklist

### Step 1: Hugging Face Account Setup
- [ ] Go to https://huggingface.co/ and sign in (or create account)
- [ ] Navigate to Settings → Access Tokens
- [ ] Click "New token"
- [ ] Name it "Lunaverse Show Brain"
- [ ] Select "Read" type
- [ ] Click "Generate token"
- [ ] **COPY THE TOKEN** (shows only once!)

### Step 2: Hugging Face Endpoint (Choose One)

**Option A: Use Direct API (Easiest)**
- [ ] Use URL: `https://api-inference.huggingface.co/models/meta-llama/Llama-3-8b-instruct`
- [ ] No endpoint setup needed

**Option B: Create Inference Endpoint**
- [ ] Go to https://huggingface.co/models
- [ ] Search "meta-llama/Llama-3-8b-instruct"
- [ ] Click model → "Deploy" tab
- [ ] Click "Inference Endpoints" → "New Endpoint"
- [ ] Configure endpoint (CPU Basic for free)
- [ ] Wait for deployment (5-10 min)
- [ ] Copy endpoint URL

### Step 3: Generate JWT Secret
- [ ] Open terminal
- [ ] Run: `python3 -c "import secrets; print(secrets.token_urlsafe(64))"`
- [ ] **COPY THE OUTPUT**

### Step 4: Edit .env File
- [ ] Open `.env` file in editor
- [ ] Find `HF_API_URL=` and paste your endpoint URL (or use direct API URL)
- [ ] Find `HF_API_KEY=` and paste your Hugging Face token
- [ ] Find `JWT_SECRET_KEY=` and paste your generated secret
- [ ] Save file

### Step 5: Verify
- [ ] Check all three values are filled (no placeholders remain)
- [ ] No extra spaces or quotes around values
- [ ] File saved successfully

## Minimum Required Changes

You **MUST** change these 3 lines:

```bash
HF_API_URL=<your-url-here>
HF_API_KEY=<your-token-here>
JWT_SECRET_KEY=<your-secret-here>
```

Everything else can stay as default for local development!

## Quick Commands Reference

**Generate JWT Secret:**
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(64))"
```

**Or using OpenSSL:**
```bash
openssl rand -hex 32
```

**Open .env file:**
```bash
nano .env
# or
code .env
```

## Need Help?

See `docs/env-setup-guide.md` for detailed instructions with screenshots guidance.

