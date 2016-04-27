#!/usr/bin/env python
#-*- coding: utf-8 -*-

DOCUMENTATION = '''
---
module: linux_bridge
short_description: Manage Linux bridges
requirements: [ brctl ]
description:
    - Manage Linux bridges
options:
    bridge:
        required: true
        description:
            - Name of bridge to manage
    state:
        required: false
        default: "present"
        choices: [ present, absent ]
        description:
            - Whether the bridge should exist
'''

EXAMPLES = '''
# Create bridge a named br-int
- linux_bridge: bridge=br-int state=present
'''

class LinuxBridge (object) :

    def __init__ (self, module) :
        self.module = module
        self.bridge = module.params['bridge']
        self.state = module.params['state']
	self.stp =  module.params['stp']
        return

    def brctl (self, cmd) :

        return self.module.run_command (['brctl'] + cmd)


    def ifconfig (self, cmd) :

        return self.module.run_command (['ifconfig'] + cmd)


    def br_exists (self) :
        
        syspath = "/sys/class/net/" + self.bridge
        if os.path.exists (syspath) :
            return True
        else :
            return False

        return 

<<<<<<< HEAD
    def stp_status (self) :
       pShow = subprocess.Popen(["brctl", "show"], stdout=subprocess.PIPE)
       pGrep =  subprocess.Popen([ "grep","-w", self.bridge], stdin=pShow.stdout, stdout=subprocess.PIPE)
       pShow.stdout.close()
       (output, err)  = pGrep.communicate()
       stp_status = output.split()[2]
       if stp_status == "yes" :
                return True
       else :
                return False
=======

>>>>>>> 067d16ce8b4ca538512cbfe9e8934024d44e27f3
    def addbr (self) :
        
        (rc, out, err) = self.brctl (['addbr', self.bridge])

        if rc != 0 :
            raise Exception (err)

        self.ifconfig ([self.bridge, 'up'])

        return


    def delbr (self) :
        
        self.ifconfig ([self.bridge, 'down'])

        (rc, out, err) = self.brctl (['delbr', self.bridge])

        if rc != 0 :
            raise Exception (err)
    
        return

<<<<<<< HEAD
    def confstp (self) :
        (rc, out, err) = self.brctl (['stp', self.bridge, self.stp])
=======
    def stpon (self) :
        (rc, out, err) =   self.brctl (['stp', self.bridge, self.stp])

>>>>>>> 067d16ce8b4ca538512cbfe9e8934024d44e27f3
        if rc != 0 :
            raise Exception (err)

        return

    def check (self) :

        try :
            if self.state == 'absent' and self.br_exists () :
                changed = True
            elif self.state == 'present' and not self.br_exists () :
                changed = True
            else :
                changed = False

        except Exception, e :
            self.module.fail_json (msg = str (e))

        self.module.exit_json (changed = changed)

        return
        

    def run (self) :

        changed = False

        try :
            if self.state == 'absent' and self.br_exists () :
                self.delbr ()
                changed = True

            elif self.state == 'present' and not self.br_exists () :
                self.addbr ()
                changed = True
		if self.stp == 'on' :
<<<<<<< HEAD
			self.confstp ()

            elif self.state == 'present' and self.br_exists () :
                if self.stp == 'on' and not self.stp_status () :
                        changed = True
                        self.confstp ()
                elif self.stp == 'off' and  self.stp_status () :
			changed = True
                        self.confstp ()
=======
			self.stpon ()
			changed = True

>>>>>>> 067d16ce8b4ca538512cbfe9e8934024d44e27f3
        except Exception, e :
            self.module.fail_json (msg = str (e))


        self.module.exit_json (changed = changed)

        return
            

def main () :

    module = AnsibleModule (
        argument_spec = {
            'bridge' : { 'required' : True },
            'state' : {'default' : 'present', 
                       'choices' : ['present', 'absent']
                       },
            'stp' : { 'default' : 'off', 'choices' : ['on', 'off']
                       }
            },
        supports_check_mode = True,
        )

    br = LinuxBridge (module)

    if module.check_mode :
        br.check ()
    else :
        br.run ()

    return

from ansible.module_utils.basic import *
main ()
