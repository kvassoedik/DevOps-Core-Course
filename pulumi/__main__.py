import os
import subprocess
import time

import pulumi
from pulumi import Config


def run(cmd: str) -> str:
    p = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    if p.returncode != 0:
        raise RuntimeError(f"Command failed: {cmd}\nSTDOUT:\n{p.stdout}\nSTDERR:\n{p.stderr}")
    return p.stdout.strip()


cfg = Config()

name = cfg.get("name") or "lab04-pu"
image = cfg.get("image") or "ubuntu:24.04"
ssh_user = cfg.get("sshUser") or "ubuntu"

ssh_public_key_path = cfg.get("sshPublicKeyPath") or os.path.expanduser("~/.ssh/id_ed25519.pub")
host_ssh_port = int(cfg.get("hostSshPort") or "2222")
host_http_port = int(cfg.get("hostHttpPort") or "8081")
host_app_port = int(cfg.get("hostAppPort") or "15000")

if not os.path.exists(ssh_public_key_path):
    raise FileNotFoundError(f"SSH public key not found: {ssh_public_key_path}")

pubkey = open(ssh_public_key_path, "r", encoding="utf-8").read().strip()

# Create container if missing
try:
    run(f"lxc info {name}")
except Exception:
    run(f"lxc launch {image} {name}")

time.sleep(3)

# Ensure ssh + sudo + user + key
run(f"lxc exec {name} -- bash -lc 'apt-get update || true'")
run(f"lxc exec {name} -- bash -lc 'apt-get install -y openssh-server sudo || true'")
run(f"lxc exec {name} -- bash -lc 'id -u {ssh_user} >/dev/null 2>&1 || useradd -m -s /bin/bash {ssh_user}'")
run(f"lxc exec {name} -- bash -lc 'usermod -aG sudo {ssh_user}'")
run(
    f"lxc exec {name} -- bash -lc \"mkdir -p /home/{ssh_user}/.ssh && "
    f"echo '{pubkey}' > /home/{ssh_user}/.ssh/authorized_keys\""
)
run(f"lxc exec {name} -- bash -lc 'chown -R {ssh_user}:{ssh_user} /home/{ssh_user}/.ssh'")
run(f"lxc exec {name} -- bash -lc 'chmod 700 /home/{ssh_user}/.ssh && chmod 600 /home/{ssh_user}/.ssh/authorized_keys'")
run(
    f"lxc exec {name} -- bash -lc \"echo '{ssh_user} ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/{ssh_user} && "
    f"chmod 440 /etc/sudoers.d/{ssh_user}\""
)
run(f"lxc exec {name} -- bash -lc 'systemctl enable --now ssh || systemctl enable --now sshd || true'")

# Port forwards
devices = run(f"lxc config device show {name}")
if "tf-ssh" not in devices:
    run(f"lxc config device add {name} tf-ssh proxy listen=tcp:0.0.0.0:{host_ssh_port} connect=tcp:127.0.0.1:22")
if "tf-http" not in devices:
    run(f"lxc config device add {name} tf-http proxy listen=tcp:0.0.0.0:{host_http_port} connect=tcp:127.0.0.1:80")
if "tf-app" not in devices:
    run(f"lxc config device add {name} tf-app proxy listen=tcp:0.0.0.0:{host_app_port} connect=tcp:127.0.0.1:5000")

pulumi.export("container_name", name)
pulumi.export("ssh_command", f"ssh -p {host_ssh_port} {ssh_user}@127.0.0.1")
pulumi.export("http_url", f"http://<SERVER_PUBLIC_IP>:{host_http_port}")
pulumi.export("app_url", f"http://<SERVER_PUBLIC_IP>:{host_app_port}")
