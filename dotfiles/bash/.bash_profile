######################### My changes #########################
# Change PATH env variable
REPO_DIR=~/Library/Mobile\ Documents/com~apple~CloudDocs/scripts_and_dotfiles
# https://unix.stackexchange.com/a/633011
export PATH=$PATH:.:$REPO_DIR/bash_scripts:$REPO_DIR/private_scripts:$(find ${REPO_DIR}/python_scripts -type d -maxdepth 1 | paste -sd ":" -)
#########################
# colorized ls
alias ls='ls -G'
#########################
# cd directly on Desktop 
cd ~/Desktop
#########################
# conda inizialization
# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/opt/anaconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/opt/anaconda3/etc/profile.d/conda.sh" ]; then
        . "/opt/anaconda3/etc/profile.d/conda.sh"
    else
        export PATH="/opt/anaconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<
#########################
# brew inizialization
# Source: https://github.com/Homebrew/install/blob/9d6f09136c472978b4b18294d895010077008744/install.sh#L119-L129
UNAME_MACHINE="$(/usr/bin/uname -m)"

if [[ "${UNAME_MACHINE}" == "arm64" ]]
then
    # On ARM macOS, this script installs to /opt/homebrew only
    HOMEBREW_PREFIX="/opt/homebrew"
    HOMEBREW_REPOSITORY="${HOMEBREW_PREFIX}"
else
    # On Intel macOS, this script installs to /usr/local only
    HOMEBREW_PREFIX="/usr/local"
    HOMEBREW_REPOSITORY="${HOMEBREW_PREFIX}/Homebrew"
fi
eval "$(${HOMEBREW_REPOSITORY}/bin/brew shellenv)"
#########################
