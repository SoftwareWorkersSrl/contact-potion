from fabric.api import env


env.user = 'SERVERUSER'
env.hosts = [
    'SERVERHOSTNAME'
]
env.base_dir = '/path/to/server/base/dir'
env.git_repo = 'git@github.com:path/to/git/repo'
env.git_branch = 'master'
env.restart_cmd = 'ls'
