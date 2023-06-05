import networkx as nx
import matplotlib.pyplot as plt


class State:
    def __init__(self, names=None):
        if names is None:
            names = []
        if not isinstance(names, list):
            names = [names]
        self.names = names
        self.num = 0

    def merge(self, y):
        self.names = list(set(self.names) | set(y.names))

    def __str__(self):
        if len(self.names) == 1:
            return self.names[0]
        self.names.sort()
        return '[' + ', '.join(self.names) + ']'

    def __eq__(self, other):
        return len(self.names) == len(other.names) and len(self.names) == len(set(self.names) | set(other.names))

    def __contains__(self, item):
        return len(self.names) == len(set(self.names) | set(item.names))

    def __len__(self):
        return len(self.names)

    def to_nx_node(self, is_final=False):
        return self.num, {'names': self.names, 'name_str': self.__str__(),
                          'final': is_final, 'initial': False}


class Transition:
    def __init__(self, fr, to, char):
        if not isinstance(to, list):
            to = [to]
        self.fr = fr
        self.to = to
        self.char = char

    def __str__(self):
        to_str = ', '.join(str(state) for state in self.to)
        template = '({}, {} -> {})' if len(self.to) == 1 else '({}, {} -> {{{}}})'
        return template.format(self.fr, self.char, to_str)

    def to_nx_edge(self):
        edges = []
        for to in self.to:
            edges.append((self.fr.num, to.num, {'char': self.char}))
        return edges


class Function:
    def __init__(self, transitions=None):
        if transitions is None:
            transitions = []
        self.transitions = transitions

    def __iter__(self):
        return self.transitions.__iter__()

    def __getitem__(self, item):
        return self.transitions[item]

    def __setitem__(self, key, value):
        self.transitions[key] = value

    def __str__(self):
        ret_str = ' | '.join(str(transition) for transition in self.transitions)

        return ret_str

    def append(self, transition):
        self.transitions.append(transition)

    def to_nx_edges(self):
        edges = []
        for transition in self.transitions:
            edges += transition.to_nx_edge()
        return edges


class Automaton:
    def __init__(self, states=None, function=Function(), characters=None, initial=None, final=None):
        if characters is None:
            characters = []
        if states is None:
            states = []
        if final is None:
            final = []
        self.states = states
        self.function = function
        self.initial = initial
        self.final = final
        self.characters = characters

    def __str__(self):
        states_str = '{' + ', '.join([str(state) for state in self.states]) + '}'

        characters_str = '{' + ', '.join([str(char) for char in self.characters]) + '}'

        final_str = '{' + ', '.join([str(final) for final in self.final]) + '}'

        return '{}\n{}\n{}\n{}\n{}\n'.format(states_str, characters_str, self.function, self.initial, final_str)

    def transition(self, state, char):
        # Compute the next state(s) after transitioning with a character
        next_state = State()

        for transition in self.function:
            if transition.fr in state and transition.char == char:
                for state in transition.to:
                    next_state.merge(state)

        return next_state if len(next_state) > 0 else None

    def to_dfa(self):
        dfa_states = []
        dfa_function = Function()
        dfa_initial = State()
        dfa_final = []

        dfa_initial = self.initial

        for state in self.states:
            dfa_states.append(state)

        for final in self.final:
            dfa_final.append(final)

        for state in dfa_states:
            # 处理字母表中的每个字符
            for char in self.characters:
                # 获取使用字符进行转换后的下一个状态
                next_state = self.transition(state, char)
                # 如果转换后为空集，则不考虑
                if next_state is None:
                    continue
                flag = False
                for final in self.final:
                    if final in next_state:
                        flag = True

                # 检查下一个状态是否已经存在于DFA中
                if next_state not in dfa_states:
                    dfa_states.append(next_state)
                    if flag:
                        dfa_final.append(next_state)
                else:
                    # 如果已经存在，则替换为现有的状态
                    for state_ in dfa_states:
                        if next_state == state_:
                            next_state = state_

                transition = Transition(state, next_state, char)
                dfa_function.append(transition)

        # 创建新的自动机对象
        dfa = Automaton(states=dfa_states, function=dfa_function, characters=self.characters,
                        initial=dfa_initial, final=dfa_final)

        return dfa

    def to_networkx(self):
        graph = nx.DiGraph()
        for i in range(len(self.states)):
            self.states[i].num = i
        print(len(self.states))
        graph.add_nodes_from([state.to_nx_node(is_final=state in self.final) for state in self.states])
        graph.add_edges_from(self.function.to_nx_edges())
        graph.nodes[self.initial.num]["initial"] = True
        return graph
