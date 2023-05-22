import json
import os
import requests
import shutil 
import time
import uuid

token = "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"

headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": "Bearer {}".format(token),
}

out_dir = ""

def clone_repos(repos):

    for i in repos:
        out_name = "{}-{}".format(i['name'], uuid.uuid4())
        os.system('cd {} && git clone --depth 1 --single-branch {} {}'.format(out_dir, i['html_url'], out_name))

def get_github_public_repos(pages):
    
    url = "https://api.github.com/repositories?since={}"

    r = requests.get(url.format(0), headers=headers)
    clone_repos(r.json())

    total = 1;

    while 'url' in r.links['next'] and total < pages:
            
        r = requests.get(r.links['next']['url'], headers=headers)
        clone_repos(r.json())

        total += 1 

if __name__ == "__main__":
    
    out_dir = os.path.join(os.getcwd(), 'repos')
    
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    get_github_public_repos(pages = 2)
