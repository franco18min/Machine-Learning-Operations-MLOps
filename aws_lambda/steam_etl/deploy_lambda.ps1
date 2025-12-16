# Deploy Script for Windows (PowerShell) - Layers Method (Zero Cost)

# --- CONFIGURACIÓN ---
$FunctionName = "steam-etl-processor"
$Runtime = "python3.11"
$RoleArn = "arn:aws:iam::476277674914:role/lambda-dynamodb-role"
$ZipFile = "fileb://lambda_deployment.zip"
$Handler = "lambda_function.lambda_handler"
$Timeout = 300
$Memory = 256
# ARN oficial de AWS SDK Pandas (Data Wrangler) para Python 3.11 en us-east-1
# Fuente: https://github.com/aws/aws-sdk-pandas
$LayerArn = "arn:aws:lambda:us-east-1:336392948345:layer:AWSSDKPandas-Python311:12"

# --- PROCESO ---

Write-Host "Iniciando despliegue directo con Layers..."

# Verificar si la función ya existe
aws lambda get-function --function-name $FunctionName 2>$null >$null

if ($LASTEXITCODE -eq 0) {
    Write-Host "   🔄 La función existe. Actualizando código..."
    aws lambda update-function-code `
        --function-name $FunctionName `
        --zip-file $ZipFile
        
    Write-Host "   🔄 Actualizando configuración de Layers..."
    aws lambda update-function-configuration `
        --function-name $FunctionName `
        --layers $LayerArn
} else {
    Write-Host "   ✨ Creando nueva función..."
    aws lambda create-function `
        --function-name $FunctionName `
        --runtime $Runtime `
        --role $RoleArn `
        --handler $Handler `
        --zip-file $ZipFile `
        --timeout $Timeout `
        --memory-size $Memory `
        --layers $LayerArn `
        --description "ETL Pipeline para Steam Games Data"
}

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ DESPLIEGUE COMPLETADO EXITOSAMENTE."
} else {
    Write-Host "`n❌ Error en el despliegue de Lambda."
}
