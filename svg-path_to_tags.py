# SVG Path 2 tags converter (c) 2020 Baltasar MIT License <baltasarq@gmail.com>

class SVG:
    def __init__(self):
        self._cmds = []
        
    @property
    def cmds(self):
        return list(self._cmds)
    
    def add(self, cmd):
        self._cmds.append(cmd)
        
    def add_all(self, lcmds):
        self._cmds = self._cmds + lcmds
        
    def __str__(self):
        toret = ""
        
        for cmd in self._cmds:
                toret += str(cmd) + '\n'
                
        return str.join('\n', [str(cmd) for cmd in self._cmds])
    
    
class Cmd:
    def __init__(self, id, args):
        self._id = id
        self._args = list(args)
        
    @property
    def id(self):
        return self._id
        
    @property
    def args(self):
        return list(self._args)
    
    def add(self, arg):
        self._cmds.append(arg)
    
    def __str__(self):
        return self.id + ": " + str.join(", ", [str(arg) for arg in self._args])
    

        

class XmlCmd:
    def __init__(self, cmd, pos):
        self._cmd = cmd
        self._pos = pos
        
    @property
    def pos(self):
        return self._pos
    
    @property
    def cmd(self):
        return self._cmd
        
    _CLASS_ASSOCIATIONS = {
        CmdMove:    XmlCmdMove,
        CmdMoveTo:  XmlCmdMoveTo,
        CmdLine:    XmlCmdLine,
        CmdLineTo:  XmlCmdLineTo
    }
    
    @staticmethod
    def create_for(cmd, pos):
        toret = XmlCmd._CLASS_ASSOCIATIONS.get(cmd.__class__)
        
        if not toret:
            raise NotImplementedError("No XML command for: " + str(cmd))
        
        return toret(cmd, pos)
        
        
class CmdMove(Cmd):
    NUM_ARGS = 2
    
    def __init__(self, x, y):
        super().__init__("move", [x, y])


class XmlCmdMove(XmlCmd):
    def __init__(self, cmd, pos):
        super().__init__(cmd)
        
    def generate(self):
        self._pos[0] = self._cmd.args[0]
        self._pos[1] = self._cmd.args[1]
        
        return self._pos
        
    def __str__(self):
        return ""    


class CmdMoveTo(Cmd):
    NUM_ARGS = 2
    
    def __init__(self, x, y):
        super().__init__("move_to_delta", [x, y])
        
        
class XmlCmdMoveTo(XmlCmd):
    def __init__(self, cmd, pos):
        super().__init__(cmd)
        
    def generate(self):
        self._pos[0] += self._cmd.args[0]
        self._pos[1] += self._cmd.args[1]
        
        return self._pos
        
    def __str__(self):
        return ""
        

class CmdLine(Cmd):
    NUM_ARGS = 2
    
    def __init__(self, x, y):
        super().__init__("line", [x, y])
        

class XmlCmdLine(XmlCmd):
    def __init__(self, cmd, pos):
        super().__init__(cmd)
        
    def generate(self):
        self.org = list(self._pos)
        self._pos[0] = self._cmd.args[0]
        self._pos[1] = self._cmd.args[1]
        
        return self._pos
        
    def __str__(self):
        return ("<line x1=\"" + self.org[0]
                    + "\" y1=\"" + self.org[1]
                    + "\" y1=\"" + self._pos[0]
                    + "\" y2=\"" + self._pos[1]
                    + "\"/>")
    

class XmlCmdLineTo(XmlCmd):
    def __init__(self, cmd, pos):
        super().__init__(cmd)
        
    def generate(self):
        self.org = list(self._pos)
        self._pos[0] += self._cmd.args[0]
        self._pos[1] += self._cmd.args[1]
        
        return self._pos
        
    def __str__(self):
        return ("<line x1=\"" + self.org[0]
                    + "\" y1=\"" + self.org[1]
                    + "\" y1=\"" + self._pos[0]
                    + "\" y2=\"" + self._pos[1]
                    + "\"/>")        


class CmdLineTo(Cmd):
    NUM_ARGS = 2
    
    def __init__(self, x, y):
        super().__init__("line_to", [x, y])
    
    
class Parser:
    def __init__(self, str_path):
        self._str_path = str(str_path).strip()
        self._dict_cmds = {
            'm': CmdMoveTo,
            'M': CmdMove,
            'L': CmdLine,
            'l': CmdLineTo
        }
        
    def parse(self):
        i = 0
        toret = SVG()
        
        while i < len(self._str_path):
            ch = self._str_path[i]
            cmd = None
            
            if ch == ' ':
                continue
            else:
                cmd_class = self._dict_cmds.get(ch)
                
                if cmd_class:
                    i, args = self.read_args(cmd_class.NUM_ARGS, i + 1)
                    cmd = cmd_class(*args)
                else:
                    raise(NotImplementedError("no cmd: " + ch + ", at: " + str(i)))
   
            i += 1
            i = self.skip_spaces(i)
            toret.add(cmd)
            
        return toret
    
    def read_args(self, num_args, pos):
        toret = []
        
        for _ in range(num_args):
            pos, arg = self.read_arg(pos)
            toret.append(arg)
            
        return (pos, toret)
    
    def read_arg(self, pos):
        pos = self.skip_spaces(pos)
        arg = ""
        
        if self._str_path[pos] == '-':
            arg = '-'
            pos += 1
        
        while pos < len(self._str_path) and self._str_path[pos].isdigit():
            arg += self._str_path[pos]
            pos += 1
            
        return (pos, arg)
    
    def skip_spaces(self, pos):
        while pos < len(self._str_path) and self._str_path[pos] == ' ':
            pos += 1
            
        return pos
    

class XMLSVG:
    def __init__(self, svg):
        self._svg = svg
        
    def generate(self):
        pos = [0, 0]
        toret = []
        
        for cmd in self._svg.cmds:
            xml_cmd = XmlCmd.create_for(cmd, pos)
            pos = xml_cmd.generate()
            toret.append(xml_cmd)
            
        return toret
        
    def __str__(self):
        return str.join('\n', [str(cmd) in self.generate()])


if __name__ == "__main__":
    print(str(XMLSVG(Parser("M111 222 L 333 444 l555 -666").parse())))
