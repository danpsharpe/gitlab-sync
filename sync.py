#!/usr/bin/python
import argparse, os
import sys, subprocess
import requests, json

ri = 1

def gpr(t):
  return requests.get('https://gitlab.com/api/v4/projects', params={
    'owned': True,
    'private_token': t,
    'archived': False,
    'recursive': True
  })

def ppr(rs):
  global ri
  # If there are repo's and all is working, start creating folders and cloning.
  for r in rs:
    print("Repo [" + str(ri) + "]: " + r['path_with_namespace'] + ".")
    if r['empty_repo'] is not True and 'default_branch' in r:
      if os.path.isdir(r['path_with_namespace']):
        print("Updating Repository...")
        pc("cd " + r['path_with_namespace'] + " && git add -A && git stash && git pull")
      else:
        print("Cloning Repository...")
        pc("git clone " + r['ssh_url_to_repo'] + " " + r['path_with_namespace'])
      with open(r['path_with_namespace'] + '/.GITLAB-PROPERTIES.json', 'w') as outfile:
        json.dump(r, outfile)
    ri += 1

def pc(c):
  p = subprocess.Popen(c, stdout=subprocess.PIPE, shell=True)
  o, e = p.communicate()
  if e is not None:
    return e
  return o

# This is a basic script that clones all repo's in a group.
if __name__ == "__main__":

  # Parse arguments passed into this command.
  parser = argparse.ArgumentParser()
  parser.add_argument("-t", help="Access Token.", type=str)
  args = parser.parse_args()

  # Determine if a caching version argument was passed.
  if args.t == None:
    print("You must specify a private token. Generate one with API grant:")
    print("https://gitlab.com/profile/personal_access_tokens")
    print("Goodbye.")
    exit()

  print("Processing... initial processing will take ~60 minutes, I'd get a coffee...")

  p = gpr(args.t)

  # Check script connected properly.
  if p.status_code != 200:
    print("Error connecting to Gitlab!")
    print("Goodbye.")
    exit()

  rs = p.json()
  ppr(rs)