from gub import target

class Libffi (target.AutoBuild):
    source = 'ftp://sourceware.org/pub/libffi/libffi-3.0.9.tar.gz'
    dependencies = [
        'tools::automake',
        'tools::libtool',
        'tools::pkg-config',
        ]
    # huh?
    install_flags = (target.AutoBuild.install_flags
                     + """ includesdir='$(includedir)' """ )
    def install (self):
        target.AutoBuild.install (self)
        self.system ('cd %(install_prefix)s && mv lib/libffi-3.0.9/include .')
        self.system ('cd %(install_prefix)s && rm -rf lib/libffi-3.0.9')
                
