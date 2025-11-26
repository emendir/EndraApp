#!/usr/bin/env bash
# set -euo pipefail

# the absolute path of this script's directory
_SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 ; pwd -P )"
PROJ_DIR="$( cd -- "${_SCRIPT_DIR}/../../../" >/dev/null 2>&1 ; pwd -P )"

check_commands() {
    local missing=()

    for cmd in "$@"; do
        if ! command -v "$cmd" >/dev/null 2>&1; then
            missing+=("$cmd")
        fi
    done

    if (( ${#missing[@]} > 0 )); then
        echo "ERROR: The following required commands are missing:" >&2
        printf '  - %s\n' "${missing[@]}" >&2
        return 1
    fi
}

## Example usage:
# check_commands curl git jq
# check_commands "${required_commands[@]}"

PYTHON="${PYTHON:-python}"
OS=$($PYTHON -c "import platform;print(platform.system())")
ARCH=$($PYTHON -c "import platform;print(platform.machine())")
echo "Platform: $OS"
echo "Architecture: $ARCH"
echo "Python: $PYTHON"

# Determine platform-specific requirements directory
case "$OS" in
    Linux)
        PLATFORM_BASE="linux"
        ;;
    Darwin)
        PLATFORM_BASE="macos"
        ;;
    Windows)
        PLATFORM_BASE="windows"
        ;;
    *)
        echo "Error: Unsupported platform: $OS"
        echo "If using MSYS2 on Windows, make sure you set the PYTHON environment variable to your native windows python executable."
        exit 1
        ;;
esac

# Normalize architecture names
case "$ARCH" in
    x86_64|AMD64|amd64)
        ARCH_DIR="x86_64"
        ;;
    aarch64|arm64|ARM64)
        ARCH_DIR="arm64"
        ;;
    *)
        echo "Error: Unsupported architecture: $ARCH"
        exit 1
        ;;
esac


add_to_windows_system_path() {
    local posix_path="$1"

    if [[ -z "$posix_path" ]]; then
        echo "Usage: add_to_windows_system_path <path>"
        return 1
    fi

    # Convert MSYS2/POSIX path → Windows path
    local win_path
    win_path=$(cygpath -w "$posix_path")

    echo "Windows path to add: $win_path"

    # Read current Windows SYSTEM PATH using PowerShell
    local current_sys_path
    current_sys_path=$(powershell -NoProfile -Command \
        '[Environment]::GetEnvironmentVariable("Path", "Machine")')

    if [[ -z "$current_sys_path" ]]; then
        echo "ERROR: Could not read system PATH. Are you running as Administrator?"
        return 1
    fi

    echo "Current system PATH length: ${#current_sys_path}"

    # Check if already present
    case ";$current_sys_path;" in
        *";$win_path;"*)
            echo "System PATH already contains: $win_path"
            return 0
            ;;
    esac

    # Append our directory
    local new_sys_path="${current_sys_path};${win_path}"

    echo "Updating system PATH..."

    # Safely update without truncation
    powershell -NoProfile -Command \
        "[Environment]::SetEnvironmentVariable('Path', '$new_sys_path', 'Machine')"

    echo "Done. Restart terminals or applications to see the updated PATH."
}
