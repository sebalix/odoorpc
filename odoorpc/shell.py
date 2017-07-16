#!/usr/bin/env python
# -*- coding: utf-8 -*-
import code

import odoorpc


BANNER = u"""
   ___     _          ___ ___  ___            _        _ _
  / _ \ __| |___  ___| _ \ _ \/ __|  ___   __| |_  ___| | |
 | (_) / _` / _ \/ _ \   /  _/ (__  |___| (_-< ' \/ -_) | |
  \___/\__,_\___/\___/_|_\_|  \___|       /__/_||_\___|_|_|
___________________________________________________________
"""
USAGE = u"""
Your Odoo session is available through the 'odoo' object. E.g:\n
\tPartner = odoo.env['res.partner']
"""


class Shell(code.InteractiveConsole):
    """Shell used to interact with a OdooRPC session."""
    def __init__(self, *args, **kwargs):
        code.InteractiveConsole.__init__(self, *args, **kwargs)
        self.set_locals()
        self.set_readline()

    def set_locals(self):
        """Define locals , i.e. objects directly available
        to the user within the interactive shell.
        """
        self.locals = {
            'odoorpc': odoorpc,
            'ODOO': odoorpc.ODOO,
            # 'odoo': odoorpc.ODOO(),   # TODO
        }

    def set_readline(self):
        """Configure the behaviour of the interactive shell
        (history, completion...).
        """
        try:
            import readline
        except ImportError:
            print("Module readline not available.")
        else:
            import rlcompleter
            readline.set_completer(
                rlcompleter.Completer(self.locals).complete)
            readline.parse_and_bind("tab: complete")


def main():
    """Run the interactive shell."""
    banner = (BANNER.lstrip('\n'), USAGE.lstrip('\n'))
    shell = Shell()
    shell.interact(u"\n".join(banner))


if __name__ == "__main__":
    main()
