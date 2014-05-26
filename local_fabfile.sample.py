from fabric.api import env, task


@task
def production():
    env.user = 'SERVERUSER'
    env.hosts = [
        'SERVERHOSTNAME'
    ]
    env.port_number = 5000
    env.base_dir = '/path/to/server/base/dir'
    env.git_repo = 'git@github.com:path/to/git/repo'
    env.git_branch = 'master'
    env.restart_command = '/usr/bin/supervisorctl restart contact_potion:contact_potion-web'
    env.restart_command_is_sudo = 'True'
    env.config_file = 'default.config'
    env.virtualenv = '/usr/local/bin/virtualenv-2.7'
