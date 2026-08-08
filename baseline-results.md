# Baseline Assessment

| Task | Score | Evidence | Gap |
|---|---|---|---|
| Create sudo user | YELLOW | `id baselineuser`, `sudo whoami`, `/home/baselineuser` exists | Knew `useradd`, but needed help with `-m`, adding the user to the `sudo` group, and verification |
| Group-protected directory | YELLOW | Created `baselineops`, added `baselineuser`, set `/srv/baseline` group ownership, verified access with `id`, `ls -ld`, and `sudo -u baselineuser` | Needed help understanding `sudo`, `chgrp`, directory permissions, and changing mode to `770`|
| Find five largest files | YELLOW | Built `find / ... -printf "%s %p\n" 2>/dev/null \| sort -nr \| head -n 5` using `man` and `--help` | Needed to learn `-xdev`; initial result included virtual files such as `/proc/kcore` |
| Identify listening port | YELLOW | Used `ss -lntp` / `sudo ss -lntp`; identified TCP `22` listening on IPv4 and IPv6 and connected it to `sshd` | Needed help distinguishing `LISTEN` from `ESTAB` and understanding service-name vs process/port identification |
| Restart service | YELLOW | Identified `ssh.service`, inspected it with `systemctl status`, restarted it with `sudo systemctl restart ssh.service`, and verified TCP 22 was still listening | Learned that service restart requires elevated privileges and that `systemctl` may use polkit when run without `sudo` |
| Read service logs | YELLOW | Used `journalctl`, filtering and `tail -n`; identified SSH disconnects and restart activity | Needed to learn `sudo journalctl -u ssh.service -n 20 --no-pager` and the difference between text filtering and querying a systemd unit |
| Python log parser | | | |
| Git branch/commit/merge | | | |