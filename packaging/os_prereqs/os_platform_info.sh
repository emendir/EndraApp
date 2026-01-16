

## Example usage:
# check_commands curl git jq
# check_commands "${required_commands[@]}"

export PYTHON="${PYTHON:-python}"
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
        echo "For Example:"
        echo "export PYTHON=/c/Python313/python"
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
# Example usage:
# check_commands curl git jq
# check_commands "${required_commands[@]}"

export PYTHON="${PYTHON:-python}"
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
        echo "For Example:"
        echo "export PYTHON=/c/Python313/python"
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
