import json
import os
import requests
import shutil 
import sys
import time
import uuid

token = ""

headers = {}

out_dir = ""

def clone_repos(repos):

    for i in repos:
        out_name = "{}-{}".format(i['name'], uuid.uuid4())
        os.system('cd {} && git clone --depth 1 --single-branch {} {}'.format(out_dir, i['html_url'], out_name))

def get_github_public_repos(pages):
    
    url = "https://api.github.com/repositories?since={}"

    r = requests.get(url.format(0), headers=headers)
    
    if r.status_code != 200:
        return

    clone_repos(r.json())

    total = 1;

    while 'url' in r.links['next'] and total < pages:
            
        r = requests.get(r.links['next']['url'], headers=headers)

        clone_repos(r.json())

        total += 1 

if __name__ == "__main__":
    
    token = sys.argv[1]

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": "Bearer {}".format(token),
        "X-GitHub-Api-Version": "2022-11-28",
    }

    out_dir = os.path.join(os.getcwd(), 'repos')
    
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    get_github_public_repos(pages = 1)
