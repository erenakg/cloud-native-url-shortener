# 1. URL Kısaltıcı statik dosyaları / logları için S3 Bucket
resource "aws_s3_bucket" "shortener_storage" {
  bucket = "cloud-url-shortener-data"

  tags = {
    Environment = "Local"
    Project     = "CloudURLShortener"
    ManagedBy   = "Terraform"
  }
}

# 2. Kalıcı URL kayıtları ve analitikler için DynamoDB Tablosu (AWS NoSQL Veritabanı)
resource "aws_dynamodb_table" "urls_table" {
  name         = "ShortenedURLs"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "short_code"

  attribute {
    name = "short_code"
    type = "S"
  }

  tags = {
    Environment = "Local"
    Project     = "CloudURLShortener"
    ManagedBy   = "Terraform"
  }
}