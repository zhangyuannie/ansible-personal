# .bashrc

# Source global definitions
if [[ -f /etc/bashrc ]]; then
  . /etc/bashrc
fi

# User specific environment
if ! [[ "${PATH}" =~ "${HOME}/.local/bin:" ]]; then
  PATH="${HOME}/.local/bin:${PATH}"
fi

# Development environment
PATH="${HOME}/.local/go/bin:${HOME}/.deno/bin:${HOME}/.yarn/bin:${PATH}"

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
