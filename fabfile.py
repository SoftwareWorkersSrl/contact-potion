from fabric.api import run, put, local, task, cd, env
try:
    import local_fabfile
except ImportError:
    print("""WARNING: local_fabfile not found - deployment requires
          hosts and user settings""")

@task
def setup():
    """ set up hosts for deployment """
    run("mkdir -p {0}/{{releases,shared}}".format(env.base_path))


@task
def checkout():
    """ checkout code locally, prepare, and copy """
    env.tempdir = local('mktemp -d', capture=True)
    local('git clone -b {0} {1} {2}'.format(
        env.git_branch,
        env.git_repo,
        env.tempdir))


@task
def copy():
    """ copy code to remote server """
    from time import time
    env.current_release = '{0}/releases/{1}'.format(env.base_dir, time())
    run('mkdir -p {0}'.format(env.current_release))
    put('{0}/contact_potion/*'.format(env.tempdir), env.current_release)
    local('echo rm -r {0}'.format(env.tempdir))


@task
def deploy():
    checkout()
    copy()
