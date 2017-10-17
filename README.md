# Random scripts

Scripts that maybe usefull.

### Space eater
[Space eater](space_eater.py): is a scripts that scans a directory looking for filenames and dirs that contain space in their names and replace the space with underscore.
 
It has 2 params:
  * "-s" to show what is supposed to be done without doing it.
  * "-a" apply the changes: replace the spaces with underscores in the filenames.

---
### Parallel execution
[pexec](pexec.sh): Bash script for parallel execution of the same command on N nodes.

The script allows you to execute the same command on N nodes at the same time.
The inventory or the list of servers can be specified in 2 ways:

1. Set in the configuration file /etc/pexec/groups in the following format:
```
group1: host1 host2 [...] hostN
group2: host1 host2 [...] hostN
.
.
.
```

2. A file that contains all the servers in the following format:

  host1

  host2
  
  [...]
  
  hostN

It has the following output when executed:

1/3: [host1]
output of the command

2/3: [host2]
output of the command

3/3: [host3]
output of the command

---
### Bash getopts template
[getopts template](getopts.template.sh): is a template of a bash script that has options using the function "getopts".


