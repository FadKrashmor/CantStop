#Revision: 2
#Includes code aiming to analyse the value of moves
from tkinter import Tk, Frame, Label, Entry, Button, StringVar, \
                    N, S, E, W
TWO_DICE_TOTALS = ('2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12')


def cant_stop_pc(val):
    """
    Input: Tuple - values between 2 and 12 
    Returns: Float - the % chance that you succeed to get one of the 
    given values when rolling dice as in the game "Cant Stop".
    
    Three types of pairings of four dice
              col
       row:   d1 - d2  --> pair 1
                 x
              d3   d4  --> pair 2
          (p6)       (p5)
             (p3) (p4)

    (Terminology is getting confusing: for clarity...
        there are three types of pairings of pairs of dice, to whit...
            pair 1  &  pair 2   = die 1 and die 2, die 3 and die 4
            pair 3  &  pair 4   = die 1 and die 3, die 2 and die 4
            pair 5  &  pair 6   = die 1 and die 4, die 2 and die 3
        and the player will choose which of the three to use.)
    """
    pair1_fail = throws_for_value(val, False)
    pair2_fail = throws_for_value(val, False)
    tot_fails = 0
    for el_a in pair1_fail: 
        for el_b in pair2_fail:
            if el_a[0] + el_b[0] not in val:
                tot_fails += 1 # out of 36*36
            if el_a[1] + el_b[1] not in val:
                tot_fails += 1 # now out of 2*1296
            if el_a[0] + el_b[1] not in val:
                tot_fails += 1 # now out of 3*1296
            if el_a[1] + el_b[0] not in val:
                tot_fails += 1 # now out of 4*1296
    return 100 - tot_fails*100/5184

def doit(*args):
    print("Yo!")
    entries = []
    num1 = total1.get()
    num2 = total2.get()
    num3 = total3.get()
    print('Numbers entered:', num1, num2, num3)
    if num1 in TWO_DICE_TOTALS:
        entries.append(int(num1))
    if num2 in TWO_DICE_TOTALS:
        entries.append(int(num2))
    if num3 in TWO_DICE_TOTALS:
        entries.append(int(num3))
    if len(entries) > 0:
        success_rate = cant_stop_pc(entries)
    else:
        success_rate = 0
    result.set(str(round(success_rate, 2)))
    return

#Utilities..................................................................
def throws_for_value(val, succeed=True, throws=None):
    """
    Input: A value, or list/tuple of values to test.
           Boolean switch whether to test success or failure.
           A list in which to place the result.
    Returns: a list of two-dice throws [x, y] that give the required value.
    """
    if throws == None:
        throws = []
    if type(val) == int:
        test_val = [val]    
    else:
        test_val = val
    for i in range(1,7):
        for j in range(1,7):
            if i + j in test_val:
                if succeed == True:
                    throws.append([i, j])
            else:
                if succeed == False:
                    throws.append([i, j])
    return throws

def throw_percent(scores=None):
    """
    Counts the number of times each total can be thrown using two dice, then
    calculates the percentage chance of rolling each total.
    Returns this info in the given dictionary.
    """
    if scores == None:
        scores = {}
    for i in range(1,7):
        for j in range(1,7):
            throw = i + j
            value = scores.get(throw, 0)
            scores[throw] = value + 1
    total_scores = 0
    for freq in scores.values():
        total_scores += freq
    for key, value in scores.items():
        scores[key] = value, value*100/total_scores
    return scores
           
def calc_pc_val(pc_vals=None):
    # Multiplies column-step-value by % chance of throwing the number
    VALS = (4.33, 2.6, 1.86, 1.44, 1.18, 1, 1.18, 1.44, 1.86, 2.6, 4.33)
    if pc_vals == None:
        pc_vals = []
    scores = throw_percent()
    for key, value in scores.items():
        pc_vals.append(value[1] * VALS[key-2])
    return pc_vals
        
def print_cant_stop_passing(rate, tofile=False):
    """
    Prints all % chances to roll one of three values, ordered by value
    """
    for i in range(2,11):
        for j in range(3,12):
            if (i >= j):
                continue
            for k in range(4,13):
                if (j >= k):
                    continue
                success_rate = cant_stop_pc((i, j, k))
                if success_rate > rate:
                    print('%2d %2d %2d: ' % (i,j,k), end='')
                    print('Likelihood of Success: ', \
                          round(success_rate, 2), '%', sep='')

def print_cant_stop_pass_pc(rate, tofile=False):
    """
    Prints all % chances to roll one of three values, ordered by percentage
    """
    t = []
    for i in range(2,11):
        for j in range(3,12):
            if (i >= j):
                continue
            for k in range(4,13):
                if (j >= k):
                    continue
                success_rate = cant_stop_pc((i, j, k))
                if success_rate > rate:
                    t.append([success_rate, (i, j, k)])
    t.sort()
    for item in t:
        print('%g;' % round(item[0], 2), end='')
        print('%2d; %2d; %2d' % item[1])
                        

if __name__ == "__main__":
    tc = 4
    if tc == 1: #Test 1: Print one percentage calculation, one of three wanted.
        test_val = (4, 6, 7)
        print('TC01: Test values: %d, %d, %d' % \
              (test_val[0], test_val[1], test_val[2]), end=':  ')
        success_rate = cant_stop_pc(test_val)
        print('Likelihood of Success:', round(success_rate, 2), '%')
    if tc == 2:
        print('TC02: the % chance that you succeed \
               to get one of the three values')
        print_cant_stop_passing(0) # All, by dice throw
#        print_cant_stop_pass_pc(0) # All, by %
    if tc == 3:
        print('TC03: get percentage chance of throwing a number with two dice')
        chances = throw_percent()
        for key, value in chances.items():
            print(key, ':', round(value[1], 2))
#            print(key, ':', value[0], '-', round(value[1], 2))
    if tc == 4:
        print('TC04: Not sure how valuable this info. is')
        vals = calc_pc_val()
        for pc in vals:
            print(round(pc, 2))
            
root = Tk()
#rename the title of the window
root.title("Percentage chances")
mainframe = Frame(root).\
            grid(column=0, row=0, sticky=(N, W, E, S))
#
current_row = 1
current_col = 0
label = Label(mainframe, text="Enter totals required when throwing 2 dice").\
             grid(row=current_row, column=current_col, columnspan=3)
#
current_row += 1
t1_label = Label(mainframe, text="Total 1").\
           grid(row=current_row, column=current_col, sticky=W)
current_col +=1
t2_label = Label(mainframe, text="Total 2").\
           grid(row=current_row, column=current_col, sticky=W)
current_col +=1
t3_label = Label(mainframe, text="Total 3").\
           grid(row=current_row, column=current_col, sticky=W)
current_col += 1
run_button = Button(mainframe, text="Calculate %", command=doit).\
             grid(row=current_row, column=current_col, sticky=W)
#
current_row += 1
current_col = 0
total1 = StringVar()
tot1 = Entry(mainframe, textvariable=total1)
tot1.insert(0, "0")
tot1.grid(row=current_row, column=current_col)
current_col +=1
total2 = StringVar()
tot2 = Entry(mainframe, textvariable=total2)
tot2.insert(0, "0")
tot2.grid(row=current_row, column=current_col)
current_col +=1
total3 = StringVar()
tot3 = Entry(mainframe, textvariable=total3)
tot3.insert(0, "0")
tot3.grid(row=current_row, column=current_col)
current_col +=1
result = StringVar()
res = Entry(mainframe, textvariable=result).\
      grid(row=current_row, column=current_col)
root.bind("<Return>", doit)
#
root.mainloop()
