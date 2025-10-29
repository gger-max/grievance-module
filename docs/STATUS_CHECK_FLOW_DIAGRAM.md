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
│  │  👋 Welcome to the Grievance & Feedback system            │     │
│  │  What would you like to do today?                          │     │
│  │                                                             │     │
│  │  [ Submit a grievance? ]                                   │     │
│  │  [ Check status? ]         ◄─── USER SELECTS THIS        │     │
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
│  │ GET /api/grievances/   │  │      │  │ Please paste a full  │   │
│  │ {lookup_id}            │  │      │  │ GRV ID               │   │
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
│  │ STATUS:  │  │    │  │ I couldn't   │  │        │
│  │ Under    │  │    │  │ find that    │  │        │
│  │ Review   │  │    │  │ reference    │  │        │
│  │          │  │    │  │              │  │        │
│  │ DETAILS  │  │    │  │ [ Try again ]│  │        │
│  │ ...      │  │    │  └──────────────┘  │        │
│  └──────────┘  │    └─────────┬──────────┘        │
└────┬───────────┘              │                   │
     │                           │                   │
     │                           └───────────────────┘
     │                                   │
     │                           ┌───────▼────────┐
     └──────────────────────────▶│  RE-ENTER ID   │
                                 │  OR EXIT       │
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
   GRV-123 (too short)
   │
   ├─▶ Typebot regex validation fails
   └─▶ Error: "Please paste a full GRV ID"
       └─▶ Return to input prompt

2. GRIEVANCE NOT FOUND
   │
   GRV-01K88INVALID0000000000
   │
   ├─▶ Typebot validation passes
   ├─▶ API call made
   ├─▶ Database returns null
   └─▶ API returns 404
       └─▶ Error: "I couldn't find that reference"
           └─▶ Return to input prompt

3. SYSTEM TEMPORARILY UNAVAILABLE
   │
   API connection timeout
   │
   ├─▶ Network/server issue
   ├─▶ No response received
   └─▶ Error: "Our system is busy right now"
       └─▶ Wait 60 seconds
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
│  │ ✅ id                 │  │
│  │ ✅ external_status    │  │
│  │ ✅ category_type      │  │
│  │ ✅ island, details    │  │
│  │ ❌ complainant_name   │  │
│  │ ❌ complainant_email  │  │
│  │ ❌ complainant_phone  │  │
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
│  │ ✅ id                 │  │
│  │ ✅ external_status    │  │
│  │ ✅ category_type      │  │
│  │ ✅ island, details    │  │
│  │ ✅ complainant_name   │  │
│  │ ✅ complainant_email  │  │
│  │ ✅ complainant_phone  │  │
│  └───────────────────────┘  │
└─────────────────────────────┘
```

---

## Key Components

### Typebot Groups (from JSON config)
- `efypu2p9ta19ka6j7wjh58jy` - Welcome screen with options
- `zyx72qhxfuz2eg8l4l4wxvdt` - Status lookup (ID input)
- `tw52lmlbc9nuvs2ei1gy428f` - Fetch grievance (API webhook)
- `t7lcrwdj8j93dwmyohmb72h4` - Route lookup (response handling)
- `rs3ppgp6g8pim55rwigako4u` - Show status (display block)
- `gjuezqnqlpvn34k5qzj8pr4p` - Not found error
- `znbo90i4kdy2zsid50epuzv2` - Invalid ID error
- `xyuyggayijho4c468yfxhg4i` - Temporary error

### Backend Components
- **Router**: `app/routers/grievances.py`
- **Endpoint**: `get_grievance(gid: str, db: Session)`
- **Model**: `models.Grievance`
- **Schema**: `schemas.GrievancePublic`
- **Database**: PostgreSQL table `grievance`

### Test Coverage
- `test_status_check_flow.py` - 6 comprehensive tests
- `test_typebot_integration.py` - 3 status lookup tests
- `test_grievances.py` - Core retrieval tests

---

**Legend**
- `│` Flow direction
- `▼` Process continues
- `◀─▶` Bidirectional communication
- `──▶` Request/Response
- `✅` Field included in response
- `❌` Field excluded (privacy)
