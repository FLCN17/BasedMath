#base to base
#Turns any input number into another base system - convert binary, octal, decimal, hexadeciml, and more - up to 91 chars
#Accepts a number string, inBase, outBase, and msb - can pass as direction or True for right
import random as rn

class basedNumber:
    Digits = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ !@#$%^&*()_+-=<>,.?/[]|~`':;"
    base91_alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                           'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                                        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                                        'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                                        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '!', '#', '$',
                                        '%', '&', '(', ')', '*', '+', ',', '.', '/', ':', ';', '<', '=',
                                        '>', '?', '@', '[', ']', '^', '_', '`', '{', '|', '}', '~', '"']
    randDigits = ""


    def flipString(instr):
        outString = ""
        #flip string over
        for x in range(len(instr)-1,-1,-1):
            outString += instr[x]
        return outString

    def stripPrepend(instr, reverse = True):
        last = 0
        if reverse:
            sloop = len(instr)-1
            eloop = -1
            step = -1
        else:
            sloop = 0
            eloop = len(instr)
            step = 1
        for x in range(sloop, eloop, step):
            while instr[x] == "0":
                last = x
        if reverse and last != 0:
            instr = instr[0:last]
        else:
            instr = instr[last:len(instr)]
        return instr

    def generateDigits():
        #generates a random digit pool for encrypted math
        tdigits = baseConverter.Digits
        while len(tdigits)>0:
            spot = rn.randint(0, len(tdigits)-1)
            baseConverter.randDigits += tdigits[spot]
            tdigits = tdigits.replace(tdigits[spot], "")	

    def toBase(strNum, inBase, outBase, msbin = "l", msbout = "l", digits = Digits, bitLimit = 128):
        num = 0
        total = 0
        outTotal = 0

        #Ensure num is string
        strNum = str(strNum)
        if msbin[0].lower() == "r":
            strNum = baseConverter.flipString(strNum)
        outString = ""

        #get base from input
        if inBase != "lim":
            inBase = int(inBase)
        else:
            inBase = len(digits)
        if outBase != "lim":
            outBase = int(outBase)
        else:
            outBase = len(digits)

        #depending on msb direction,convert from right or left
        power = 0

        #get decimal value
        for x in range(len(strNum)-1,-1,-1):
            num = baseConverter.add((digits.find(strNum[x]) * inBase**power), num, 10)
            power += 1

        #broken here#

        '''
		Goal:
		take number, in base 10, and subtract the equivilant value in the out base ^digit power
		eg 32 -> b16
		get bitspace -
		'''
        #get bitrange
        bits = 4
        while num - outBase**bits > 0:
            bits<<1

        firstnum = False
        inc = 0
        for x in range(bits-1, -1, -1):
            while baseConverter.greater(baseConverter.sub(num, outBase**x, 10), "0", 10) or baseConverter.equal(num, "0", 10):
                inc+=1
                num = baseConverter.sub(num, outBase**x, 10)
            if inc != 0: #dont place prepending zeroes
                firstnum = True
            if firstnum: #output digit at that place
                outString += digits[inc%outBase]
                if inc >= outBase:
                    inc -= outBase

        #if outputting as msb left, flip string
        if msbout[0].lower() == "l":
            outString = baseConverter.flipString(outString)

        return outString

    def add(a, b, base, msbin = "l", msbout = "l", digits = Digits):
        if base != "lim":
            base = int(base)
        else:
            base = len(digits)
        a = str(a)
        b = str(b)

        #if msb to right, swap them around and pretend
        if msbin[0].lower() == "r":
            a = baseConverter.flipString(a)
            b = baseConverter.flipString(b)

        #make even using prepended zeroes
        #find a better way...
        if len(a) < len(b):
            difference = len(b)-len(a)
            newa = "0"*difference
            a = newa+a
        elif len(a) > len(b):
            difference = len(a)-len(b)
            newb = "0"*difference
            b = newb+b

        outString = ""
        newIndex = 0
        for x in range(len(a)-1,-1,-1):
            newIndex += digits.find(a[x])+digits.find(b[x])
            outString += digits[newIndex%base]
            if newIndex >= base:
                newIndex = 1
            else:
                newIndex = 0
            if x == 0 and newIndex:
                outString += str(newIndex)

        baseConverter.stripPrepend(outString)
        #output - check msbout - if left return
        if msbout[0].lower() == "l":
            outString = baseConverter.flipString(outString)

        return outString

    def sub(a, b, base, msbin = "l", msbout = "l", digits = Digits):
        if base != "lim":
            base = int(base)
        else:
            base = len(digits)
        a = str(a)
        b = str(b)

        #if msb to left, swap them around and pretend
        if msbin[0].lower() == "r":
            a = baseConverter.flipString(a)
            b = baseConverter.flipString(b)

        #make even
        if len(a) < len(b):
            difference = len(b)-len(a)
            newa = "0"*difference
            a = newa+a
        elif len(a) > len(b):
            difference = len(a)-len(b)
            newb = "0"*difference
            b = newb+b

        outString = ""
        newIndex = 0

        for x in range(len(a)-1,-1,-1):
            newIndex += digits.find(a[x])-digits.find(b[x])
            if newIndex < 0:
                outString += digits[newIndex+base]
                newIndex = -1
            else:
                outString += digits[newIndex]
                newIndex = 0


        baseConverter.stripPrepend(outString)	

        if msbout[0].lower() == "l":
            outString = baseConverter.flipString(outString)
        print(outString)
        return outString


    def mul(a, b, base, msbin = "l", msbout = "l", digits = Digits):
        #for each number, add it to the above digit 
        if base != "lim":
            base = int(base)
        else:
            base = len(digits)

        #if msb to left, swap them around and pretend
        if msbin[0].lower() == "r":
            a = baseConverter.flipString(a)
            b = blipString(b)

        #make even using prepended zeroes
        if len(a) < len(b):
            difference = len(b)-len(a)
            newa = "0"*difference
            a = newa+a
        elif len(a) > len(b):
            difference = len(a)-len(b)
            newb = "0"*difference
            b = newb+b

        outString = ""
        newIndex = 0

        ###New idea - multiplication is just repeated addition based on digits and power of digits - cycle through,
        # use index to figure out the base^x multiplier, and add anything in the carry - set it to 0
        # 

        #   ab
        # * 0c -> b, c times
        #
        #go through chars
        acc = 0
        power = 0
        carry = 0
        outdig = 0
        for x in range(len(b)-1, -1, -1):
            acc = carry
            for y in range(len(a)-1, -1, -1):
                for z in range(digits.find(b[x])):
                    acc += digits.find(a[y]) * base**power
            power+=1
            #every x shift, both have shifted to the next digit for sure- use a sep power to then write that digit and move the carry forward
            carry = acc//base
            outString += digits[acc%base]
        while carry:
            outString += digits[carry%base]
            carry = carry//base


        baseConverter.stripPrepend(outString)		
        #output - check msbout
        if msbout[0].lower() == "l":
            outString = baseConverter.flipString(outString)
        return outString


    def div(a, b, base, msbin = "l", msbout = "l", digits = Digits):
        #for each number, add it to the above digit 
        if base != "lim":
            base = int(base)
        else:
            base = len(digits)

        #if msb to left, swap them around and pretend
        if msbin[0].lower() == "r":
            a = baseConverter.flipString(a)
            b = baseConverter.flipString(b)

        #make even using prepended zeroes
        if len(a) < len(b):
            difference = len(b)-len(a)
            newa = "0"*difference
            a = newa+a
        elif len(a) > len(b):
            difference = len(a)-len(b)
            newb = "0"*difference
            b = newb+b

        outString = ""
        newIndex = 0

        ##division is really just subtracting until you cant
        #inc every time subtraction doesn't lead to a negative number, then return the inc.
        #while 


        baseConverter.stripPrepend(outString)		
        #output - check msbout
        if msbout[0].lower() == "l":
            outString = baseConverter.flipString(outString)
        return outString



    def mod(a, b, base, msbin = "l", msbout = "l", digits = Digits):
        #for each number, add it to the above digit 
        if base != "lim":
            base = int(base)
        else:
            base = len(digits)

        #if msb to left, swap them around and pretend
        if msbin[0].lower() == "r":
            a = baseConverter.flipString(a)
            b = baseConverter.flipString(b)

        #make even using prepended zeroes
        if len(a) < len(b):
            difference = len(b)-len(a)
            newa = "0"*difference
            a = newa+a
        elif len(a) > len(b):
            difference = len(a)-len(b)
            newb = "0"*difference
            b = newb+b

        outString = ""
        newIndex = 0

        ##division is really just subtracting until you cant
        #inc every time subtraction doesn't lead to a negative number, then return the remainder.



        baseConverter.stripPrepend(outString)		
        #output - check msbout
        if msbout[0].lower() == "l":
            outString = baseConverter.flipString(outString)
        return outString


    def comp(a, b, base, msbin = "l", msbout = "l", digits = Digits):
        #determine if two input strings are inequivalent based on given digits and base
        #is a > b?
        if base != "lim":
            base = int(base)
        else:
            base = len(digits)

        #if msb to left, swap them around and pretend
        if msbin[0].lower() == "r":
            a = baseConverter.flipString(a)
            b = baseConverter.flipString(b)

        #make even using prepended zeroes
        if len(a) < len(b):
            difference = len(b)-len(a)
            newa = "0"*difference
            a = newa+a
        elif len(a) > len(b):
            difference = len(a)-len(b)
            newb = "0"*difference
            b = newb+b

        #verify, digit by digit, that one number is greater- if not, and its not equal, its false- else true
        #eg af > a - treat as
        #  af -a
        # >0a -b
        # -> val(a(0)) > val(b(0))
        res = ""
        greater = False
        equal = False
        lesser = False
        while not greater and not lesser:
            for x in range(0, len(a)):
                if digits.find(a[x]) > digits.find(b[x]):
                    greater = True
                    equal = False
                    res = "great"
                    break
                elif digits.find(a[x]) == digits.find(b[x]):
                    equal = True
                    res = "equal"
                else:
                    lesser = True
                    res = "less"
                    break
        return res



    '''
	returns true if the first number is greater, otherwise
	'''
    def greater(a, b, base, msbin = "l", msbout = "l", digits = Digits):
        if baseConverter.comp(a, b, base, msbin, msbout, digits) == "great":
            return True
        else:
            return False

    def lesser(a, b, base, msbin = "l", msbout = "l", digits = Digits):
        if baseConverter.comp(a, b, base, msbin, msbout, digits) == "less":
            return True
        else:
            return False

    def equal(a, b, base, msbin = "l", msbout = "l", digits = Digits):
        if a == b:
            return True
        else:
            return False



