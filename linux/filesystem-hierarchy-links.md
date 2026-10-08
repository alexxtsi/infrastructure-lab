\# Linux Filesystem Hierarchy, Inodes and Links



\## Goal



Understand how Linux presents storage and kernel information through one filesystem tree, and understand the relationship between:



```text

disk

→ block device

→ filesystem

→ mount point

→ directory entry

→ inode

→ data

```



This lab was performed on `ubuntu-admin`.



\---



\# 1. Linux Filesystem Hierarchy



Linux exposes one directory tree beginning at:



```text

/

```



Different filesystems can be attached to different locations in that tree.



Inspect the root filesystem:



```bash

findmnt /

```



Observed:



```text

TARGET SOURCE    FSTYPE OPTIONS

/      /dev/sda2 ext4   ...

```



This means:



```text

/dev/sda2

&#x20;   ↓

ext4 filesystem

&#x20;   ↓

mounted at /

```



Important distinction:



```text

/dev/sda2 = block device representing a partition

ext4      = filesystem stored on that partition

/         = mount point where the filesystem appears

```



\---



\# 2. Important Root Directories



\## `/etc`



Contains system-wide configuration.



Examples:



```text

/etc/ssh/sshd\_config

/etc/fstab

/etc/passwd

/etc/hosts

```



Configuration files do not need a `.conf` extension.



Mental model:



```text

/etc

→ how the system and services should behave

```



\---



\## `/var`



Contains variable data that changes while the system operates.



Examples:



```text

/var/log

/var/lib

/var/cache

/var/spool

/var/backups

```



Example:



```text

/etc/nginx/nginx.conf

&#x20;       ↓

configuration



/var/log/nginx/

&#x20;       ↓

runtime-generated data

```



\---



\## `/home`



Contains normal users' home directories.



Example:



```text

/home/atsigane

```



Typical contents:



```text

documents

repositories

scripts

.bashrc

.ssh/

.config/

.local/

```



Files and directories beginning with `.` are normally hidden from plain `ls`.



\---



\## `/usr`



Contains most installed userspace programs, libraries and shared data.



Examples:



```text

/usr/bin

/usr/sbin

/usr/lib

/usr/share

```



On this Ubuntu system:



```text

/bin  -> /usr/bin

/sbin -> /usr/sbin

/lib  -> /usr/lib

```



Inspect a command:



```bash

which ls

readlink -f "$(which ls)"

```



`/usr` does not mean "programs used only by normal users."



System services and administrators also use binaries and libraries under `/usr`.



\---



\## `/opt`



Typically used for optional or self-contained third-party software.



Example:



```text

/opt/company/application/

```



It may be empty on a normal system.



\---



\## `/boot`



Contains files involved in system boot.



Examples can include:



```text

kernel images

initramfs

bootloader-related files

```



\---



\## `/root`



The home directory of the `root` user.



It is separate from:



```text

/home

```



\---



\## `/tmp`



Used for temporary files created by users and applications.



Data here should not be considered permanent.



\---



\## `/srv`



Traditionally used for data provided by system services.



Our lab uses:



```text

/srv/baseline

```



for shared/service-related data.



\---



\## `/mnt`



Commonly used for manually or temporarily mounted filesystems.



\---



\## `/media`



Commonly used for removable media mounts.



\---



\# 3. Not Everything Under `/` Is Stored on the Root Disk



Inspect:



```bash

findmnt /proc

findmnt /sys

findmnt /dev

findmnt /run

```



Observed:



```text

/proc → proc

/sys  → sysfs

/dev  → devtmpfs

/run  → tmpfs

```



So although all of these appear inside the same directory tree, they are different filesystem types.



Conceptually:



```text

/

├── etc/     ext4

├── home/    ext4

├── usr/     ext4

├── var/     ext4

│

├── proc/    procfs

├── sys/     sysfs

├── dev/     devtmpfs

└── run/     tmpfs

```



\---



\# 4. `/proc`



`/proc` is a virtual filesystem called `procfs`.



It exposes information maintained by the kernel.



Examples:



```text

/proc/cpuinfo

/proc/meminfo

/proc/loadavg

/proc/uptime

```



Numeric directories usually represent processes:



```text

/proc/1

/proc/21472

```



Inspect the current shell:



```bash

echo $$

ls -ld /proc/$$

head /proc/$$/status

```



Conceptually:



```text

running process

&#x20;     ↓

kernel state

&#x20;     ↓

/proc/<PID>

```



These are not ordinary files stored on `/dev/sda2`.



\---



\# 5. `/sys`



`/sys` is a virtual filesystem called `sysfs`.



It exposes the kernel's device and object model.



Example:



```bash

ls /sys/class/net

```



Observed:



```text

enp0s3

enp0s8

lo

```



These correspond to network interfaces known to the kernel.



Another example:



```bash

ls /sys/class/block

```



\---



\# 6. `/dev`



`/dev` contains device nodes.



Inspect:



```bash

ls -l /dev/null /dev/tty /dev/sda

```



Observed:



```text

crw-rw-rw- /dev/null

brw-rw---- /dev/sda

crw-rw-rw- /dev/tty

```



The first character indicates the object type:



```text

c = character device

b = block device

```



Examples:



```text

/dev/sda  → block device representing the disk

/dev/tty  → terminal character device

/dev/null → special character device

```



Device nodes also have major and minor device numbers.



Example:



```text

/dev/sda → 8,0

```



Simplified model:



```text

userspace program

&#x20;     ↓

open("/dev/...")

&#x20;     ↓

kernel

&#x20;     ↓

device driver

&#x20;     ↓

hardware or virtual hardware

```



\---



