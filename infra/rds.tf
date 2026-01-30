resource "aws_db_subnet_group" "postgres" {
  name       = "${var.app_name}-db-subnets"
  subnet_ids = [aws_subnet.private.id, aws_subnet.private_b.id]

  tags = {
    Name = "${var.app_name}-db-subnets"
  }
}

resource "aws_db_instance" "postgres" {
  identifier          = "${var.app_name}-db"
  engine              = "postgres"
  instance_class      = "db.t3.micro"
  allocated_storage   = 20
  db_name             = var.db_name
  username            = var.db_username
  password            = var.db_password
  publicly_accessible = false
  db_subnet_group_name = aws_db_subnet_group.postgres.name
  vpc_security_group_ids = [aws_security_group.db.id]
  skip_final_snapshot = true
}
