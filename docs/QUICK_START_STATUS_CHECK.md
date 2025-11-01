# Quick Start: Status Check Feature

## For End Users

### How to Check Your Grievance Status

1. **Open the Typebot chatbot** at your configured URL (e.g., http://localhost:8082)

2. **From the welcome screen**, select:
   ```
   ☑️ Check status?
   ```

3. **Enter your tracking ID** when prompted:
   ```
   Please enter your reference ID (e.g., GRV-01ABC…):
   
   [Enter: GRV-01K88MF7431X7NF9D4GHQN5742]
   ```

4. **View your status information**:
   ```
   📊 Status for GRV-01K88MF7431X7NF9D4GHQN5742

   **Status Information**
   Status: Under Review
   Note: Case assigned to social worker
   Submitted: 2025-10-23T10:30:00Z

   **Location**
   Island: Tarawa
   District: South Tarawa
   Village: Bairiki

   **Details**
   Category: Service Delivery
   Type: Named
   Household ID: HH2024001
   ```

### Where to Find Your Tracking ID

Your tracking ID is provided when you submit a grievance:
- ✅ In the confirmation message from Typebot
- 📧 In your email receipt (if you provided an email and submitted as non-anonymous)
- 📄 In your PDF receipt (download from Typebot confirmation or via direct URL)

**Download your PDF receipt:**
- URL format: `http://localhost:8000/api/grievances/{YOUR_ID}/receipt.pdf`
- Example: `http://localhost:8000/api/grievances/GRV-01K88MF7431X7NF9D4GHQN5742/receipt.pdf`
- Filename will be: `{YOUR_ID}.pdf` (e.g., `GRV-01K88MF7431X7NF9D4GHQN5742.pdf`)

**Important:** 
- Save your tracking ID! You'll need it to check your status.
- Tracking IDs are generated server-side for security
- Format: `GRV-` followed by 26 alphanumeric characters (30 chars total)

### What Information You'll See

#### For Everyone:
- ✅ Current status (Pending, Under Review, Resolved, etc.)
- ✅ Status notes from case workers
- ✅ Submission date and time
- ✅ Location (Island, District, Village)
- ✅ Category type
- ✅ Household ID (if applicable)

#### For Named Submissions (not anonymous):
- ✅ Your name
- ✅ Your email address
- ✅ Your phone number

#### For Anonymous Submissions:
- 🔒 Personal information is **not** displayed
- ✅ All other information is available

### Common Status Values

| Status | Meaning |
|--------|---------|
| **Pending** | Just submitted, awaiting review |
| **Under Review** | Being evaluated by case workers |
| **In Progress** | Action is being taken |
| **Resolved** | Issue has been addressed |
| **Closed** | Case is complete |

### Tips

- 💡 You can check your status as many times as you want
- 💡 Status updates appear immediately when you check
- 💡 Keep your tracking ID safe and confidential
- 💡 If you get an error, double-check your tracking ID is complete

### Troubleshooting

**Problem:** "I couldn't find that reference"
- **Solution:** Make sure you entered the complete ID starting with "GRV-"
- **Example:** `GRV-01K88MF7431X7NF9D4GHQN5742` (30 characters total)

**Problem:** "Please paste a full GRV ID"
- **Solution:** Your ID format is incorrect. Check that:
  - It starts with "GRV-"
  - It's exactly 30 characters long
  - It contains no spaces

**Problem:** "Our system is busy right now"
- **Solution:** Wait 60 seconds and try again
- The system may be temporarily unavailable

---

## For Developers

### API Usage

**Check status programmatically:**

```bash
# Get grievance status
curl -X GET "http://localhost:8000/api/grievances/GRV-01K88MF7431X7NF9D4GHQN5742"
```

**Response:**
```json
{
  "id": "GRV-01K88MF7431X7NF9D4GHQN5742",
  "created_at": "2025-10-23T10:30:00Z",
  "updated_at": "2025-10-23T10:30:00Z",
  "external_status": "Under Review",
  "external_status_note": "Case assigned to social worker",
  "is_anonymous": false,
  "island": "Tarawa",
  "district": "South Tarawa",
  "village": "Bairiki",
  "category_type": "Service Delivery",
  ...
}
```

### Testing

Run status check tests:
```bash
# All status check tests
pytest tests/test_status_check_flow.py -v

# Specific test
pytest tests/test_status_check_flow.py::test_complete_status_check_flow -v

# Run all tests (118 total: 117 pass + 1 skip)
pytest tests/ -v

# With coverage
pytest tests/test_status_check_flow.py --cov=app.routers.grievances
```

### Implementation Details

- **Endpoint:** `GET /api/grievances/{gid}`
- **No authentication required** (public endpoint for status checking)
- **ID validation:** Regex pattern `^GRV-[A-Z0-9]{26}$`
- **ID generation:** Server-side only (client-provided IDs are rejected)
- **Returns:** Full `GrievancePublic` schema
- **Error handling:** Returns 404 for non-existent IDs
- **Auto-categorization:** Applied automatically when category not provided

### Documentation

- 📖 **Full documentation:** [STATUS_CHECK_FEATURE.md](STATUS_CHECK_FEATURE.md)
- 📖 **Main README:** [../README.md](../README.md)
- 🧪 **Test suite:** `backend/tests/test_status_check_flow.py`

---

## For Administrators

### Updating Status

**Via External System (Odoo) - Authenticated Endpoint:**
```bash
curl -X PUT "http://localhost:8000/api/status/GRV-01K88MF7431X7NF9D4GHQN5742/status" \
  -H "Authorization: Bearer YOUR_ODOO_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "Under Review",
    "note": "Case assigned to social worker",
    "updated_at": "2025-10-23T10:30:00Z"
  }'
```

**Via Internal API (No Auth Required):**
```bash
curl -X PUT "http://localhost:8000/api/grievances/GRV-01K88MF7431X7NF9D4GHQN5742/status" \
  -H "Content-Type: application/json" \
  -d '{
    "external_status": "Resolved",
    "external_status_note": "Issue has been resolved",
    "external_updated_at": "2025-10-23T15:00:00Z"
  }'
```

**Batch Update (Multiple Grievances):**
```bash
curl -X PUT "http://localhost:8000/api/grievances/status-batch" \
  -H "Content-Type: application/json" \
  -d '{
    "updates": [
      {
        "gid": "GRV-01K90BWNRHP3XGS9FSM6H0S8JF",
        "external_status": "resolved",
        "island": "Tongatapu",
        "district": "Lapaha",
        "village": "Lapaha Village"
      },
      {
        "gid": "GRV-01K90C8JA782FM391FFTZ0S20D",
        "external_status": "under_review"
      }
    ]
  }'
```

### Best Practices

1. **Update status regularly** - Keep users informed
2. **Use clear language** - Avoid technical jargon in notes
3. **Be timely** - Update within 24-48 hours of changes
4. **Be specific** - Include actionable information when possible
5. **Monitor frequently checked IDs** - May indicate cases needing attention

### Status Guidelines

**When to use each status:**

- **Pending** → New submissions, not yet reviewed
- **Under Review** → Case is being evaluated
- **In Progress** → Active work is happening
- **Resolved** → Issue has been addressed, awaiting confirmation
- **Closed** → Case is complete, no further action needed

**Include status notes that explain:**
- What action was taken
- What happens next
- Expected timeline (if applicable)
- How to get more help (if needed)

### Monitoring

Track status check usage:
```bash
# Check API logs for status lookup patterns
docker compose logs api | grep "GET /api/grievances/"

# Count status checks per day
docker compose logs api | grep "GET /api/grievances/" | grep "$(date +%Y-%m-%d)" | wc -l
```

---

## Support

Need help? 
- 📧 Review the full documentation in [STATUS_CHECK_FEATURE.md](STATUS_CHECK_FEATURE.md)
- 🐛 Check the test suite for expected behavior
- 💬 Contact the development team for technical issues
