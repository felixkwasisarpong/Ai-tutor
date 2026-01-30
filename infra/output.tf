output "vpc_id" {
  value = aws_vpc.this.id
}

output "ecs_cluster_name" {
  value = aws_ecs_cluster.this.name
}


output "ecs_service_name" {
  value = aws_ecs_service.backend.name
}
output "alb_dns_name" {
  value = aws_lb.backend.dns_name
}

output "ui_cloudfront_url" {
  value = aws_cloudfront_distribution.ui.domain_name
}