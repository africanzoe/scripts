# Random scripts

Scripts that maybe usefull.

### GitLab CLI
GitLab CLI that allows you to display groups/users/projects/import-export projects between different GitLabs and more. Refer to the [README](gitlab/README.md) for more information.

### Parallel execution
[pexec](pexec.sh): Bash script for parallel execution of the same command on N nodes.

The script allows you to execute the same command on N nodes at the same time using ssh.
The inventory or the list of servers can be specified in 2 ways:

1. Set in the configuration file /etc/pexec/groups in the following format:
```
group1: host1 host2 [...] hostN
group2: host1 host2 [...] hostN
...
```

2. A file that contains all the servers in the following format:
```
  host1
  host2
  [...]
  hostN
```

It has the following output when executed:
```
1/3: [host1]
output of the command

2/3: [host2]
output of the command

3/3: [host3]
output of the command
```

### Bash getopts template
[getopts template](getopts.template.sh): is a template of a bash script that has options using the function "getopts".

### Ansible-playbook bash completion for inventory option
Ansible-playbook inventory [bash completion](ansible.bash): is a bash completion script to be placed in /etc/bash_completion.d, it will complete the inventory for you after the option "-l" of Ansible-playbook command.

### Pass software bash completion
Bash script to source at login for ex to be able to have Bash completion for `pass` software.
