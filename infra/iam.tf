
# Lambda role
resource "aws_iam_role" "lambda_exec" {
  # Separate roles for each hame instance
  name               = "${var.prefix}_serverless_lambda"
  assume_role_policy = jsonencode({
    Version   = "2012-10-17"
    Statement = [
      {
        Action    = "sts:AssumeRole"
        Effect    = "Allow"
        Sid       = ""
        Principal = { Service = "lambda.amazonaws.com" }
      }
    ]
  })
  tags               = merge(local.default_tags, { Name = "${var.prefix}_serverless_lambda" })
}

resource "aws_iam_role_policy_attachment" "lambda_policy" {
  role       = aws_iam_role.lambda_exec.name
  # Lambda must have rights to connect to VPC
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
}

# Create the policy to access secrets manager in the region
resource "aws_iam_policy" "secrets-policy" {
  # We need a separate policy for each hame instance, since they have separate secrets
  name        = "${var.prefix}-lambda-secrets-policy"
  path        = "/"
  description = "Lambda db secrets policy"

  policy = jsonencode({
    Version   = "2012-10-17"
    Statement = [
      {
        Action   = [
          "secretsmanager:GetResourcePolicy",
          "secretsmanager:GetSecretValue",
          "secretsmanager:DescribeSecret",
          "secretsmanager:ListSecretVersionIds"
        ],
        Effect   = "Allow",
        Resource = [
          aws_secretsmanager_secret.hame-db-su.arn,
          aws_secretsmanager_secret.hame-db-admin.arn,
          aws_secretsmanager_secret.hame-db-rw.arn,
          aws_secretsmanager_secret.hame-db-r.arn
        ]
      }
    ]
  })
  tags   = merge(local.default_tags, { Name = "${var.prefix}-lambda-secrets-policy" })
}

resource "aws_iam_role_policy_attachment" "lambda_secrets_attachment" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = aws_iam_policy.secrets-policy.arn
}

# Allow lambda to access ECR. This should be created automatically when ECR images are
# added to lambda, but apparently that does not happen:
# https://docs.aws.amazon.com/lambda/latest/dg/images-create.html#gettingstarted-images-permissions

resource "aws_iam_policy" "ecr-policy" {
  # We need a separate policy for each hame instance, since they have separate secrets
  name        = "${var.prefix}-lambda-ecr-policy"
  path        = "/"
  description = "Lambda ECR image access policy"

  policy = jsonencode({
    Version   = "2012-10-17"
    Statement = [
      {
      "Sid": "LambdaECRImageRetrievalPolicy",
      "Effect": "Allow",
      "Action": [
        "ecr:BatchGetImage",
        "ecr:DeleteRepositoryPolicy",
        "ecr:GetDownloadUrlForLayer",
        "ecr:GetRepositoryPolicy",
        "ecr:SetRepositoryPolicy"
      ],
      "Resource" : [
        aws_ecr_repository.db_manager.arn,
        aws_ecr_repository.koodistot_loader.arn,
        aws_ecr_repository.ryhti_client.arn,
        aws_ecr_repository.mml_loader.arn
        ]
    }
    ]
  })
  tags   = merge(local.default_tags, { Name = "${var.prefix}-lambda-ecr-policy" })
}

resource "aws_iam_role_policy_attachment" "lambda_ecr_attachment" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = aws_iam_policy.ecr-policy.arn
}


# Lambda update user
resource "aws_iam_user" "lambda_update_user" {
  name               = var.AWS_LAMBDA_USER
  tags               = merge(local.default_tags, { Name = "${var.prefix}_lambda_update" })
}

# Create the policy to update lambda functions
resource "aws_iam_policy" "lambda_update_policy" {
  # We need a separate policy for each hame instance, since they have separate lambda functions
  name        = "${var.prefix}-lambda_update_policy"
  path        = "/"
  description = "Github CI lambda update policy"

  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Effect" : "Allow",
        "Action" : [
          # Necessary IAM permission to publish an image in ECR
          "ecr:DescribeImages",
          "ecr:DescribeRepositories",
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage",
          "ecr:BatchCheckLayerAvailability",
          "ecr:InitiateLayerUpload",
          "ecr:UploadLayerPart",
          "ecr:CompleteLayerUpload",
          "ecr:PutImage"
        ],
        "Resource" : [
          aws_ecr_repository.db_manager.arn,
          aws_ecr_repository.koodistot_loader.arn,
          aws_ecr_repository.ryhti_client.arn,
          aws_ecr_repository.mml_loader.arn
          ]
      },
      {
          "Action": [
              "ecr:GetAuthorizationToken"
          ],
          "Effect": "Allow",
          "Resource": "*"
      },
      {
        "Effect" : "Allow",
        "Action" : [
          "lambda:CreateFunction",
          "lambda:UpdateFunctionCode",
          "lambda:InvokeFunction",
          "lambda:UpdateFunctionConfiguration"
         ],
        "Resource" : [
          aws_lambda_function.db_manager.arn,
          aws_lambda_function.koodistot_loader.arn,
          aws_lambda_function.ryhti_client.arn,
          aws_lambda_function.mml_loader.arn,
        ]
      }
    ]
  })
  tags   = merge(local.default_tags, { Name = "${var.prefix}-lambda_update_policy" })
}

resource "aws_iam_policy_attachment" "lambda_update_attachment" {
  name       = "${var.prefix}-lambda_update_attachment"
  users      = [aws_iam_user.lambda_update_user.name]
  policy_arn = aws_iam_policy.lambda_update_policy.arn
}

# This IAM role will be used by the docker daemon
resource "aws_iam_role" "backend-task-execution" {
  name               = "${var.prefix}-backend-task-execution"
  assume_role_policy = jsonencode(
  {
    Version   = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
        Action    = "sts:AssumeRole"
      }
    ]
  })
  tags               = merge(local.default_tags, { Name = "${var.prefix}-backend-task-execution" })

}

# The IAM role above will be allowed to pull docker image from ECR, and to create Cloudwatch log groups
# See: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_execution_IAM_role.html
resource "aws_iam_role_policy_attachment" "backend" {
  role       = aws_iam_role.backend-task-execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

#
# Bastion
#

# Adding a role for the EC2 machine allows making AWS service APIs available via IAM policies
resource "aws_iam_role" "ec2-role" {
  name               = "${var.prefix}-ec2-iam-role"
  path               = "/"
  assume_role_policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": "sts:AssumeRole",
            "Principal": {
               "Service": "ec2.amazonaws.com"
            },
            "Effect": "Allow",
            "Sid": ""
        }
    ]
}
EOF

  tags = merge(local.default_tags, {
    Name = "${var.prefix}-ec2-iam-role"
  })
}

resource "aws_iam_instance_profile" "ec2-iam-profile" {
  name = "${var.prefix}-ec2-iam-profile"
  role = aws_iam_role.ec2-role.name
}

resource "aws_iam_role_policy_attachment" "ssm-policy-attachment" {
  role       = aws_iam_role.ec2-role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}
