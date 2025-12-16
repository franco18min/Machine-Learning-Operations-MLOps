param(
    [string]$FunctionName = "steam-api-processor",
    [string]$RoleArn = "",
    [string]$Region = "us-east-1"
)

$ErrorActionPreference = "Continue"

Write-Host "Iniciando despliegue..."

# 1. Empaquetar
if (Test-Path "lambda_deployment.zip") { Remove-Item "lambda_deployment.zip" -Force }
Compress-Archive -Path "lambda_function.py" -DestinationPath "lambda_deployment.zip" -Force
Write-Host "ZIP creado."

# 2. Desplegar funcion
Write-Host "Verificando funcion..."
aws lambda get-function --function-name $FunctionName --region $Region 2>$null | Out-Null

if ($LASTEXITCODE -eq 0) {
    Write-Host "Actualizando funcion existente..."
    aws lambda update-function-code --function-name $FunctionName --zip-file fileb://lambda_deployment.zip --region $Region
} else {
    Write-Host "Creando nueva funcion..."
    if ([string]::IsNullOrEmpty($RoleArn)) {
        Write-Host "Error: Debes especificar -RoleArn para crear la funcion." -ForegroundColor Red
        exit 1
    }
    aws lambda create-function --function-name $FunctionName --runtime python3.11 --role $RoleArn --handler lambda_function.lambda_handler --zip-file fileb://lambda_deployment.zip --timeout 30 --memory-size 256 --region $Region
}

# 3. Layer
Write-Host "Configurando Layer..."
$LayerArn = "arn:aws:lambda:$Region`:336392948345:layer:AWSSDKPandas-Python311:12"
aws lambda update-function-configuration --function-name $FunctionName --layers $LayerArn --region $Region | Out-Null

# 4. URL Publica
Write-Host "Configurando URL..."
aws lambda get-function-url-config --function-name $FunctionName --region $Region 2>$null | Out-Null
if ($LASTEXITCODE -ne 0) {
    # Escapado especial para PowerShell y AWS CLI
    # Usamos comillas simples externas y escapamos las comillas dobles internas con backslash
    aws lambda create-function-url-config --function-name $FunctionName --auth-type NONE --cors '{\"AllowOrigins\":[\"*\"],\"AllowMethods\":[\"GET\"]}' --region $Region
}

# 5. Resultado
$ConfigJson = aws lambda get-function-url-config --function-name $FunctionName --region $Region
$Config = $ConfigJson | ConvertFrom-Json

Write-Host "`nDEPLOY COMPLETO" -ForegroundColor Green
Write-Host "URL: $($Config.FunctionUrl)" -ForegroundColor Cyan
Write-Host "Prueba: curl $($Config.FunctionUrl)?top=true"
