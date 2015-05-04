"""
Custom Ansible callbacks

These callbacks override the chatty behaviour of default Ansible playbook
callbacks, allowing us to collect the info and only log the progress to
debug logging.
"""
from ansible import utils  # Must import this due to a circular dependency in Ansible
from ansible import callbacks
import logging

AggregateStats = callbacks.AggregateStats
log = logging.getLogger('cloudman')


class PlaybookRunnerCallbacks(callbacks.PlaybookRunnerCallbacks):
    """Playbook runner callbacks

    Override version of ansible.callbacks.PlaybookRunnerCallbacks that
    only logs to default logger with debug messages, not actually doing
    anything else.
    """
    def __init__(self, stats, verbose=None):
        callbacks.PlaybookRunnerCallbacks.__init__(self, stats, verbose)
        # log = logging.getLogger('prc')

    def on_unreachable(self, host, results):
        log.debug('host unreachable %s %s' % (host, results))

    def on_failed(self, host, results, ignore_errors=False):
        log.debug('host failed %s %s' % (host, results))

    def on_ok(self, host, host_result):
        log.debug('host ok %s %s' % (host, host_result))

    def on_skipped(self, host, item=None):
        log.debug('skip %s item %s' % (host, item))

    def on_no_hosts(self):
        log.debug('no hosts')

    def on_async_poll(self, host, res, jid, clock):
        log.debug('async poll %s' % host)

    def on_async_ok(self, host, res, jid):
        log.debug('async ok %s' % host)

    def on_async_failed(self, host, res, jid):
        log.debug('async failed %s' % host)

    def on_file_diff(self, host, diff):
        log.debug('file diff %s' % host)


class PlaybookCallbacks(callbacks.PlaybookCallbacks):
    """Playbook callbacks

    Override version of ansible.callbacks.PlaybookCallbacks that only logs
    to default logger with debug messages, not actually doing anything else.

    Please note that callback on_vars_prompt is NOT overridden, so if your
    code asks for variables we will use the standard chatty query version!
    """

    def __init__(self, verbose=False):
        callbacks.PlaybookCallbacks.__init__(self, verbose)
        # log = logging.getLogger('pc')

    def on_start(self):
        log.debug('starting playbook')

    def on_notify(self, host, handler):
        log.debug('playbook notification')

    def on_no_hosts_remaining(self):
        log.debug('playbook no hosts remaining')

    def on_task_start(self, name, is_conditional):
        log.debug('playbook starting task "%s"' % name)

    def on_setup(self):
        log.debug('playbook setup')

    def on_import_for_host(self, host, imported_file):
        log.debug('playbook importing for host %s' % host)

    def on_not_import_for_host(self, host, missing_file):
        log.debug('playbook not importing for host %s' % host)

    def on_play_start(self, name):
        log.debug('playbook start play %s' % name)

    def on_no_hosts_matched(self):
        log.debug('no hosts')

    def on_stats(self, stats):
        log.debug('playbook statistics %s' % stats)
