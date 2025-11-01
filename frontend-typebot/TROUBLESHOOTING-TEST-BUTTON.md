# Troubleshooting: Typebot "Test" Button Error

## ❌ Error Message
```
Error! Could not reach server. Check your connection. {}
```

## ✅ Solution Applied

### Root Cause
When you click the "Test" button in Typebot Builder, the Builder service needs to execute webhooks that call `http://grievance-api:8000`. However, the typebot-builder container was **not on the same Docker network** as the API container.

### What Was Fixed

#### 1. Network Configuration (`docker-compose.yml`)
Added `typebot-builder` to the `grievance_net` network:

```yaml
typebot-builder:
  # ... other config ...
  networks:
    - default
    - grievance_net  # <-- ADDED THIS
```

#### 2. Webhook Execution Mode
Set all webhooks to execute server-side:
- `isExecutedOnClient: false` on all webhook blocks
- This forces the Typebot service (not your browser) to execute webhooks

#### 3. Network Topology
All services now communicate properly:

```
grievance_net Network:
├── grievancemodule-api-1 (172.20.0.2)
│   └── Hostname: grievance-api
├── grievancemodule-typebot-viewer-1 (172.20.0.3)
│   └── Executes published bots
└── grievancemodule-typebot-builder-1 (172.20.0.4)
    └── Executes test mode
```

## 🎯 How to Test

### Step 1: Verify Services Are Running
```powershell
docker compose ps
```

All services should show "Up":
- ✅ api
- ✅ typebot-builder  
- ✅ typebot-viewer
- ✅ db, typebot-db, redis, minio, mailhog

### Step 2: Import Updated Typebot
1. Open Typebot Builder: **http://localhost:8081**
2. Delete any old imported bots
3. Import: **`typebot-export-grievance-intake.json`**

### Step 3: Test the Bot
1. Open the imported bot
2. Click the **"Test"** button (top right corner)
3. ✅ The bot should now run without errors!
4. Test creating a grievance through the flow
5. Test looking up a grievance status

## 🔍 Verification Commands

### Check Network Connectivity
```powershell
# View containers on grievance_net
docker network inspect grievance_net -f "{{range .Containers}}{{.Name}}: {{.IPv4Address}}`n{{end}}"
```

Expected output:
```
grievancemodule-api-1: 172.20.0.2/16
grievancemodule-typebot-viewer-1: 172.20.0.3/16
grievancemodule-typebot-builder-1: 172.20.0.4/16
```

### Test API Endpoint
```powershell
# From your computer
Invoke-WebRequest http://localhost:8000/docs

# Should return: StatusCode 200
```

## 📋 File Versions

Both Typebot export files have been updated:

### 1. Production Version (Recommended)
**File:** `typebot-export-grievance-intake.json`
- ✅ URLs: `http://grievance-api:8000`
- ✅ Execution: Server-side (`isExecutedOnClient: false`)
- ✅ Use for: Testing AND Publishing

### 2. Localhost Version (Optional)
**File:** `typebot-export-grievance-intake-LOCALHOST-TEST.json`  
- ✅ URLs: `http://localhost:8000`
- ✅ Execution: Server-side (`isExecutedOnClient: false`)
- ✅ Use for: Development/debugging only

## ⚠️ Important Notes

### When You Click "Test"
- The **typebot-builder** service executes the webhooks
- It uses the Docker network to reach `http://grievance-api:8000`
- Your browser just displays the UI

### When You Publish the Bot
- The **typebot-viewer** service executes the webhooks
- Also uses Docker network to reach `http://grievance-api:8000`
- End users access via browser at `http://localhost:8082`

### Network Requirements
Both typebot-builder AND typebot-viewer MUST be on `grievance_net` to reach the API.

## 🐛 Still Not Working?

### 1. Restart All Services
```powershell
docker compose down
docker compose up -d
```

### 2. Check Logs
```powershell
# Check API logs
docker logs grievancemodule-api-1 --tail 50

# Check Typebot Builder logs
docker logs grievancemodule-typebot-builder-1 --tail 50

# Check Typebot Viewer logs  
docker logs grievancemodule-typebot-viewer-1 --tail 50
```

### 3. Verify Network Exists
```powershell
docker network ls | Select-String "grievance"
```

Should show:
- `grievance_net` (external)
- `grievancemodule_default` (auto-created)

### 4. Recreate Network (if needed)
```powershell
docker network rm grievance_net
docker network create grievance_net
docker compose up -d
```

## ✅ Success Indicators

When everything works correctly:

1. **In Typebot Builder:**
   - "Test" button runs the flow without errors
   - Webhooks return valid responses
   - Variables populate with API data

2. **In API:**
   - New grievances created with `GRV-` IDs
   - Status lookups return correct data
   - PDF receipts generate successfully

3. **Network:**
   - All 3 containers on grievance_net
   - Can ping each other using hostnames
   - No connection errors in logs

## 📚 Related Documentation

- `QUICK-START.md` - Quick setup guide
- `README-TYPEBOT-TESTING.md` - Comprehensive testing guide
- `docker-compose.yml` - Service configuration

## 🎉 Summary

**Before:** typebot-builder ❌ → grievance-api (different networks)

**After:** typebot-builder ✅ → grievance_net → grievance-api (same network)

The test button now works because all services can communicate!
