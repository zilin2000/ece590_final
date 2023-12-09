from nfa import *
from state import *

class Regex:
    def __repr__(self):
        ans=str(type(self))+"("
        sep=""
        for i in self.children:
            ans = ans + sep + repr(i)
            sep=", "
            pass
        ans=ans+")"
        return ans
    def transformToNFA(self):
        pass
    pass

class ConcatRegex(Regex):
    def __init__(self, r1, r2):
        self.children=[r1,r2]
        pass
    def __str__(self):
        return "{}{}".format(self.children[0],self.children[1])
    def transformToNFA(self):
        # 获取第一个和第二个正则表达式的 NFA
        nfa1 = self.children[0].transformToNFA()
        nfa2 = self.children[1].transformToNFA()

        # 创建一个新的 NFA
        concat_nfa = NFA()

        # 将第一个 NFA 的状态添加到新 NFA 中
        state_mapping1 = concat_nfa.addStatesFrom(nfa1)

        # 将第二个 NFA 的状态添加到新 NFA 中
        state_mapping2 = concat_nfa.addStatesFrom(nfa2)

        # 获取第一个 NFA 的接受状态和第二个 NFA 的起始状态
        accept_states_nfa1 = [state for state, is_accepting in nfa1.is_accepting.items() if is_accepting]
        start_state_nfa2 = nfa2.states[0]

        # 将第一个 NFA 的接受状态的 epsilon 转换指向第二个 NFA 的起始状态
        for accept_state_id in accept_states_nfa1:
            mapped_accept_state = concat_nfa.states[state_mapping1[accept_state_id]]
            mapped_start_state_nfa2 = concat_nfa.states[state_mapping2[start_state_nfa2.id]]
            concat_nfa.addTransition(mapped_accept_state, mapped_start_state_nfa2, '&')

        # 更新新 NFA 的接受状态
        for state_id, is_accepting in nfa2.is_accepting.items():
            mapped_state_id = state_mapping2[state_id]
            concat_nfa.is_accepting[mapped_state_id] = is_accepting

        return concat_nfa
    pass

class StarRegex(Regex):
    def __init__(self, r1):
        self.children=[r1]
        pass
    def __str__(self):
        return "({})*".format(self.children[0])
    def transformToNFA(self):
        # 获取子正则表达式的 NFA
        child_nfa = self.children[0].transformToNFA()

        # 创建一个新的 NFA
        star_nfa = NFA()

        # 将子 NFA 的状态添加到新 NFA
        state_mapping = star_nfa.addStatesFrom(child_nfa)

        # 创建一个新的起始状态和接受状态
        start_state = State(0)
        accept_state = State(len(star_nfa.states))

        # 添加新的起始状态和接受状态到新 NFA
        star_nfa.states.append(start_state)
        star_nfa.states.append(accept_state)

        # 从新的起始状态添加 epsilon 转换到子 NFA 的起始状态和新的接受状态
        star_nfa.addTransition(start_state, star_nfa.states[state_mapping[child_nfa.startS]], '&')
        star_nfa.addTransition(start_state, accept_state, '&')

        # 从每个子 NFA 的接受状态添加 epsilon 转换回到子 NFA 的起始状态和到新的接受状态
        for state_id, is_accepting in child_nfa.is_accepting.items():
            if is_accepting:
                mapped_accept_state = star_nfa.states[state_mapping[state_id]]
                mapped_start_state_nfa2 = star_nfa.states[state_mapping[child_nfa.startS]]
                star_nfa.addTransition(mapped_accept_state, mapped_start_state_nfa2, '&')
                star_nfa.addTransition(mapped_accept_state, accept_state, '&')

        # 设置新的接受状态
        star_nfa.is_accepting[accept_state.id] = True

        return star_nfa
    pass

