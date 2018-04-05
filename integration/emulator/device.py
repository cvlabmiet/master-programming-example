import re, operator, array

class Lram(bytearray):
    pass

class Pram(Lram):
    def __init__(self):
        # grammar: [u8:0]add(u8:0, u8:100)
        # op[0] - outputs
        # op[1] - operator
        # op[2] - inputs
        self.instruction = re.compile(r'\[([^\]]+)\](\w+)\(([^\)]+)\)')
        self.operation = dict(add=operator.add, mul=operator.mul, mod=operator.mod, sub=operator.sub, div=operator.truediv)
        self.type = dict(i8='b', u8='B', s16='h', u16='H', s32='l', u32='L', f32='f')

    def _parse_arguments(self, op, lram):
        arguments = [x.split(':') for x in op.split(',')]
        return [array.array(self.type[x[0]], lram[int(x[1]):]) for x in arguments]

    def _vectorize(self, op, output, inputs):
        for x in zip(range(len(output)), *inputs):
            output[x[0]] = op(*x[1:])

    def run(self, lram):
        operations = self.instruction.findall(str(self).replace(' ', ''))
        for op in operations:
            output = self._parse_arguments(op[0], lram)[0]
            inputs = self._parse_arguments(op[2], lram)
            self._vectorize(self.operation[op[1]], output, inputs)
            lram[:] = output.tobytes()

class Unit(object):
    def __init__(self):
        self.lram = Lram()
        self.pram = Pram()

class Ctrl(list):
    def __init__(self, units):
        self.units = units

    def wait(self):
        for number in self:
            unit = self.units[number]
            unit.pram.run(unit.lram)

        res = self[:]
        del self[:]
        return res

class Device(object):
    def __init__(self, units):
        self.units = [Unit() for _ in range(units)];
        self.ctrl = Ctrl(self.units)
