locals {
  database_url = "postgresql+psycopg2://${var.db_username}:${var.db_password}@${aws_db_instance.postgres.address}:${aws_db_instance.postgres.port}/${var.db_name}"
  availability_zones = [
    for az in data.aws_availability_zones.available.names : az if az != "us-east-2a"
  ]
}
