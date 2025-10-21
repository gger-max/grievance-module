# 🚀 Quick Start: Testing Typebot Webhooks

## Problem Solved ✅
When you click "Test" in Typebot Builder, you get:
```
Error! Could not reach server. Check your connection.{}
```

**Root Cause:** Webhooks need to be explicitly configured to execute **server-side** (not client-side/browser).

**What We Fixed:**
- Set `isExecutedOnClient: false` on all webhook blocks
- This forces the Typebot Viewer container to execute webhooks (which can reach `http://grievance-api:8000`)
- Without this setting, webhooks try to execute from your browser (which can't reach Docker internal networks)

## Solution: Use Updated Versions with Server-Side Execution

### Step 1: Import the Production Version
1. Open Typebot Builder: **http://localhost:8081**
2. **Delete the old bot** (if you previously imported one)
3. Click **"Create a typebot"** → **"Import a file"**
4. Select: **`typebot-export-grievance-intake-qwdn4no.json`**
5. You'll see: **"Grievance Intake"**

### Step 2: Test the Bot
1. Open the imported bot
2. Click **"Test"** button (top right)
3. ✅ **Webhooks should now execute server-side and work!**

### Why This Works Now:
- ✅ Webhooks are set to `isExecutedOnClient: false`
- ✅ Typebot Viewer (server) executes the webhook → can reach `http://grievance-api:8000`
- ✅ Both API and Typebot Viewer are on the same Docker network (`grievance_net`)

---

## ⚠️ Important: Both Versions Now Work for Testing!

**Good News:** Both files now have `isExecutedOnClient: false` set on all webhooks!

### When to Use Each Version:

**Production Version (`qwdn4no.json`):**
- ✅ Use for production deployment
- ✅ Use for testing the full bot flow
- Uses: `http://grievance-api:8000` (Docker network)
- **Publish this version** for end users

**LOCALHOST Test Version (`LOCALHOST-TEST.json`):**
- 🧪 Optional - for development/debugging
- Uses: `http://localhost:8000`
- Useful if you need to test against localhost API
- **Don't publish this version**

---

## File Comparison

| File | URLs | Execution | Where Runs | Can Test? | Can Publish? |
|------|------|-----------|------------|-----------|--------------|
| `LOCALHOST-TEST.json` | `localhost:8000` | **Client-side** (browser) | Your Browser | ✅ Yes | ❌ No |
| `qwdn4no.json` | `grievance-api:8000` | **Server-side** (container) | Typebot Server | ❌ No* | ✅ Yes |

*Testing the production version in Builder won't work because your browser can't reach Docker internal networks.

**Key Difference:**
- **LOCALHOST-TEST**: Webhooks execute in your browser → can reach `http://localhost:8000` ✅
- **Production**: Webhooks execute server-side → can reach `http://grievance-api:8000` ✅

---

## Test the API Manually

Verify API is running:
```powershell
# Test API health
Invoke-WebRequest http://localhost:8000/docs

# Create a test grievance
$body = @{is_anonymous=$true; grievance_details="Test"} | ConvertTo-Json
Invoke-WebRequest -Uri http://localhost:8000/api/grievances/ -Method POST -Body $body -ContentType "application/json"
```

---

## Services Checklist

Make sure all services are running:
```bash
docker compose ps
```

Required services:
- ✅ **grievancemodule-api-1** (port 8000)
- ✅ **grievancemodule-typebot-builder-1** (port 8081)
- ✅ **grievancemodule-typebot-viewer-1** (port 8082)
- ✅ **grievancemodule-db-1** (port 5432)
- ✅ **grievancemodule-typebot-db-1** (port 5433)

---

## Need Help?

See **README-TYPEBOT-TESTING.md** for detailed documentation.
