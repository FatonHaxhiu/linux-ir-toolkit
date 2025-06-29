import subprocess
import hashlib
import os
from datetime import datetime
import tarfile
import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        description="Linux Forensics + Incident Response Toolkit"
    )
    parser.add_argument(
        "--output", "-o", default=None, help="Output directory (default: timestamped)"
    )
    parser.add_argument(
        "--package",
        "-p",
        action="store_true",
        help="Package artifacts into a tar.gz archive",
    )
    parser.add_argument(
        "--encrypt",
        action="store_true",
        help="Encrypt archive with GPG (AES256 symmetric)",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose output"
    )
    return parser.parse_args()


def log(message, verbose):
    if verbose:
        print(message)


ARTIFACT_DIR = f"artifacts_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
os.makedirs(ARTIFACT_DIR, exist_ok=True)


def save_command_output(cmd, outfile, verbose=False):
    log(f"Running command: {' '.join(cmd)} -> {outfile}", verbose)
    with open(os.path.join(ARTIFACT_DIR, outfile), "w") as f:
        subprocess.run(cmd, stdout=f, stderr=subprocess.DEVNULL, text=True)


def save_file_copy(src, dest, verbose=False):
    if os.path.exists(src):
        log(f"Copying file: {src} -> {dest}", verbose)
        with open(src, "r") as f_src, open(
            os.path.join(ARTIFACT_DIR, dest), "w"
        ) as f_dst:
            f_dst.write(f_src.read())


def compute_hash(filepath):
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def package_artifacts(encrypt=False):
    archive_name = ARTIFACT_DIR + ".tar.gz"
    with tarfile.open(archive_name, "w:gz") as tar:
        tar.add(ARTIFACT_DIR)
    print(f"Artifacts packaged into {archive_name}")

    if encrypt:
        enc_name = archive_name + ".gpg"
        subprocess.run(
            [
                "gpg",
                "--symmetric",
                "--cipher-algo",
                "AES256",
                "-o",
                enc_name,
                archive_name,
            ]
        )
        print(f"Encrypted archive created: {enc_name}")


def collect_cron_jobs(verbose=False):
    save_command_output(["crontab", "-l"], "crontab.txt", verbose)
    save_command_output(["ls", "-lR", "/etc/cron*"], "cron_dirs.txt", verbose)


def collect_user_artifacts(verbose=False):
    home = os.path.expanduser("~")
    save_file_copy(os.path.join(home, ".bash_history"), "bash_history", verbose)
    ssh_dir = os.path.join(home, ".ssh")
    if os.path.isdir(ssh_dir):
        save_command_output(["ls", "-lR", ssh_dir], "ssh_dir_listing.txt", verbose)
        for file in os.listdir(ssh_dir):
            file_path = os.path.join(ssh_dir, file)
            save_file_copy(file_path, f"ssh_{file}", verbose)


def collect_login_history(verbose=False):
    save_command_output(["who"], "who.txt", verbose)
    save_command_output(["w"], "w.txt", verbose)
    save_command_output(["last"], "last.txt", verbose)
    save_command_output(["lastlog"], "lastlog.txt", verbose)


def collect_network_config(verbose=False):
    save_file_copy("/etc/hosts", "hosts", verbose)
    save_file_copy("/etc/resolv.conf", "resolv.conf", verbose)
    save_command_output(["iptables", "-L"], "iptables.txt", verbose)


def generate_report():
    report_path = os.path.join(ARTIFACT_DIR, "report.md")
    with open(report_path, "w") as f:
        f.write("# Incident Response Report\n\n")
        f.write(f"Generated on: {datetime.now()}\n\n")
        f.write("## Collected Artifacts\n")
        for root, _, files in os.walk(ARTIFACT_DIR):
            for file in files:
                if file != "report.md":
                    f.write(f"- {file}\n")


def main():
    args = parse_args()

    global ARTIFACT_DIR
    if args.output:
        ARTIFACT_DIR = args.output
    else:
        ARTIFACT_DIR = f"artifacts_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    os.makedirs(ARTIFACT_DIR, exist_ok=True)

    save_command_output(["ps", "auxf"], "processes.txt", args.verbose)
    save_command_output(["netstat", "-tulpen"], "netstat.txt", args.verbose)
    save_command_output(["lsof"], "lsof.txt", args.verbose)
    save_command_output(["lsmod"], "lsmod.txt", args.verbose)
    save_command_output(["dmesg", "--ctime"], "dmesg.txt", args.verbose)

    save_file_copy("/etc/passwd", "passwd", args.verbose)
    save_file_copy("/etc/shadow", "shadow", args.verbose)
    save_file_copy("/etc/sudoers", "sudoers", args.verbose)
    save_file_copy("/var/log/auth.log", "auth.log", args.verbose)
    save_file_copy("/var/log/syslog", "syslog", args.verbose)

    collect_cron_jobs(args.verbose)
    collect_user_artifacts(args.verbose)
    collect_login_history(args.verbose)
    collect_network_config(args.verbose)

    manifest = []
    for root, _, files in os.walk(ARTIFACT_DIR):
        for name in files:
            path = os.path.join(root, name)
            filehash = compute_hash(path)
            manifest.append(f"{name}\t{filehash}")

    with open(os.path.join(ARTIFACT_DIR, "manifest.txt"), "w") as f:
        f.write("\n".join(manifest))

    if args.package:
        package_artifacts(encrypt=args.encrypt)

    generate_report()


if __name__ == "__main__":
    main()
