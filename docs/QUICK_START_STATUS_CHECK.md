# Quick Start: Status Check Feature

## For End Users

### How to Check Your Grievance Status

1. **Open the Typebot chatbot** at your configured URL (e.g., http://localhost:8082)

2. **From the welcome screen**, select:
   ```
   Check the status of a grievance
   ```

3. **Enter your tracking ID** when prompted:
   ```
   Please enter your reference ID (e.g., GRV-01ABC…):
   
   [Placeholder: GRV-01ABC…]
   ```
   
   **ID Validation:** The system validates that your ID matches the format `^GRV-[A-Z0-9]{26}$`

4. **View your status information**:
   ```
   Status for GRV-01K88MF7431X7NF9D4GHQN5742

   Status Information
   Status: Under Review
   Note: Case assigned to social worker
   Updated: Mon Oct 23 2025 3:30:00 PM

   Details
   Created: Mon Oct 23 2025 10:30:00 AM
   Category: 2.3 HH member not registered
   Type: Named
   Household ID*: HH2024001
   For more details: Receipt.pdf (clickable link)

   Location*
   Island: Tongatapu
   District: Lapaha
   Village: Lapaha Village

   An email will also be send with the above info*.

   * = If not anonymous
   ```

5. **Options after viewing**:
   - **Check another** - Look up a different grievance ID
   - **Done** - Exit the status check flow

### Where to Find Your Tracking ID

Your tracking ID is provided when you submit a grievance:
- In the confirmation message from Typebot
- In your email receipt (if you provided an email and submitted as non-anonymous)
- In your PDF receipt (download from Typebot confirmation or via direct URL)

**Download your PDF receipt:**
- URL format: `http://localhost:8000/api/grievances/{YOUR_ID}/receipt.pdf`
- Example: `http://localhost:8000/api/grievances/GRV-01K88MF7431X7NF9D4GHQN5742/receipt.pdf`
- Filename will be: `{YOUR_ID}.pdf` (e.g., `GRV-01K88MF7431X7NF9D4GHQN5742.pdf`)

**Important:** 
- Save your tracking ID! You'll need it to check your status.
- Tracking IDs are generated server-side for security
- Format: `GRV-` followed by 26 alphanumeric characters (30 chars total)

### What Information You'll See

The status display shows:

#### Status Information Section:
- **Status** - Current status (defaults to "Pending" if not set)
- **Note** - Status notes from case workers
- **Updated** - Last update timestamp (formatted as readable date/time)

#### Details Section:
- **Created** - Submission date and time (formatted as readable date/time)
- **Category** - Category type (e.g., "2.3 HH member not registered")
- **Type** - "Anonymous" or "Named"
- **Household ID*** - Household registration ID (if applicable)
- **Receipt.pdf** - Clickable link to download PDF receipt

#### Location Section*:
- **Island** - Island location
- **District** - District location
- **Village** - Village location

**Note:** Fields marked with * are only displayed for non-anonymous submissions. Anonymous submissions will see "Anonymous" as Type and won't see Household ID, Location, or email notification.

### Common Status Values

| Status | Meaning |
|--------|---------|
| **Pending** | Just submitted, awaiting review |
| **Under Review** | Being evaluated by case workers |
| **In Progress** | Action is being taken |
| **Resolved** | Issue has been addressed |
| **Closed** | Case is complete |

### Tips

- You can check your status as many times as you want
- Status updates appear immediately when you check
- Keep your tracking ID safe and confidential
- If you get an error, double-check your tracking ID is complete

### Troubleshooting

**Problem:** "I couldn't find that GRV reference"
- **Solution:** Make sure you entered the complete ID
- **Tip:** Paste the full ID starting with "GRV-"
- **Example:** `GRV-01K88MF7431X7NF9D4GHQN5742` (exactly 30 characters)

**Problem:** Invalid ID format error
- **Solution:** Check that your ID:
  - Starts with "GRV-"
  - Is exactly 30 characters long (GRV- + 26 alphanumeric characters)
  - Contains only uppercase letters and numbers after GRV-
  - Has no spaces or special characters

**Problem:** ID validation fails in Typebot
- **Solution:** The system validates using regex pattern `^GRV-[A-Z0-9]{26}$`
- If your ID doesn't match this exact pattern, it won't proceed to lookup

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

- **Full documentation:** [STATUS_CHECK_FEATURE.md](STATUS_CHECK_FEATURE.md)
- **Main README:** [../README.md](../README.md)
- **Test suite:** `backend/tests/test_status_check_flow.py`

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
- Review the full documentation in [STATUS_CHECK_FEATURE.md](STATUS_CHECK_FEATURE.md)
- Check the test suite for expected behavior
- Contact the development team for technical issues
