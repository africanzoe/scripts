# completion for ansible-playbook
_ansible_playbook ()
{
    local cur prev grps words=() #split=false

    COMPREPLY=()
    words=("${COMP_WORDS[@]}")
    check=$(echo "${COMP_WORDS[@]}" | grep -- '-i ')
    if [[ "$check" ]]
    then
        HOSTS=$(echo "$check" | awk '/-i / || /--inventory-file / {print $(NF-1)}')
    else
        HOSTS="/data/workshop/iac/ansible/hosts"
    fi

    grps=$(awk '/^\[/ {print substr($1,2,length($1)-2)}' "${HOSTS}" | cut -d':' -f1 | sort -u)
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"


    case $prev in
        -l|--limit)
            COMPREPLY=( $(compgen -W "$grps" -- ${cur}) )
            #COMPREPLY=( $( compgen -W 'one two three' -- "$cur" ) )
                ;;
    esac
  
      return 0
} &&
complete -F _ansible_playbook -o filenames ansible-playbook ansible-playbook.py
