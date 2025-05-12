# Release

How to release from dev branch to main branch with a version tag.

``` shell
git fetch --all
git checkout dev
git pull origin dev
git checkout main
git pull origin main
git merge dev
git add .
git commit -m "merge dev - release v0.1.6"
git tag v0.1.6
git push origin main
git push origin v0.1.6
```

``` shell
➜  oneworldsync_python git:(dev) ✗ git fetch --all 
➜  oneworldsync_python git:(dev) git checkout dev
Already on 'dev'
Your branch is up to date with 'origin/dev'.
➜  oneworldsync_python git:(dev) git pull origin dev
From https://github.com/mcgarrah/oneworldsync_python
 * branch            dev        -> FETCH_HEAD
Already up to date.
➜  oneworldsync_python git:(dev) git checkout main
Switched to branch 'main'
Your branch is up to date with 'origin/main'.
➜  oneworldsync_python git:(main) git pull origin main
From https://github.com/mcgarrah/oneworldsync_python
 * branch            main       -> FETCH_HEAD
Already up to date.
➜  oneworldsync_python git:(main) git merge dev
Updating 17bfb60..c9125e6
Fast-forward
 .github/dependabot.yaml                   |    12 +
 .vscode/settings.json                     |     2 +-
 README.md                                 |    40 +-
 TODO.md                                   |     9 +
 oneworldsync/__init__.py                  |     2 +-
 oneworldsync/client.py                    |     7 +-
 pyproject.toml                            |     2 +-
 setup.py                                  |     2 +-
 swagger/preprod_swagger_fetch_model.json  | 10048 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 swagger/preprod_swagger_search_model.json |   406 ++++
 swagger/prod_swagger_fetch_model.json     | 10048 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 swagger/prod_swagger_search_model.json    |   406 ++++
 12 files changed, 20957 insertions(+), 27 deletions(-)
 create mode 100644 .github/dependabot.yaml
 create mode 100644 swagger/preprod_swagger_fetch_model.json
 create mode 100644 swagger/preprod_swagger_search_model.json
 create mode 100644 swagger/prod_swagger_fetch_model.json
 create mode 100644 swagger/prod_swagger_search_model.json
➜  oneworldsync_python git:(main) git add .
➜  oneworldsync_python git:(main) git commit -m "merge dev for release v0.1.6"
On branch main
Your branch is ahead of 'origin/main' by 3 commits.
  (use "git push" to publish your local commits)

nothing to commit, working tree clean
➜  oneworldsync_python git:(main) git tag v0.1.6
➜  oneworldsync_python git:(main) git push origin main
Total 0 (delta 0), reused 0 (delta 0), pack-reused 0
To https://github.com/mcgarrah/oneworldsync_python.git
   17bfb60..c9125e6  main -> main
➜  oneworldsync_python git:(main) git push origin v0.1.6
Total 0 (delta 0), reused 0 (delta 0), pack-reused 0
To https://github.com/mcgarrah/oneworldsync_python.git
 * [new tag]         v0.1.6 -> v0.1.6
➜  oneworldsync_python git:(main) 
```