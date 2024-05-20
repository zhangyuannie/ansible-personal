# .bashrc

# Source global definitions
if [[ -f /etc/bashrc ]]; then
  . /etc/bashrc
fi

path_add_front() {
  case "${PATH}" in
    *"$1"*) : ;;
    *) PATH="$1:${PATH}" ;;
  esac
}

path_add_front "${HOME}/.local/bin"
path_add_front "${HOME}/.local/go/bin"
path_add_front "${HOME}/.local/cargo/bin"

unset path_add_front

# Prompt
if [[ -f /usr/share/git-core/contrib/completion/git-prompt.sh ]]; then
  . /usr/share/git-core/contrib/completion/git-prompt.sh
  get_prompt() {
    local COLOR='\[\e[34m\]'
    local RESET='\[\e[0m\]'
    local GIT='$(__git_ps1 " \[\e[35m\](%s)")'
    echo "${COLOR}\u@\h \W${GIT}${RESET}\n\\$ "
  }
  export GIT_PS1_SHOWDIRTYSTATE=1
  export GIT_PS1_SHOWUNTRACKEDFILES=1
  PS1="$(get_prompt)"
  unset get_prompt
fi

if [[ -d "${HOME}/.bashrc.d" ]]; then
	for rc in "${HOME}/.bashrc.d/"*; do
		if [[ -f "${rc}" ]]; then
			. "${rc}"
		fi
	done
fi

alias gitl='git log --oneline'
