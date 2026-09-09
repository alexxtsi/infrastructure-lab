# Linux System and Filesystem

## Goal
Learn how the Linux filesystem is organized and understand the purpose of important system directories such as `/etc`, `/var`, `/home`, `/tmp`, `/proc`, and `/sys`.

## 1. Linux Filesystem Overview
Linux uses a single root directory, `/`, as the top of the filesystem tree. Everything in the system is under this root, including configuration files, user data, logs, temporary files, and kernel information.

Example:

```bash
ls /
```

Common directories include:

- `/bin` - essential user binaries
- `/boot` - bootloader and kernel files
- `/etc` - system configuration files
- `/home` - personal user directories
- `/var` - variable data such as logs and databases
- `/tmp` - temporary files
- `/proc` - virtual process and kernel information
- `/sys` - kernel device and hardware information

## 2. File and Directory Basics
A file stores data, while a directory stores other files and folders.

Example:

```bash
mkdir -p /tmp/demo
echo "hello from linux" > /tmp/demo/example.txt
ls -l /tmp/demo
cat /tmp/demo/example.txt
```

What this does:

- `mkdir -p` creates a directory
- `echo` writes text to a file
- `ls -l` shows file metadata
- `cat` displays the file content

## 3. Important System Directories

### /etc
`/etc` contains system configuration files.

Examples:

```bash
ls /etc
ls /etc/ssh
cat /etc/hosts
```

Typical files:

- `/etc/passwd` - user account information
- `/etc/group` - groups
- `/etc/hosts` - hostname mappings
- `/etc/nginx/nginx.conf` - web server config

This directory is mainly for settings that control how the machine behaves.

### /var
`/var` contains variable data that changes as the system runs. It usually stores logs, mail, caches, databases, and application-generated data.

Examples:

```bash
ls /var
ls /var/log
ls -l /var/log
```

Typical locations:

- `/var/log` - system logs
- `/var/lib` - application data
- `/var/mail` - email storage
- `/var/spool` - queued jobs and temporary app data

Example:

```bash
tail -n 20 /var/log/syslog
```

### /home
`/home` contains user home directories.

Examples:

```bash
ls /home
ls /home/student
```

Each user usually has a folder like:

- `/home/alex`
- `/home/student`
- `/home/ubuntu`

This is where users keep their personal files, projects, documents, and configuration files.

### /tmp
`/tmp` is used for temporary files. It is usually writable by all users and may be cleaned automatically.

Examples:

```bash
echo "temporary file" > /tmp/test.txt
ls -l /tmp/test.txt
rm /tmp/test.txt
```

Important notes:

- files here are often not meant to be permanent
- data may be deleted on reboot or by cleanup processes
- useful for short-lived work files and caches

### /proc
`/proc` is a virtual filesystem that provides information about running processes and kernel state. It does not contain real files on disk; it exposes runtime system information.

Examples:

```bash
ls /proc
cat /proc/meminfo
cat /proc/cpuinfo
```

Useful examples:

- `/proc/meminfo` - memory information
- `/proc/cpuinfo` - CPU information
- `/proc/loadavg` - system load
- `/proc/[pid]/status` - details for a running process

Example to inspect a process:

```bash
ps -ef | head
cat /proc/$$/status
```

### /sys
`/sys` is another virtual filesystem that exposes kernel and hardware information. It is used to view or change system parameters at runtime.

Examples:

```bash
ls /sys
ls /sys/class
ls /sys/class/net
```

Typical uses:

- hardware discovery
- network information
- block devices
- kernel settings
- device state and attributes

Example:

```bash
ls /sys/class/net
cat /sys/class/net/lo/mtu
```

## 4. Comparing the Main Directories

- `/etc` = configuration files
- `/var` = changing runtime data and logs
- `/home` = user files and projects
- `/tmp` = temporary files
- `/proc` = live process and kernel details
- `/sys` = kernel and hardware information

## 5. Example Commands

```bash
ls -ld /etc /var /home /tmp /proc /sys
ls -l /etc
ls -l /var/log
ls -l /home
ls -l /tmp
cat /proc/meminfo
ls /sys/class/net
```

## 6. Summary
The Linux filesystem is organized around the root directory `/`. Each important directory has a specific role:

- `/etc` manages system configuration
- `/var` stores variable and log data
- `/home` stores user work and files
- `/tmp` stores temporary data
- `/proc` exposes running processes and system runtime info
- `/sys` exposes kernel and hardware information

Understanding these directories is essential for Linux administration, troubleshooting, and system management.