class OrRegex(Regex):
    def __init__(self, r1, r2):
        self.children=[r1,r2]
        pass
    def __str__(self):
        return "(({})|({}))".format(self.children[0],self.children[1])
    def transformToNFA(self):
        # 获取两个子正则表达式的 NFA
        nfa1 = self.children[0].transformToNFA()
        nfa2 = self.children[1].transformToNFA()

        # 创建一个新的 NFA
        or_nfa = NFA()

        # 将两个子 NFA 的状态添加到新 NFA 中
        state_mapping1 = or_nfa.addStatesFrom(nfa1)
        state_mapping2 = or_nfa.addStatesFrom(nfa2)

        # 创建新的起始状态和接受状态
        new_start_state = State(len(or_nfa.states))
        or_nfa.states.append(new_start_state)
        or_nfa.startS = new_start_state.id

        # 从新的起始状态添加 epsilon 转换指向两个子 NFA 的起始状态
        or_nfa.addTransition(new_start_state, or_nfa.states[state_mapping1[nfa1.states[0].id]], '&')
        or_nfa.addTransition(new_start_state, or_nfa.states[state_mapping2[nfa2.states[0].id]], '&')

        # 合并两个子 NFA 的接受状态
        for state_id, is_accepting in nfa1.is_accepting.items():
            mapped_state_id = state_mapping1[state_id]
            or_nfa.is_accepting[mapped_state_id] = is_accepting

        for state_id, is_accepting in nfa2.is_accepting.items():
            mapped_state_id = state_mapping2[state_id]
            or_nfa.is_accepting[mapped_state_id] = is_accepting
        

        return or_nfa
    pass

class SymRegex(Regex):
    def __init__(self, sym):
        self.sym=sym
        pass
    def __str__(self):
        return self.sym
    def __repr__(self):
        return self.sym
    def transformToNFA(self):
        # 创建一个新的 NFA 对象
        nfa = NFA()

        # 创建两个状态：一个起始状态和一个接受状态
        start_state = State(0)
        accept_state = State(1)

        # 添加状态到 NFA 的状态列表
        nfa.states.append(start_state)
        nfa.states.append(accept_state)

        nfa.addTransition(start_state, accept_state, self.sym)

        # 设置接受状态
        nfa.is_accepting[accept_state.id] = True

        return nfa
    pass

class EpsilonRegex(Regex):
    def __init__(self):
        pass
    def __str__(self):
        return '&'
    def __repr__(self):
        return '&'
    def transformToNFA(self):
        # 创建一个新的 NFA 对象
        nfa = NFA()

        # 创建两个状态：一个起始状态和一个接受状态
        start_state = State(0)
        accept_state = State(1)

        # 添加状态到 NFA 的状态列表
        nfa.states.append(start_state)
        nfa.states.append(accept_state)

        nfa.addTransition(start_state, accept_state,'&')

        # 设置接受状态
        nfa.is_accepting[accept_state.id] = True

        return nfa
    pass

class ReInput:
    def __init__(self,s):
        self.str=s
        self.pos=0
        pass
    def peek(self):
        if (self.pos < len(self.str)):
            return self.str[self.pos]
        return None
    def get(self):
        ans = self.peek()
        self.pos +=1
        return ans
    def eat(self,c):
        ans = self.get()
        if (ans != c):
            raise ValueError("Expected " + str(c) + " but found " + str(ans)+
                             " at position " + str(self.pos-1) + " of  " + self.str)
        return c
    def unget(self):
        if (self.pos > 0):
            self.pos -=1
            pass
        pass
    pass

# R -> C rtail
# rtail -> OR C rtail | eps
# C -> S ctail
# ctail -> S ctail | eps
# S -> atom stars
# atom -> (R) | sym | &
# stars -> * stars | eps


#It gets a regular expression string and returns a Regex object. 
def parse_re(s):
    inp=ReInput(s)
    def parseR():
        return rtail(parseC())
    def parseC():
        return ctail(parseS())
    def parseS():
        return stars(parseA())
    def parseA():
        c=inp.get()
        if c == '(':
            ans=parseR()
            inp.eat(')')
            return ans
        if c == '&':
            return EpsilonRegex()
        if c in ')|*':
            inp.unget()
            inp.fail("Expected open paren, symbol, or epsilon")
            pass
        return SymRegex(c)
    def rtail(lhs):
        if (inp.peek()=='|'):
            inp.get()
            x = parseC()
            return rtail(OrRegex(lhs,x))
        return lhs
    def ctail(lhs):
        if(inp.peek() is not None and inp.peek() not in '|*)'):
            temp=parseS()
            return ctail(ConcatRegex(lhs,temp))
        return lhs
    def stars(lhs):
        while(inp.peek()=='*'):
            inp.eat('*')
            lhs=StarRegex(lhs)
            pass
        return lhs
    return parseR()