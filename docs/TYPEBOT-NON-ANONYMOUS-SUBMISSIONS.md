# Non-Anonymous Grievance Submissions from Typebot

## Overview

The Grievance Management System fully supports both **anonymous** and **non-anonymous** grievance submissions through Typebot. Users can choose whether to provide their personal information when submitting a grievance.

## How It Works

### 1. Anonymous Flow (is_anonymous = true)

When a user chooses to remain anonymous:
- Typebot skips collecting complainant information
- User proceeds directly to entering grievance details
- No personal information is stored
- Tracking ID is still provided for status lookups

### 2. Non-Anonymous Flow (is_anonymous = false)

When a user chooses NOT to remain anonymous:
- Typebot collects:
  - Full name (required)
  - Email address (optional)
  - Phone number (optional)
  - Gender (optional)
  - Household registration info (optional)
  - Household ID and address (if registered)
- All information is stored with the grievance
- User receives email confirmation (if email provided)

## Empty String Handling

### The Challenge

Typebot sends empty fields as **empty strings** (`""`) rather than `null`, which can cause validation issues, especially for email fields.

### The Solution

The backend automatically converts empty strings to `null` for all optional fields:

```python
# Example: What Typebot sends
{
  "is_anonymous": false,
  "complainant_name": "John Doe",
  "complainant_email": "",      # Empty string - would fail validation
  "complainant_phone": "+676123456",
  "grievance_details": "Need help"
}

# After backend processing
{
  "is_anonymous": false,
  "complainant_name": "John Doe",
  "complainant_email": null,    # Converted to null - passes validation
  "complainant_phone": "+676123456",
  "grievance_details": "Need help"
}
```

### Affected Fields

Empty strings are automatically converted to `null` for:
- `complainant_name`
- `complainant_email` ⚠️ (critical - prevents EmailStr validation errors)
- `complainant_phone`
- `complainant_gender`
- `hh_id`
- `hh_address`
- `island`
- `district`
- `village`
- `category_type`
- `details` / `grievance_details`

## Webhook Payload Example

### Non-Anonymous Submission (typical)

```json
{
  "is_anonymous": false,
  "complainant_name": "Maria Garcia",
  "complainant_email": "maria@example.com",
  "complainant_phone": "+676789012",
  "complainant_gender": "Female",
  "is_hh_registered": true,
  "hh_id": "HH2024123",
  "hh_address": "Village Center, Island",
  "island": "Tongatapu",
  "district": "",
  "village": "Nuku'alofa",
  "category_type": "",
  "grievance_details": "I need help with housing assistance",
  "grievance_details_attachment_friendly": "",
  "attachments": null
}
```

### Anonymous Submission

```json
{
  "is_anonymous": true,
  "complainant_name": "",
  "complainant_email": "",
  "complainant_phone": "",
  "complainant_gender": "",
  "is_hh_registered": null,
  "hh_id": "",
  "hh_address": "",
  "grievance_details": "Anonymous complaint about service delays",
  "attachments": null
}
```

## API Response

After successful submission, the API returns the created grievance with a tracking ID:

```json
{
  "id": "GRV-01K88MF7431X7NF9D4GHQN5742",
  "created_at": "2025-10-23T21:30:00.000Z",
  "updated_at": "2025-10-23T21:30:00.000Z",
  "is_anonymous": false,
  "complainant_name": "Maria Garcia",
  "complainant_email": "maria@example.com",
  "complainant_phone": "+676789012",
  "complainant_gender": "Female",
  "is_hh_registered": true,
  "hh_id": "HH2024123",
  "hh_address": "Village Center, Island",
  "island": "Tongatapu",
  "district": null,
  "village": "Nuku'alofa",
  "category_type": null,
  "details": "I need help with housing assistance",
  "attachments": null,
  "external_status": null,
  "external_status_note": null
}
```

## Confirmation Flow in Typebot

After webhook submission:

1. **Set Grievance ID**: `{{response.body.id}}` is captured
2. **Conditional Display**: Different confirmation messages for anonymous vs. non-anonymous
3. **Email Receipt**: If email provided and is non-anonymous, send confirmation email
4. **Display Links**:
   - Status tracking: `/api/grievances/{{grievance_id}}`
   - PDF receipt: `/api/grievances/{{grievance_id}}/receipt.pdf`

## Testing

### Running Tests

```bash
cd backend
pytest tests/test_empty_string_handling.py -v
pytest tests/test_typebot_integration.py -v
```

### Test Coverage

✅ **52 tests passing** including:
- Empty string conversion to null
- Non-anonymous with missing email
- Mixed empty and filled fields
- Anonymous with all empty fields
- Realistic Typebot payload scenarios
- Email validation for valid addresses

## Common Scenarios

### User provides name only
```json
{
  "is_anonymous": false,
  "complainant_name": "John Doe",
  "complainant_email": "",
  "complainant_phone": "",
  "grievance_details": "Issue description"
}
```
✅ **Works** - Empty email/phone converted to null

### User provides name and phone, skips email
```json
{
  "is_anonymous": false,
  "complainant_name": "Jane Smith",
  "complainant_email": "",
  "complainant_phone": "+676123456",
  "grievance_details": "Issue description"
}
```
✅ **Works** - Empty email converted to null, phone retained

### User provides all information
```json
{
  "is_anonymous": false,
  "complainant_name": "Bob Johnson",
  "complainant_email": "bob@example.com",
  "complainant_phone": "+676987654",
  "complainant_gender": "Male",
  "grievance_details": "Issue description"
}
```
✅ **Works** - All data retained as provided

## Benefits

1. **Flexible Data Collection**: Users can skip optional fields without errors
2. **Email Validation**: Empty strings won't trigger email format validation
3. **Clean Data Storage**: `null` values instead of empty strings in database
4. **Backward Compatible**: Existing payloads with `null` still work
5. **User-Friendly**: No forced fields beyond the minimum required

## Technical Implementation

See `backend/app/schemas.py` - `GrievanceCreate.convert_empty_strings_to_none()` validator.

```python
@model_validator(mode='before')
@classmethod
def convert_empty_strings_to_none(cls, data: Any) -> Any:
    """
    Convert empty strings to None for optional fields.
    This handles Typebot's behavior of sending empty strings 
    instead of null/undefined.
    """
    if isinstance(data, dict):
        string_fields = [
            'complainant_name', 'complainant_email', 'complainant_phone',
            'complainant_gender', 'hh_id', 'hh_address', 'island',
            'district', 'village', 'category_type', 'details',
            'grievance_details', 'grievance_details_attachment_friendly'
        ]
        
        for field in string_fields:
            if field in data and data[field] == '':
                data[field] = None
    
    return data
```

## Troubleshooting

### Issue: "value is not a valid email address"

**Cause**: Typebot sending empty string for email field

**Solution**: ✅ Fixed - Empty strings are now automatically converted to `null`

### Issue: Database stores empty strings

**Cause**: Old backend version without empty string conversion

**Solution**: ✅ Fixed - All empty strings converted to `null` before storage

## Related Files

- `backend/app/schemas.py` - Schema validation with empty string handling
- `backend/app/routers/grievances.py` - Grievance creation endpoint
- `backend/tests/test_empty_string_handling.py` - Test suite for empty strings
- `backend/tests/test_typebot_integration.py` - Full Typebot integration tests
- `frontend-typebot/typebot-export-grievance-intake-qwdn4no.json` - Typebot flow configuration
