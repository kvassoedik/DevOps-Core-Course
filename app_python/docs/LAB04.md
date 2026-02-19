# LAB04 — Terraform & Pulumi

## Task 1 — Terraform Infrastructure

### Goal

Provision a virtual machine-like environment using Infrastructure as Code.

### Implementation

Instead of using AWS (no cloud access), LXD containers were used as local VM equivalents.

Terraform provisions:

* Ubuntu 24.04 container
* SSH access
* Port forwarding (simulating security groups)

### Commands Used

```bash
terraform init
terraform plan
terraform apply
```

### Outputs

```
terraform_data.lxd_container (local-exec): Device tf-ssh added to lab04-tf
terraform_data.lxd_container (local-exec): Device tf-http added to lab04-tf
terraform_data.lxd_container: Still creating... [04m50s elapsed]
terraform_data.lxd_container (local-exec): Device tf-app added to lab04-tf
terraform_data.lxd_container: Creation complete after 4m51s [id=4ac8b90e-05b6-63e1-476d-fc0092e45c39]

Apply complete! Resources: 1 added, 0 changed, 1 destroyed.

Outputs:

app_url = "http://<SERVER_PUBLIC_IP>:15000"
container_name = "lab04-tf"
http_url = "http://<SERVER_PUBLIC_IP>:8081"
ssh_command = "ssh -p 2222 ubuntu@127.0.0.1"
```

### Verification

Container created:

```bash
lxc list
```

SSH access works:

```bash
ssh -p 2222 ubuntu@127.0.0.1
```

`docs/screenshots/10-terraform-ssh.png`

### Destroy Infrastructure

```bash
terraform destroy
```

`docs/screenshots/11-terraform-destroy.png`

## Task 2 — Pulumi Infrastructure

### Goal

Recreate the same infrastructure using Pulumi.

### Approach

Pulumi was used with Python runtime to orchestrate LXD commands.

This simulates:

* Compute instance
* Security group (via port proxy)
* Provisioning (user + SSH key)

### Stack Initialization

```bash
pulumi stack init dev
pulumi config
```

### Deployment

```bash
pulumi up
```

`docs/screenshots/12-pulumi-up.png`

### Outputs

```bash
pulumi stack output
```

### Verification

Container is running:

```bash
lxc list
```

SSH proof:

```bash
ssh -p 2222 ubuntu@127.0.0.1
uname -a
```

`docs/screenshots/13-pulumi-ssh.png`

### Cleanup

```bash
pulumi destroy
```

`docs/screenshots/14-pulumi-destroy.png`

## Comparison: Terraform vs Pulumi

| Feature        | Terraform         | Pulumi                   |
| -------------- | ----------------- | ------------------------ |
| Declarative    | Yes               | No (imperative possible) |
| Language       | HCL               | Python                   |
| Flexibility    | Limited           | High                     |
| State          | terraform.tfstate | Pulumi state             |
| Learning Curve | Easier            | Requires programming     |
| Use Case       | Standard infra    | Complex automation       |

## Conclusion

Terraform is simpler and ideal for predictable infrastructure.
Pulumi provides more flexibility and integrates better with real programming logic.

Both tools successfully provisioned identical environments using LXD instead of cloud providers.

## Result

Infrastructure lifecycle successfully demonstrated:

Create → Configure → Access → Destroy

This satisfies the goals of Infrastructure as Code without requiring public cloud access.
