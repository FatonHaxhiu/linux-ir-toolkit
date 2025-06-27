import subprocess
import hashlib
import os
from datetime import datetime
import tarfile
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Linux IR Toolkit")
    parser.add_argument('--output', '-o', default=None, help="Output directory (default: timestamped)")
    parser.add_argument('--package', '-p', action='store_true', help="Package artifacts into a tar.gz archive")
    # Add more args like --report, --verbose later
    return parser.parse_args()

ARTIFACT_DIR = f"artifacts_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
os.makedirs(ARTIFACT_DIR, exist_ok=True)

def save_command_output(cmd, outfile):
    with open(os.path.join(ARTIFACT_DIR, outfile), 'w') as f:
        subprocess.run(cmd, stdout=f, stderr=subprocess.DEVNULL, text=True)

def save_file_copy(src, dest):
    if os.path.exists(src):
        with open(src, 'r') as f_src, open(os.path.join(ARTIFACT_DIR, dest), 'w') as f_dst:
            f_dst.write(f_src.read())

def compute_hash(filepath):
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            sha256.update(chunk)
    return sha256.hexdigest()

def package_artifacts():
    archive_name = ARTIFACT_DIR + '.tar.gz'
    with tarfile.open(archive_name, 'w:gz') as tar:
        tar.add(ARTIFACT_DIR)
    print(f"Artifacts packaged into {archive_name}")

def main():
    args = parse_args()
    global ARTIFACT_DIR
    if args.output:
        ARTIFACT_DIR = args.output
    else:
        ARTIFACT_DIR = f"artifacts_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    os.makedirs(ARTIFACT_DIR, exist_ok=True)
    # Collect process list
    save_command_output(['ps', 'auxf'], 'processes.txt')
    # Collect network info
    save_command_output(['netstat', '-tulpen'], 'netstat.txt')
    # Collect open files
    save_command_output(['lsof'], 'lsof.txt')
    # Collect kernel modules and messages
    save_command_output(['lsmod'], 'lsmod.txt')
    save_command_output(['dmesg', '--ctime'], 'dmesg.txt')

    # Copy important config files
    save_file_copy('/etc/passwd', 'passwd')
    save_file_copy('/etc/shadow', 'shadow')
    save_file_copy('/etc/sudoers', 'sudoers')
    # Logs
    save_file_copy('/var/log/auth.log', 'auth.log')
    save_file_copy('/var/log/syslog', 'syslog')

    # TODO: Add more artifacts: cron jobs, bash history, etc.

    # Compute hashes for all collected files
    manifest = []
    for root, _, files in os.walk(ARTIFACT_DIR):
        for name in files:
            path = os.path.join(root, name)
            filehash = compute_hash(path)
            manifest.append(f"{name}\t{filehash}")

    # Write manifest file
    with open(os.path.join(ARTIFACT_DIR, 'manifest.txt'), 'w') as f:
        f.write('\n'.join(manifest))

    # Package all artifacts into a .tar.gz archive
    if args.package:
        package_artifacts()

if __name__ == '__main__':
    main()
