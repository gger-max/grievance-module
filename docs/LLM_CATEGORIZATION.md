# LLM-Based Grievance Categorization

This document describes the LLM-powered automatic categorization feature for grievances in the Vaka Sosiale Grievance Management System.

## Overview

The system uses OpenAI's GPT models to automatically categorize grievances based on the details provided by complainants. This helps streamline the grievance processing workflow by suggesting appropriate categories before submission to Odoo.

## Categories

The system supports the following Vaka Sosiale categories:

### 1. Inquiries and suggestions
- **1.1** Inquiries
- **1.2** Suggestions/feedback

### 2. Registration related
- **2.1** HH not registered - not informed
- **2.2** HH not registered - could not attend
- **2.3** HH member not registered
- **2.4** Request to update data

### 3. Socioeconomic (PMT classification)
- **3.1** Poor/vulnerable excluded
- **3.2** Non-poor included
- **3.3** HH not registered

### 4. Misbehavior of registrant
- **4.1** Fraud (false information)
- **4.2** Discourtesy

### 5. Staff performance
- **5.1** Fraud
- **5.2** Inaction to requests
- **5.3** Discourtesy or poor service
- **5.4** Collection of any kind

### 6. Gender-based violence
- **6.1** Sexual exploitation and abuse
- **6.2** Sexual harassment

### 7. Others (please describe)
- For grievances that don't fit into other categories

## Configuration

### Environment Variables

Add these variables to your `.env` file:

```bash
# OpenAI API Configuration
OPENAI_API_KEY=your-api-key-here
OPENAI_MODEL=gpt-4o-mini  # Optional, defaults to gpt-4o-mini
```

### Supported Models

The service supports any OpenAI chat completion model, including:
- `gpt-4o-mini` (recommended, cost-effective)
- `gpt-4o`
- `gpt-4-turbo`
- `gpt-3.5-turbo`

## API Endpoint

### POST `/api/grievances/categorize/`

Categorize grievance details using an LLM.

#### Request Body

```json
{
  "details": "My household member was not registered during enrollment even though they live with us."
}
```

**Fields:**
- `details` (string, required): The grievance description text (minimum 1 character)

#### Response

```json
{
  "category": "2",
  "subcategory": "2.3",
  "category_name": "Registration related",
  "subcategory_name": "HH member not registered",
  "confidence": "high",
  "reasoning": "The grievance clearly states that a household member was not registered during the enrollment process.",
  "display": "2.3 HH member not registered"
}
```

**Response Fields:**
- `category` (string): Main category number (1-7)
- `subcategory` (string|null): Subcategory code (e.g., "2.3") or null for category 7
- `category_name` (string): Human-readable category name
- `subcategory_name` (string|null): Human-readable subcategory name
- `confidence` (string): Confidence level - "high", "medium", or "low"
- `reasoning` (string): Brief explanation for the categorization
- `display` (string): Formatted display string for UI presentation

#### Error Responses

**400 Bad Request** - Invalid input
```json
{
  "detail": "Grievance details cannot be empty"
}
```

**422 Unprocessable Entity** - Validation error
```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "details"],
      "msg": "String should have at least 1 character"
    }
  ]
}
```

**500 Internal Server Error** - LLM service error
```json
{
  "detail": "LLM service error: API connection failed"
}
```

## Usage Examples

### cURL

```bash
curl -X POST "http://localhost:8000/api/grievances/categorize/" \
  -H "Content-Type: application/json" \
  -d '{"details": "The staff was very rude to me when I asked for help"}'
```

### Python

```python
import requests

response = requests.post(
    "http://localhost:8000/api/grievances/categorize/",
    json={"details": "The staff was very rude to me when I asked for help"}
)

result = response.json()
print(f"Category: {result['display']}")
print(f"Confidence: {result['confidence']}")
print(f"Reasoning: {result['reasoning']}")
```

### JavaScript/TypeScript (Typebot)

```javascript
// In Typebot Script block
const response = await fetch('http://localhost:8000/api/grievances/categorize/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    details: grievanceDetails
  })
});

const result = await response.json();
setVariable('category', result.category);
setVariable('subcategory', result.subcategory);
setVariable('category_display', result.display);
```

