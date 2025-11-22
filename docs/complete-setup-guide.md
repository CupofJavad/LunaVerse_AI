# Complete Setup Guide - Lunaverse Show Brain v1
## From Zero to Running Application

This guide assumes you have **nothing** installed and walks you through every single step, click-by-click.

---

## Table of Contents

1. [Prerequisites Installation](#part-1-prerequisites-installation)
2. [Project Setup](#part-2-project-setup)
3. [Hugging Face Account Setup](#part-3-hugging-face-account-setup)
4. [Environment Configuration](#part-4-environment-configuration)
5. [Starting the Application](#part-5-starting-the-application)
6. [Database Initialization](#part-6-database-initialization)
7. [Creating Your First User](#part-7-creating-your-first-user)
8. [Testing the Application](#part-8-testing-the-application)
9. [Troubleshooting](#part-9-troubleshooting)

---

## Part 1: Prerequisites Installation

### Step 1.1: Check Your Operating System

1. **Click the Apple logo** (🍎) in the top-left corner of your Mac screen
2. **Click "About This Mac"**
3. **Note your macOS version** (should be macOS 10.15 or later)
4. **Close the window** (click the red X or press Cmd+Q)

### Step 1.2: Install Homebrew (Package Manager for Mac)

Homebrew makes installing software easier on Mac.

1. **Open Terminal**:
   - Press `Cmd + Space` (Command key + Spacebar)
   - Type: `Terminal`
   - Press `Enter`
   - A black window should open

2. **Copy this command** (don't run it yet):
   ```
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

3. **Paste into Terminal**:
   - Click in the Terminal window
   - Press `Cmd + V` to paste
   - Press `Enter`

4. **Enter your password** when prompted:
   - Type your Mac login password (you won't see characters as you type - this is normal)
   - Press `Enter`
   - Wait for installation (5-10 minutes)

5. **Follow any on-screen prompts**:
   - If it asks to install Xcode Command Line Tools, type `Y` and press `Enter`
   - Wait for completion

6. **Verify installation**:
   - In Terminal, type: `brew --version`
   - Press `Enter`
   - You should see a version number (e.g., "Homebrew 4.x.x")
   - If you see an error, wait 2 minutes and try again

### Step 1.3: Install Git

Git is used to manage code versions.

1. **In Terminal**, type: `brew install git`
2. **Press Enter**
3. **Wait for installation** (2-5 minutes)
4. **Verify installation**:
   - Type: `git --version`
   - Press `Enter`
   - You should see "git version 2.x.x"

### Step 1.4: Install Docker Desktop

Docker runs the application in containers.

1. **Open your web browser** (Safari, Chrome, or Firefox)

2. **Go to Docker website**:
   - Click in the address bar (top of browser)
   - Type: `https://www.docker.com/products/docker-desktop/`
   - Press `Enter`

3. **Download Docker Desktop**:
   - Look for a button that says "Download for Mac" or "Get Docker Desktop"
   - **Click the button**
   - Wait for download to complete (file will be in your Downloads folder)

4. **Install Docker Desktop**:
   - **Open Finder** (click the blue face icon in your Dock)
   - **Click "Downloads"** in the left sidebar
   - **Find "Docker.dmg"** file
   - **Double-click** the Docker.dmg file
   - A window will open with Docker icon
   - **Drag the Docker icon** to the Applications folder
   - Wait for copy to complete

5. **Open Docker Desktop**:
   - **Open Finder** → **Applications**
   - **Find "Docker"** application
   - **Double-click** Docker
   - **Click "Open"** if asked about security
   - Wait for Docker to start (you'll see a whale icon in your menu bar)

6. **Complete Docker Setup**:
   - Docker will ask you to sign in or create account
   - **Click "Skip"** or create a free account (your choice)
   - Wait for Docker to finish starting (whale icon stops animating)

7. **Verify Docker is running**:
   - **Open Terminal** (Cmd+Space, type "Terminal")
   - Type: `docker --version`
   - Press `Enter`
   - You should see "Docker version 24.x.x"
   - Type: `docker compose version`
   - Press `Enter`
   - You should see "Docker Compose version v2.x.x"

### Step 1.5: Install Python (for generating JWT secret)

1. **Check if Python is installed**:
   - In Terminal, type: `python3 --version`
   - Press `Enter`
   - If you see a version (e.g., "Python 3.9.x"), skip to next step
   - If you see "command not found", continue:

2. **Install Python via Homebrew**:
   - In Terminal, type: `brew install python`
   - Press `Enter`
   - Wait for installation (5-10 minutes)

3. **Verify Python**:
   - Type: `python3 --version`
   - Press `Enter`
   - Should show "Python 3.x.x"

---

## Part 2: Project Setup

### Step 2.1: Navigate to Your Projects Folder

1. **Open Terminal** (if not already open)

2. **Navigate to your home directory**:
   - Type: `cd ~`
   - Press `Enter`

3. **Create a projects folder** (if it doesn't exist):
   - Type: `mkdir -p Projects`
   - Press `Enter`

4. **Go into Projects folder**:
   - Type: `cd Projects`
   - Press `Enter`

### Step 2.2: Verify Project Files Exist

You should already have the project files. Let's verify:

1. **In Terminal**, type: `cd ~/PycharmProjects/LunaVerse_AI`
2. **Press Enter**

3. **List files**:
   - Type: `ls -la`
   - Press `Enter`
   - You should see folders: `backend`, `frontend`, `infrastructure`, `docs`

4. **If files don't exist**, you need to get them first:
   - Ask the person who gave you this project for the files
   - Or if it's in Git, ask for the repository URL

### Step 2.3: Verify Project Structure

1. **Check backend folder**:
   - Type: `ls backend`
   - Press `Enter`
   - Should see `app`, `requirements.txt`, `Dockerfile`

2. **Check frontend folder**:
   - Type: `ls frontend`
   - Press `Enter`
   - Should see `src`, `package.json`, `Dockerfile`

3. **Check infrastructure folder**:
   - Type: `ls infrastructure`
   - Press `Enter`
   - Should see `docker-compose.yml`

---

## Part 3: Hugging Face Account Setup

### Step 3.1: Create Hugging Face Account

1. **Open your web browser**

2. **Go to Hugging Face**:
   - Click address bar
   - Type: `https://huggingface.co/`
   - Press `Enter`

3. **Sign Up**:
   - **Click "Sign Up"** button (top right)
   - Choose sign-up method:
     - **Option A**: Click "Sign up with email"
       - Enter your email
       - Create a password
       - Click "Sign up"
       - Check email for verification link
       - Click verification link in email
     - **Option B**: Click "Sign up with GitHub" (if you have GitHub)
       - Authorize Hugging Face
     - **Option C**: Click "Sign up with Google"
       - Sign in with Google account

4. **Complete profile** (if asked):
   - Choose a username
   - Select your interests (optional)
   - Click "Continue"

### Step 3.2: Create API Token

1. **Click your profile picture/avatar** (top right corner)

2. **Click "Settings"** from dropdown menu

3. **Click "Access Tokens"** in left sidebar
   - Or go directly to: `https://huggingface.co/settings/tokens`

4. **Create new token**:
   - **Click "New token"** button
   - **Token name**: Type `Lunaverse Show Brain`
   - **Token type**: Select **"Read"** (from dropdown)
   - **Click "Generate token"** button

5. **Copy the token**:
   - **IMPORTANT**: The token appears only once!
   - **Click the copy icon** next to the token (looks like two overlapping squares)
   - Or **select all text** (Cmd+A) and **copy** (Cmd+C)
   - **Paste it somewhere safe** (TextEdit, Notes app, etc.)
   - Token looks like: `hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - **Write it down or save it** - you'll need it soon!

### Step 3.3: Choose LLM Endpoint Option

You have two options:

**Option A: Use Free Inference API (Easiest - Recommended for Testing)**

1. **No setup needed!**
2. **Use this URL**: `https://api-inference.huggingface.co/models/meta-llama/Llama-3-8b-instruct`
3. **Note**: Free tier has rate limits and may queue requests
4. **Skip to Part 4** if choosing this option

**Option B: Create Inference Endpoint (Better Performance)**

1. **Go to models page**:
   - In browser, go to: `https://huggingface.co/models`
   - **Click in search box** (top of page)
   - Type: `meta-llama/Llama-3-8b-instruct`
   - Press `Enter`

2. **Click on the model** (first result)

3. **Go to Deploy tab**:
   - **Click "Deploy"** tab at top of page
   - **Click "Inference Endpoints"** option

4. **Create endpoint**:
   - **Click "New Endpoint"** button
   - **Endpoint name**: Type `lunaverse-llm`
   - **Compute**: Click dropdown, select **"CPU Basic"** (free) or **"GPU"** (paid)
   - **Region**: Select closest to you (e.g., "US East")
   - **Task**: Select **"Text Generation"** from dropdown
   - **Click "Create Endpoint"** button

5. **Wait for deployment**:
   - Status will show "Building" then "Running"
   - This takes **5-10 minutes**
   - **Don't close the page!**

6. **Copy endpoint URL**:
   - Once status shows "Running"
   - **Find the URL** (looks like: `https://xxxxx.us-east-1.aws.endpoints.huggingface.cloud`)
   - **Click copy icon** next to URL
   - **Save this URL** - you'll need it in Part 4

---

## Part 4: Environment Configuration

### Step 4.1: Open .env File

1. **Open Terminal** (if not open)

2. **Navigate to project**:
   - Type: `cd ~/PycharmProjects/LunaVerse_AI`
   - Press `Enter`

3. **Open .env file in editor**:
   - **Option A - Using VS Code** (if installed):
     - Type: `code .env`
     - Press `Enter`
   - **Option B - Using TextEdit**:
     - Type: `open -a TextEdit .env`
     - Press `Enter`
   - **Option C - Using nano** (Terminal editor):
     - Type: `nano .env`
     - Press `Enter`
     - (To save in nano: Press `Ctrl+O`, then `Enter`, then `Ctrl+X`)

### Step 4.2: Generate JWT Secret Key

1. **Open a new Terminal window** (keep .env editor open):
   - Press `Cmd+T` in Terminal (or open new Terminal)

2. **Generate secret**:
   - Type: `python3 -c "import secrets; print(secrets.token_urlsafe(64))"`
   - Press `Enter`
   - A long random string will appear

3. **Copy the output**:
   - **Select the entire string** (click and drag, or triple-click)
   - **Copy it** (Cmd+C)
   - **Paste it somewhere temporary** (TextEdit, Notes)

### Step 4.3: Fill in Environment Variables

In your `.env` file editor, find and replace these lines:

#### Line 1: HF_API_URL

**Find this line:**
```bash
HF_API_URL=https://api-inference.huggingface.co/models/meta-llama/Llama-3-8b-instruct
```

**Replace with:**
- **If using Option A (Free API)**: Keep as is, or change to:
  ```bash
  HF_API_URL=https://api-inference.huggingface.co/models/meta-llama/Llama-3-8b-instruct
  ```
- **If using Option B (Custom Endpoint)**: Replace with your endpoint URL:
  ```bash
  HF_API_URL=https://xxxxx.us-east-1.aws.endpoints.huggingface.cloud
  ```
  (Replace `xxxxx` with your actual endpoint URL)

#### Line 2: HF_API_KEY

**Find this line:**
```bash
HF_API_KEY=your-hf-api-key-here
```

**Replace with:**
```bash
HF_API_KEY=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
(Replace with the token you copied in Step 3.2)

#### Line 3: JWT_SECRET_KEY

**Find this line:**
```bash
JWT_SECRET_KEY=change-me-in-production-use-long-random-string
```

**Replace with:**
```bash
JWT_SECRET_KEY=<paste-your-generated-secret-here>
```
(Paste the secret you generated in Step 4.2)

### Step 4.4: Save .env File

1. **If using TextEdit**:
   - Press `Cmd+S` to save
   - Close TextEdit window

2. **If using VS Code**:
   - Press `Cmd+S` to save
   - Close VS Code window

3. **If using nano**:
   - Press `Ctrl+O` (save)
   - Press `Enter` (confirm filename)
   - Press `Ctrl+X` (exit)

### Step 4.5: Verify .env File

1. **In Terminal**, type: `cat .env | grep -E "HF_API_KEY|JWT_SECRET_KEY|HF_API_URL"`

2. **Press Enter**

3. **Check output**:
   - `HF_API_KEY` should NOT say "your-hf-api-key-here"
   - `JWT_SECRET_KEY` should NOT say "change-me-in-production"
   - `HF_API_URL` should be a valid URL
   - If any still have placeholders, go back and fix them

---

## Part 5: Starting the Application

### Step 5.1: Ensure Docker is Running

1. **Look at your Mac menu bar** (top of screen)
2. **Find the Docker whale icon** 🐳
3. **If you don't see it**:
   - Open Docker Desktop (Applications → Docker)
   - Wait for it to start (whale icon appears)
4. **If whale icon is animating**: Wait until it stops (Docker is starting)
5. **If whale icon is static**: Docker is running ✅

### Step 5.2: Navigate to Infrastructure Folder

1. **Open Terminal**

2. **Navigate to infrastructure**:
   - Type: `cd ~/PycharmProjects/LunaVerse_AI/infrastructure`
   - Press `Enter`

3. **Verify docker-compose.yml exists**:
   - Type: `ls`
   - Press `Enter`
   - Should see `docker-compose.yml`

### Step 5.3: Start Docker Services

1. **Start all services**:
   - Type: `docker compose up -d`
   - Press `Enter`
   - This will take **5-10 minutes** the first time (downloading images)

2. **Watch the output**:
   - You'll see lines like "Pulling..." and "Creating..."
   - Wait until you see "Done" or the command prompt returns
   - **Don't close Terminal!**

3. **Check service status**:
   - Type: `docker compose ps`
   - Press `Enter`
   - You should see 4 services:
     - `db` - Status: "Up"
     - `api` - Status: "Up"
     - `frontend` - Status: "Up"
     - `caddy` - Status: "Up"
   - If any show "Exit" or errors, see Troubleshooting section

### Step 5.4: View Logs (Optional but Helpful)

1. **View all logs**:
   - Type: `docker compose logs`
   - Press `Enter`
   - Scroll through to see if there are errors

2. **View specific service logs**:
   - Type: `docker compose logs api`
   - Press `Enter`
   - Look for errors (red text)

3. **Follow logs in real-time**:
   - Type: `docker compose logs -f api`
   - Press `Enter`
   - Press `Ctrl+C` to stop watching

---

## Part 6: Database Initialization

### Step 6.1: Wait for Database to be Ready

1. **Check database is running**:
   - Type: `docker compose ps db`
   - Press `Enter`
   - Status should be "Up"

2. **Wait 30 seconds** after starting services (database needs time to initialize)

### Step 6.2: Run Database Schema

1. **Execute schema SQL**:
   - Type: `docker compose exec db psql -U postgres -d lunaverse -f /docker-entrypoint-initdb.d/schema.sql`
   - Press `Enter`

2. **If you see errors**:
   - Type: `docker compose exec db psql -U postgres -d postgres -c "CREATE DATABASE lunaverse;"`
   - Press `Enter`
   - Then run the schema command again

3. **Verify tables created**:
   - Type: `docker compose exec db psql -U postgres -d lunaverse -c "\dt"`
   - Press `Enter`
   - Should see list of tables: users, events, rooms, etc.

---

## Part 7: Creating Your First User

### Step 7.1: Create Admin User via Python Script

1. **Create a Python script**:
   - Type: `cd ~/PycharmProjects/LunaVerse_AI`
   - Press `Enter`

2. **Create script file**:
   - Type: `cat > create_user.py << 'EOF'`
   - Press `Enter`
   - **Paste this code** (then press Enter, type EOF, press Enter):
   ```python
   import sys
   sys.path.append('/app')
   from app.db.base import SessionLocal
   from app.models.users import User
   from app.auth.password_hash import hash_password
   
   db = SessionLocal()
   email = input("Enter email: ")
   password = input("Enter password: ")
   
   user = User(
       email=email,
       password_hash=hash_password(password),
       role='admin'
   )
   db.add(user)
   db.commit()
   print(f"User {email} created successfully!")
   db.close()
   ```
   - Type: `EOF`
   - Press `Enter`

3. **Run the script inside Docker**:
   - Type: `docker compose -f infrastructure/docker-compose.yml exec api python3 create_user.py`
   - Press `Enter`
   - **Enter email**: Type your email (e.g., `admin@example.com`)
   - Press `Enter`
   - **Enter password**: Type a password (e.g., `admin123`)
   - Press `Enter`
   - Should see "User created successfully!"

### Step 7.2: Alternative - Create User via SQL

If the Python method doesn't work:

1. **Generate password hash**:
   - Type: `docker compose -f infrastructure/docker-compose.yml exec api python3 -c "from app.auth.password_hash import hash_password; print(hash_password('admin123'))"`
   - Press `Enter`
   - **Copy the output** (long hash string)

2. **Insert user via SQL**:
   - Type: `docker compose exec db psql -U postgres -d lunaverse`
   - Press `Enter`

3. **Run SQL command** (replace `<hash>` with the hash from step 1):
   ```sql
   INSERT INTO users (email, password_hash, role) VALUES ('admin@example.com', '<hash>', 'admin');
   ```
   - Press `Enter`

4. **Exit SQL**:
   - Type: `\q`
   - Press `Enter`

---

## Part 8: Testing the Application

### Step 8.1: Access the Frontend

1. **Open your web browser**

2. **Go to application**:
   - Click address bar
   - Type: `http://localhost:4173`
   - Press `Enter`

3. **You should see**:
   - Login page with "Lunaverse Show Brain" title
   - Email and password fields
   - Login button

### Step 8.2: Test Login

1. **Enter credentials**:
   - **Email field**: Type the email you created (e.g., `admin@example.com`)
   - **Password field**: Type the password you created (e.g., `admin123`)
   - **Click "Login" button**

2. **Expected result**:
   - Page redirects to Dashboard
   - You see "Lunaverse Show Brain" header
   - "New Event" button visible
   - "Recent Events" section (empty for now)

3. **If login fails**:
   - Check you're using correct email/password
   - Check browser console for errors (F12 → Console tab)
   - Check API logs: `docker compose logs api`

### Step 8.3: Test API Directly

1. **Open new browser tab**

2. **Go to API docs**:
   - Type: `http://localhost:8000/docs`
   - Press `Enter`

3. **You should see**:
   - Swagger/OpenAPI documentation page
   - List of API endpoints

4. **Test health endpoint**:
   - **Find "/health"** endpoint
   - **Click it**
   - **Click "Try it out"** button
   - **Click "Execute"** button
   - **Check response**: Should show `{"status": "healthy", "service": "lunaverse-show-brain"}`

### Step 8.4: Test Event Creation (Basic)

1. **In browser**, go back to: `http://localhost:4173`

2. **Click "New Event"** button

3. **Fill in event form**:
   - **Event Name**: Type `Test Event`
   - **Client Name**: Type `Test Client`
   - **Start Date**: Click date field, select today's date
   - **End Date**: Click date field, select tomorrow's date
   - **Venue**: Type `Test Venue`
   - **City**: Type `Test City`
   - **State**: Type `CA`
   - **Country**: Type `USA`
   - **Timezone**: Type `America/Los_Angeles`

4. **Add a room**:
   - **Room Name**: Type `Main Hall`
   - **Room Type**: Select "General Session" from dropdown
   - **Capacity**: Type `100`

5. **Click "Generate Plan"** button

6. **Expected result**:
   - Loading indicator appears
   - After 20-60 seconds, plan is generated
   - You're redirected to Plan Viewer page
   - You see equipment and crew tables

7. **If it fails**:
   - Check browser console (F12)
   - Check API logs: `docker compose logs api`
   - Verify HF_API_KEY is correct in .env
   - Verify HF_API_URL is accessible

---

## Part 9: Troubleshooting

### Problem: Docker won't start

**Symptoms**: Docker whale icon keeps animating, or error messages

**Solutions**:
1. **Restart Docker Desktop**:
   - Click whale icon in menu bar
   - Click "Quit Docker Desktop"
   - Wait 10 seconds
   - Open Docker Desktop again (Applications → Docker)

2. **Check system requirements**:
   - macOS 10.15 or later
   - At least 4GB RAM available
   - Close other applications to free memory

3. **Restart your Mac**:
   - Apple menu → Restart
   - After restart, open Docker Desktop first
   - Wait for it to fully start before proceeding

### Problem: "docker compose: command not found"

**Solutions**:
1. **Use docker-compose instead**:
   - Replace `docker compose` with `docker-compose` in all commands
   - Example: `docker-compose up -d`

2. **Update Docker Desktop**:
   - Docker Desktop → Settings → General
   - Enable "Use Docker Compose V2"
   - Restart Docker Desktop

### Problem: Services won't start

**Symptoms**: `docker compose ps` shows services as "Exit" or "Restarting"

**Solutions**:
1. **Check logs**:
   ```bash
   docker compose logs api
   docker compose logs db
   ```

2. **Common issues**:
   - **Port already in use**: Another app is using port 8000 or 5432
     - Solution: Stop other apps, or change ports in docker-compose.yml
   - **Database connection error**: Database not ready yet
     - Solution: Wait 30 seconds, then `docker compose restart api`
   - **Missing .env file**: Environment variables not set
     - Solution: Verify .env file exists and has correct values

3. **Rebuild containers**:
   ```bash
   docker compose down
   docker compose up -d --build
   ```

### Problem: "HF_API_KEY invalid" or LLM errors

**Symptoms**: Plan generation fails with authentication errors

**Solutions**:
1. **Verify token**:
   - Go to https://huggingface.co/settings/tokens
   - Check token exists and is active
   - Generate new token if needed

2. **Check .env file**:
   - Ensure no extra spaces around `=`
   - Ensure no quotes around values
   - Verify token starts with `hf_`

3. **Test token manually**:
   ```bash
   curl -H "Authorization: Bearer YOUR_TOKEN" https://api-inference.huggingface.co/models/meta-llama/Llama-3-8b-instruct
   ```

### Problem: Can't access frontend at localhost:4173

**Symptoms**: Browser shows "Can't connect" or "Refused"

**Solutions**:
1. **Check frontend is running**:
   ```bash
   docker compose ps frontend
   ```

2. **Check frontend logs**:
   ```bash
   docker compose logs frontend
   ```

3. **Restart frontend**:
   ```bash
   docker compose restart frontend
   ```

4. **Try different port**:
   - Check if port 4173 is in use: `lsof -i :4173`
   - Change port in docker-compose.yml if needed

### Problem: Database connection errors

**Symptoms**: API logs show "could not connect to database"

**Solutions**:
1. **Wait longer**: Database takes 30-60 seconds to be ready

2. **Check database is running**:
   ```bash
   docker compose ps db
   ```

3. **Restart database**:
   ```bash
   docker compose restart db
   # Wait 30 seconds
   docker compose restart api
   ```

4. **Recreate database**:
   ```bash
   docker compose down
   docker volume rm infrastructure_postgres_data
   docker compose up -d
   # Wait 60 seconds, then run schema again
   ```

### Problem: "Module not found" or Python errors

**Symptoms**: API logs show import errors

**Solutions**:
1. **Rebuild API container**:
   ```bash
   docker compose build api
   docker compose up -d api
   ```

2. **Check requirements.txt exists**:
   ```bash
   ls backend/requirements.txt
   ```

### Problem: Login works but can't create events

**Symptoms**: Dashboard loads but "New Event" doesn't work

**Solutions**:
1. **Check browser console** (F12 → Console tab)
   - Look for red error messages
   - Common: CORS errors, API connection errors

2. **Verify API is accessible**:
   - Go to: http://localhost:8000/health
   - Should see JSON response

3. **Check CORS settings**:
   - In .env, verify `CORS_ORIGINS` includes `http://localhost:4173`
   - Restart API: `docker compose restart api`

### Getting Help

If you're still stuck:

1. **Collect information**:
   ```bash
   docker compose ps
   docker compose logs api > api_logs.txt
   docker compose logs db > db_logs.txt
   ```

2. **Check these files**:
   - `.env` file (verify all values)
   - `infrastructure/docker-compose.yml`
   - Browser console errors (F12)

3. **Common solutions**:
   - Restart everything: `docker compose down && docker compose up -d`
   - Check Docker has enough resources (Settings → Resources)
   - Verify all prerequisites are installed correctly

---

## Success Checklist

You've successfully set up the application when:

- ✅ Docker Desktop is running
- ✅ All 4 services show "Up" in `docker compose ps`
- ✅ You can access http://localhost:4173 and see login page
- ✅ You can log in with your created user
- ✅ You can see the dashboard
- ✅ API docs are accessible at http://localhost:8000/docs
- ✅ Health endpoint returns success

---

## Next Steps After Setup

1. **Ingest inventory data**:
   - Export products CSV from Current RMS
   - Upload via `/ingest/inventory` endpoint

2. **Add historic events**:
   - Upload past event data via `/ingest/historic-events`

3. **Add templates/SOPs**:
   - Upload standard packages via `/ingest/templates`

4. **Generate your first real plan**:
   - Create an event with full details
   - Generate plan
   - Review and export results

---

## Quick Reference Commands

**Start services:**
```bash
cd infrastructure
docker compose up -d
```

**Stop services:**
```bash
docker compose down
```

**View logs:**
```bash
docker compose logs -f api
```

**Restart a service:**
```bash
docker compose restart api
```

**Check status:**
```bash
docker compose ps
```

**Access database:**
```bash
docker compose exec db psql -U postgres -d lunaverse
```

**Rebuild everything:**
```bash
docker compose down
docker compose build --no-cache
docker compose up -d
```

---

**Congratulations!** You've successfully set up Lunaverse Show Brain v1! 🎉

