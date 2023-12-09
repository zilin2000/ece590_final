from state import *
import regex
import copy


# NFA is a class with four fields:
# -states = a list of states in the NFA
#  Note that the start state is always state 0
# -accepting = A dictionary, the key is the state id 
#  and value is a boolean indicating which states are acceping
# -alphabet = a list of symbols in the alphabet of the regular language.
#  Note that & can not be included because we use it as epsilon
# -startS = it is the start state id which we assume it is always 0
class NFA:
    def __init__(self):
        self.states = []
        self.is_accepting = dict()
        self.alphabet = []
        self.startS = 0
        pass
    def __str__(self):
        pass
    # You should write this function.
    # It takes two states and a symbol. It adds a transition from 
    # the first state of the NFA to the other input state of the NFA.
    def addTransition(self, s1, s2, sym = '&'):
        # 确保 s1 的 transition 字典中有对应 sym 的条目
        if sym not in self.states[s1.id].transition:
            self.states[s1.id].transition[sym] = set()

        # 在 s1 的 transition 字典中添加到 s2 的转换
        self.states[s1.id].transition[sym].add(s2)
    # You should write this function.
    # It takes an nfa, adds all the states from that nfa and return a 
    # mapping of (state number in old NFA to state number in this NFA) as a dictionary.
    def addStatesFrom(self, nfa):
        state_mapping = {}
        for old_state in nfa.states:
            # 创建一个新的状态，ID为当前NFA状态列表的长度
            new_state = State(len(self.states))
            new_state.transition = copy.deepcopy(old_state.transition) # 深拷贝转换
            self.states.append(new_state)
            state_mapping[old_state.id] = new_state.id  # 映射旧状态ID到新状态ID

        # 更新接受状态信息
        for old_state_id, is_accepting in nfa.is_accepting.items():
            new_state_id = state_mapping[old_state_id]
            self.is_accepting[new_state_id] = is_accepting

        return state_mapping
    # You should write this function.
    # It takes a state and returns the epsilon closure of that state 
    # which is a set of states which are reachable from this state 
    #on epsilon transitions.
    def epsilonClose(self, ns):
        states = []
        for n in ns:
            for sym, nn in self.states[n.id].transition.items():  
                if sym == '&':
                    for s in nn:
                        states.append(s)
        return states
    # It takes a string and returns True if the string is in the language of this NFA
    # def isStringInLanguage(self, string):
    #     queue = [(self.states[0], 0)]
    #     currS = self.states[0]
    #     pos = 0
    #     visited = []
    #     while queue:
    #         currS, pos = queue.pop()
    #         if pos == len(string):
    #             if currS.id in self.is_accepting and self.is_accepting[currS.id]:
    #                 return self.is_accepting[currS.id]
    #             for n in self.epsilonClose([currS]):
    #                 queue.append((n, pos))
    #             continue
    #         for s in self.states:
    #             if s.id == currS.id:
    #                 if string[pos] in s.transition:
    #                     stats = s.transition[string[pos]]
    #                     for stat in stats:
    #                         queue.extend([(stat,pos+1)])
    #                         queue.extend([(s,pos+1) for s in self.epsilonClose([stat])])
    #                 else:
    #                     for n in self.epsilonClose([currS]):
    #                         queue.append((n, pos))
    #                 break
    #     if pos == len(string):
    #         return currS.id in self.is_accepting and self.is_accepting[currS.id]
    #     else:
    #         return False
    # pass

    # def isStringInLanguage(self, string):
    #     queue = [(self.states[0], 0)]
    #     visited = set()
        
    #     while queue:
    #         currS, pos = queue.pop(0)
    #         visited.add((currS.id, pos))
    #         if pos == len(string):
    #             if currS.id in self.is_accepting and self.is_accepting[currS.id]:
    #                 return True
    #             for n in self.epsilonClose([currS]):
    #                 if (n.id, pos) not in visited:
    #                     queue.append((n, pos))
    #             continue

    #         if string[pos] in currS.transition:
    #             for stat in currS.transition[string[pos]]:
    #                 if (stat.id, pos + 1) not in visited:
    #                     queue.append((stat, pos + 1))
    #                     for s in self.epsilonClose([stat]):
    #                         if (s.id, pos + 1) not in visited:
    #                             queue.append((s, pos + 1))

    #     return False
    
    def isStringInLanguage(self, string):
        queue = [(self.states[0], 0)]
        visited = set()
        
        while queue:
            currS, pos = queue.pop(0)
            visited.add((currS.id, pos))

            if pos == len(string):
                if currS.id in self.is_accepting and self.is_accepting[currS.id]:
                    return True
                for n in self.epsilonClose([currS]):
                    if (n.id, pos) not in visited:
                        queue.append((n, pos))
                continue

            if string[pos] in currS.transition:
                for stat in currS.transition[string[pos]]:
                    if (stat.id, pos + 1) not in visited:
                        queue.append((stat, pos + 1))
                        for s in self.epsilonClose([stat]):
                            if (s.id, pos + 1) not in visited:
                                queue.append((s, pos + 1))

        return False

