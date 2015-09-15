_PREFIX2DIGIT_DICT = {
    "" : 0,
    "m" : -3,
    "u" : -6,
    "n" : -9
    }

class Prefix():
    prefix2digit_dict = _PREFIX2DIGIT_DICT
    digit2prefix_dict = dict(
        (v, k) for k, v in _PREFIX2DIGIT_DICT.items())
    
    def __init__(self, arg):

        @functools.singledispatch
        def factory(arg):
            raise ValueError("can't make \
instance by {arg.__class__.__name__} object {arg}"\
                             .format(**locals()))
        @factory.register(str)
        def _(string):
            if string in self.prefix2digit_dict:
                self.prefix = string
                self.digit  = self.prefix2digit_dict[string]
            else:
                raise ValueError("{string} is not valid prefix"\
                                 .format(**locals()))
        @factory.register(int)
        def _(digit):
            if digit in self.digit2prefix_dict:
                self.prefix = self.digit2prefix_dict[digit]
                self.digit  = digit
            else:
                raise ValueError("prefix equals e{digit} is not valid"\
                                 .format(**locals()))

        factory(arg)



    def __repr__(self):
        return 'Prefix "{self.prefix}" equals e{self.digit}'\
               .format(**locals())



class PrefixedNumber:
    prefix_class = Prefix
    def __new__(cls, num = 0, prefix = None):
        new_num = super(PrefixedNumber, cls).__new__(cls, num)
        new_num.prefix = prefix
        return new_num

    def __repr__(self):
        
        if self.prefix is None:
            log10 = np.log10(abs(self))
            digits = sorted(self.prefix_class.digit2prefix_dict)
            for digit0, digit1 in zip(digits[:], digits[1:]):
                if digit0 <= log10 < digit1:
                    self.prefix = self.prefix_class(digit0)
            if self.prefix is None:
                self.prefix = self.prefix_class(digits[-1])

        return "{0} {1}".format(
            self / 10 ** self.prefix.digit,
            self.prefix.prefix
            )

class Unit:
    unit = ""
    def __repr__(self):
        return "{0}{1.unit}".format(
            super().__repr__(),
            self
            )

class Voltage(Unit):
    unit = "V"

class Current(Unit):
    unit = "A"


class PrefixedFloat(PrefixedNumber, float):pass
class VoltageFloat(Voltage, PrefixedFloat):pass
class CurrentFloat(Current, PrefixedFloat):pass


del _PREFIX2DIGIT_DICT