## Integration Workflow

### Recommended Flow

1. **Collect grievance details** from the complainant via Typebot
2. **Call categorization endpoint** with the details
3. **Present suggested category** to the complainant for confirmation
4. **Allow manual override** if the complainant disagrees
5. **Submit grievance** with the final category to the backend

### Example Typebot Integration

```
┌─────────────────────────────────────┐
│ Collect Grievance Details          │
│ (Text input)                        │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Script: Call Categorization API     │
│ Store result in variables           │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Display: "We categorized this as:   │
│ {{category_display}}"                │
│ "Is this correct?"                  │
└──────────────┬──────────────────────┘
               │
         ┌─────┴─────┐
         │           │
         ▼           ▼
      [Yes]       [No, let me choose]
         │           │
         │           ▼
         │    ┌────────────────┐
         │    │ Show category  │
         │    │ selection menu │
         │    └────────────────┘
         │           │
         └───────┬───┘
                 │
                 ▼
         ┌───────────────┐
         │ Webhook: POST │
         │ /api/grievances│
         └───────────────┘
```

## Error Handling

The service implements robust error handling:

### Fallback Behavior

If the LLM service fails for any reason (API error, invalid response, etc.), the system automatically:
1. Logs the error
2. Returns category "7" (Others)
3. Sets confidence to "low"
4. Provides a descriptive error message in the reasoning field

### Common Issues

| Issue | Solution |
|-------|----------|
| Missing API Key | Set `OPENAI_API_KEY` environment variable |
| Invalid API Key | Check key validity in OpenAI dashboard |
| Rate Limiting | Implement request queuing or use a higher tier API key |
| Network Errors | Service returns fallback category (7) |
| Invalid JSON Response | Service returns fallback category (7) |

## Performance Considerations

### Response Times

- **Average**: 1-3 seconds per categorization
- **Max**: 10 seconds (API timeout)

### Cost Optimization

Using `gpt-4o-mini` (recommended):
- **Cost**: ~$0.0001-0.0002 per categorization
- **Quality**: High accuracy for categorization tasks
- **Speed**: Fast response times

### Caching Recommendations

For production deployments, consider:
1. Caching common grievance patterns
2. Rate limiting categorization requests
3. Batching requests during high traffic

## Testing

### Running Tests

```bash
cd backend
OPENAI_API_KEY=test-key pytest tests/test_categorization.py -v
```

### Test Coverage

The test suite includes:
- ✅ All 7 main categories
- ✅ Various subcategories
- ✅ Error handling scenarios
- ✅ Edge cases (invalid JSON, missing keys)
- ✅ Validation tests (empty details, missing fields)
- ✅ Fallback behavior

**Total**: 14 comprehensive tests, all passing

## Security Considerations

### API Key Security

- **Never commit** API keys to version control
- Store keys in environment variables only
- Use separate keys for development and production
- Rotate keys regularly

### Input Validation

- Details are validated for minimum length
- Maximum length enforced by grievance creation endpoint (10,000 characters)
- No SQL injection risk (using parameterized queries)
- No code injection risk (LLM output is validated and sanitized)

### Rate Limiting

Consider implementing:
- Per-IP rate limiting
- Per-user rate limiting
- API key rotation policies

## Monitoring and Logging

### Recommended Metrics

1. **Categorization accuracy** - Track user overrides
2. **Response times** - Monitor LLM API latency
3. **Error rates** - Track fallback category usage
4. **Cost tracking** - Monitor API usage

### Logging

The service logs:
- API calls and responses
- Errors and exceptions
- Fallback category assignments
- Performance metrics

## Future Enhancements

Potential improvements:
1. **Multi-language support** - Categorize grievances in multiple languages
2. **Fine-tuning** - Train on historical grievance data for better accuracy
3. **Confidence thresholds** - Auto-approve high-confidence categorizations
4. **Batch categorization** - Process multiple grievances simultaneously
5. **Analytics dashboard** - Visualize category distributions and trends

## Support

For issues or questions:
1. Check the [main README](../README.md)
2. Review test examples in `tests/test_categorization.py`
3. Contact the development team
