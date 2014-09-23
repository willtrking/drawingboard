# coding: utf-8

import uuid
import time

class Aminate(object):



    def __init__(self,aminate_command="aminate"):
        
        self._id = uuid.uuid4()

        self.aminate_command = aminate_command
        self.ordered_args = []
        self.arg_names = {}
        self.arg_desc = {}
        self.bool_args = set()
        self.str_args = set()

    def load_available_args(self,args):
        """
            expects list of tuples 
            IN ORDER THAT THEY WILL BE WRITTEN TO CLI
            [
                (arg,bool/string,name,description)
            ]
        """
        for arg_info in args:
            arg = arg_info[0]
            arg_type = arg_info[1]
            arg_name = arg_info[2]
            arg_desc = arg_info[3]

            self.arg_names[arg_name] = arg
            self.arg_desc[arg_name] = arg_desc

            self.ordered_args.append(arg)

            if arg_type == bool:
                self.bool_args.add(arg)
            elif arg_type == string:
                self.str_args.add(arg)
            else:
                raise RuntimeError("Bad type %s for arg %s" % (arg_type,arg_name))


    def _form_command(self,args):
        """
            expects dict
            {
                "arg" : "arg_value"
            }
        """

        if not self.ordered_args:
            raise RuntimeError("Run load_available_args first!")

        command = self.aminate_command
        
        for arg in self.ordered_args:
            if arg in args:
                command = "%s %s" % (
                    command,
                    self.format_arg(
                        arg,
                        args[arg]
                    )
                )

        return command

    def _format_arg(self,arg,val):
        if arg in self.bool_args:
            return arg
        elif arg in self.str_args:
            return "%s %s" % (arg,val)
        else:
            raise RuntimeError("Unknown arg to format %s" % arg)
            
