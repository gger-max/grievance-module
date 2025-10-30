# Simple PowerShell HTTP server
$port = 8090
$path = "D:\grievanceModule\frontend-typebot\public"

$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add("http://localhost:$port/")
$listener.Start()

Write-Host "Server running at http://localhost:$port/"
Write-Host "Press Ctrl+C to stop..."

while ($listener.IsListening) {
    $context = $listener.GetContext()
    $request = $context.Request
    $response = $context.Response
    
    $requestPath = $request.Url.LocalPath
    if ($requestPath -eq "/") {
        $requestPath = "/simple-form.html"
    }
    
    $filePath = Join-Path $path $requestPath.TrimStart('/')
    
    if (Test-Path $filePath) {
        $content = [System.IO.File]::ReadAllBytes($filePath)
        $response.ContentLength64 = $content.Length
        $response.ContentType = "text/html"
        $response.OutputStream.Write($content, 0, $content.Length)
    } else {
        $response.StatusCode = 404
        $message = [System.Text.Encoding]::UTF8.GetBytes("File not found")
        $response.OutputStream.Write($message, 0, $message.Length)
    }
    
    $response.Close()
}

$listener.Stop()
