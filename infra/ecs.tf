# Cluster is a collection of compute resources that can run tasks and services (docker containers in the end)
resource "aws_ecs_cluster" "x-road_securityserver" {
  name = "${var.prefix}-x-road_securityserver"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }

  tags = merge(local.default_tags, {Name = "${var.prefix}-cluster"})
}

# Task definition is a description of parameters given to docker daemon, in order to run a container
resource "aws_ecs_task_definition" "x-road_securityserver" {
  family                   = "${var.prefix}-x-road_securityserver"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  # This is the IAM role that the docker daemon will use, e.g. for pulling the image from ECR (AWS's own docker repository)
  execution_role_arn       = aws_iam_role.backend-task-execution.arn
  # If the containers in the task definition need to access AWS services, we'd specify a role via task_role_arn.
  # task_role_arn = ...
  cpu                      = var.x-road_securityserver_cpu
  memory                   = var.x-road_securityserver_memory
  container_definitions    = jsonencode(
  [
    {
      name         = "x-road_securityserver-from-dockerhub"
      image        = var.x-road_securityserver_image
      cpu          = var.x-road_securityserver_cpu
      memory       = var.x-road_securityserver_memory
      # try out AWS EFS volume for storing x-road configuration!
      mountPoints  = [
        {
          "sourceVolume": "configuration-volume",
          "containerPath": "/etc/xroad"
        }
      ]
      volumesFrom  = []
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group = "/aws/ecs/${var.prefix}-x-road_securityserver"
          awslogs-region = var.AWS_REGION_NAME
          awslogs-stream-prefix = "ecs"
        }
      }
      essential    = true
      portMappings = [
        {
          # admin UI
          hostPort = 4000
          containerPort = 4000
          protocol      = "tcp"
        },
        {
          # health check
          hostPort = 5588
          containerPort = 5588
          protocol      = "tcp"
        },
        {
          # consumer HTTP
          hostPort = 8080
          containerPort = 8080
          protocol      = "tcp"
        },
        # These are not needed if we don't provide X-road services
        # {
        #   # message exchange between security servers
        #   hostPort = 5500
        #   containerPort = 5500
        #   protocol = "tcp"
        # },
        # {
        #   # OCSP responses between security servers
        #   hostPort = 5577
        #   containerPort = 5577
        #   protocol = "tcp"
        # }
      ]
      # With Fargate, we use awsvpc networking, which will reserve a ENI (Elastic Network Interface) and attach it to
      # our VPC
      networkMode  = "awsvpc"
      environment  = [
        {
          name = "XROAD_ADMIN_USER"
          value = var.x-road_secrets.admin_user
        },
        {
          name = "XROAD_ADMIN_PASSWORD"
          value = var.x-road_secrets.admin_password
        },
      ]
    }
  ])

  volume {
  name = "configuration-volume"
    efs_volume_configuration {
      file_system_id          = aws_efs_file_system.x-road_configuration_volume.id
      transit_encryption      = "ENABLED"
      # transit_encryption_port = 2999
      # authorization_config {
      #   access_point_id = aws_efs_access_point.test.id
      #   iam             = "ENABLED"
      # }
    }
  }

  tags = merge(local.default_tags, {Name = "${var.prefix}-x-road_securityserver-definition"})
}
