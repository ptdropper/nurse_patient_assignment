import subprocess

def get_git_version():
    try:
        version = subprocess.check_output(
            ['git', 'describe', '--tags', '--always'],
            stderr=subprocess.DEVNULL
        ).decode('utf-8').strip()
        return version
    except Exception:
        return "unknown"

if __name__ == "__main__":
    version = get_git_version()
    with open("version.txt", "w") as f:
        f.write(version)