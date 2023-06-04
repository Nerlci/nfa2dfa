class State:
    def __init__(self, names=None):
        if names is None:
            names = []
        if not isinstance(names, list):
            names = [names]
        self.names = names

    def merge(self, y):
        self.names = list(set(self.names) & set(y.names))

    def __str__(self):
        if len(self.names) == 1:
            return self.names[0]
        ret_str = '['
        for name in self.names:
            ret_str += name + ', '
        ret_str += ']'
        return ret_str


class Transfer:
    def __init__(self, fr, to, char):
        if not isinstance(to, list):
            to = [to]
        self.fr = fr
        self.to = to
        self.char = char

    def __str__(self):
        return '({}, {} -> {})'.format(self.fr, self.char, self.to)


class Func:
    def __init__(self, trans=None):
        if trans is None:
            trans = []
        self.trans = trans

    def __iter__(self):
        return self.trans.__iter__()

    def __str__(self):
        ret_str = ''
        for trans in self.trans:
            ret_str += trans + ' | '

        return ret_str

    def append(self, trans):
        self.trans.append(trans)


class Automaton:
    def __init__(self, states=None, func=Func(), chars=None, init=None, final=None):
        if chars is None:
            chars = []
        if states is None:
            states = []
        if final is None:
            final = []
        self.states = states
        self.func = func
        self.init = init
        self.final = final
        self.chars = chars

    def __str__(self):
        states_str = '{'
        for state in self.states:
            states_str += state + ', '
        states_str += '}'

        chars_str = '{'
        for char in self.chars:
            chars_str += char + ', '
        chars_str += '}'

        final_str = '{'
        for final in self.final:
            final_str += final + ', '
        final_str += '}'

        return '{}\n{}\n{}\n{}\n{}\n'.format(states_str, chars_str, self.func, self.init, final_str)

    def to_dfa(self):
        new_states = self.states
        new_func = Func()
        new_final = []
        flag = False
        for trans in self.func:
            if len(trans.to) > 1:
                new_state = State()
                for state in trans.to:
                    new_state.merge(state)
                    if state in self.final:
                        flag = True

                if flag:
                    new_final.append(new_state)

                new_states.append(new_state)
                new_func.append(Transfer(trans.fr, [new_state], trans.char))
            else:
                new_func.append(trans)
        return Automaton(new_states, new_func, self.init, new_final)

    def to_networkx(self):
        pass
