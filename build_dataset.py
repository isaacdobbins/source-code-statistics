import json
import os
import requests
import shutil 
import sys
import time
import uuid

class context:
    token = ""
    headers = {}
    out_dir = ""

def prepare_args(context):

    context.token = sys.argv[1]

    context.headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": "Bearer {}".format(context.token),
        "X-GitHub-Api-Version": "2022-11-28",
    }

    context.out_dir = os.path.join(os.getcwd(), 'repos')

def create_dir(dir):

    if os.path.exists(dir):
        shutil.rmtree(dir)

    if not os.path.exists(dir):
        os.makedirs(dir)

    if not os.path.exists(dir):
        os.makedirs(dir)

def clone_repos(repos, out_dir):

    for i in repos:
        out_name = "{}-{}".format(i['name'], uuid.uuid4())
        os.system('cd {} && git clone --depth 1 --single-branch {} {}'.format(out_dir, i['html_url'], out_name))

def get_github_public_repos(context, pages):
    
    url = "https://api.github.com/repositories?since={}"

    r = requests.get(url.format(0), headers=context.headers)
    
    if r.status_code != 200:
        return

    clone_repos(r.json(), context.out_dir)

    total = 1;

    while 'url' in r.links['next'] and total < pages:
            
        r = requests.get(r.links['next']['url'], headers=context.headers)

        clone_repos(r.json())

        total += 1 

if __name__ == "__main__":
    
    ctx = context()

    prepare_args(ctx)

    create_dir(ctx.out_dir)

    get_github_public_repos(ctx, pages = 1)
