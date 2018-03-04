#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import getpass
import requests
import argparse
from prettytable import PrettyTable
from robobrowser import RoboBrowser
from time import sleep
from urllib import parse


def forge_header(auth):
    """Customize the header based on the type of the authentication."""

    authentication = dict()
    if next (iter (auth.keys())) == "token":
        token = next (iter (auth.values()))
        authentication['PRIVATE-TOKEN'] = token

    return authentication

def generic_listing(url, category, auth, page, per_page=100):
    """List all the entries of a category from Gitlab."""

    headers = forge_header(auth)
    req = requests.get(
        "{url}/api/v4/{category}?per_page={per_page}&page={page}".format(
            url=url,
            category=category,
            per_page=per_page,
            page=page),
        headers=headers)
    status = req.status_code

    if status == 200:
        disp = PrettyTable()
        disp.field_names = ["List of {category} / Page {page}".format(category=category, page=page)]
        for item in req.json():
            disp.add_row([item['name']])
        print(disp)
    else:
        print("The request failed with the status code: {status}".format(status=status))
        sys.exit(1)

def list_group_projects(url, group, auth, page, per_page=100):
    """List the projects of a group."""

    headers = forge_header(auth)
    req = requests.get(
        "{url}/api/v4/groups/{group}/projects?per_page={per_page}&page={page}".format(
            url=url,
            group=group,
            per_page=per_page,
            page=page),
        headers=headers)
    status = req.status_code

    if status == 200:
        disp = PrettyTable()
        disp.field_names = ["List of projects in group {group}".format(group=group)]
        for item in req.json():
            disp.add_row([item['name']])
        print(disp)
    else:
        print("The request failed with the status code: {status}".format(status=status))
        sys.exit(1)

    return req.json()

def generic_search(url, name, category, auth):
    """Search for a string within a category.

    N.B: the search string has to be at least 3 chars long, Gitlab requirement
    """

    headers = forge_header(auth)
    req = requests.get(
        "{url}/api/v4/{category}?search={name}".format(
            url=url,
            category=category,
            name=name),
        headers=headers)
    status = req.status_code

    if status == 200:
        disp = PrettyTable()
        disp.field_names = ['id', category, 'web url']
        for item in req.json():
            disp.add_row([item['id'], item['name'], item['web_url']])
        print(disp)
    else:
        print("The request failed with the status code: {status}".format(status=status))
        sys.exit(1)

def generic_information(url, target, auth, page, per_page=100):
    """Print information about a target."""

    headers = forge_header(auth)
    req = requests.get(
        "{url}/api/v4/{target}?per_page={per_page}&page={page}".format(
            url=url,
            target=target,
            per_page=per_page,
            page=page),
        headers=headers)
    status = req.status_code

    if status == 200:
        disp = PrettyTable()
        # TODO: output all fields if verbose option enabled -> ugly display
        #ITEMS = [k for k,v in req.json()[0].items()]
        ITEMS = [
            'id',
            'name',
            'visibility' if target != "users" else 'state',
            'web_url',
            'request_access_enabled' if target != "users" else 'email',
            ]
        disp.field_names = ITEMS

        for item in req.json():
            disp.add_row([item[i] for i in ITEMS])
        print(disp.get_string(title=target))
    else:
        print("The request failed with the status code: {status}".format(status=status))
        sys.exit(1)

def get_group_id(url, group, auth):
    """Get the id of the project from its name."""

    headers = forge_header(auth)
    req = requests.get(
        "{url}/api/v4/groups?search={group}".format(
            url=url,
            group=group),
        headers=headers)
    status = req.status_code

    if status == 200:
        if len(req.json()) == 1:
            group_id = req.json()[0]['id']
            return group_id
        elif len(req.json()) > 1:
            print("The group name you provide is not unique")
            sys.exit(1)
        else:
            print("Could not find the group id from the name {group}".format(group=group))
            sys.exit(1)
    else:
        print("The request failed with the status code: {status}".format(status=status))
        sys.exit(1)

def export_project(url, project, username, password):
    """Export GitLab project."""

    # login phase
    browser = RoboBrowser(parser="html.parser", history=True)
    browser.open('{url}/users/sign_in'.format(url=url))
    login_form = browser.get_form(action="/users/auth/ldapmain/callback")
    login_form['username'].value = username
    login_form['password'].value = password
    browser.submit_form(login_form)

    # Export phase
    browser.open("{url}/{project}/edit".format(url=url, project=project))
    post_result = browser.session.post(
        "{url}/{project}/export".format(url=url, project=project),
        data={
            "authenticity_token": browser.parsed.find_all("meta", {"name":"csrf-token"})[0].attrs['content']
            }
        )

    # Download phase
    sleep(20)
    browser.open("{url}/{project}/edit".format(url=url, project=project))
    get_result = browser.session.get(
        "{url}/{project}/download_export".format(url=url, project=project),
        data={
            "authenticity_token": browser.parsed.find_all("meta", {"name":"csrf-token"})[0].attrs['content']
            }
        )
    proj = project.replace('/', '-')
    tmp_file = "/tmp/{project}.tar.gz".format(project=proj)
    with open(tmp_file, 'wb') as content:
        content.write(get_result.content)

    print("The exported project is:", tmp_file)

