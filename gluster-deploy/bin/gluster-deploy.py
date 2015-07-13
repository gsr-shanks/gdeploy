#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2015 Nandaja Varma <nvarma@redhat.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#

import argparse
import sys
import os
from glusterlib import Global
from glusterlib import PlaybookGen


class GlusterDeploy(PlaybookGen, Global):
    '''
    This class makes use of the class PlaybookGen inside glusterlib
    library to create the ansible playbooks and variable files.
    Then calls ansible-playbook command to setup back-end and
    deploy GlusterFS
    '''

    def __init__(self):
        args = self.parse_arguments()
        config_file = args.config_file.name
        PlaybookGen(config_file)
        self.deploy_gluster()
        if not int(args.keep):
           self.cleanup_and_quit()
        else:
            print "You can view the generated configuration files "\
                "inside /tmp/playbooks/"

    def parse_arguments(self):
        '''
        This methos uses argparser to parse the command line inputs
        to the gluster-deploy script
        '''
        parser = argparse.ArgumentParser(version='1.0')
        parser.add_argument('-c', dest='config_file',
                            help="Configuration file",
                            type=argparse.FileType('rt'),
                            required=True)
        parser.add_argument('-k', dest='keep', const='1',
                            default='0',
                            action='store',
                            nargs='?',
                            help="Keep the generated ansible utility files")
        try:
            return parser.parse_args()
        except IOError as msg:
            parser.error(str(msg))

    def deploy_gluster(self):
        '''
        Checks if the necessary variables for backend-setup and
        gluster deploy are populated.
        '''
        if Global.do_setup_backend:
            self.set_up_yml = self.get_file_dir_path(Global.base_dir,
                                                'setup-backend.yml')
            print "Setting up back-end..."
            self.call_ansible_command(self.set_up_yml)
        if Global.do_gluster_deploy:
            self.gluster_deploy_yml = self.get_file_dir_path(Global.base_dir,
                                            'gluster-deploy.yml')
            print "Deploying GlusterFS... Coming Soon!!!"
            #self.call_ansible_command(self.gluster_deploy_yml)

    def call_ansible_command(self, playbooks):
        '''
        Calls the ansible-playbook command on necessary yamls
        '''
        try:
            cmd = 'ansible-playbook -i %s %s' % (
                Global.inventory, playbooks)
            self.exec_cmds(cmd, '')
        except:
            print "Error: Looks like there is something wrong with " \
                "your ansible installation."


if __name__ == '__main__':
    GlusterDeploy()