from gub import target

class Mingw_extras (target.AutoBuild):
    source = 'http://lilypond.org/download/gub-sources/mingw-extras-0.1.tar.gz'
    dependencies = ['tools::libtool']
    subpackage_names = ['']
