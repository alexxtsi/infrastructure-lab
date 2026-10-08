\# Linux Permissions, Ownership, Groups and ACLs



\## Goal



Understand how Linux decides whether a process can access a filesystem object.



Topics:



```text

rwx permissions

users and groups

directory traversal

setgid

umask

ACLs

find

permission troubleshooting

```



\---



\# 1. Traditional Linux Permissions



Example:



```text

\-rw-r--r--

```



Breakdown:



```text

\-   rw-   r--   r--

│    │     │     │

│    │     │     └── others

│    │     └──────── group

│    └────────────── owner

└─────────────────── object type

```



For files:



```text

r = read contents

w = modify contents

x = execute

```



\---



\# 2. Directory Permissions



Permissions have different meanings on directories.



```text

r = list directory entries

w = create/delete/rename entries

x = traverse/search through directory

```



The `x` permission on directories is especially important.



A file can have readable permissions but still be inaccessible if the process cannot traverse a parent directory.



\---



\# 3. Path Traversal



Example:



```text

/home/atsigane/labs/permissions/shared/data.txt

```



To access the file, the process may need to traverse:



```text

/

↓

home

↓

atsigane

↓

labs

↓

permissions

↓

shared

↓

data.txt

```



Useful command:



```bash

namei -l /path/to/file

```



It displays ownership and permissions for each path component.



\---



\# 4. Relative vs Absolute Paths



A process has a current working directory.



Inspect the current shell:



```bash

readlink /proc/$$/cwd

```



Example:



```text

/home/atsigane/labs/permissions

```



A relative pathname:



```bash

cat shared/data.txt

```



starts resolution from the current working directory.



An absolute pathname:



```bash

cat /home/atsigane/labs/permissions/shared/data.txt

```



starts from `/`.



This can produce different permission behavior when a process already has a reference to its current directory.



\---



\# 5. Users and Groups



Inspect user identity:



```bash

id USER

```



Inspect group:



```bash

getent group GROUP

```



Example:



```bash

id baselineuser

getent group baselineops

```



Linux access decisions depend on the process credentials:



```text

UID

primary GID

supplementary groups

```



\---



\# 6. Shared Directory With setgid



Create:



```bash

sudo mkdir -p /srv/baseline

sudo chown root:baselineops /srv/baseline

sudo chmod 2770 /srv/baseline

```



Inspect:



```bash

ls -ld /srv/baseline

```



Example:



```text

drwxrws--- root baselineops /srv/baseline

```



The leading:



```text

2

```



in:



```text

2770

```



enables the \*\*setgid bit\*\*.



For a directory, setgid causes newly created children to inherit the directory's group.



Example:



```text

/srv/baseline

owner = root

group = baselineops

setgid = enabled

&#x20;      ↓

baselineuser creates file

&#x20;      ↓

owner = baselineuser

group = baselineops

```



Important:



```text

owner → creator

group → inherited from setgid directory

```



setgid does not change the owner to `root`.



\---



\# 7. Umask



A umask removes permission bits during file/directory creation.



Inspect:



```bash

umask

umask -S

```



Observed:



```text

atsigane     → 0002

baselineuser → 0022

```



Normal regular files commonly request:



```text

666 = rw-rw-rw-

```



For `atsigane`:



```text

requested: 666

umask:     002

result:    664

```



Result:



```text

rw-rw-r--

```



For `baselineuser`:



```text

requested: 666

umask:     022

result:    644

```



Result:



```text

rw-r--r--

```



This explained:



```text

from-atsigane.txt

\-rw-rw-r--



from-baselineuser.txt

\-rw-r--r--

```



even though both inherited:



```text

group = baselineops

```



\---



\# 8. Files vs Directories and Umask



Normal files commonly start from:



```text

666

```



because files should not become executable automatically.



Directories commonly start from:



```text

777

```



Example with umask `002`:



```text

file:

666 → 664



directory:

777 → 775

```



\---



\# 9. ACL Tools



Install:



```bash

sudo apt install acl

```



Commands:



```bash

getfacl

setfacl

```



ACLs allow more detailed permissions than:



```text

owner

group

other

```



\---



\# 10. Default ACL



A directory can define ACL rules that new children inherit.



