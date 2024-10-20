# This is a sample Python script.



def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def b(fil, simp):
    for i in (0,len(fil)):
        if simp in fil[i]:
            return i
    return -1

def setup(fil):
    ordered_simp = []
    all_simp = []
    for f in fil:
        for s in f:
            all_simp.append(s)
    all_simp = list(set(all_simp)) # remove duplicates
    for simp in all_simp:
        if len(ordered_simp) == 0:
            ordered_simp.append(simp)
            continue
        for i in (0,len(ordered_simp)):
            if b(fil, simp) < b(fil, ordered_simp[i]):
                ordered_simp.insert(simp, i)
            elif b(fil, simp) == b(fil, ordered_simp[i]):
                if simp in ordered_simp[i]:
                    ordered_simp.insert(simp, i)
        ordered_simp.append(simp)
    return ordered_simp


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # Initiate filtration

    filtration = [['a', 'b', 'c'],
                  ['a', 'b', 'c', 'd', 'ab', 'ac', 'bc'],
                  ['a', 'b', 'c', 'd', 'ab', 'ac', 'bc', 'cd', 'bd'],
                  ['a', 'b', 'c', 'd', 'ab', 'ac', 'bc', 'cd', 'bd', 'bcd']
                 ]

    print(setup(filtration))

