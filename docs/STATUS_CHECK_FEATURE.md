# Grievance Status Check Feature

## Overview

The Grievance Management System provides a comprehensive status check feature that allows users to track their submitted grievances using their unique reference ID. This feature is fully integrated with the Typebot chatbot interface and accessible via the REST API.

## User Flow

### From Typebot Interface

1. **Welcome Screen**
   - User is presented with two options:
     - "Submit a grievance?"
     - "Check status?"

2. **Status Check Selection**
   - When user selects "Check status?", they are prompted to enter their reference ID

3. **ID Validation**
   - The system validates the ID format using regex: `^GRV-[A-Z0-9]{26}$`
   - Valid IDs are 30 characters long: "GRV-" prefix + 26-character ULID
   - Invalid formats are rejected with a helpful error message

4. **Status Display**
   - Upon successful lookup, the system displays:
     - **Status Information**
       - Current status (e.g., "Pending", "Under Review", "Resolved")
       - Status notes from case workers
       - Submission date/time
     - **Location Details**
       - Island
       - District
       - Village
     - **Case Details**
       - Category type
       - Whether it's anonymous or named
       - Household ID (if registered)

5. **Next Actions**
   - User can check another grievance ID
   - User can exit the chatbot

## API Endpoint

### Get Grievance by ID

**Endpoint:** `GET /api/grievances/{gid}`

**Parameters:**
- `gid` (path parameter): The grievance reference ID (e.g., "GRV-01K88MF7431X7NF9D4GHQN5742")

**Response (200 OK):**
```json
{
  "id": "GRV-01K88MF7431X7NF9D4GHQN5742",
  "created_at": "2025-10-23T10:30:00Z",
  "updated_at": "2025-10-23T10:30:00Z",
  "external_status": "Under Review",
  "external_status_note": "Case assigned to social worker",
  "is_anonymous": false,
  "complainant_name": "John Doe",
  "complainant_email": "john@example.com",
  "complainant_phone": "+676123456",
  "complainant_gender": "Male",
  "is_hh_registered": true,
  "hh_id": "HH2024001",
  "hh_address": "123 Main Street",
  "island": "Tarawa",
  "district": "South Tarawa",
  "village": "Bairiki",
  "category_type": "Service Delivery",
  "details": "Description of the grievance",
  "attachments": [
    {
      "name": "document.pdf",
      "url": "https://storage.example.com/document.pdf",
      "size": 256000,
      "type": "application/pdf"
    }
  ]
}
```

**Error Responses:**

- **404 Not Found:** When the grievance ID doesn't exist
  ```json
  {
    "detail": "Not found"
  }
  ```

## Privacy Considerations

### Anonymous Grievances

When a grievance is marked as anonymous (`is_anonymous: true`):
- Personal information fields return `null`:
  - `complainant_name`
  - `complainant_email`
  - `complainant_phone`
  - `complainant_gender`
- The tracking ID is still functional
- Location and category information is still visible
- Status updates are still accessible

### Named Grievances

When a grievance is not anonymous (`is_anonymous: false`):
- All submitted information is returned
- Personal details are visible to anyone with the tracking ID
- Users should be advised to keep their tracking ID confidential

## Status Updates

### Status Flow

Grievances typically follow this status progression:

1. **Pending** (default) - Just submitted, awaiting review
2. **Under Review** - Being evaluated by case workers
3. **In Progress** - Action is being taken
4. **Resolved** - Issue has been addressed
5. **Closed** - Case is complete

### Update Sources

Status updates can come from:
- **External Systems** (e.g., Odoo): Case workers update status through their management system
- **Authenticated API Calls**: Using the `/api/status/{gid}/status` endpoint with Bearer token authentication

### Real-time Updates

- Status changes are immediately visible when users check their grievance
- No caching is applied to status information
- Users can check status as many times as needed

## ID Format and Generation

### Reference ID Structure

- **Prefix:** `GRV-` (identifies this as a grievance)
- **Unique Identifier:** 26-character ULID (Universally Unique Lexicographically Sortable Identifier)
- **Total Length:** 30 characters
- **Example:** `GRV-01K88MF7431X7NF9D4GHQN5742`

### ULID Benefits

- **Sortable:** IDs are naturally time-ordered
- **Unique:** Collision-free across distributed systems
- **Readable:** Uses Crockford's Base32 encoding (no ambiguous characters like 0/O or 1/I/L)
- **Compact:** More efficient than UUIDs

## Error Handling

### Invalid ID Format

Typebot validates the ID format before making the API call:
- Must start with "GRV-"
- Must be exactly 30 characters long
- Must contain only uppercase letters and numbers in the ULID portion

