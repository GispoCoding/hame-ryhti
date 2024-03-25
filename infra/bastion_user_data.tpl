Content-Type: multipart/mixed; boundary="//"
MIME-Version: 1.0

--//
Content-Type: text/cloud-config; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Content-Disposition: attachment; filename="cloud-config.txt"

#cloud-config
${yamlencode(
  {
    cloud_final_modules = ["users-groups", "once"],
    users = [
      {name = "ec2-user",
      sudo = "ALL=(ALL) NOPASSWD:ALL",
      ssh-authorized-keys: [ec2_user_public_key,]},
      {name = "ec2-tunnel",
      sudo = false,
      ssh-authorized-keys: [%{ for key in ec2_tunnel_public_keys ~}key,%{ endfor ~}]}
    ],
    ssh_keys = {
      "rsa_private": ec2_host_private_key,
      "rsa_public": ec2_host_public_key
    }
  }
)}
--//
Content-Type: text/x-shellscript; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Content-Disposition: attachment; filename="userdata.sh"

#!/bin/bash
sudo dnf update
sudo dnf install postgresql15 -y
--//--
