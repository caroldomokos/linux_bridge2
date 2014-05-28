#!/usr/bin/env python
#-*- coding: utf-8 -*-

DOCUMENTATION = '''
module: vlan
short_description: Manage vlan
requirements: [ ip ]
description:
    - Manage VLAN. vlan interface name is DEV.ID
options:
    vlan:
        required: true
        description:
            - vlan id 
    port:
        required: true
        description:
            - interface for tagged vlan
    state:
        required: false
        default: "present"
        choices: [ present, absent ]
        description:
            - Whether the vlan should exist
'''

EXAMPLES = '''
# Create vlan id 3000 interface on interface eth0
- vlan: vlan=3000 port=eth0
'''

class Vlan (object) :

    def __init__ (self, module) :
        self.module = module
        self.vlan = module.params['vlan']
        self.port = module.params['port']
        self.state = module.params['state']
        self.vif = "%s.%s" % (self.port, self.vlan)

        return

    def ip (self, cmd) :
        
        return self.module.run_command (['ip'] + cmd)

    def ifconfig (self, cmd) :

        return self.module.run_command (['ifconfig'] + cmd)

    def vlan_exists (self) :
        
        syspath = "/sys/class/net/" + self.vif

        return os.path.exists (syspath)

    def addvlan (self) :

        cmd = ['link', 'add', 'link', self.port, 'name', self.vif,
               'type', 'vlan', 'id', self.vlan ]

        (rc, out, err) = self.ip (cmd)

        if rc != 0 :
            raise Exception (err)

        self.ifconfig ([self.vif, 'up'])

        return

    def delvlan (self) :

        self.ifconfig ([self.vif, 'down'])

        cmd = ['link', 'del', 'dev', self.vif]

        (rc, out, err) = self.ip (cmd)

        if rc != 0 :
            raise Exception (err)

        return

    def check (self) :

        try :
            if self.state == 'absent' and self.vlan_exists () :
                changed = True
            elif self.state == 'present' and not self.vlan_exists () :
                changed = True
            else :
                changed = False

        except :
            self.module.fail_json (msg = str (e))

        self.module.exit_json (changed = changed)

        return


    def run (self) :

        changed = False

        try :
            if self.state == 'absent' and self.vlan_exists () :
                self.delvlan ()
                changed = True

            elif self.state == 'present' and not self.vlan_exists () :
                self.addvlan ()
                changed = True

        except Exception, e :
            self.module.fail_json (msg = str (e))

        self.module.exit_json (changed = changed)

        return

def main () :

    module = AnsibleModule (
        argument_spec = {
            'vlan' : { 'required' : True },
            'port' : { 'required' : True },
            'state' : {'default' : 'present',
                       'choices' : ['present', 'absent']
                       }
            },
        supports_check_mode = True,
        )

    vlan = Vlan (module)

    if module.check_mode :
        vlan.check ()
    else :
        vlan.run ()

    return

from ansible.module_utils.basic import *
main ()