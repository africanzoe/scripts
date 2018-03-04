# Gitlab CLI

This is a basic CLI based on both the GitLab API using the exposed endpoints and the HTML parsing of the site.

It allows you to:
* List groups, projects, users
* Show information about groups, projects, users
* Search for a string in the groups, projects, users
* Display all the projects of a specific group
* Export a project
* Import a project
* `Export a project from one GitLab and import it to another one.`
* Transfer a project from one group into another.

N.B:
- GitLab API use pagination in the returned data, so the number of displayed entries is limited to 100 line per page (page number is displayed), use the option `--page` to list entries for a different page.
- The string used for the search option has to be at least 3 chars long (GitLab requirement).

# Authentication

As the script uses both the GitLab API and HTML parsing it will ask you for the required credentials depending on your actions.

For the token you have the possibility to set it as an environment variable (even if NOT advised to do so) as follows:

export GITLAB_TOKEN="abcde12345"

# Usage

To display either groups, projects or users:
```
# gitlab-cli.py -l groups|projects|users
```

Sample output:
```
+-----------------+
|  List of groups |
+-----------------+
|     group_1     |
|     group_2     |
|     group_3     |
+-----------------+
```

To search for all project names containing the string `scw`:
```
# gitlab-cli -s scw projects
```

Sample output:
```
+-------------------------+
| Items found in projects |
+-------------------------+
|       scw-hiring        |
|       scw-succes        |
|       scw-adventure     |
+-------------------------+
```

To search for all usernames containing the string `john`:
```
# gitlab-cli -s john users
```

Sample output:
```
+----------------------+
| Items found in users |
+----------------------+
|   John doe           |
|   Doe John           |
+----------------------+
```

To list all the projects of a specific group:
1. List the available groups or search for it:
```
# gitlab-cli -l groups
```

2. Show the projects of the desired group
```
# gitlab-cli -p group_1
```

# Export/Import projects

The option `--export-import` allow you to export a project from one GitLab and import it to another GitLab, ex:
```
# gitlab-cli --export-import group_1/project_1 dest_group project_name
```

It has 3 params that should be supplied in an ordered manner:
1. The source project that will be exported from the source GitLab in the form: `namespace/project`, ex: `group_1/project_1`
2. The target group in the destination GitLab that the project will be imported in
3. The new name of the project once imported

**N.B**:
- As the script use both the GitLab API and HTML parsing it required the tokens AND username/password of the 2 Gitlabs.
- You need to be the owner on the target group to be able to import projects to it.

# Transfer a project

You can transfer a project into another group by using the option `--transfer` as the following:
```
# gitlab-cli --transfer project_name destination_group
```

## Explanation

The script will simulate a login on the source GitLab and export the desired project, then will download it to a local file in `/tmp`.
Once the the project downloaded, the script will login to the target GitLab and search for the id of the group from its name, then upload the project tarball to the specified group.

# Requirements

It requires `python3`.

The following libraries are required also:
* PrettyTable
* RoboBrowser

# Important notes

- The default GitLab URL is: `https://gitlab.com`, so change it with the option `--url`.
- 2FA is not supported by this script, so you need to disable it beforehand.
