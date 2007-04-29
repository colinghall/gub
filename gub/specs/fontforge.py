from gub import toolpackage 
import re

class Fontforge (toolpackage.ToolBuildSpec):
    def __init__ (self, settings):
        toolpackage.ToolBuildSpec.__init__ (self, settings)
        self.with (mirror='http://lilypond.org/download/gub-sources/fontforge_full-%(version)s.tar.bz2',
                   version="20060501")


    def get_build_dependencies (self):
        return ['freetype']

    def patch (self):
        toolpackage.ToolBuildSpec.patch (self)
        self.system ('cd %(srcdir)s && patch -p0 < %(patchdir)s/fontforge-20060501-srcdir.patch')
        self.system ('cd %(srcdir)s && patch -p1 < %(patchdir)s/fontforge-20060501-execprefix.patch')

    def configure_command (self):
        return (toolpackage.ToolBuildSpec.configure_command (self)
                + ' --without-freetype-src ')

    def srcdir (self):
        return re.sub ('_full', '', toolpackage.ToolBuildSpec.srcdir (self))

    def license_file (self):
        return '%(srcdir)s/LICENSE' 
        
    def install_command (self):
        return self.broken_install_command ()

    def packaging_suffix_dir (self):
        return ''