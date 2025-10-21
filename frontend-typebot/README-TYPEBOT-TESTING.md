# Typebot Import Files

This folder contains two versions of the Grievance Intake Typebot flow:

## Files

### 1. `typebot-export-grievance-intake-qwdn4no.json` ✅ PRODUCTION
**Use this for:** Production deployment and published bots

**Webhook URLs:** `http://grievance-api:8000`
- Works when the bot runs in Typebot Viewer (server-side execution)
- Uses Docker internal network names
- **Best for:** Final deployment

**How to use:**
1. Open Typebot Builder: http://localhost:8081
2. Import this file
3. Publish the bot
4. Share the viewer URL with end users

---

### 2. `typebot-export-grievance-intake-LOCALHOST-TEST.json` 🧪 TESTING
**Use this for:** Testing webhooks in Typebot Builder

**Webhook URLs:** `http://localhost:8000`
- Works when you click "Test" in the Builder (browser execution)
- Uses localhost instead of Docker network names
- **Best for:** Development and testing

**How to use:**
1. Open Typebot Builder: http://localhost:8081
2. Import this file
3. Click "Test" on any webhook block - should work! ✅
4. Make your changes and test
5. **Do NOT publish this version** - it won't work for end users

---

## Quick Reference

### When to use each version:

| Scenario | File to Use |
|----------|-------------|
| Testing webhooks in Builder | `LOCALHOST-TEST.json` |
| Publishing for end users | `qwdn4no.json` (production) |
| Making flow changes | Either (test with LOCALHOST) |
| Final deployment | `qwdn4no.json` (production) |

### API Endpoints Reference

Both versions use these endpoints:

**Create Grievance (POST):**
- Production: `http://grievance-api:8000/api/grievances`
- Testing: `http://localhost:8000/api/grievances`

**Get Grievance Status (GET):**
- Production: `http://grievance-api:8000/api/grievances/{id}`
- Testing: `http://localhost:8000/api/grievances/{id}`

**Download Receipt (GET):**
- Production: `http://grievance-api:8000/api/grievances/{id}/receipt.pdf`
- Testing: `http://localhost:8000/api/grievances/{id}/receipt.pdf`

---

## Workflow Recommendation

1. **Development:**
   - Import `LOCALHOST-TEST.json`
   - Make changes
   - Test using the "Test" button ✅

2. **Before Publishing:**
   - Import `qwdn4no.json` (production version)
   - Apply the same changes
   - Publish this version

3. **Or (simpler):**
   - Work on `LOCALHOST-TEST.json`
   - When done, manually change webhook URLs from `localhost:8000` → `grievance-api:8000`
   - Publish

---

## Troubleshooting

### "Could not reach server" error when testing
- ✅ **Solution:** Make sure you're using the `LOCALHOST-TEST.json` version
- Check that API is running: http://localhost:8000/docs

### Published bot not working
- ❌ **Problem:** You published the LOCALHOST version
- ✅ **Solution:** Import and publish the production version (`qwdn4no.json`)

### Test works but published bot fails
- Verify all services are running: `docker compose ps`
- Check logs: `docker compose logs api`
- Ensure webhook URLs use `http://grievance-api:8000` (not localhost)

---

## Services

All services must be running for the bot to work:

```bash
docker compose up -d
```

- **API:** http://localhost:8000 (FastAPI backend)
- **Typebot Builder:** http://localhost:8081 (for editing)
- **Typebot Viewer:** http://localhost:8082 (for end users)
- **MailHog:** http://localhost:8025 (email testing)
- **MinIO Console:** http://localhost:9001 (file storage)