If validation fails, users see:
- Error message: "Please paste a full GRV ID"
- Option to try again
- Returns to ID input prompt

### Grievance Not Found

If the API returns 404 (grievance doesn't exist):
- Error message: "I couldn't find that reference. Please ensure it starts with GRV- and paste the full ID."
- Option to try again
- Returns to ID input prompt

### Temporary System Issues

If the API is temporarily unavailable:
- Error message: "Our system is busy right now. Please try again in a minute."
- 60-second wait period
- Option to retry

## Technical Implementation

### Typebot Configuration

The status check flow is implemented in the Typebot configuration file:
- **File:** `frontend-typebot/typebot-export-grievance-intake-qwdn4no.json`
- **Groups:**
  - `zyx72qhxfuz2eg8l4l4wxvdt` - Status lookup (ID input and validation)
  - `tw52lmlbc9nuvs2ei1gy428f` - Fetch Grievance (API call)
  - `t7lcrwdj8j93dwmyohmb72h4` - Route lookup (handle response)
  - `rs3ppgp6g8pim55rwigako4u` - Show status (display information)

### Backend Implementation

- **Router:** `backend/app/routers/grievances.py`
- **Endpoint Function:** `get_grievance(gid: str, db: Session)`
- **Response Model:** `GrievancePublic` (defined in `backend/app/schemas.py`)
- **Database Model:** `Grievance` (defined in `backend/app/models.py`)

### Database Schema

Relevant fields for status checking:
```sql
CREATE TABLE grievance (
    id VARCHAR PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    external_status VARCHAR,
    external_status_note TEXT,
    external_updated_at TIMESTAMP WITH TIME ZONE,
    is_anonymous BOOLEAN NOT NULL,
    -- ... other fields
);
```

## Testing

Comprehensive test coverage is provided in:
- `backend/tests/test_status_check_flow.py` - Full status check flow tests
- `backend/tests/test_typebot_integration.py` - Typebot-specific integration tests
- `backend/tests/test_grievances.py` - Core grievance retrieval tests

### Test Coverage

The test suite verifies:
- ✅ Complete status check flow from submission to lookup
- ✅ Status updates by external systems
- ✅ Anonymous grievance privacy protection
- ✅ Invalid ID format handling
- ✅ Multiple status checks for same grievance
- ✅ Household information display
- ✅ 404 error handling for non-existent IDs
- ✅ Proper response structure and field presence

## Usage Examples

### Example 1: Basic Status Check

User submits a grievance and receives: `GRV-01K88MF7431X7NF9D4GHQN5742`

Later, they return to check status:
1. Select "Check status?"
2. Enter: `GRV-01K88MF7431X7NF9D4GHQN5742`
3. See current status: "Under Review"
4. See note: "Case assigned to social worker"

### Example 2: Anonymous Status Check

Anonymous user receives: `GRV-01K89ABC123XYZ789DEF456GH`

When checking status:
- Status and notes are visible
- No personal information is displayed
- Location and category are shown

### Example 3: Tracking Progress

User checks status multiple times:
- **Day 1:** Status shows "Pending"
- **Day 3:** Status shows "Under Review"
- **Day 7:** Status shows "Resolved" with resolution notes

## Best Practices

### For Users

1. **Save Your Reference ID**
   - Screenshot the confirmation message
   - Write down the full ID
   - Save the receipt PDF

2. **Check Regularly**
   - Status can be checked multiple times
   - No limit on lookup frequency
   - Updates appear immediately

3. **Keep ID Confidential**
   - Don't share your ID publicly
   - Anyone with the ID can view your grievance details
   - Especially important for non-anonymous submissions

### For Administrators

1. **Update Status Regularly**
   - Keep users informed of progress
   - Add meaningful status notes
   - Use clear, user-friendly language

2. **Use Standard Status Values**
   - Maintain consistency across cases
   - Use predefined status options when available
   - Document custom status meanings

3. **Monitor Status Check Usage**
   - Track how often users check status
   - Identify cases needing updates
   - Use analytics to improve communication

## Future Enhancements

Potential improvements to consider:

1. **Email Notifications**
   - Automatic emails when status changes
   - Configurable notification preferences
   - Link to status check in email

2. **Status History**
   - Timeline of all status changes
   - Audit trail of updates
   - Duration in each status

3. **Estimated Resolution Time**
   - Predictive timeline based on category
   - Average resolution times
   - SLA tracking

4. **SMS Status Updates**
   - Text message notifications
   - Direct link to status check
   - Support for users without email

## Support

For issues or questions about the status check feature:
- Review the test suite for expected behavior
- Check API logs for debugging
- Consult the main README.md for system architecture
- Contact the development team