def import_project(url, group_name, project_name, up_file, username, password, auth):
    """Import GitLab project."""

    # login phase
    browser = RoboBrowser(parser="html.parser", history=True)
    browser.open('{url}/users/sign_in'.format(url=url))
    login_form = browser.get_form(action="/users/auth/ldapmain/callback")
    login_form['username'].value = username
    login_form['password'].value = password
    browser.submit_form(login_form)

    group_id = get_group_id(url, group_name, auth)
    # Upload phase
    browser.open(
        "{url}/import/gitlab_project/new?namespace_id={group_id}&path={project_name}".format(
            url=url,
            group_id=group_id,
            project_name=project_name)
        )
    upload_form = browser.get_form(action="/import/gitlab_project")
    upload_form['file'].value = open(up_file, 'rb')
    browser.submit_form(upload_form)

def transfer_project(url, project_name, group_name, auth):
    """Transfer GitLab project."""

    headers = forge_header(auth)
    group_id = get_group_id(url, group_name, auth)
    project = parse.quote_plus(project_name)

    req = requests.post(
        "{url}/api/v4/groups/{group_id}/projects/{project}".format(
            url=url,
            group_id=group_id,
            project=project),
        headers=headers)
    status = req.status_code

    if status == 201:
        print("Project {project_name} successfuly transfered to the group {group_name}".format(
            project_name=project_name,
            group_name=group_name)
        )
    else:
        print("The request failed with the status code: {status}".format(status=status))
        sys.exit(1)

def parse_args():

    choices = ['groups', 'projects', 'users']
    parser = argparse.ArgumentParser(allow_abbrev=True)
    parser.add_argument('--export',
                        metavar="project_name",
                        help='export a project')

    parser.add_argument('--import',
                        dest='imp',
                        nargs=3,
                        metavar=('group_id', 'project_name', '/path/to/project_file'),
                        help='import a project from a file')

    parser.add_argument('-i',
                        '--information',
                        choices=choices,
                        help='display information of a category')

    parser.add_argument('-l',
                        '--list',
                        choices=choices,
                        help='list all items of a category')

    parser.add_argument('--export-import',
                        dest="expimp",
                        nargs=3,
                        metavar=(
                            'source_project',
                            'group_id',
                            'project_name',
                        ),
                        help='massively export projects from one GitLab and imports them to another')

    parser.add_argument('-p',
                        '--projects',
                        metavar="group",
                        help='list all projects of a group')

    parser.add_argument('--page',
                        type=int,
                        metavar="number",
                        help='print information of a specific page')

    parser.add_argument('-s',
                        '--search',
                        nargs=2,
                        metavar=('string', 'namespace'),
                        help='search for a specific string within a namespace')

    parser.add_argument('--transfer',
                        nargs=2,
                        metavar=('project_name', 'destination_group'),
                        help='transfer a project to a new group/namespace')

    parser.add_argument('--url',
                        help='provide GitLab URL')

    parser.add_argument('--dest-url',
                        dest="durl",
                        metavar="URL",
                        help='provide destination GitLab URL used for export/import ONLY')

    return parser.parse_args()

def main():
    args = parse_args()

    # Authorization token of the source GitLab
    _auth = dict()
    # URL of the source GitLab
    URL = os.getenv('GITLAB_URL', "https://gitlab.com") if not args.url else args.url
    # URL of the source GitLab
    D_URL = os.getenv('GITLAB_DEST_URL') if not args.durl else args.durl
    page = args.page if args.page else 1

    if os.getenv('GITLAB_TOKEN'):
        _auth['token'] = os.getenv('GITLAB_TOKEN')
    else:
        _auth['token'] = getpass.getpass("Enter your token for {url}: ".format(url=URL))

    if args.list:
        generic_listing(URL, args.list, _auth, page)

    if args.search:
        generic_search(URL, args.search[0], args.search[1], _auth)

    if args.information:
        generic_information(URL, args.information, _auth, page)

    if args.projects:
        list_group_projects(URL, args.projects, _auth, page)

    if args.export or args.imp:
        username = input("Enter username: ")
        password = getpass.getpass("Enter password: ")
        if args.export:
            export_project(URL, args.export, username, password)
        else:
            import_project(D_URL, args.imp[0], args.imp[1], args.imp[2], username, password, _auth)

    if args.transfer:
        transfer_project(URL, args.transfer[0], args.transfer[1], _auth)

    # TODO: use yaml file for massive import
    if args.expimp:
        # Authorization token of the destination GitLab
        _d_auth = dict()
        # Source GitLab credentials
        username = input("Enter username for {url}: ".format(url=URL))
        password = getpass.getpass("Enter password for {url}: ".format(url=URL))

        # Destination GitLab credentials
        d_username = input("Enter username for {url}: ".format(url=D_URL))
        d_password = getpass.getpass("Enter password for {url}: ".format(url=D_URL))
        _d_auth['token'] = getpass.getpass("Enter your token for {url}: ".format(url=D_URL))

        # Export the project from the source GitLab
        export_project(URL, args.expimp[0], username, password)
        project = args.expimp[0].replace('/', '-')
        tmp_file = "/tmp/{project}.tar.gz".format(project=project)

        # Import the project to the destination GitLab
        import_project(
            D_URL,
            args.expimp[1],
            args.expimp[2],
            tmp_file,
            d_username,
            d_password,
            _d_auth,
        )

if __name__ == '__main__':
    main()
