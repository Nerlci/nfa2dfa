import networkx as nx
from matplotlib import pyplot as plt
from netgraph import Graph
from automaton import State, Transition, Function, Automaton


def get_states(state_str: str):
    # 根据输入的状态字符串，构造状态对象
    state_str = state_str.replace('{', '').replace('}', '').replace(' ', '').split(',')
    states = []

    for state in state_str:
        states.append(State(state))

    return states


def get_named_state(name_str: str, states: list[State]):
    # 根据名字查找状态
    for state in states:
        if len(state.names) > 1:
            continue
        if state.names[0] == name_str:
            return state


def get_chars(chars_str: str):
    # 根据输入的字母表，构造字母表列表
    return chars_str.replace('{', '').replace('}', '').replace(' ', '').split(',')


def get_trans(trans_str: str, states):
    # 根据转换字符串，构造转换对象
    trans_str = trans_str.replace('(', '').replace(')', '')
    head_str, to_str = trans_str.split('->')
    to_str = to_str.replace('{', '').replace('}', '').replace(' ', '').split(',')
    to_states = []
    fr, char = head_str.split(',')
    fr, char = fr.strip(), char.strip()
    fr = get_named_state(fr, states)
    for to in to_str:
        to_states.append(get_named_state(to, states))
    return Transition(fr, to_states, char)


def get_func(func_str: str, states):
    # 根据输入的转换字符串，构造转换函数对象
    func_str = func_str.split('|')
    trans = []
    for trans_str in func_str:
        trans_str = trans_str.strip()
        trans.append(get_trans(trans_str, states))

    return Function(trans)


def get_final(final_str, states):
    # 根据输入的接受状态字符串，构造接受状态列表
    final_str = final_str.replace('{', '').replace('}', '').replace(' ', '').split(',')
    final_states = []
    for final in final_str:
        final_states.append(get_named_state(final, states))
    return final_states


def plot_graph(G):
    # 将networkx图进行可视化绘制
    pos = nx.spring_layout(G)
    node_labels = nx.get_node_attributes(G, 'name_str')
    node_final = nx.get_node_attributes(G, 'final')
    node_initial = nx.get_node_attributes(G, 'initial')
    edge_labels = nx.get_edge_attributes(G, 'char')

    for key in node_final:
        if node_final[key]:
            node_final[key] = 3
        else:
            node_final[key] = 0.5

    for key in node_initial:
        if node_initial[key]:
            node_initial[key] = 'b'
        else:
            node_initial[key] = 'black'

    Graph(G, node_layout=pos, edge_layout='arc', origin=(-1, -1), scale=(3, 3),
          node_size=15., node_labels=node_labels, node_label_fontdict=dict(size=10),
          edge_labels=edge_labels, edge_label_fontdict=dict(size=12),
          arrows=True, edge_layout_kwargs=dict(k=0.025), edge_width=4., node_edge_width=node_final,
          node_edge_color=node_initial
          )

    plt.show()


state = get_states(input(u'请输入状态: '))
chars = get_chars(input(u'请输入输入字母表: '))
func = get_func(input(u'请输入转移函数: '), state)
init = get_named_state(input(u'请输入初始状态: '), state)
final = get_final(input(u'请输入接受状态: '), state)

automaton = Automaton(state, func, chars, init, final)

dfa = automaton.to_dfa()

print(u'转换后的DFA:')
print(dfa)

G = dfa.to_networkx()

plot_graph(G)
