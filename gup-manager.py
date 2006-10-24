#!/usr/bin/python

'''
 gup-manager - Keep GUB root up to date
 
 License: GNU GPL
'''

import re
import string
import sys
import optparse

sys.path.insert (0, 'lib/')

import gup
import oslog

def sort (lst):
    list.sort (lst)
    return lst

class Command:
    def __init__ (self, pm, options):
        self.pm = pm
        self.options = options

    def available (self):
        print '\n'.join (self.pm._packages.keys ())

    def files (self):
        '''list installed files'''
        for p in self.options.arguments:
            if not self.pm.is_installed (p):
                print '%s not installed' % p
            else:
                print '\n'.join (self.pm.installed_files (p))

    def find (self):
        '''package containing file'''
        # urg
        self.options.packagename = self.options.arguments[0]
        regexp = re.sub ('^%s/' % self.options.root, '/',
                self.options.packagename)
        regexp = re.compile (regexp)
        hits = []
        for p in sort (self.pm.installed_packages ()):
            hits += ['%s: /%s' % (p, i)
                for i in self.pm.installed_files (p)
                if regexp.search ('/%s' % i)]
        print (string.join (hits, '\n'))

    def install (self):
        '''download and install packages with dependencies'''
        packs=[]
        for p in self.options.arguments:
            if self.pm.is_installed (p):
                print '%s already installed' % p
            else:
                packs.append (p)

        packs = gup.topologically_sorted (packs, {}, self.pm.dependencies)
        for p in packs:
            self.pm.install_package (p)

    def list (self):
        '''installed packages'''
        if self.options.print_only_name:
            print '\n'.join (sort (self.pm.installed_packages ()))
        else:
            print '\n'.join (sort (['%(split_name)-20s%(version)s' % d for d in self.pm.installed_package_dicts()]))

    def remove_package (self, p):
        if not self.pm.is_installed (p):
            print '%s not installed' % p
        else:
            self.pm.uninstall_package (p)
        
    def remove (self):
        '''uninstall packages'''

        packages = gup.topologically_sorted (self.options.arguments, {},
                                             self.pm.dependencies,
                                             recurse_stop_predicate=lambda p: p not in self.options.arguments)
        packages.reverse ()
        for p in packages:
            self.remove_package (p) 


def get_cli_parser ():
    p = optparse.OptionParser ()

    p.usage = '%prog [OPTION]... COMMAND\n\nCommands:\n'
    d = Command.__dict__
    commands = [(k, d[k].__doc__) for k in d.keys ()
                if d[k].__doc__ and type (d[k]) == type (lambda x: x)]
    commands.sort ()

    for (command, doc) in commands:
        p.usage += "    %s - %s\n" % (re.sub ('_', '-', command), doc)

    p.add_option ('-B', '--branch',
                  default="HEAD",
                  dest='branch',
                  help="VC branch to use")
    
    p.add_option ('-p', '--platform',
                  default=None,
                  dest='platform',
                  metavar="PLATFORM",
                  help="platform to use")
    
    p.add_option ('', '--name',
                  help="print package name only",
                  action="store_true",
                  dest="print_only_name")
    p.add_option ('-r','--root',
                  help="set platform root",
                  metavar="DIR",
                  dest="root",
                  action="store")
    p.add_option ('-x', '--no-deps',
                  help="ignore dependencies",
                  action="store",
                  dest="no_deps")
    p.add_option ('','--dbdir',
                  action="store",
                  dest="dbdir",
                  help="set db directory")
    p.add_option ('-v', '--verbose',
                  action='store_true',
                  dest="be_verbose",
                  help="be verbose")


    
    return p




def parse_options ():
    p = get_cli_parser ()
    (options, arguments) = p.parse_args()

    options.command = ''
    options.arguments = []
    
    if len (arguments) > 0:
        options.command = re.sub ('-', '_', arguments.pop (0))
        
    options.arguments = arguments
    if not options.root:
        if not options.platform:
            sys.stderr.write ('need platform or root setting, use -p option')
            sys.stderr.write ('\n\n')
            p.print_help()
            sys.exit (2)
        options.root = ('target/%s/system' % options.platform)


    return options



def main ():
    options = parse_options ()

    target_manager = gup.DependencyManager (options.root, oslog.Os_commands ("/dev/null"), dbdir=options.dbdir)
    
    if options.command == 'install':
        platform = options.platform
        target_manager.read_package_headers ('uploads/%(platform)s/' % locals (), options.branch)
#        target_manager.read_package_headers ('uploads/%(platform)s-cross/' % locals(), options.branch)
    
    if options.command:
        commands = Command (target_manager, options)
        if options.command in Command.__dict__:
            Command.__dict__[options.command] (commands)
        else:
            sys.stderr.write ('no such command: ' + options.command)
            sys.stderr.write ('\n')
            sys.exit (2)

if __name__ == '__main__':
    main ()
