from time import time
from fabric.api import run, put, local, task, cd, env
try:
    from local_fabfile import *
except ImportError:
    print("""WARNING: local_fabfile not found - deployment requires
          hosts and user settings""")


# stolen largely from https://gist.github.com/mahmoudimus/384895

@task
def update():
    """ copy project and updates environment and symlink """
    checkout()
    update_environment()
    symlink()


@task
def checkout():
    """ checkout code locally, prepare, and copy """

    env.current_release = '{0}/releases/{1:.0f}'.format(env.base_dir, time())
    env.tmpdir = local('mktemp -d', capture=True)
    local('git clone -b {0} {1} {2}'.format(
        env.git_branch,
        env.git_repo,
        env.tmpdir))
    run('mkdir -p {0}'.format(env.current_release))
    put('{0}/*'.format(env.tmpdir), env.current_release)
    local('rm -fr {0}'.format(env.tmpdir))


@task
def update_environment():
    """ update server environment """
    if not env.has_key('current_release'):
        releases()
    run('{0} {1}'.format(env.virtualenv, env.current_release))
    run('{0}/bin/pip install -r {0}/requirements.txt'.
        format(env.current_release))


@task
def symlink():
    if not env.has_key('current_release'):
        releases()
    run('ln -nfs {0} {1}/current'.format(env.current_release, env.base_dir))


@task
def releases():
    """ list releases and set current_release and previous_release """
    env.releases = sorted(
        run('ls -x {0}/releases'.format(env.base_dir)).split())
    if len(env.releases) >= 1:
        env.current_revision = env.releases[-1]
        env.current_release = '{0}/releases/{1}'.format(env.base_dir,
                                                        env.current_revision)
    if len(env.releases) > 1:
        env.previous_revision = env.releases[-1]
        env.previous_release = '{0}/releases/{1}'.format(env.base_dir,
                                                         env.previous_revision)


@task
def restart():
    """ restart the server using configured restart command """
    if (env.has_key('restart_command_is_sudo')
        and env.restart_command_is_sudo == 'True'):
        sudo(env.restart_command)
    else:
        run(env.restart_command)


@task
def setup():
    """ set up hosts for deployment """
    run("mkdir -p {0}/{{releases,shared}}".format(env.base_dir))


@task
def cleanup():
    """ clean up old releases """
    if not env.has_key('releases'):
        releases()
    if len(env.releases) > 3:
        directories = env.releases
        directories.reverse()
        del(directories[:3])
        env.directories = ' '.join(
            ['{0}/releases/{1}'.format(env.base_dir, release)
             for release in directories])
        run('rm -rf {0}'.format(env.directories))


@task
def rollback():
    """ rolls back to the previous version and restarts """
    rollback_code()
    restart()


@task
def deploy():
    """ update and restart """
    update()
    restart()
    cleanup()
