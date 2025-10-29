# Solution: Display Grievance ID to Users

## Problem
Typebot webhooks cannot access response body/headers, making it impossible to capture the server-generated grievance ID.

## Solution
Generate the grievance ID **client-side** in Typebot BEFORE submitting, then pass it to the API.

## Implementation Steps

### 1. Add ID Generation Block in Typebot Builder

**Location**: Add this BEFORE the "Send to Backend" webhook block

**Block Type**: "Set variable"

**Variable to set**: `grievance_id`

**Value (JavaScript code)**:
```javascript
// ULID-compatible ID generator
(function() {
    const ENCODING = '0123456789ABCDEFGHJKMNPQRSTVWXYZ';
    const now = Date.now();
    
    // Timestamp component (10 chars)
    let timeString = '';
    let timeValue = now;
    for (let i = 0; i < 10; i++) {
        timeString = ENCODING[timeValue % 32] + timeString;
        timeValue = Math.floor(timeValue / 32);
    }
    
    // Random component (16 chars)
    let randomString = '';
    for (let i = 0; i < 16; i++) {
        randomString += ENCODING[Math.floor(Math.random() * 32)];
    }
    
    return 'GRV-' + timeString + randomString;
})()
```

### 2. Update Webhook Body

In the "Send to Backend" webhook block, **add the `id` field**:

```json
{
  "id": "{{grievance_id}}",
  "is_anonymous": true,
  "grievance_details": "{{grievance_details}}",
  "attachments": []
}
```

### 3. Display the ID

In confirmation blocks, use:
```
Your grievance has been submitted successfully!

Tracking ID: {{grievance_id}}

Please save this ID to check the status of your grievance.
```

## How It Works

1. **Typebot generates the ID** using JavaScript (compatible with Python's ULID format)
2. **ID is stored** in the `grievance_id` variable
3. **ID is sent to API** in the webhook payload
4. **API validates and uses** the client-provided ID
5. **Typebot displays** the ID from its own variable (no response parsing needed)

## Testing

API has been updated to:
- Accept optional `id` field in `GrievanceCreate` schema
- Validate the ID format (GRV-{26 uppercase alphanumeric})
- Use client ID if valid, otherwise generate server-side
- Return the same ID in the response

## Benefits

- ✅ No dependency on webhook response capture
- ✅ Works with any Typebot version
- ✅ IDs are ULID-compatible (sortable, timestamp-based)
- ✅ Fallback to server generation if client ID is invalid
- ✅ Anonymous users can track their grievances

## Files Modified

- `backend/app/schemas.py`: Added optional `id` field to `GrievanceCreate`
- `backend/app/routers/grievances.py`: Updated to use client-provided ID
- `backend/app/main.py`: Simplified CORS middleware (removed complex response parsing)
