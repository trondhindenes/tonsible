from collections import namedtuple

class OptionParser:
    @staticmethod
    def parse_opts(opts, playbook=None):
        keys = opts.keys()

        if playbook is None:
            playbook = opts['playbook']

        options = namedtuple('Options', [])
        for key in keys:
            if key not in ["playbook"]:
                options = namedtuple('Options', options._fields+(key, ))


        return playbook, None
