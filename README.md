# Linux Forensics + Incident Response Toolkit

[![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)  
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)  
[![Linux](https://img.shields.io/badge/Linux-Ubuntu-orange)](https://ubuntu.com/)  
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-automated-green)](https://github.com/features/actions)
[![ps](https://img.shields.io/badge/ps-procps-green)](https://gitlab.com/procps-ng/procps)  
[![netstat](https://img.shields.io/badge/netstat-net-tools-blue)](https://sourceforge.net/projects/net-tools/)  
[![iptables](https://img.shields.io/badge/iptables-GPL-red)](https://netfilter.org/projects/iptables/index.html)  



## Overview

This toolkit automates the collection, hashing, packaging, and basic reporting of forensic artifacts from a Linux system. Designed for incident response (IR) scenarios, it helps security analysts and system administrators quickly gather critical system information to investigate potential compromises or suspicious activity.

The toolkit collects processes, network info, configuration files, logs, user activity, and more — packaging everything securely for further analysis.

---

## Features

- Collects system artifacts such as:
  - Running processes (`ps auxf`)
  - Network connections and open ports (`netstat -tulpen`)
  - Open files (`lsof`)
  - Kernel modules and messages (`lsmod`, `dmesg`)
  - Important configuration files (`/etc/passwd`, `/etc/shadow`, `/etc/sudoers`)
  - User bash history and cron jobs
  - Installed packages, login history, and firewall rules

- Computes SHA256 hashes for collected files (chain of custody)

- Packages all artifacts into a timestamped `.tar.gz` archive

- Generates a basic Markdown report summarizing collected data

- CLI support for customizable output directory, packaging, and verbosity

- Graceful error handling and permission checks

---

## Tools & Technologies Used

- **Python 3.8+** — primary language for scripting  
- **Linux utilities** — `ps`, `netstat`, `lsof`, `lsmod`, `dmesg`, `crontab`, `iptables`  
- **WSL (Windows Subsystem for Linux)** — recommended development and testing environment on Windows 11  
- **Git & GitHub** — version control and repository hosting  
- Optional: Docker (for containerized testing)

---

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/linux-ir-toolkit.git
   cd linux-ir-toolkit