\# 7. `/sys` vs `/dev`



Simplified relationship:



```text

hardware appears

&#x20;     ↓

kernel detects it

&#x20;     ↓

/sys exposes device information

&#x20;     ↓

udev reacts to device events

&#x20;     ↓

/dev contains device nodes

&#x20;     ↓

userspace programs use them

```



Example:



```text

/sys/class/block/sda

```



describes the disk from the kernel/device-model perspective.



```text

/dev/sda

```



is the device node programs can open to access the block device.



\---



\# 8. `/run`



`/run` is usually a `tmpfs`.



It stores runtime state such as:



```text

PID files

Unix sockets

locks

service runtime data

```



It is normally recreated during boot.



Example distinction:



```text

running process

&#x20;   ↓

/proc/<PID>



runtime state related to service

&#x20;   ↓

/run/...

```



\---



\# 9. Userspace and Kernel Space



Normal programs run in \*\*userspace\*\*.



Examples:



```text

bash

cat

ssh

git

python

nginx

```



The Linux kernel runs in \*\*kernel space\*\*.



The kernel manages:



```text

CPU scheduling

memory

filesystems

networking

device drivers

hardware access

```



A userspace program asks the kernel to perform operations using \*\*system calls\*\*.



Example:



```text

cat file.txt

&#x20;     ↓

open/read/write system calls

&#x20;     ↓

kernel

&#x20;     ↓

VFS/filesystem

&#x20;     ↓

data

```



Even a process running as `root` is still a userspace process.



```text

root != kernel

```



\---



\# 10. System Calls



A system call is the controlled mechanism a userspace process uses to request a service from the kernel.



Examples:



```text

open/openat

read

write

close

socket

connect

execve

mmap

```



Simplified example:



```text

userspace program

&#x20;     ↓

open()

&#x20;     ↓

system-call boundary

&#x20;     ↓

kernel executes request

&#x20;     ↓

result returned to userspace

```



\---



\# 11. Virtual File System — VFS



Linux supports many filesystem implementations:



```text

ext4

tmpfs

procfs

sysfs

NFS

...

```



Programs do not need to understand each filesystem individually.



The kernel provides the \*\*Virtual File System layer\*\*.



Simplified:



```text

userspace program

&#x20;     ↓

system call

&#x20;     ↓

VFS

&#x20;     ↓

specific filesystem implementation

&#x20;     ↓

data

```



Example:



```bash

cat file.txt

```



roughly causes:



```text

openat()

↓

VFS path lookup

↓

filesystem

↓

inode

↓

read()

↓

data returned to program

```



\---



\# 12. Inodes



A filename is not the file itself.



Simplified model:



```text

directory entry

"file.txt"

&#x20;     ↓

inode

&#x20;     ↓

file data

```



An inode contains filesystem metadata such as:



```text

owner

group

permissions

timestamps

size

link count

references to file data

```



Inspect:



```bash

ls -li FILE

stat FILE

```



\---



\# 13. Hard Links



Create:



```bash

printf "Linux is interesting\\n" > original.txt

ln original.txt hardlink.txt

```



Inspect:



```bash

ls -li

stat original.txt

stat hardlink.txt

```



A hard link creates another directory entry pointing to the same inode.



```text

original.txt ─┐

&#x20;             ├──→ inode → data

hardlink.txt ─┘

```



The inode link count increases.



Writing through either pathname modifies the same data:



```bash

echo "new line" >> hardlink.txt

cat original.txt

```



\---



\# 14. Symbolic Links



Create:



```bash

ln -s original.txt symlink.txt

```



Inspect:



```bash

ls -li

readlink symlink.txt

```



A symbolic link has its own inode and stores a pathname.



```text

symlink.txt

&#x20;    ↓

"original.txt"

&#x20;    ↓

target file

```



If the target pathname disappears, the symlink becomes dangling.



Example:



```bash

rm original.txt



cat hardlink.txt

cat symlink.txt

```



Result:



```text

hard link → still works

symlink   → broken

```



Because:



```text

hardlink.txt → inode directly



symlink.txt → pathname "original.txt"

&#x20;                      ↓

&#x20;                no longer exists

```



\---



\# 15. `rm` and `unlink`



Removing a filename does not necessarily mean the data immediately disappears.



Conceptually:



```text

rm original.txt

&#x20;       ↓

remove directory-entry reference

&#x20;       ↓

decrease inode link count

```



The underlying data can remain while another hard link still references the inode.



This relates to the Unix/Linux `unlink()` operation.



\---



\# 16. File Descriptors



When a process opens a file, the kernel gives that process a small integer called a \*\*file descriptor\*\*.



Standard descriptors:



```text

0 → stdin

1 → stdout

2 → stderr

```



Additional open files may use:



```text

3

4

5

...

```



Simplified:



```text

process

&#x20; ↓

file descriptor

&#x20; ↓

kernel open-file state

&#x20; ↓

inode

&#x20; ↓

data

```



File descriptors will be revisited later with:



```text

/proc/<PID>/fd

lsof

pipes

sockets

processes

deleted-open files

```



\---



\# 17. Core Mental Models



\## Storage



```text

disk

&#x20;↓

block device

&#x20;↓

partition

&#x20;↓

filesystem

&#x20;↓

mount point

&#x20;↓

directory tree

```



\## File



```text

directory entry / filename

&#x20;       ↓

inode

&#x20;       ↓

data

```



\## File Access



```text

userspace process

&#x20;       ↓

system call

&#x20;       ↓

kernel

&#x20;       ↓

VFS

&#x20;       ↓

filesystem

&#x20;       ↓

inode

&#x20;       ↓

data

```

