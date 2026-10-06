\# CS615 01 — Administrator Mindset and Git



\## Machine Inventory



Date: 2026-10-06



\### Identity



\- Hostname: `ubuntu-admin`

\- User: `atsigane`

\- Home directory: `/home/atsigane`



\### Operating System



\- Distribution: Ubuntu 26.04 LTS

\- Kernel: Linux 7.0.0-31-generic

\- Architecture: x86\_64



\### Networking



| Interface | Address | Purpose |

|---|---|---|

| lo | 127.0.0.1/8 | Loopback |

| enp0s3 | 10.0.2.15/24 | NAT / external connectivity |

| enp0s8 | 192.168.56.11/24 | Host-only network / SSH from Windows |



\### Storage



Root filesystem:



\- Device: `/dev/sda2`

\- Mount point: `/`

\- Size: 25 GB

\- Used: 5.1 GB

\- Available: 19 GB

\- Usage: 22%



\### Memory



\- Total RAM: 3.3 GiB

\- Available RAM: approximately 2.9 GiB

\- Swap: none



\## Five Commands



\### `pwd`



Prints the current working directory.



Example:



```bash

pwd

/home/atsigane



\### `ls`



atsigane@ubuntu-admin:\~$ ls

python-baseline

atsigane@ubuntu-admin:\~$ ls -lh

total 4.0K

drwxrwxr-x 2 atsigane atsigane 4.0K Aug  7 13:53 python-baseline

atsigane@ubuntu-admin:\~$ ls -la

total 68

drwxr-x--- 8 atsigane atsigane  4096 Aug  7 13:56 .

drwxr-xr-x 5 root     root      4096 Sep 11 08:23 ..

\-rw------- 1 atsigane atsigane 10397 Sep 11 17:29 .bash\_history

\-rw-r--r-- 1 atsigane atsigane   220 Feb 13  2026 .bash\_logout

\-rw-r--r-- 1 atsigane atsigane  3771 Feb 13  2026 .bashrc

drwx------ 3 atsigane atsigane  4096 Aug  7 13:56 .cache

drwx------ 4 atsigane atsigane  4096 Aug  7 13:56 .copilot

\-rw------- 1 atsigane atsigane   116 Aug  7 13:49 .lesshst

drwx------ 3 atsigane atsigane  4096 Aug  7 13:51 .local

\-rw-r--r-- 1 atsigane atsigane   807 Feb 13  2026 .profile

drwx------ 2 atsigane atsigane  4096 Aug  6 19:37 .ssh

\-rw------- 1 atsigane atsigane  2316 Aug  7 13:53 .viminfo

drwxr-x--- 5 atsigane atsigane  4096 Aug  7 23:21 .vscode-server

\-rw-rw-r-- 1 atsigane atsigane   183 Aug  7 13:55 .wget-hsts

drwxrwxr-x 2 atsigane atsigane  4096 Aug  7 13:53 python-baseline

atsigane@ubuntu-admin:\~$

