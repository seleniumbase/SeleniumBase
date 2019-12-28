from seleniumbase.virtual_display.easyprocess import EasyProcess
from seleniumbase.virtual_display.abstractdisplay import AbstractDisplay

PROGRAM = 'Xvfb'


class XvfbDisplay(AbstractDisplay):
    '''
    Xvfb wrapper

    Xvfb is an X server that can run on machines with no display
    hardware and no physical input devices. It emulates a dumb
    framebuffer using virtual memory.
    '''
    def __init__(self, size=(1024, 768), color_depth=24,
                 bgcolor='black', fbdir=None):
        '''
        :param bgcolor: 'black' or 'white'
        :param fbdir: If non-null, the virtual screen is memory-mapped
            to a file in the given directory ('-fbdir' option)
        '''
        self.screen = 0
        self.size = size
        self.color_depth = color_depth
        self.process = None
        self.bgcolor = bgcolor
        self.display = None
        self.fbdir = fbdir
        AbstractDisplay.__init__(self)

    @classmethod
    def check_installed(cls):
        p = EasyProcess([PROGRAM, '-help'])
        p.enable_stdout_log = False
        p.enable_stderr_log = False
        p.call()

    @property
    def _cmd(self):
        cmd = [dict(black='-br', white='-wr')[self.bgcolor],
               '-nolisten',
               'tcp',
               '-screen',
               str(self.screen),
               'x'.join(map(str, list(self.size) + [self.color_depth])),
               self.new_display_var,
               ]
        if self.fbdir:
            cmd += ['-fbdir', self.fbdir]
        return [PROGRAM] + cmd
