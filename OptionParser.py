from collections import namedtuple

class ParserOptions:
    extra_vars = None

class OptionParser:
    @staticmethod
    def parse_opts(opts, playbook=None):
        keys = opts.keys()
        extra_vars = []
        if playbook is None:
            playbook = opts['playbook']

        options = namedtuple('Options', [])
        for key in keys:
            if key not in ["playbook"]:
                extra_vars.append({key: opts[key]})

        opts = ParserOptions()
        opts.extra_vars = extra_vars
        return playbook, opts
