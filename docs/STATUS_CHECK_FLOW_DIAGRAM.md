# Status Check Flow Diagram

## User Journey: Checking Grievance Status

```
┌─────────────────────────────────────────────────────────────────────┐
│                     USER OPENS TYPEBOT CHATBOT                      │
└─────────────────────┬───────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      WELCOME SCREEN                                 │
│  ┌───────────────────────────────────────────────────────────┐     │
│  │  Welcome to the Grievance & Feedback system               │     │
│  │  What would you like to do today?                          │     │
│  │                                                             │     │
│  │  [ Submit a grievance ]                                    │     │
│  │  [ Check the status of a grievance ]  ◄─── USER SELECTS  │     │
│  └───────────────────────────────────────────────────────────┘     │
└─────────────────────┬───────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    STATUS LOOKUP - ID INPUT                         │
│  ┌───────────────────────────────────────────────────────────┐     │
│  │  Please enter your reference ID (e.g., GRV-01ABC…):       │     │
│  │  ┌────────────────────────────────────────────┐           │     │
│  │  │ GRV-01K88MF7431X7NF9D4GHQN5742            │           │     │
│  │  └────────────────────────────────────────────┘           │     │
│  └───────────────────────────────────────────────────────────┘     │
└─────────────────────┬───────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      ID FORMAT VALIDATION                           │
│  ┌───────────────────────────────────────────────────────────┐     │
│  │  Regex Check: ^GRV-[A-Z0-9]{26}$                          │     │
│  │  - Must start with "GRV-"                                  │     │
│  │  - Must be exactly 30 characters                           │     │
│  │  - ULID must be 26 uppercase alphanumeric characters      │     │
│  └───────────────────────────────────────────────────────────┘     │
└─────┬────────────────────────────────────────────────┬──────────────┘
      │ VALID                                          │ INVALID
      ▼                                                ▼
┌──────────────────────────────┐      ┌─────────────────────────────┐
│   FETCH GRIEVANCE            │      │   ERROR MESSAGE             │
│  ┌────────────────────────┐  │      │  ┌──────────────────────┐   │
│  │ GET /api/grievances/   │  │      │  │ Validation failed    │   │
│  │ {lookup_id}            │  │      │  │ (handled by Typebot) │   │
│  │                        │  │      │  │                      │   │
│  │ Server: grievance-api  │  │      │  │ [ Try again ]        │   │
│  │ Port: 8000             │  │      │  └──────────────────────┘   │
│  └────────────────────────┘  │      └─────────────┬───────────────┘
└───────┬──────────────────────┘                    │
        │                                            │
        ▼                                            │
┌──────────────────────────────┐                    │
│   API RESPONSE ROUTING       │                    │
└───┬──────────────────────┬───┘                    │
    │ 200 OK               │ 404 NOT FOUND          │
    ▼                      ▼                         │
┌────────────────┐    ┌────────────────────┐        │
│  SHOW STATUS   │    │  NOT FOUND ERROR   │        │
│  ┌──────────┐  │    │  ┌──────────────┐  │        │
│  │ Status   │  │    │  │ I couldn't   │  │        │
│  │ Info:    │  │    │  │ find that    │  │        │
│  │ - Status │  │    │  │ GRV reference│  │        │
│  │ - Note   │  │    │  │              │  │        │
│  │ - Updated│  │    │  │ [ Try again ]│  │        │
│  │          │  │    │  └──────────────┘  │        │
│  │ Details: │  │    └─────────┬──────────┘        │
│  │ - Created│  │              │                   │
│  │ - Category│ │              │                   │
│  │ - Type   │  │              │                   │
│  │ - PDF    │  │              │                   │
│  │          │  │              │                   │
│  │ Location*│  │              │                   │
│  └──────────┘  │              │                   │
└────┬───────────┘              │                   │
     │                           │                   │
     │                           └───────────────────┘
     │                                   │
     │                           ┌───────▼────────┐
     └──────────────────────────▶│ Check another  │
                                 │ or Done        │
                                 └────────────────┘
```

## System Architecture Flow

```
┌──────────────────────────────────────────────────────────────────┐
│                         COMPONENTS                               │
└──────────────────────────────────────────────────────────────────┘

┌─────────────┐          ┌─────────────┐          ┌──────────────┐
│   TYPEBOT   │  HTTP    │  FASTAPI    │   SQL    │  POSTGRESQL  │
│   VIEWER    │ ──────▶  │     API     │ ◀─────▶  │   DATABASE   │
│             │          │             │          │              │
│  Port 8082  │          │  Port 8000  │          │  Port 5432   │
└─────────────┘          └─────────────┘          └──────────────┘
      │                         │
      │                         │
      ▼                         ▼
  User inputs           GET /api/grievances/{id}
  GRV-01K...            ↓
      │                 Fetch from database
      │                 ↓
      └────────────────▶ Return GrievancePublic
                        {
                          id, status, details,
                          location, timestamps...
                        }
```

## Data Flow: Status Check

