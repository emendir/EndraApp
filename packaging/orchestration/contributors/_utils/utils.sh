ask_yes_no() {
    local prompt="$1"
    local default="$2"   # "y", "n", or empty for no default
    local answer

    while true; do
        case "$default" in
            y)  read -rp "$prompt [Y/n]: " answer ;;
            n)  read -rp "$prompt [y/N]: " answer ;;
            *)  read -rp "$prompt [y/n]: " answer ;;
        esac

        # Apply default if input is empty
        if [[ -z "$answer" && -n "$default" ]]; then
            answer="$default"
        fi
        echo ""

        case "$answer" in
            [Yy]|[Yy][Ee][Ss]) return 0 ;;
            [Nn]|[Nn][Oo])     return 1 ;;
            *) echo "Please answer yes or no." ;;
        esac
    done
}




# Detect if the script is being executed instead of sourced
(return 0 2>/dev/null) && sourced=1 || sourced=0
if [ "$sourced" -eq 0 ]; then
    echo "Error: This script must be sourced, not executed." >&2
    exit 1
fi