Example:



```bash

sudo setfacl -d -m g:baselineops:rwx /srv/baseline

```



Inspect:



```bash

getfacl /srv/baseline

```



Example:



```text

default:user::rwx

default:group::rwx

default:group:baselineops:rwx

default:mask::rwx

default:other::---

```



`default:` means:



```text

these rules are used when creating children

```



\---



\# 11. Access ACL vs Default ACL



A directory can have:



```text

access ACL

\+

default ACL

```



The access ACL controls access to the directory itself.



The default ACL determines ACL inheritance for future children.



Example:



```text

/srv/baseline

&#x20;    ↓ default ACL



/srv/baseline/newdir

&#x20;    ├── access ACL

&#x20;    └── default ACL inherited for future children

```



A regular file receives an access ACL but does not need a default ACL because it cannot contain children.



\---



\# 12. ACL Mask



Example:



```text

user::rw-

group::rwx                    #effective:rw-

group:baselineops:rwx         #effective:rw-

mask::rw-

other::---

```



The ACL entry says:



```text

baselineops → rwx

```



but the ACL mask says:



```text

rw-

```



Therefore the effective permission is:



```text

rwx AND rw-

=

rw-

```



This is why `getfacl` displays:



```text

\#effective:rw-

```



\---



\# 13. Why a New File Did Not Become Executable



The directory default ACL contained:



```text

default:group:baselineops:rwx

```



but a normal file creation typically requests only:



```text

0666

```



Therefore execute permission does not automatically appear.



Conceptually:



```text

default ACL

\+

permissions requested during creation

&#x20;       ↓

new object's access ACL

```



The default ACL is not simply copied byte-for-byte.



\---



\# 14. Extended ACL Indicator



When `ls -l` shows:



```text

\-rw-rw----+

&#x20;        ^

```



the `+` indicates additional ACL information.



Inspect it with:



```bash

getfacl FILE

```



This matters because `ls -l` alone may not reveal the whole access-control configuration.



\---



\# 15. Searching With `find`



Find configuration files:



```bash

find \~/labs/find -type f -name "\*.conf"

```



Find executable files:



```bash

find \~/labs/find -type f -executable

```



Find exact permissions:



```bash

find \~/labs/find -type f -perm 600 -ls

```



Find files belonging to a user:



```bash

find /srv/baseline -type f -user baselineuser -ls

```



Observed:



```text

from-baselineuser.txt

from-baselineuser-2.txt

acl-test.txt

```



Find files belonging to a group:



```bash

find /srv/baseline -type f -group baselineops -ls

```



Find `.conf` files owned by `atsigane`:



```bash

find \~/labs/find -type f -user atsigane -name "\*.conf" -ls

```



Find world-writable regular files:



```bash

find \~/labs/find -type f -perm -o=w -ls

```



\---



\# 16. Permission Troubleshooting Workflow



If a process receives:



```text

Permission denied

```



do not immediately run:



```bash

chmod 777

```



Instead determine:



```text

1\. Which user is the process running as?

2\. Which groups does it belong to?

3\. Can it traverse every required directory?

4\. Who owns the target object?

5\. What are the normal mode bits?

6\. Is setgid involved?

7\. Does an ACL exist?

8\. What is the ACL mask?

9\. What exact operation is required?

```



Useful commands:



```bash

id USER



namei -l /path/to/file



ls -ld /path/to/directory

ls -l /path/to/file



getfacl /path/to/directory

getfacl /path/to/file

```



Then:



```text

identify exact missing permission

&#x20;       ↓

apply smallest correct change

&#x20;       ↓

test as actual user/service account

&#x20;       ↓

verify

```



\---



\# 17. Core Mental Model



When Linux evaluates access:



```text

process UID/GIDs

&#x20;      ↓

pathname traversal

&#x20;      ↓

directory permissions

&#x20;      ↓

file owner/group/mode

&#x20;      ↓

ACL entries

&#x20;      ↓

ACL mask

&#x20;      ↓

allow or deny operation

```



For shared directories:



```text

setgid

→ controls inherited group



umask

→ removes permissions at creation



default ACL

→ defines inherited ACL policy



ACL mask

→ limits effective ACL permissions

```

