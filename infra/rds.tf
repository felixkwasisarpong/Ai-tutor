resource "aws_db_instance" "postgres" {
    identifier = "${var.app_name}-db"
    engine = "postgres"
    instance_class = "db.t3.micro"
    allocated_storage = 20
    db_name = var.db_name
    username = var.db_username
    password = var.db_password
    publicly_accessible = false
    skip_final_snapshot = true
  }
  
