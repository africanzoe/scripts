# completion for ansible-playbook
_ansible_playbook ()
{
    local cur prev grps words=() #split=false

    COMPREPLY=()
        HOSTS="/etc/ansible/hosts"
    grps=$(awk '/^\[/ {print substr($1,2,length($1)-2)}' $HOSTS | cut -d':' -f1 | sort -u)
        words=("${COMP_WORDS[@]}")
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

# TODO: get the inventory dynamically
