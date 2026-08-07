# Linux Home Lab Network

## Purpose

The lab uses two adapters per VM:

- NAT provides outbound internet access.
- Host-only networking provides predictable private administration addresses.

## Address table

| System | Interface purpose | Address |
|---|---|---|
| Windows host | Host-only adapter | 192.168.56.1/24 |
| ubuntu-admin | NAT | 10.0.2.15/24 |
| ubuntu-admin | Host-only | 192.168.56.11/24 |
| rocky-admin | NAT | 10.0.2.15/24 |
| rocky-admin | Host-only | 192.168.56.12/24 |

## Topology

Internet
   |
VirtualBox NAT
   |
   +-- ubuntu-admin
   +-- rocky-admin

Windows host: 192.168.56.1
   |
VirtualBox host-only network: 192.168.56.0/24
   |
   +-- ubuntu-admin: 192.168.56.11
   +-- rocky-admin: 192.168.56.12

## Verification

- Both VMs reach the internet through NAT.
- Ubuntu and Rocky ping each other over the host-only network.
- Windows reaches both VMs over SSH.
- Key-based SSH works between the VMs and from Windows.
- Both VMs have a tested clean-networked-baseline snapshot.