```
1. USER ACTION
   │
   ├─▶ Opens Typebot chatbot
   ├─▶ Selects "Check status?"
   └─▶ Enters tracking ID: GRV-01K88MF7431X7NF9D4GHQN5742
       │
       ▼
2. TYPEBOT VALIDATION
   │
   ├─▶ Regex validation: ^GRV-[A-Z0-9]{26}$
   ├─▶ Format check passed
   └─▶ Prepare webhook request
       │
       ▼
3. API REQUEST
   │
   ├─▶ Method: GET
   ├─▶ URL: http://grievance-api:8000/api/grievances/{id}
   ├─▶ Headers: Content-Type: application/json
   └─▶ No authentication required (public endpoint)
       │
       ▼
4. BACKEND PROCESSING
   │
   ├─▶ Route: grievances.py::get_grievance()
   ├─▶ Extract gid from path parameter
   ├─▶ Query database: db.get(models.Grievance, gid)
   └─▶ Check if grievance exists
       │
       ├─ Found ──────────────────┐
       │                          │
       └─ Not Found               │
          │                       │
          ▼                       ▼
    404 Response         200 Response
    {                    {
      "detail":            "id": "GRV-...",
      "Not found"          "external_status": "Under Review",
    }                      "external_status_note": "...",
          │                "created_at": "2025-10-23...",
          │                "island": "Tarawa",
          │                "category_type": "Service Delivery",
          │                ...
          │              }
          │                       │
          ▼                       ▼
5. TYPEBOT RESPONSE HANDLING
   │
   ├─▶ Parse response.status
   ├─▶ Route based on status code
   │   ├─ 200 → Show status block
   │   └─ 404 → Show not found error
   │
   └─▶ Display formatted information to user
       │
       ▼
6. USER SEES RESULT
   │
   ├─▶ Status information displayed
   ├─▶ Options: Check another | Done
   └─▶ Can repeat process or exit
```

## Error Handling Flow

```
┌─────────────────────────────────────────────────────────┐
│                    ERROR SCENARIOS                      │
└─────────────────────────────────────────────────────────┘

1. INVALID FORMAT
   │
   GRV-123 (too short) or invalid characters
   │
   ├─▶ Typebot regex validation fails
   └─▶ Error handled inline by Typebot
       └─▶ Return to input prompt

2. GRIEVANCE NOT FOUND
   │
   GRV-01K88INVALID0000000000
   │
   ├─▶ Typebot validation passes (format is correct)
   ├─▶ API call made
   ├─▶ Database returns null
   └─▶ API returns 404
       └─▶ Error: "I couldn't find that GRV reference"
           └─▶ Return to input prompt
```

## Status Update Integration

```
┌─────────────────────────────────────────────────────────┐
│           EXTERNAL SYSTEM STATUS UPDATES                │
└─────────────────────────────────────────────────────────┘

ODOO (Case Management)
      │
      │ PUT /api/status/{gid}/status
      │ Authorization: Bearer {token}
      ▼
┌──────────────────┐
│  Status API      │
│  (Authenticated) │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Update Database │
│  - external_     │
│    status        │
│  - external_     │
│    status_note   │
│  - external_     │
│    updated_at    │
└────────┬─────────┘
         │
         ▼
     USER CHECKS STATUS
         │
         ▼
   Updated info displayed
```

## Privacy Protection Flow

```
ANONYMOUS SUBMISSION
      │
      ├─▶ is_anonymous: true
      │
      ▼
┌─────────────────────────────┐
│  Status Check Response      │
│  ┌───────────────────────┐  │
│  │ id                    │  │
│  │ external_status       │  │
│  │ category_type         │  │
│  │ island, details       │  │
│  │ complainant_name: null│  │
│  │ complainant_email:null│  │
│  │ complainant_phone:null│  │
│  └───────────────────────┘  │
└─────────────────────────────┘

NAMED SUBMISSION
      │
      ├─▶ is_anonymous: false
      │
      ▼
┌─────────────────────────────┐
│  Status Check Response      │
│  ┌───────────────────────┐  │
│  │ id                    │  │
│  │ external_status       │  │
│  │ category_type         │  │
│  │ island, details       │  │
│  │ complainant_name      │  │
│  │ complainant_email     │  │
│  │ complainant_phone     │  │
│  └───────────────────────┘  │
└─────────────────────────────┘
```

---

## Key Components

### Typebot Groups (from JSON config)
- "Welcome" - Welcome screen with options
- "Check Status" - ID input and validation
- "Show status" - Display formatted status information
- "Not found" - Error handling for non-existent IDs

**Note:** Specific group IDs in the Typebot JSON may change when reimporting. Refer to group titles for identification.

### Backend Components
- **Router**: `app/routers/grievances.py`
- **Endpoint**: `get_grievance(gid: str, db: Session)`
- **Model**: `models.Grievance`
- **Schema**: `schemas.GrievancePublic`
- **Database**: PostgreSQL table `grievance`

### Test Coverage
- `test_status_check_flow.py` - Status check flow tests
- `test_typebot_integration.py` - Typebot integration tests
- `test_grievances.py` - Core retrieval tests
- **Total:** 118 tests (117 passing + 1 skipped)

---

**Legend**
- `│` Flow direction
- `▼` Process continues
- `◀─▶` Bidirectional communication
- `──▶` Request/Response
- `*` Field only for non-anonymous submissions
