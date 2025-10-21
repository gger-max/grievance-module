param(
  [string]$ApiBase = "http://localhost:8000",
  [string]$OdooToken = "change-me-very-secret"
)

function Invoke-Json {
  param(
    [string]$Method,
    [string]$Uri,
    [hashtable]$Headers = @{},
    $Body = $null
  )
  $params = @{ Method = $Method; Uri = $Uri; Headers = $Headers }
  if ($null -ne $Body) { $params.ContentType = "application/json"; $params.Body = $Body }
  Invoke-RestMethod @params -TimeoutSec 30
}

# 1) Create
$createBody = @{
  is_anonymous = $true
  summary      = "Streetlight broken"
  details      = "The streetlight on main road is off for 3 nights."
  island       = "Central"
  district     = "North"
  village      = "Katoa"
} | ConvertTo-Json

$createResp = Invoke-Json -Method POST -Uri "$ApiBase/api/grievances" -Body $createBody
$gid = $createResp.id
Write-Output ("Created: " + $gid)

# 2) Get
$getResp = Invoke-Json -Method GET -Uri "$ApiBase/api/grievances/$gid"
$extStatus = "N/A"
if ($getResp -and $getResp.external_status) { $extStatus = $getResp.external_status }
Write-Output ("Fetched status: " + $extStatus)

# 3) Export
$export = Invoke-Json -Method GET -Uri "$ApiBase/api/grievances/export"
$exportCount = 0
if ($export) { $exportCount = $export.Count }
Write-Output ("Export count: " + $exportCount)

# 4) Update status
$updateBody = @{ status = "in_review"; note = "Auto-categorized" } | ConvertTo-Json
$headers = @{ Authorization = "Bearer $OdooToken" }
$updateResp = Invoke-Json -Method PUT -Uri "$ApiBase/api/grievances/$gid/status" -Headers $headers -Body $updateBody
$updated = ""
if ($updateResp -and $updateResp.status) { $updated = $updateResp.status }
Write-Output ("Updated status to: " + $updated)

# 5) Re-fetch
$getResp2 = Invoke-Json -Method GET -Uri "$ApiBase/api/grievances/$gid"
$extStatus2 = "N/A"
if ($getResp2 -and $getResp2.external_status) { $extStatus2 = $getResp2.external_status }
Write-Output ("Current status: " + $extStatus2)

# 6) Receipt URL
$receiptUrl = "$ApiBase/api/grievances/$gid/receipt.pdf"
Write-Output ("Receipt: " + $receiptUrl)
