# Path to your oh-my-zsh installation.
export ZSH="$HOME/.oh-my-zsh"

# Set name of the theme to load --- if set to "random", it will
# load a random theme each time oh-my-zsh is loaded, in which case,
# to know which specific one was loaded, run: echo $RANDOM_THEME
# See https://github.com/ohmyzsh/ohmyzsh/wiki/Themes
ZSH_THEME="robbyrussell"

# auto-update behavior
zstyle ':omz:update' mode reminder  # just remind me to update when it's time

# Uncomment the following line to enable command auto-correction.
ENABLE_CORRECTION="true"

# Which plugins would you like to load?
# Standard plugins can be found in $ZSH/plugins/
# Custom plugins may be added to $ZSH_CUSTOM/plugins/
# Example format: plugins=(rails git textmate ruby lighthouse)
# Add wisely, as too many plugins slow down shell startup.
plugins=(
	git
	zsh-autosuggestions
)

source $ZSH/oh-my-zsh.sh

######################### My changes #########################
# Change PATH env variable
REPO_DIR=~/Library/Mobile\ Documents/com~apple~CloudDocs/scripts_and_dotfiles
# https://unix.stackexchange.com/a/633011
export PATH=$PATH:.:$REPO_DIR/bash_scripts:$REPO_DIR/private_scripts:$(find ${REPO_DIR}/python_scripts -type d -maxdepth 1 | paste -sd ":" -)
#########################
# load file with aliases
. ~/.zsh_aliases
#########################
# cd directly on Desktop 
cd ~/Desktop
#########################
# conda inizialization
# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/opt/anaconda3/bin/conda' 'shell.zsh' 'hook' 2> /dev/null)"
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
# Show absolute path on zsh prompt: https://stackoverflow.com/a/62203156
PROMPT=${PROMPT/\%c/\%~}
#########################