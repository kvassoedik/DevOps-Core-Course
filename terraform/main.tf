locals {
  cloud_init = <<-CLOUDINIT
    #cloud-config
    users:
      - name: ${var.ssh_user}
        groups: sudo
        shell: /bin/bash
        sudo: ["ALL=(ALL) NOPASSWD:ALL"]
        ssh_authorized_keys:
          - ${trimspace(file(var.ssh_public_key_path))}
    packages:
      - openssh-server
    runcmd:
      - systemctl enable --now ssh
  CLOUDINIT
}

resource "terraform_data" "lxd_container" {
  input = {
    name          = var.name
    image         = var.image
    ssh_user      = var.ssh_user
    pubkey_sha1   = sha1(file(var.ssh_public_key_path))
    host_ssh_port = var.host_ssh_port
    host_http     = var.host_http_port
    host_app      = var.host_app_port
  }

  provisioner "local-exec" {
  interpreter = ["bash", "-lc"]
  command = <<-BASH
    set -euo pipefail

    if ! command -v lxc >/dev/null 2>&1; then
      echo "ERROR: lxc not found. Install LXD first." >&2
      exit 1
    fi

    # 1) Create container if not exists
    if ! lxc info ${var.name} >/dev/null 2>&1; then
      lxc launch ${var.image} ${var.name}
    fi

    # 2) Wait a bit for container to boot
    sleep 3

    # 3) Install openssh-server and sudo inside container
    lxc exec ${var.name} -- bash -lc 'apt-get update && apt-get install -y openssh-server sudo'

    # 4) Create user if not exists, add to sudo
    lxc exec ${var.name} -- bash -lc 'id -u ${var.ssh_user} >/dev/null 2>&1 || useradd -m -s /bin/bash ${var.ssh_user}'
    lxc exec ${var.name} -- bash -lc 'usermod -aG sudo ${var.ssh_user}'

    # 5) Put SSH key
    PUBKEY="$(cat ${var.ssh_public_key_path})"
    lxc exec ${var.name} -- bash -lc "mkdir -p /home/${var.ssh_user}/.ssh && echo '$PUBKEY' > /home/${var.ssh_user}/.ssh/authorized_keys"
    lxc exec ${var.name} -- bash -lc "chown -R ${var.ssh_user}:${var.ssh_user} /home/${var.ssh_user}/.ssh && chmod 700 /home/${var.ssh_user}/.ssh && chmod 600 /home/${var.ssh_user}/.ssh/authorized_keys"

    # 6) Allow passwordless sudo (for labs)
    lxc exec ${var.name} -- bash -lc "echo '${var.ssh_user} ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/${var.ssh_user} && chmod 440 /etc/sudoers.d/${var.ssh_user}"

    # 7) Ensure ssh is enabled
    lxc exec ${var.name} -- bash -lc 'systemctl enable --now ssh || systemctl enable --now sshd || true'

    # 8) Port forwards (host -> container)
    if ! lxc config device show ${var.name} | grep -q 'tf-ssh'; then
      lxc config device add ${var.name} tf-ssh proxy listen=tcp:0.0.0.0:${var.host_ssh_port} connect=tcp:127.0.0.1:22
    fi

    if ! lxc config device show ${var.name} | grep -q 'tf-http'; then
      lxc config device add ${var.name} tf-http proxy listen=tcp:0.0.0.0:${var.host_http_port} connect=tcp:127.0.0.1:80
    fi

    if ! lxc config device show ${var.name} | grep -q 'tf-app'; then
      lxc config device add ${var.name} tf-app proxy listen=tcp:0.0.0.0:${var.host_app_port} connect=tcp:127.0.0.1:5000
    fi
  BASH
}
  provisioner "local-exec" {
    when    = destroy
    interpreter = ["bash", "-lc"]
    command = <<-BASH
      set -euo pipefail
      if lxc info ${self.input.name} >/dev/null 2>&1; then
        lxc delete ${self.input.name} --force
      fi
    BASH
  }
}
