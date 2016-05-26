
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.utils.vars import load_extra_vars
from ansible.inventory import Inventory
from ansible.playbook.play import Play
from ansible.playbook import Playbook
from ansible.playbook.block import Block
from ansible.playbook.play_context import PlayContext
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.executor.task_queue_manager import TaskQueueManager

import threading
import yaml


class AnsibleRunner:
    def __init__(self, playbook, options):
        self.playbook = playbook
        self.options = options
        self.vault_pass = None
        self.display = None

    def run(self):
        playbook = self.playbook
        Options = namedtuple('Options',['connection', 'module_path', 'forks', 'become', 'become_method', 'become_user',
                                        'check', 'listhosts', 'listtasks', 'syntax'])

        # initialize needed objects
        variable_manager = VariableManager()
        loader = DataLoader()
        options = Options(connection='local', module_path='/path/to/mymodules', forks=100, become=None,
                          become_method=None, become_user=None, check=False, listhosts=None, listtasks=None, syntax=None)


        variable_manager.extra_vars = load_extra_vars(loader=loader, options=self.options)


        passwords = dict(vault_pass=self.vault_pass)

        # create inventory and pass to var manager
        inventory = Inventory(loader=loader, variable_manager=variable_manager, host_list='/etc/ansible/hosts')
        variable_manager.set_inventory(inventory)


        # create play with tasks
        play_source = dict(
            name="Ansible Play",
            hosts='windows',
            gather_facts='no',
            tasks=[
                dict(action=dict(module='win_ping'))
            ]
        )
        pbex = PlaybookExecutor(playbooks=['/home/thadministrator/' + playbook], inventory=inventory, variable_manager=variable_manager,
                                loader=loader, options=Options, passwords=passwords)
        results = pbex.run()

        '''
        stats = None
        pb = Playbook.load(file_name='/home/thadministrator/' + playbook, variable_manager=variable_manager, loader=loader)
        plays = pb.get_plays()
        for play in plays:
            # actually run it
            tqm = None
            try:
                tqm = TaskQueueManager(
                    inventory=inventory,
                    variable_manager=variable_manager,
                    loader=loader,
                    options=options,
                    passwords=passwords,
                    stdout_callback='default',
                )
                result = tqm.run(play)
                stats = tqm._stats

            finally:
                pass

        if tqm is not None:
            tqm.cleanup()

        #play = Play().load(play_source, variable_manager=variable_manager, loader=loader)
        #pbex = PlaybookExecutor(playbooks='/home/thadministrator/wintest.yaml', inventory=inventory, variable_manager=variable_manager,
        #                        loader=loader)
        #results = pbex.run()
        '''
        return results

