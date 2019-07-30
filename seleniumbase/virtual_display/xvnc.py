from seleniumbase.virtual_display.easyprocess import EasyProcess
from seleniumbase.virtual_display.abstractdisplay import AbstractDisplay

PACKAGE = 'tightvncserver'
PROGRAM = 'Xvnc'
URL = None


class XvncDisplay(AbstractDisplay):
    '''
    Xvnc wrapper
    '''
    def __init__(self, size=(1024, 768), color_depth=24,
                 bgcolor='black', rfbport=5900):
        '''
        :param bgcolor: 'black' or 'white'
        :param rfbport: Specifies the TCP port on which Xvnc listens for
         connections from viewers (the protocol used in VNC is called
         RFB - "remote framebuffer").
         The default is 5900 plus the display number.
        '''
        self.screen = 0
        self.size = size
        self.color_depth = color_depth
        self.process = None
        self.bgcolor = bgcolor
        self.display = None
        self.rfbport = rfbport
        AbstractDisplay.__init__(self)

    @classmethod
    def check_installed(cls):
        EasyProcess([PROGRAM, '-help'], url=URL,
                    ubuntu_package=PACKAGE).check_installed()

    @property
    def _cmd(self):
        cmd = [PROGRAM,
               '-depth', str(self.color_depth),
               '-geometry', '%dx%d' % (self.size[0], self.size[1]),
               '-rfbport', str(self.rfbport),
               self.new_display_var,
               ]
        return cmd
