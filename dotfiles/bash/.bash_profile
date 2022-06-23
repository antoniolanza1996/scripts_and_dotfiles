######################### My changes #########################
# Change PATH env variable
repo_dir=~/Library/Mobile\ Documents/com~apple~CloudDocs/scripts_and_dotfiles
# https://unix.stackexchange.com/a/633011
export PATH=$PATH:.:$repo_dir/bash_scripts:$repo_dir/private_scripts:$(find $repo_dir/python_scripts -type d -maxdepth 1 | paste 
-sd ":" -)
#########################
# colorized ls
alias ls='ls -G'
#########################
# cd directly on Desktop 
cd Desktop
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
eval "$(/opt/homebrew/bin/brew shellenv)"
#########################
