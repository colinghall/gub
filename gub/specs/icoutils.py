from gub import toolpackage

class Icoutils (toolpackage.ToolBuildSpec):
    def __init__ (self, settings):
        toolpackage.ToolBuildSpec.__init__ (self, settings)
	from gub import mirrors
        self.with_template (version='0.26.0', mirror=mirrors.nongnu_savannah)
    def get_build_dependencies (self):
        return ['libpng-devel']
    def get_dependency_dict (self):
        return {'': ['libpng']}
    def configure_command (self):
        return (toolpackage.ToolBuildSpec.configure_command (self)
                + ' --with-libintl-prefix=%(system_prefix)s/ ')

class Icoutils__darwin (Icoutils):
    def patch (self):
        for f in 'wrestool', 'icotool':
            self.file_sub ([(r'\$\(LIBS\)', '$(INTLLIBS) $(LIBS)')],
                           '%(srcdir)s/' + f + "/Makefile.in")

Icoutils__darwin__x86 = Icoutils__darwin
