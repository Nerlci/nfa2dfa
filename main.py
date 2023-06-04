import networkx as nx
from matplotlib import pyplot as plt
from automaton import State, Transfer, Func, Automaton


def get_states(state_str: str):
    state_str = state_str.replace('{', '').replace('}', '').replace('}', '').split(',')
    states = []

    for state in state_str:
        states.append(State(state))

    return states


def get_named_state(name_str: str, states: list[State]):
    for state in states:
        if len(state.names) > 1:
            continue
        if state.names[0] == name_str:
            return state


def get_chars(chars_str: str):
    return chars_str.replace('{', '').replace('}', '').replace('}', '').split(',')


def get_trans(trans_str: str, states):
    head_str, to = trans_str.split('->')
    fr, char = head_str.split(',')
    fr, to, char = fr.strip(), to.strip(), char.strip()
    fr, to = get_named_state(fr), get_named_state(to)
    return Transfer(fr, to, char)


def get_func(func_str: str, states):
    func_str = func_str.split('|')
    trans = []
    for trans_str in func_str:
        trans_str = trans_str.strip()
        trans.append(get_trans(trans_str, states))

    return Func(trans)

def get_final(final_str, states):
    state_str = state_str.replace('{', '').replace('}', '').replace('}', '').split(',')


state = get_states(input('Please enter state'))
chars = get_chars(input('Please enter input characters'))
func = get_func(input('Please enter transfer functions'), state)
init = get_named_state(input('Please enter initial state'), state)
final = get_final(input('Please enter final states'), state)