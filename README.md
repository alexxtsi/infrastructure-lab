# Infrastructure Career Lab

Hands-on infrastructure and DevOps learning environment built around
Linux administration, networking, automation and modern infrastructure tooling.

## Lab Environment

Two Linux virtual machines running in VirtualBox:

| Host | Distribution | Private IP | Purpose |
|---|---|---|---|
| ubuntu-admin | Ubuntu Server | 192.168.56.11 | Linux administration / automation control node |
| rocky-admin | Rocky Linux | 192.168.56.12 | RHEL-family administration / managed node |

Each VM uses:

- NAT for internet access
- Host-only networking for private lab communication
- OpenSSH
- Key-based authentication
- Tested VirtualBox baseline snapshots

## Repository

- `linux/` — Linux administration labs
- `networking/` — TCP/IP, DNS and packet analysis
- `virtualization/` — VirtualBox and VM labs
- `automation/` — Python and Bash automation
- `ansible/` — Configuration management
- `containers/` — Docker and Compose
- `monitoring/` — Prometheus and Grafana
- `cloud/` — AWS and Terraform
- `kubernetes/` — Kubernetes labs
- `cs615/` — Adapted CS615 exercises
- `interview-notes/` — Technical interview preparation

## Learning Method

For each practical lab:

1. Predict the expected behavior.
2. Perform the task.
3. Verify the result.
4. Break something intentionally.
5. Diagnose the problem.
6. Repair it.
7. Document what happened.

## Security

This repository contains only home-lab and sanitized examples.

No company-confidential information, credentials, private keys,
internal hostnames or proprietary code are stored here.# Infrastructure Career Lab

Hands-on infrastructure and DevOps learning environment built around
Linux administration, networking, automation and modern infrastructure tooling.

## Lab Environment

Two Linux virtual machines running in VirtualBox:

| Host | Distribution | Private IP | Purpose |
|---|---|---|---|
| ubuntu-admin | Ubuntu Server | 192.168.56.11 | Linux administration / automation control node |
| rocky-admin | Rocky Linux | 192.168.56.12 | RHEL-family administration / managed node |

Each VM uses:

- NAT for internet access
- Host-only networking for private lab communication
- OpenSSH
- Key-based authentication
- Tested VirtualBox baseline snapshots

## Repository

- `linux/` — Linux administration labs
- `networking/` — TCP/IP, DNS and packet analysis
- `virtualization/` — VirtualBox and VM labs
- `automation/` — Python and Bash automation
- `ansible/` — Configuration management
- `containers/` — Docker and Compose
- `monitoring/` — Prometheus and Grafana
- `cloud/` — AWS and Terraform
- `kubernetes/` — Kubernetes labs
- `cs615/` — Adapted CS615 exercises
- `interview-notes/` — Technical interview preparation

## Learning Method

For each practical lab:

1. Predict the expected behavior.
2. Perform the task.
3. Verify the result.
4. Break something intentionally.
5. Diagnose the problem.
6. Repair it.
7. Document what happened.

## Security

This repository contains only home-lab and sanitized examples.

No company-confidential information, credentials, private keys,
internal hostnames or proprietary code are stored here.