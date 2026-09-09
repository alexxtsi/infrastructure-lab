# Linux Kernel — Detailed Practical Guide

## Goal

Understand what the Linux kernel is, why it exists, how it separates applications from hardware, and how its major subsystems work together. The focus is practical system administration and DevOps troubleshooting on Rocky Linux and similar distributions.

> The kernel is not the entire operating system. Linux is the kernel; a working Linux system also includes userspace tools, libraries, services, a shell, and distribution-specific packages.

---

## 1. Where the Kernel Fits

The Linux kernel is the privileged core of the operating system. Applications cannot safely control the CPU, memory, disks, or network interfaces directly. They request services from the kernel.

![Linux kernel interfaces](https://commons.wikimedia.org/wiki/Special:Redirect/file/Linux_kernel_interfaces.svg)

*Original illustration: [Linux kernel interfaces](https://commons.wikimedia.org/wiki/File:Linux_kernel_interfaces.svg) by ScotXW, licensed under [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/). The diagram shows the interfaces between applications, libraries, the system-call interface, kernel subsystems, and hardware.*

The basic relationship is:

```text
Applications and services
          │
          ▼
Userspace libraries, such as glibc
          │
          ▼
System-call interface
          │
          ▼
Linux kernel
  ├── scheduler
  ├── memory manager
  ├── virtual filesystem
  ├── network stack
  ├── security framework
  └── device drivers
          │
          ▼
Hardware
```

The kernel provides controlled sharing. Many processes can use the same CPU, memory, disks, and network devices without being allowed to overwrite one another's data.

---

## 2. Kernel Space and User Space

Modern CPUs support privilege levels. Linux uses them to create two important execution environments.

### User space

User space contains normal programs:

- Shells such as Bash
- Services such as `sshd`, Nginx, and databases
- Command-line tools such as `ls`, `cp`, and `curl`
- Language runtimes such as Python and Java
- Containers and the processes running inside them

A userspace process has its own virtual address space and restricted access. It cannot normally read another process's memory or execute privileged hardware instructions.

### Kernel space

Kernel code runs with high privilege. It can:

- Access physical memory
- Configure hardware
- Handle CPU interrupts
- Schedule processes
- Enforce filesystem and network permissions
- Load kernel modules

This power creates risk. A userspace application crash normally affects one process. A serious kernel or driver fault can crash or corrupt the whole system.

### Context switches

When a program requests kernel work, the CPU transitions from user mode to kernel mode. After the request is handled, execution returns to user mode. This controlled transition is part of a **system call**.

Do not confuse these two terms:

- A **mode switch** changes CPU privilege between user mode and kernel mode.
- A **process context switch** changes which process or thread is running.

They may occur near each other, but they are not the same operation.

---

## 3. System Calls

System calls are the main programming interface between userspace and the kernel.

Common examples include:

| System call | Purpose |
|---|---|
| `openat()` | Open a file relative to a directory or the current directory |
| `read()` | Read bytes from a file descriptor |
| `write()` | Write bytes to a file descriptor |
| `fork()` / `clone()` | Create a process or thread-like task |
| `execve()` | Replace a process with a new program |
| `mmap()` | Map files or anonymous memory into a process |
| `socket()` | Create a communication endpoint |
| `connect()` | Connect a socket to a remote endpoint |
| `mount()` | Attach a filesystem to the directory tree |

A command such as `cat /etc/hosts` is a userspace program. In simplified form, it:

1. Calls `openat()` to request access to `/etc/hosts`.
2. The kernel resolves the path and checks permissions.
3. The filesystem and storage layers obtain the data.
4. `cat` calls `read()` to receive the bytes.
5. `cat` calls `write()` to send them to the terminal.

Inspect system calls with `strace`:

```bash
strace -e trace=openat,read,write cat /etc/hosts
```

`strace` is valuable when a program says only “permission denied,” “file not found,” or “connection failed.” It shows what the process asked the kernel to do and the returned error code.

---

## 4. Major Kernel Subsystems

![Linux kernel architecture](https://commons.wikimedia.org/wiki/Special:Redirect/file/Linux_kernel_diagram.svg)

*Original illustration: [Linux kernel diagram](https://commons.wikimedia.org/wiki/File:Linux_kernel_diagram.svg) by Kuzux, licensed under [CC BY-SA 2.5](https://creativecommons.org/licenses/by-sa/2.5/). It is an older high-level diagram, but the core separation of subsystems remains useful.*

### 4.1 Process scheduler

Linux usually runs far more tasks than there are CPU cores. The scheduler chooses which runnable task receives CPU time and on which CPU it runs.

A process may be:

- **Running:** currently executing or ready to execute
- **Sleeping:** waiting for an event, timer, or I/O
- **Stopped:** suspended by a signal or debugger
- **Zombie:** finished, but its parent has not collected its exit status

Useful commands:

```bash
ps -eo pid,ppid,stat,ni,comm
top
uptime
cat /proc/loadavg
```

The load average is not CPU percentage. It represents tasks that are runnable or in uninterruptible sleep, averaged over 1, 5, and 15 minutes. High load can therefore come from CPU pressure or blocked I/O.

#### Priorities

The nice value influences normal scheduling priority:

```bash
nice -n 10 command
renice 5 -p 1234
```

Lower nice values request more CPU preference; raising priority usually requires additional privilege. Nice values do not impose a hard CPU limit. For enforceable resource control, use cgroups.

### 4.2 Memory management

Each process sees a private **virtual address space**. The kernel and CPU memory-management unit translate virtual addresses to physical memory.

This provides:

- Isolation between processes
- Controlled sharing of memory
- Memory-mapped files
- Demand paging
- Copy-on-write behavior
- Use of swap when configured

Important concepts:

- **Page:** fixed-size unit used for virtual-memory management, commonly 4 KiB on x86-64.
- **Page table:** maps virtual pages to physical memory.
- **Page fault:** occurs when a process accesses a page that is not currently mapped as required. Many page faults are normal.
- **Page cache:** RAM used to cache file data and improve I/O performance.
- **Anonymous memory:** memory not backed by a regular file, such as heap and stack allocations.
- **Swap:** disk-backed space that can hold selected memory pages under pressure.

Useful commands:

```bash
free -h
cat /proc/meminfo
vmstat 1
ps -eo pid,comm,rss,vsz --sort=-rss | head
```

Linux deliberately uses otherwise idle RAM for caches. A low value in the `free` column does not by itself mean the server is out of memory. The `available` estimate is more useful.

#### Out-of-memory handling

If the kernel cannot satisfy critical memory allocations, the OOM killer may terminate a process to recover memory.

```bash
journalctl -k | grep -i -E 'out of memory|oom|killed process'
cat /proc/1234/oom_score
cat /proc/1234/oom_score_adj
```

An OOM kill is usually evidence of memory exhaustion or incorrect limits, not the root cause itself. Check application demand, leaks, concurrency, container limits, and swap policy.

### 4.3 Virtual Filesystem Switch

The Virtual Filesystem Switch (**VFS**) gives programs one common file API even when storage uses different filesystem implementations such as XFS, ext4, NFS, or tmpfs.

```text
Application
    │ open/read/write
    ▼
VFS common interface
    ├── XFS
    ├── ext4
    ├── NFS
    ├── tmpfs
    └── procfs/sysfs
```

VFS works with objects such as:

- **Inodes:** filesystem objects and metadata
- **Dentries:** directory-entry and path-lookup information
- **Superblocks:** mounted filesystem information
- **File objects:** state associated with an open file

Useful commands:

```bash
findmnt
df -hT
stat /etc/hosts
ls -li /etc/hosts
cat /proc/filesystems
```

`df` reports filesystem capacity, while `du` walks directories and totals visible file sizes. Their results can differ because of deleted-but-still-open files, mount boundaries, metadata, snapshots, sparse files, or reserved space.

### 4.4 Device drivers

A driver translates the kernel's standard interfaces into operations understood by a particular hardware or virtual device.

Drivers can be:

- Built into the kernel image
- Compiled as loadable kernel modules

Inspect devices and drivers:

```bash
lspci -k
lsusb
lsblk
ip link
ls -l /sys/class/net
```

The `/dev` tree exposes device nodes to userspace, while `/sys` exposes the kernel's device model and attributes.

### 4.5 Network stack

The kernel implements core networking behavior, including:

- Network-device handling
- Ethernet and IP processing
- TCP and UDP
- Routing
- Sockets
- Packet filtering and connection tracking
- Network namespaces
- Traffic control

Useful commands:

```bash
ip -brief address
ip route
ss -lntup
sysctl net.ipv4.ip_forward
nft list ruleset
```

Applications normally work with sockets. The kernel handles packet construction, routing decisions, firewall rules, retransmission, and interaction with the network driver.

### 4.6 Inter-process communication

Processes communicate using mechanisms managed by the kernel:

- Pipes
- Signals
- Unix-domain sockets
- Network sockets
- Shared memory
- Message queues
- Futexes and other synchronization primitives

```bash
ls -l /proc/$$/fd
ss -lx
ipcs
```

### 4.7 Security

The kernel enforces several layers of security:

- User and group identities
- File modes and ACLs
- Process capabilities
- SELinux through the Linux Security Module framework
- Seccomp system-call filtering
- Namespaces for resource isolation
- Cgroups for resource accounting and control

On Rocky Linux:

```bash
id
getcap -r /usr/bin 2>/dev/null
getenforce
ls -Z /var/www/html
```

Root is powerful, but modern services can be designed with a smaller set of Linux capabilities instead of unrestricted root access.

---

## 5. Processes, Threads, and PID 1

The kernel represents processes and threads as schedulable tasks. Threads in one process share resources such as address space and open files but have separate execution state.

Each process has:

- A process ID (**PID**)
- A parent process ID (**PPID**)
- Credentials and capabilities
- Virtual memory mappings
- Open file descriptors
- Signal handlers
- Namespace and cgroup membership

On Rocky Linux, PID 1 is normally `systemd`:

```bash
ps -p 1 -o pid,comm,args
```

PID 1 starts and supervises userspace services and adopts orphaned processes. The kernel starts the first userspace process after completing early initialization.

### Signals

Signals are asynchronous notifications delivered through the kernel.

```bash
kill -TERM 1234    # Request graceful termination
kill -KILL 1234    # Kernel-enforced termination; cannot be caught
kill -HUP 1234     # Often used to request reload, if the program supports it
```

Use `SIGTERM` before `SIGKILL`. `SIGKILL` prevents cleanup, graceful shutdown, and application-level recovery.

---

## 6. Interrupts and Hardware Events

Hardware devices need a way to notify the CPU that work has completed or attention is required. An **interrupt** temporarily transfers control to a kernel handler.

Examples include:

- A network card receiving a packet
- A disk completing an I/O request
- A timer firing
- A keyboard event

```bash
cat /proc/interrupts
```

Kernel work triggered by an interrupt is divided so the most urgent work happens quickly and deferred work occurs later. This reduces the time the CPU spends with normal execution interrupted.

---

## 7. Kernel Modules

A kernel module is code that can be loaded into or removed from the running kernel, commonly for drivers, filesystems, or networking features.

```bash
lsmod                         # Loaded modules
modinfo xfs                   # Module metadata and parameters
sudo modprobe module_name     # Load a module with dependencies
sudo modprobe -r module_name  # Remove a module when safe
```

`modprobe` understands module dependencies and configuration; it is usually preferable to lower-level `insmod` and `rmmod`.

Locations and configuration:

```text
/lib/modules/$(uname -r)/     modules for the running kernel release
/etc/modprobe.d/              module options and blacklist configuration
```

Loading kernel code is a privileged and high-impact operation. A bad or untrusted module can compromise or crash the entire host. Secure Boot and module-signature enforcement may restrict which modules can load.

---

## 8. Kernel Interfaces in the Filesystem

### `/proc`

`procfs` presents live process and kernel information.

```bash
cat /proc/cpuinfo
cat /proc/meminfo
cat /proc/loadavg
cat /proc/$$/status
ls -l /proc/$$/fd
```

Numeric directories represent PIDs. Data changes as the system changes and is generated by the kernel rather than stored as ordinary persistent files.

### `/sys`

`sysfs` exposes devices, drivers, buses, modules, and kernel object relationships.

```bash
ls /sys/class/net
cat /sys/class/net/eth0/operstate
ls /sys/block
ls /sys/module
```

### `/dev`

Device nodes are special files that connect userspace operations to drivers.

```bash
ls -l /dev/null /dev/zero
lsblk
tty
```

### `/run`

`/run` stores volatile userspace runtime state such as PID files, sockets, and service metadata. It is recreated each boot.

The distinction matters:

| Path | Main purpose | Persistent? |
|---|---|---|
| `/proc` | Processes and kernel runtime state | No |
| `/sys` | Device and kernel object model | No |
| `/dev` | Device nodes | Dynamically managed |
| `/run` | Current-boot userspace runtime state | No |

---

## 9. Runtime Kernel Parameters

Many settings are exposed under `/proc/sys` and managed with `sysctl`.

Read a setting:

```bash
sysctl net.ipv4.ip_forward
cat /proc/sys/net/ipv4/ip_forward
```

Change the running value:

```bash
sudo sysctl -w net.ipv4.ip_forward=1
```

Create a persistent configuration:

```text
# /etc/sysctl.d/99-custom.conf
net.ipv4.ip_forward = 1
```

Then load and validate it:

```bash
sudo sysctl --system
```

Do not copy random “performance tuning” values into production. Kernel parameters interact with workload, memory, networking, and security. Establish a measured problem and test the change under representative load.

---

## 10. The Linux Boot Path

A simplified Rocky Linux boot sequence is:

```text
Power on
   │
   ▼
Firmware: BIOS or UEFI
   │
   ▼
Bootloader: normally GRUB 2
   │ loads kernel + initramfs
   ▼
Linux kernel starts
   │ initializes CPU, memory, and essential drivers
   ▼
initramfs provides early userspace
   │ locates and mounts the real root filesystem
   ▼
Kernel starts PID 1: systemd
   │
   ▼
systemd starts targets, services, mounts, and login sessions
```

Important files:

```text
/boot/vmlinuz-*       compressed bootable kernel image
/boot/initramfs-*     early userspace image and required drivers
/boot/grub2/          GRUB configuration on many BIOS installations
/boot/efi/            EFI System Partition mount on UEFI systems
```

Inspect the current boot:

```bash
uname -r
cat /proc/cmdline
journalctl -b
journalctl -k -b
systemd-analyze
systemd-analyze blame
```

The initramfs is important when the kernel requires drivers or logic before it can mount the real root filesystem—for example, storage, LVM, encryption, or RAID support.

---

## 11. Kernel Releases and Updates on Rocky Linux

Show the running release:

```bash
uname -r
```

Show installed kernel packages:

```bash
rpm -q kernel
dnf list installed 'kernel*'
```

Install available updates:

```bash
sudo dnf upgrade
```

Installing a kernel package places a new kernel on disk, but the current kernel continues running in memory. Reboot to use the new release:

```bash
sudo systemctl reboot
```

After reboot:

```bash
uname -r
```

Enterprise distributions may backport security and bug fixes without changing to the newest upstream major version. Do not judge patch status only by comparing the visible version number with the latest kernel.org release; check the distribution package changelog and security advisories.

Before a production reboot, verify:

- A maintenance window and rollback plan exist.
- The new kernel and initramfs are present in `/boot`.
- `/boot` has sufficient space.
- Required third-party modules are compatible.
- Console or out-of-band access is available.
- Cluster capacity can tolerate taking the node out of service.

---

## 12. Namespaces, Cgroups, and Containers

Containers do not normally contain their own kernel. Container processes share the host kernel.

### Namespaces isolate visibility

Linux namespaces can isolate:

- Process IDs
- Mount points
- Network stacks
- Hostnames
- Users and user IDs
- IPC resources
- Cgroup views

### Cgroups control resources

Control groups can account for and limit:

- CPU usage
- Memory
- I/O
- Number of processes

```bash
systemd-cgls
systemd-cgtop
cat /proc/self/cgroup
```

Container isolation depends on kernel mechanisms plus configuration. Containers are not virtual machines: a kernel vulnerability can affect isolation across containers on the same host.

---

## 13. Observability and Troubleshooting

### Kernel log

```bash
journalctl -k
journalctl -k -b
journalctl -k -b -1
dmesg --level=err,warn
```

Depending on security settings, reading all kernel messages may require elevated privileges.

Look for patterns involving:

- OOM kills
- Disk or filesystem errors
- Driver initialization failures
- Network-link changes
- Soft lockups or hung tasks
- Machine-check events
- SELinux denials, usually also inspected through audit logs

### CPU pressure

```bash
uptime
top
vmstat 1
pidstat 1
```

Ask whether CPU is genuinely busy, tasks are waiting for I/O, or a cgroup CPU quota is throttling a container.

### Memory pressure

```bash
free -h
vmstat 1
cat /proc/pressure/memory
journalctl -k | grep -i -E 'oom|out of memory|killed process'
```

### Storage and I/O

```bash
df -hT
lsblk -f
findmnt
iostat -xz 1
```

A filesystem at 100% capacity, inode exhaustion, a read-only remount, and slow block I/O are different problems and require different responses.

```bash
df -ih
findmnt -o TARGET,SOURCE,FSTYPE,OPTIONS
```

### Network

```bash
ip -s link
ip route
ss -s
ss -lntup
```

Start from evidence. Avoid rebooting immediately: a reboot may temporarily clear symptoms and remove the best live evidence of the cause.

---

## 14. Kernel Panic and System Failure

A **kernel panic** is a fatal kernel error from which safe continuation is not possible. It is different from a normal application crash.

Possible causes include:

- Kernel or driver bugs
- Failing hardware
- Corrupted memory
- Severe filesystem or storage problems
- Invalid third-party modules

For post-crash analysis, Linux can use `kdump` to boot a small capture kernel and save the crashed kernel's memory as a `vmcore`.

```bash
systemctl status kdump
kdumpctl status
```

Production investigation normally correlates:

- The crash dump
- Kernel and system logs
- Recent package or configuration changes
- Hardware-management logs
- Monitoring data before the failure

---

## 15. Practical Lab

Run these commands on a disposable Rocky Linux lab host. Read output before making changes.

### Identify the kernel

```bash
uname -a
cat /etc/rocky-release
cat /proc/cmdline
rpm -q kernel
```

### Explore kernel interfaces

```bash
cat /proc/loadavg
cat /proc/meminfo | head -n 15
ls /sys/class/net
ls /sys/block
ls -l /dev/null /dev/zero
```

### Inspect a process

```bash
sleep 300 &
LAB_PID=$!
cat /proc/$LAB_PID/status
ls -l /proc/$LAB_PID/fd
cat /proc/$LAB_PID/cgroup
kill -TERM $LAB_PID
```

### Observe a system call

```bash
sudo dnf install -y strace
strace -e trace=openat,read,write cat /etc/hostname
```

### Inspect modules and logs

```bash
lsmod | head
modinfo xfs
journalctl -k -b | tail -n 50
```

### Questions

1. Why can an application not directly read another process's memory?
2. What is the difference between a system call and a normal function call?
3. Why can load average be high while CPU usage is not 100%?
4. Why is low `free` memory not automatically a problem?
5. What role does VFS play when an application reads a file?
6. Why does a container share the host kernel?
7. Why does a newly installed kernel require a reboot?
8. When would `strace` be useful?
9. What is the difference between `/proc`, `/sys`, `/dev`, and `/run`?
10. Why should `SIGTERM` normally be tried before `SIGKILL`?

---

## 16. Interview-Level Summary

- The Linux kernel is a monolithic kernel with modular support: core services run in kernel space, and many components can be loaded as modules.
- Userspace applications request privileged work through system calls.
- The scheduler shares CPU time; the memory manager provides virtual memory and isolation.
- VFS presents a common file interface over many filesystem implementations.
- Drivers connect generic kernel subsystems to specific hardware or virtual devices.
- `/proc` exposes process and runtime state; `/sys` exposes kernel objects and devices; `/dev` exposes device nodes.
- Namespaces isolate what processes can see; cgroups account for and constrain resources.
- Containers share the host kernel and are therefore different from virtual machines.
- Kernel logs, pressure data, process state, and device statistics should be collected before disruptive troubleshooting.
- Rocky Linux may backport fixes, so an older-looking kernel version is not necessarily unpatched.

---

## References and Image Credits

- [The Linux Kernel documentation](https://docs.kernel.org/)
- [Core API documentation](https://docs.kernel.org/core-api/index.html)
- [Linux kernel architecture documentation](https://docs.kernel.org/arch/index.html)
- [Linux kernel interfaces — original image and license](https://commons.wikimedia.org/wiki/File:Linux_kernel_interfaces.svg)
- [Linux kernel diagram — original image and license](https://commons.wikimedia.org/wiki/File:Linux_kernel_diagram.svg)

