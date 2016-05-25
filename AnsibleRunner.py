
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
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
    def __init__(self, playbook):
        self.playbook = playbook

    def run(self):
        playbook = self.playbook
        Options = namedtuple('Options',
                             ['connection', 'module_path', 'forks', 'become', 'become_method', 'become_user', 'check'])
        # initialize needed objects
        variable_manager = VariableManager()
        loader = DataLoader()
        #options = Options(connection='local', module_path='/path/to/mymodules', forks=100, become=None,
        #                  become_method=None, become_user=None, check=False)
        options = Options(connection='local', module_path='/path/to/mymodules', forks=100, become=None,
                            become_method=None, become_user=None, check=False)
        passwords = dict(vault_pass='secret')

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
                if tqm is not None:
                    tqm.cleanup()

        #play = Play().load(play_source, variable_manager=variable_manager, loader=loader)
        #pbex = PlaybookExecutor(playbooks='/home/thadministrator/wintest.yaml', inventory=inventory, variable_manager=variable_manager,
        #                        loader=loader)
        #results = pbex.run()



        return stats

