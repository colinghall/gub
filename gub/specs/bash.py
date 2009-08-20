from gub import context
from gub import target
from gub import tools

class Bash (target.AutoBuild):
    source = 'ftp://ftp.cwru.edu/pub/bash/bash-3.2.tar.gz'
    def _get_build_dependencies (self):
        return ['libtool', 'gettext-devel']

class Bash__mingw (Bash):
    source = 'http://ufpr.dl.sourceforge.net/sourceforge/mingw/bash-2.05b-MSYS-src.tar.bz2&strip=2'
    def patch (self):
        self.file_sub ([(r'test \$ac_cv_sys_tiocgwinsz_in_termios_h != yes',
                         r'test "$ac_cv_sys_tiocgwinsz_in_termios_h" != yes'),
                        ], '%(srcdir)s/configure')
    def config_cache_overrides (self, str):
        str += 'bash_cv_have_mbstate_t=yes\n'
        return str
 
class Bash__tools (tools.AutoBuild, Bash):
# let's not use patch in a bootstrap package
#    patches = ['bash-3.2-librestrict.patch']
    def force_sequential_build (self):
        return True
    @context.subst_method
    def LDFLAGS (self):
        return '%(rpath)'
    def patch (self):
        tools.AutoBuild.patch (self)
        self.file_sub ([('^  (check_dev_tty [(][)];)', r'  /* \1 */')],
                       '%(srcdir)s/shell.c')
    def install (self):
        tools.AutoBuild.install (self)
        self.system ('cd %(install_prefix)s/bin && ln -s bash sh')
    def wrap_executables (self):
        # using rpath
        pass
