"""Galaxy-specific utility methods"""
import os
import logging
from ansible.playbook import PlayBook
# from ansible import callbacks

from git import Repo
from git import GitCommandError

from cm.util.cm_ansible import PlaybookRunnerCallbacks, PlaybookCallbacks, AggregateStats

log = logging.getLogger('cloudman')


def update_galaxy(app, changeset='master',
                  galaxy_git_repo='https://github.com/galaxyproject/galaxy.git',
                  playbook_git_repo='https://github.com/galaxyproject/galaxy-cloudman-playbook'):
    """
    Update Galaxy application.

    This method will run a set of Ansible roles to update the Galaxy app
    source code as well as perform any necessary database migrations. Any
    local changes will be discarded. Also, the assumption is that no major
    changes have been made to how Galaxy is setup.
    """
    gxy_svc = app.manager.service_registry.get('Galaxy')
    app.manager.deactivate_master_service(gxy_svc, immediately=True)
    # First clone the Ansible playbook
    playbook_dir = '/tmp/galaxy_playbook'
    try:
        Repo.clone_from(playbook_git_repo, playbook_dir)
    except GitCommandError, gce:
        if gce.status == 128:
            pass  # Repo already exists
        else:
            return "Trouble cloning playbook repo: {0}".format(gce)
    # Run the playbook to update Galaxy
    stats = AggregateStats()
    playbook_cb = PlaybookCallbacks()
    runner_cb = PlaybookRunnerCallbacks(stats)
    playbook_file = os.path.join(playbook_dir, 'galaxyFS.yml')
    pb = PlayBook(playbook=playbook_file, only_tags=['galaxy'],
                  host_list=['localhost'], stats=stats,
                  callbacks=playbook_cb, runner_callbacks=runner_cb)
    try:
        pb.run()
    except AssertionError, aerr:
        log.debug("AssertionError running Ansible playbook: {0}".format(aerr))
    if not stats.failures.get('localhost'):
        app.manager.activate_master_service(gxy_svc)
        return "Galaxy update completed."
    else:
        return "Experienced a failure during Galaxy update. Check the log."
