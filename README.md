# Linux Forensics + Incident Response Toolkit

[![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) 
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/) 
[![Linux](https://img.shields.io/badge/Linux-Ubuntu-orange)](https://ubuntu.com/) 
[![ps](https://img.shields.io/badge/ps-procps-green)](https://gitlab.com/procps-ng/procps) 
[![iptables](https://img.shields.io/badge/iptables-GPL-red)](https://netfilter.org/projects/iptables/index.html) 
[![GitHub Actions](https://github.com/FatonHaxhiu/linux-ir-toolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/FatonHaxhiu/linux-ir-toolkit/actions/workflows/ci.yml)




## Overview

This toolkit automates the collection, hashing, packaging, and basic reporting of forensic artifacts from a Linux system. Designed for incident response (IR) scenarios, it helps security analysts and system administrators quickly gather critical system information to investigate potential compromises or suspicious activity.

The toolkit collects processes, network info, configuration files, logs, user activity, and more — packaging everything securely for further analysis.

---

## Features

- Collects system artifacts such as:
  - Process list (`ps auxf`)
  - Network connections (`netstat -tulpen`)
  - Open files (`lsof`)
  - Kernel modules (`lsmod`)
  - Kernel messages (`dmesg --ctime`)
  - `/etc/passwd`, `/etc/shadow`, `/etc/sudoers`
  - `/var/log/auth.log`, `/var/log/syslog`
  - Crontab + `/etc/cron*`
  - User bash history
  - User `.ssh/` directory
  - Login sessions (`who`, `w`, `last`, `lastlog`)
  - Hostname/DNS config (`/etc/hosts`, `/etc/resolv.conf`)
  - Firewall rules (`iptables -L`)
  - SHA-256 hash manifest
  - Markdown report

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
   git clone https://github.com/FatonHaxhiu/linux-ir-toolkit.git
   cd linux-ir-toolkit

## Usage

Run the toolkit using Python 3:

```bash
python3 src/collector.py [options]
