#import termios
#import sys
#import os
#from nebula.util import module_exists
#
#
#TERMIOS = termios
#
#
#def get_terminal():
#    
#    if module_exists('msvcrt'):
#        import msvcrt
#        return WinTerminal()
#    else:
#        return LinTerminal()
#
#
#class WinTerminal():
#    def getkey(self):
#        return msvcrt.getch()
#    
#
#class LinTerminal():
#    def getkey(self):
#        fd = sys.stdin.fileno()
#        old = termios.tcgetattr(fd)
#        new = termios.tcgetattr(fd)
#        new[3] = new[3] & ~TERMIOS.ICANON & ~TERMIOS.ECHO
#        new[6][TERMIOS.VMIN] = 1
#        new[6][TERMIOS.VTIME] = 0
#        termios.tcsetattr(fd, TERMIOS.TCSANOW, new)
#        c = None
#        try:
#            c = os.read(fd, 1)
#        finally:
#            termios.tcsetattr(fd, TERMIOS.TCSAFLUSH, old)
#        return c