resource "aws_secretsmanager_secret" "database_url" {
  name = "${var.app_name}/database_url"
}

resource "aws_secretsmanager_secret_version" "database_url" {
  secret_id     = aws_secretsmanager_secret.database_url.id
  secret_string = var.database_url
}

resource "aws_secretsmanager_secret" "admin_api_key" {
  name = "${var.app_name}/admin_api_key"
}

resource "aws_secretsmanager_secret_version" "admin_api_key" {
  secret_id     = aws_secretsmanager_secret.admin_api_key.id
  secret_string = var.admin_api_key
}