def main():
    baseConverter.generateDigits()
    test1()
    #test2()



def test1():
    num = input("Enter number: ")
    inBase = input("Enter Input Base: ")
    outBase = input("Enter Output Base: ")
    #msb = input("Enter MSB direction: ")
    print(baseConverter.toBase(num, inBase, outBase))

def test2():
    print(baseConverter.add("10","10",10))
    print(baseConverter.add("849","51",10))
    print(baseConverter.add("1","1",2))
    print(baseConverter.add("4634637","999999999",10, digits = baseConverter.randDigits))
    print(baseConverter.add("bb","b",16))
    print(baseConverter.sub("bb","c",16))
    print(baseConverter.sub("bc","c",16))
    print(baseConverter.add("af","c",16))
    print(baseConverter.sub("fff","1",16))
    print(baseConverter.add("fff","1",16))
    print(baseConverter.sub("cory","fuck","lim"))
    print(baseConverter.add("cory","fuck","lim"))
    print("\""+str(baseConverter.toBase(4000005666, 10, "lim"))+"\"")
    print("\""+str(baseConverter.toBase(4000005666, 10, "lim", digits = baseConverter.randDigits))+"\"")

    print(baseConverter.toBase("42", "10", "2", msbout = "l"))

    print(baseConverter.toBase(baseConverter.add(baseConverter.toBase("42", "10", "2", msbout = "l"), 
                                                         baseConverter.toBase("42", "10", "2", msbout = "l"), 
                                                                                                                        2, 
                                                                                                                        msbin = "l",
                                                                                                                        msbout = "l"), 
                                       "2", 
                                                                        "10",
                                                                        msbin = "l", 
                                                                        msbout = "r"))

    print(baseConverter.toBase(baseConverter.add(baseConverter.toBase("42", "10", "2"), 
                                                         baseConverter.toBase("42", "10", "2"), 
                                                                                                                        2), 
                                       "2", 
                                                                        "10"))

def test3():
    num = input("Enter number: ")
    baseLim = input("Enter base limit: ")
    if baseLim != "lim":
        baseLim = int(baseLim)
    else:
        baseLim = len(baseConverter.Digits)+1

    for x in range(2, baseLim):
        print(str(num)+" in base "+str(x)+":\t"+baseConverter.toBase(num, "10", str(x)))
        #print(str(num)+" in base "+str(x)+" (encrypted): "+baseConverter.toBase(num, "10", str(x), digits=baseConverter.randDigits))

def test4():
    print(baseConverter.mul("199", "9", "10"))

main()
