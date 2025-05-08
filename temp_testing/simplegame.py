import numpy as np
import nashpy as nash

print("hello world")

def simpleValueFn(allocation, size):
    value_out = 0.0
    for i in allocation:
        value_out+=(i[1]-i[0])*i[2]
    return value_out

def onlychocolateVal(allocation, size):
    value_out = 0.0
    for i in allocation:
        value_change = (i[1]-max(size//2, i[0]))*i[2]
        if (value_change>0):
            value_out+=value_change
    return value_out


# simple 2 player moving knife
def movingKnifeAlloc(strategies, max_slice):
    out_allocs = [0, 0]
    min_cut = min(strategies)
    min_player = strategies.index(min_cut)
    if (False):
        pass
    # if (strategies[0]==strategies[1]):
    #     random_alloc = [(0, min_cut, 1), (min_cut, max_slice, 1)]
    #     out_allocs[0] = random_alloc
    #     out_allocs[1] = random_alloc
    else:
        out_allocs[min_player] = [(0,min_cut, 2)]
        out_allocs[(min_player+1)%2] = [(min_cut, max_slice, 2)]
    print("alloc out",out_allocs)
    return out_allocs

def getAllocGame(a_strat, b_strat, allocFn, valueFn_lst, max_slice):
    a_payoff = np.zeros((len(a_strat), len(b_strat)))
    b_payoff = np.zeros((len(a_strat), len(b_strat)))
    for i, a_play in enumerate(a_strat):
        for j, b_play in enumerate(b_strat):
            alloc = allocFn([a_play,b_play], max_slice)
            a_payoff[i][j] = valueFn_lst[0](alloc[0], max_slice)
            b_payoff[i][j] = valueFn_lst[1](alloc[1], max_slice)
    return nash.Game(a_payoff, b_payoff)

def floatRange(count):
    out = []
    f = (count-1)*1.0
    for i in range(0,count):
        out.append(i/f)
    return out


print(floatRange(11))
size = 5
testGame = getAllocGame(range(size), range(size), movingKnifeAlloc, [simpleValueFn, onlychocolateVal], size-1)
#testGame = getAllocGame(range(size), range(size), movingKnifeAlloc, [simpleValueFn, simpleValueFn], size-1)

print(testGame)
eqs = testGame.vertex_enumeration()
print("sup enum done")
a = list(eqs)
print("sup enum very done")
for i in a:
    i = np.round(i, 3)
    print(i[0], i[1])

# this isn't going to work to model what's really going on with continuous division of goods. 
# the algorithmic solutions for this type of thing only work for games with discrete inputs,
# they don't give a good picture of the reality with continuous inputs, kinda.
# the real problem with the above is that it doesn't have subgame dynamics. Hence, one of the equilibria produced has
# the chocolate player "threatening" to cut in a position that is purely detrimental to them.
# effectively modelling the subgame-perfect criteria in an implementation is hard. 
# fortunately, this does give me a good enough understanding of the incentive dynamics for moving knife with perfect information.
# in particular, for 2 players, moving knife will always produce a result that is equivalent to a NE outcome if the knife started
# on the opposite side and moved the opposite direction. (no player will ever cut before value=1/2, and if everyone knows that, they'll cut just before value=1/2 for
# the other guy, giving an equivalent result to if played non-nash and knife started on other side. Extending that to 3 player might be tricky, since then the 
# expected payoff for the subgame after someone leaves needs to be considered. Might not be impossible though. Bottom line I'm arriving at is that analyzing the behavior
# of equal division w/ greedy players (and perfect information) might be better done from a theoretical standpoint rather than an implementation standpoint.


