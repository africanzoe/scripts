# completion for pass
# TODO: add sub-options
_pass ()
{
    local cur prev grps words=() #split=false

    COMPREPLY=()
    words=("${COMP_WORDS[@]}")

    _words=$(pass --help | awk '/pass / {print $2}' | tr -d '[]')

    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"

    COMPREPLY=( $(compgen -W "$_words" -- ${cur}) )
    return 0
} &&
complete -F _pass -o filenames pass
