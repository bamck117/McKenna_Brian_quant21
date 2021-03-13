"""
Divisible.py

Author: Brian McKenna 

This file defines the function divisible(s, x) and the helper functions associated with it. This
function takes parameters string 's' that can contain any combonation of letters and numerical 
digits and non-negative integer 'x'. Using these parameters, divisible(s, x) returns a list
of all the consecutive integer values combonations contained in 's' that are divisible by 'x', 
but do not contain 'x' as a digit. Ex. divisible("hello4567hi123", 2) --> [4, 6, 56, 456]. 
"""

def getNumStrLyst(s):
    """Takes string 's' and returns the chunks of that string that contain numerical 
    digits in a list"""
    numLyst = [str(i) for i in list(range(10))]
    newstr = ""
    for item in s:
        if item not in numLyst:
            newstr += 'a'
        else:
            newstr += item
    lyst = newstr.split('a')
    for item1 in lyst.copy():
        if item1 == '':
            lyst.remove(item1)
    return lyst


def getNumComboLyst(num):
    """Returns all the consecutive digit combonations of a given string number num
    in a list developed recursively"""
    if num == "":
        return []
    else:
        x = getNumComboLystHelper(num)
        return x + getNumComboLyst(num[1:])


def getNumComboLystHelper(num):
    """Helper function to getNumComboLyst(num) that trims possible string combonations 
    from right to left recursively based on num and collects them into a list """

    #Ex: getNumComboLystHelper("456") --> ['456', '45', '4'] 
    if num == "":
        return []
    else:
        return [num] + getNumComboLystHelper(num[:len(num) - 1])

def divisible(s, x):
    if x <= 0:
        return []
    else:
        strNumLyst = getNumStrLyst(s)
        totalLyst = []
        for num in strNumLyst:
            totalLyst += getNumComboLyst(num)

        finalLyst = []
        for item in totalLyst:
            if ((int(item) not in finalLyst) and ((int(item) % x) == 0)) and (str(x) not in item):
                finalLyst.append(int(item))
        finalLyst = sorted(finalLyst)
    return finalLyst

