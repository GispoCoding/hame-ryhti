# Database secrets
resource "aws_secretsmanager_secret" "arho-db-su" {
  name = "${var.prefix}-postgres-database-su"
  tags = merge(local.default_tags, {Name = "${var.prefix}-postgres-database-su"})
}

resource "aws_secretsmanager_secret_version" "arho-db-su" {
  secret_id     = aws_secretsmanager_secret.arho-db-su.id
  secret_string = jsonencode(var.su_secrets)
}

resource "aws_secretsmanager_secret" "arho-db-admin" {
  name = "${var.prefix}-postgres-database-admin"
  tags = merge(local.default_tags, {Name = "${var.prefix}-postgres-database-admin"})
}

resource "aws_secretsmanager_secret_version" "arho-db-admin" {
  secret_id     = aws_secretsmanager_secret.arho-db-admin.id
  secret_string = jsonencode(var.arho_admin_secrets)
}

resource "aws_secretsmanager_secret" "arho-db-rw" {
  name = "${var.prefix}-postgres-database-rw"
  tags = merge(local.default_tags, {Name = "${var.prefix}-postgres-database-rw"})
}

resource "aws_secretsmanager_secret_version" "arho-db-rw" {
  secret_id     = aws_secretsmanager_secret.arho-db-rw.id
  secret_string = jsonencode(var.arho_rw_secrets)
}

resource "aws_secretsmanager_secret" "arho-db-r" {
  name = "${var.prefix}-postgres-database-r"
  tags = merge(local.default_tags, {Name = "${var.prefix}-postgres-database-r"})
}

resource "aws_secretsmanager_secret_version" "arho-db-r" {
  secret_id     = aws_secretsmanager_secret.arho-db-r.id
  secret_string = jsonencode(var.arho_r_secrets)
}

resource "aws_secretsmanager_secret" "xroad-db-pwd" {
  name = "${var.prefix}-xroad-postgres-database-su"
  tags = merge(local.default_tags, {Name = "${var.prefix}-xroad-postgres-database-su"})
}

resource "aws_secretsmanager_secret_version" "xroad-db-pwd" {
  secret_id     = aws_secretsmanager_secret.xroad-db-pwd.id
  secret_string = jsonencode(var.x-road_db_password)
}
