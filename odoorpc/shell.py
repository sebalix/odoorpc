#!/usr/bin/env python
# -*- coding: utf-8 -*-
import code

import odoorpc


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
    shell = Shell()
    shell.interact()


if __name__ == "__main__":
    main()
