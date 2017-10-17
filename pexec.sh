#!/bin/bash

# By CBS panda
  
GRPS="/etc/pexec/groups"
#LIST="/etc/pexec/list" 
LIST=$2

#CMD=${@:3}
CMD=${*:3}

function pexec_Group
{
eval  set -- `awk -F: '/'"$OPTARG"'/ {print $2}' $GRPS`
typeset -i pos=1
typeset -i nbr=$#

while (($#))
do
        printf "\e[32m%s\e[m \e[32m%-15s\e[m\n" "$pos/$nbr:" "[$1]"
        ssh -- $1 $CMD
        echo
	let "pos+=1"
        shift
done
}

function pexec_List
{
eval  set -- `tr '\n' ' ' < $LIST`
typeset -i pos=1
typeset -i nbr=$#

for vm in $(cat $LIST)
do
        printf "\e[32m%s\e[m \e[32m%-15s\e[m\n" "$pos/$nbr:" "[$vm]"
        ssh -- $vm $CMD
	let "pos+=1"
	echo
done
}

while getopts :g:l: opt
do
  case $opt in
    g)
        [[ ! $(grep $OPTARG $GRPS) ]] && echo -e "\t[$OPTARG]: doesn't exist in the config file." && exit 1
        [[ $CMD == "" ]] && echo -e "\tThere is no command to execute." && exit 1
        pexec_Group $*
    ;;
  
    l)  
        [[ ! -f $LIST ]] && echo -e "\t[$LIST]: either doesn't exist or is not a file" && exit 1
        [[ $CMD == "" ]] && echo -e "\tThere is no command to execute." && exit 1
        pexec_List $*
    ;;

    :)
       echo -e "\tOption -$OPTARG requires an argument" && exit 1
    ;;
   
    \?)
        echo -e "\tPlease use either -g or -l option"
    ;;
  
  esac
done
