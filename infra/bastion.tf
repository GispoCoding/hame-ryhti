# We don't want to create the key in terraform. Otherwise the private key(s) would be saved in terraform state.
# Let's save the public key(s) here as ec2 instance user data.

# Just the smallest arm instance available, for routing traffic to postgres
resource "aws_instance" "bastion-ec2-instance" {
  ami = "ami-0bf463e49ccd368ed" # Amazon Linux 2023
  instance_type = "t4g.nano"
  subnet_id     = aws_subnet.public[0].id
  vpc_security_group_ids = [aws_security_group.bastion.id]
  iam_instance_profile = aws_iam_instance_profile.ec2-iam-profile.name
  tenancy              = "default"
  user_data     = templatefile(
    "bastion_user_data.tpl",
    # multiline string has to be yaml, there are so many ways this can go wrong
    {ec2_host_private_key = "${var.bastion_ec2_host_private_key}",
    ec2_host_public_key = "${var.bastion_ec2_host_public_key}",
    ec2_user_public_key = "${var.bastion_ec2_user_public_key}",
    ec2_tunnel_public_keys = "${var.bastion_ec2_tunnel_public_keys}"}
    )

  tags = merge(local.default_tags, {
    Name = "${var.prefix}-bastion"
  })
}
