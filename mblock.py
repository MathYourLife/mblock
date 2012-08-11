################################################################################
#
# MBlock
#
# Copyright (C) 2010  Daniel Couture
#
# Release: 0.2 alpha
#
################################################################################
#
#   MBlock is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# MBlock is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Suite 500, Boston, MA  02110-1301, USA
#
################################################################################

import math
from primes_list import primes

############################################################
#
#   NUMBERS AND OPERATIONS
#
############################################################

############################################################
#
#   NUMBERS AND OPERATIONS - NUMBERS
#
############################################################


def getPrimes(up_to=100):
    #TODO adjust algorithm here to grab/calculate more primes on demand, but much too
    # processor intensive for now
    return

class rational:
    "Import numerator and denominator as integers."
    def __init__(self,numerator=1,denominator=1,exact=1):
        self.num = numerator
        self.den = denominator
        self.exact = exact

    def __add__(self,value):
        "Add rational numbers."
        value = toRational(value)
        lcmVal = lcm([self,value])
        aint = int(lcmVal.den/self.den) 
        bint = int(lcmVal.den/value.den)
        newnum = self.num * aint + value.num * bint
        if newnum==0:
            newden=1
        else:
            newden=lcmVal.den
        exact = min(self.exact,value.exact)
        return rational(newnum,newden,exact)

    def __radd__(self,value):
        "Add a rational number from the right."
        return self.__add__(value)
    
    def __sub__(self,value):
        "Subtract rational numbers."
        value = toRational(value)
        lcmVal = lcm([self,value])
        aint = int(lcmVal.den/self.den) 
        bint = int(lcmVal.den/value.den)
        newnum = self.num * aint - value.num * bint
        if newnum==0:
            newden=1
        else:
            newden = lcmVal.den
        exact = min(self.exact,value.exact)
        return rational(newnum,newden,exact)

    def __rsub__(self,value):
        "Subtract a rational number from the right."
        return -self.__add__(-value)
    
    def __mul__(self,value):
        "Multiply rational numbers."
        if type(value) is matrix:
            return value*self
        elif value.__class__ is rational:
            newnum = self.num * value.num
            if newnum==0:
                newden=1
            else:
                newden = self.den * value.den
            exact = min(self.exact,value.exact)
            return rational(newnum,newden,exact)
        else:
            value = toRational(value)
            newnum = self.num * value.num
            if newnum==0:
                newden=1
            else:
                newden = self.den * value.den
            exact = min(self.exact,value.exact)
            return rational(newnum,newden,exact)

    def __rmul__(self,value):
        "Multiply a rational number from the right."
        return self.__mul__(value)

    def __div__(self,value):
        "Divide rational numbers."
        value = toRational(value)
        newnum = self.num * value.den
        if newnum == 0:
            newden=1
        else:
            newden = self.den * value.num
        exact = min(self.exact,value.exact)
        return rational(newnum,newden,exact)

    def __rdiv__(self,value):
        "Divide a rational number from the right."
        return (self.__div__(value)).reciprocal()

    def __pow__(self,value):
        "Exponents on rationals."
        value = toRational(value)
        exp=value.reduce()
        if exp.den==1 or exp.den==-1:
            exact = min(self.exact,exp.exact)
            if value<0:
                num = self.den**exp.num
                den = self.num**exp.num
                return rational(num,den,exact)
            else:
                num = self.num**exp.num
                den = self.den**exp.num
                return rational(num,den,exact)
        elif value.num==0:
            return rational(1,1)
        else:
            return NotImplemented

    def __rpow__(self,value):
        b=toRational(value)
        return b**self
    
    def __abs__(self):
        return rational(abs(self.num),abs(self.den))

    def __eq__(self,value):
        "Check for equivalent rational values."
        value = toRational(value)
        if self.num==0 and value.num==0:
            return True
        if self.den==0 and value.den==0:
            return True
        if self.num*value.den == self.den*value.num:
            return True
        else:
            return False

    def __ne__(self,value):
        "Check for non equivalent rational values."
        value = toRational(value)
        if self==value:
            return False
        else:
            return True

    def __le__(self,value):
        "Check for less than or equal to."
        value = toRational(value)
        a=self.reduce()
        b=value.reduce()
        lcmVal = lcm([a,b])
        newnuma = a.num * (lcmVal.den/a.den)
        newnumb = b.num * (lcmVal.den/b.den)
        if newnuma<=newnumb:
            return True
        else:
            return False
    
    def __ge__(self,value):
        "Check for greater than or equal to."
        value = toRational(value)
        a=self.reduce()
        b=value.reduce()
        lcmVal = lcm([a,b])
        newnuma = a.num * (lcmVal.den/a.den)
        newnumb = b.num * (lcmVal.den/b.den)
        if newnuma>=newnumb:
            return True
        else:
            return False

    def __lt__(self,value):
        "Check less than."
        value = toRational(value)
        # Quick check for + vs - vs 0
        if (self.num == 0):
            self_group = 0
        elif (self.num >= 0 and self.den >= 0) or (self.num < 0 and self.den < 0):
            self_group = 1
        else:
            self_group = -1
        if (value.num == 0):
            value_group = 0
        elif (value.num >= 0 and value.den >= 0) or (value.num < 0 and value.den < 0):
            value_group = 1
        else:
            value_group = -1
        if (self_group != value_group):
            if self_group == -1:
                return True
            elif self_group == 0 and value_group == 1:
                return True
            else:
                return False
        a=self.reduce()
        b=value.reduce()
        lcmVal = lcm([a,b])
        newnuma = a.num * (lcmVal.den/a.den)
        newnumb = b.num * (lcmVal.den/b.den)
        if newnuma<newnumb:
            return True
        else:
            return False
    
    def __gt__(self,value):
        "Check greater than."
        value = toRational(value)
        a=self.reduce()
        b=value.reduce()
        lcmVal = lcm([a,b])
        newnuma = a.num * (lcmVal.den/a.den)
        newnumb = b.num * (lcmVal.den/b.den)
        if newnuma>newnumb:
            return True
        else:
            return False

    def __neg__(self):
        "Negate value."
        if self.den<0:
            return rational(self.num,-self.den,self.exact)
        else:
            return rational(-self.num,self.den,self.exact)

    def __pos__(self):
        return self

    def __mod__(self,value):
        "Modulus for rational values."
        a = int(self/value);
        return self - (value * a.num)

    def __rmod__(self,value):
        "Modulus for rational values."
        return value - (self * int(value/self))

    def value(self):
        "Return integer or float value."
        if self.den==0:
            raise ZeroDivisionError
        else:
            if self.num%self.den==0:
                # Return integer if modulus is zero
                return self.num//self.den
            else:
                # Return float
                return self.num/self.den

    def reduce(self):
        "Reduce rational number to relatively prime."
        if self.num==1 or self.den==1:
            return self
        elif self.num == self.den:
            n = rational(1)
        else:
            
            num=primefactorization(self.num).factors()
            den=primefactorization(self.den).factors()
            
            divisor = 1
            getPrimes(min(len(num),len(den)))
            for n in range(0,min(len(num),len(den))):
                divisor*=primes[n]**min(num[n],den[n])
            n = rational(self.num//divisor,self.den//divisor,self.exact)
        return n

    def reciprocal(self):
        "Reciprocal of the rational value."
        if self.num==0:
            if self.den>0:
                return rational(1,0,0)
            else:
                return rational(-1,0,0)
        elif self.den==0:
            return rational(0,1,1)
        else:
            return rational(self.den,self.num,self.exact)

    def printout(self,show_sign=False):
        "Print a basic representation of the rational number"
        s = sign(self,show_sign)
        if self.den == 0:
            return s+'infinity'
        num = abs(self.num)
        den = abs(self.den)
        whole = int(num/den)
        mod = abs(self.num) % abs(self.den)
        if whole != 0:
            s = s + '%d ' % whole
        if mod != 0:
            s = s + '%d/%d' % (abs(mod),abs(self.den))
        if whole == 0 and mod == 0:
            s = '0'
        return s.strip()

    def printdecimal(self,show_sign=False):
        "Print the decimal equivalent with at least 20 decimal places if needed."
        s = self.latexdec(show_sign=show_sign)
        if s.find('\overline{')>0:
            repeat=s[s.find('{')+1:s.find('}')]
            s = s.replace('\overline{','')
            s = s.replace('}','')
            while len(s)<20:
                s=s+repeat
        return s

    def latexfrac(self,show_sign=False):
        "Generate the latex code to represent the rational value."
        s = sign(self,show_sign)
        s = s + '\\frac{%d}{%d}' % (abs(self.num),abs(self.den))
        return s

    def latexmixed(self,show_sign=False):
        "Generate the latex mixed number representation."
        num = abs(self.num)
        den = abs(self.den)
        s = sign(self,show_sign)
        whole = __builtins__.int(num/den)
        mod = abs(self.num) % abs(self.den)
        s = s + '%d \\frac{%d}{%d}' % (whole,abs(mod),abs(self.den))
        return s

    def latexdec(self,show_sign=False):
        "Generate the latex decimal representation."
        whole = __builtins__.int(self.num/self.den)
        num = abs(self.num)
        den = abs(self.den)
        mod = num % den
        repeating=-1
        decimals=[]
        mods=[mod]
        while mod!=0 and repeating==-1:
            mod *= 10
            # print 'Checking mod %d' % mod
            digit = math.trunc(float(mod)/den)
            decimals.append(digit)
            mod -= digit*den
            for m in range(0,len(mods)):
                if mods[m]==mod:
                    # print 'found a repeating modulus at position %d' % m 
                    repeating=m
                    break
            if repeating ==-1:
                mods.append(mod)
        if self.num*self.den < 0:
            s = ('%d' % whole)
        elif show_sign:
            s = ('%+d' % whole)
        else:
            s = ('%d' % whole)
        s = s + '.'
        if repeating==-1:
            for d in decimals:
                s = s + '%d' % d
        else:
            for n in range(0,repeating):
                s = s + '%d' % decimals[n]
            s = s + '\overline{'
            for n in range(repeating,len(decimals)):
                s = s + '%d' % decimals[n]
            s = s + '}'
        if s[-1:]=='.':
            s=s[:-1]
        return s
    
    def latex(self,allowmixed=True,show_sign=False):
        "Generate the best latex form of the rational number."
        if self.den==1:
            if show_sign:
                s = '%+d' % self.num
            else:
                s = '%d' % self.num
        elif abs(self)>1 and allowmixed:
            s = self.latexmixed(show_sign)
        else:
            s = self.latexfrac(show_sign)
        
        return s

def toRational(num):
    "Convert input to a rational number."
    if num.__class__ is rational:
        return num
    elif (num.__class__ is type('string')) or (num.__class__ is unicode):  # Test for string
        if num.find('.')>0:
            numerator = int(num.replace('.',''))
            denominator = 10**(len(num)-num.find('.')-1)
            return rational(numerator,denominator)
        elif num.find('/')>0:
            numerator=int(num[:num.find('/')]).num
            denominator=int(num[num.find('/')+1:]).num
            return rational(numerator,denominator)
        else:
            return rational(int(num))
    elif num.__class__ is type(3):  # Test for integer
        return rational(num)
    elif num.__class__ is type(2.5):   # Test for float
        f=num.as_integer_ratio()
        return rational(f[0],f[1],0)
    else:
        print('Unrecognized type for ',num,type(num))
        raise AttributeError

class infinity:
    def __init__(self,sign):
        if sign >= 0:
            self.sign = 1
        else:
            self.sign = -1
        pass
        
    def __lt__(self,value):
        return True

############################################################
#
#   NUMBERS AND OPERATIONS - OPERATIONS
#
############################################################

def sign(x,show_sign=False):
    "Return the sign of the passed value."
    if x < 0:
        s = '-'
    elif show_sign:
        s = '+'
    else:
        s = ''
    return s
    
def sin(x):
    if x.__class__ is rational:
        t = math.sin(x.value())
        return toRational(t)
    else:
        return toRational(math.sin(x))

def cos(x):
    if x.__class__ is rational:
        t = math.cos(x.value())
        return toRational(t)
    else:
        return toRational(math.cos(x))

def tan(x):
    if x.__class__ is rational:
        t = math.tan(x.value())
        return toRational(t)
    else:
        return toRational(math.tan(x))
    
def atan2(y,x):
    y=toRational(y)
    x=toRational(x)
    if (x.__class__ is rational) and (y.__class__ is rational):
        t = math.atan2(y.value(),x.value())
        return toRational(t)
    else:
        return toRational(math.atan2(y,x))

#def int(x):
#    if x.__class__ is rational:
#        return rational(int(x.num/x.den),1)
#    else:
#        print 'here'
#        return rational(__builtins__.int(x))

#def abs(x):
#    if type(x) is rational:
#        return rational(__builtins__.abs(x.num),__builtins__.abs(x.den),x.exact)
#    elif type(x) is point:
#        return point(abs(x.x),abs(x.y),abs(x.z))
#    else:
#        return __builtins__.abs(x)

def sum(x):
    if x[0].__class__ is rational:
        total=rational(0)
        for n in x:
            total+=n
        return total
    else:
        return __builtins__.sum(x)

def gcf(values=[rational(1,1),rational(1,1)]):
    a=values[0]
    b=values[1]
    if (a.num==0 and a.den==1) or (b.num==0 and b.den==1) or \
       (a.num==1 and a.den==1) or (b.num==1 and b.den==1):
        return rational(1,1)
    if (a.__class__ is rational) and (b.__class__ is rational):
        anum = primefactorization(a.num).factors()
        bnum = primefactorization(b.num).factors()
        aden = primefactorization(a.den).factors()
        bden = primefactorization(b.den).factors()

        gcfnum = 1
        getPrimes(min(len(anum),len(bnum)))
        for n in range(0,min(len(anum),len(bnum))):
            gcfnum*=int(primes[n]**min(anum[n],bnum[n]))
        gcfden = 1
        getPrimes(min(len(aden),len(bden)))
        for n in range(0,min(len(aden),len(bden))):
            gcfden*=int(primes[n]**min(aden[n],bden[n]))
        return rational(gcfnum,gcfden)
    else:
        return 0

def lcm(values=[rational(1,1),rational(1,1)]):
    a=values[0]
    b=values[1]
    if (a.__class__ is rational) and (b.__class__ is rational):
        gcfval=gcf([a,b])
        lcmnum=abs(a.num*b.num//gcfval.num)
        lcmden=abs(a.den*b.den//gcfval.den)
        return rational(lcmnum,lcmden)

class primefactorization:
    def __init__(self,num):
        self.num = num

    def factors(self):
        if self.num==0:
            return []
        elif self.num==1:
            return []
        run = abs(self.num)
        factorList = []
        getPrimes(self.num)
        for p in primes:
            count = 0
            while run % p == 0:
                count+=1
                run/=p
            factorList.append(count)
            if run==1:
                break
        return factorList

    def latex(self):
        fl = self.factors()

        s = sign(self.num)
        first = True
        for n in range(0,len(fl)):
            if fl[n] != 0:
                if first:
                    if fl[n]==1:
                        s = s + ' %s' % (primes[n].printdecimal())
                    else:
                        s = s + ' %s^{%d}' % \
                            (primes[n].printdecimal(),fl[n])
                    first = False
                else:
                    if fl[n]==1:
                        s = s + ' \cdot %s' % (primes[n].printdecimal())
                    else:
                        s = s + ' \cdot %s^{%d}' % \
                            (primes[n].printdecimal(),fl[n])
        return s

def sqrt(x):
    num = math.sqrt(x.num)
    den = math.sqrt(x.den)
    return toRational(num/den)
        
############################################################
#
#   NUMBERS AND OPERATION - MATRICES
#
############################################################

class matrix:
    def __init__(self,matrix=[[1,2,3],[4,5,'6.2']]):
        temp1=[]
        cols = len(matrix[0])
        for row in matrix:
            if len(row) != cols:
                print('Error:  Not a rectangular matrix.')
                raise AttributeError
            temp2 = []
            for col in row:
                temp2.append(toRational(col))
            temp1.append(temp2)
        self.matrix = temp1

    def __setitem__(self, pos, value):
        "Set the value for a matrix cell."
        self.matrix[pos[0]][pos[1]] = toRational(value)

    def __getitem__(self, pos):
        "Get an item of the matrix or a submatrix."
        if type(pos[0]) == slice or type(pos[1]) == slice:
            # If a slice is passed for either argument, return a submatrix.
            new_matrix=[]
            if type(pos[0]) == slice:
                rstart = 0 if pos[0].start==None else pos[0].start
                rstop = self.size()[0] if pos[0].stop==None else pos[0].stop
                rstep = 1 if pos[0].step==None else pos[0].step
            else:
                rstart = pos[0]
                rstop = pos[0]+1
                rstep = 1
            if type(pos[1]) == slice:
                cstart = 0 if pos[1].start==None else pos[1].start
                cstop = self.size()[1] if pos[1].stop==None else pos[1].stop
                cstep = 1 if pos[1].step==None else pos[1].step
            else:
                cstart = pos[1]
                cstop = pos[1]+1
                cstep = 1
            for r in range(rstart,rstop,rstep):
                row=[]
                for c in range(cstart,cstop,cstep):
                    row.append(self[r,c])
                new_matrix.append(row)
            return matrix(new_matrix)
        else:
            # Return a single cell's value of the matrix
            return self.matrix[pos[0]][pos[1]]

    def __add__(self,value):
        "Add two matrices."
        [rows,cols]=self.size()
        if [rows,cols] != value.size():
            print('Error: Matrices to not have the same size for sum.')
            raise AttributeError
        t=[]
        for r in range(rows):t.append([0]*cols)
        for r in range(0,rows):
            for c in range(0,cols):
                t[r][c]=self[r,c]+value[r,c]
        return matrix(t)
        
    def __sub__(self,value):
        "Subtract two matrices."
        [rows,cols]=self.size()
        if [rows,cols] != value.size():
            print('Error: Matrices to not have the same size for sum.')
            raise AttributeError
        t=[]
        for r in range(rows):t.append([0]*cols)
        for r in range(0,rows):
            for c in range(0,cols):
                t[r][c]=self[r,c]-value[r,c]
        return matrix(t)

    def __mul__(self,value):
        "A matrix being multiplied by a scalar or matrix."
        if value.__class__ is rational:
            [rows,cols]=self.size()
            t=[]
            for r in range(rows):t.append([0]*cols)
            for r in range(0,rows):
                for c in range(0,cols):
                    t[r][c]=(self[r,c]*value).reduce()
            return matrix(t)
        elif type(value) is matrix:
            [rows1,cols1]=self.size()
            [rows2,cols2]=value.size()
            if cols1 != rows2:
                print('Error:  Incorrect sized matrices to muliply. %dx%d, %dx%d' % \
                      (rows1, cols1, rows2, cols2))
                raise AttributeError
            t=[]
            for r in range(rows1):t.append([0]*cols2)
            for row in range(0,rows1):
                for col in range(0,cols2):
                    total = rational(0)
                    for n in range(0,cols1):
                        total += self[row,n]*value[n,col]
                    t[row][col]=total.reduce()
            return matrix(t)
        else:
            rvalue = toRational(value)
            [rows,cols]=self.size()
            t=[]
            for r in range(rows):t.append([0]*cols)
            for r in range(0,rows):
                for c in range(0,cols):
                    t[r][c]=self[r,c]*rvalue
            return matrix(t)
            
    def __rmul__(self,value):
        "Multiply a rational value from the left."
        return self.__mul__(value)

    def __pow__(self,value):
        "Exponent on a matrix"
        value=toRational(value)
        if value==-1:
            return self.inverse()
        elif value.den==1:
            m = self
            for n in range(1,value.num):
                m=m*self
            return m
        else:
            return NotImplemented 
        
    def printmatrix(self):
        "Print out a matrix."
        s = ''
        for row in self.matrix:
            for col in row:
                s = s + '%6s' % col.value()
            s = s + '\n'
        return s

    def size(self):
        'Find the size of the matrix rows x cols.'
        rows = len(self.matrix)
        cols = len(self.matrix[0])
        return [rows,cols]

    def det(self):
        'Find the determinant of the matrix.'
        [rows,cols]=self.size()
        if rows!=cols:
            print('Error: Can not take the determinant of a non square matrix.')
            raise AttributeError
        if [rows,cols]==[1,1]:
            return self[0,0]
        else:
            b=rational(0)
            for n in range(0,len(self.matrix)):
                if n%2==0:
                    b = b+self[0,n]*(self.minor(0,n))
                else:
                    b = b-self[0,n]*(self.minor(0,n))
            return b

    def minor(self,minor_row,minor_col):
        'Find the minor matrix after removing row minor_row and column minor_col.'
        minor_matrix = []
        for row in self.matrix:
            minor_matrix.append(row[:minor_col]+row[minor_col+1:])
        m = matrix(minor_matrix[:minor_row]+minor_matrix[minor_row+1:])
        return m.det()
        
    def T(self):
        'Transpose a matrix.'
        [rows,cols]=self.size()
        t=[]
        for r in range(cols):t.append([0]*rows)
        for c in range(0,rows):
            for r in range(0,cols):
                t[r][c] = self[c,r]
        return matrix(t)

    def inverse(self):
        'Calulate the inverse of a matrix.'
        [rows,cols]=self.size()
        if rows!=cols:
            print('Error: Can not take the inverse of a non square matrix.')
            raise AttributeError
        d=self.det()
        if d==0:
            print('Error: Matrix does not have an inverse.')
            raise AttributeError
        t=[]
        for r in range(rows):t.append([0]*cols)
        for r in range(0,rows):
            for c in range(0,cols):
                if (r+c)%2==0:
                    t[c][r] = self.minor(r,c)/d
                else:
                    t[c][r] = (-self.minor(r,c))/d
        return matrix(t)

    def latex(self):
        [rows,cols] = self.size()
        s = '\left[ \\begin{array}{%s}\n' % ('c'*cols)
        for r in range(0,rows):
            for c in range(0,cols):
                s = s + self[r,c].latex() + ' & '
            s = s[:-3] + '\\\\ \n'
        s = s + '\end{array} \\right]\n'
        return s

############################################################
#
#   GEOMETRY
#
############################################################

############################################################
#
#  GEOMETRY - 1D
#
############################################################

class point:
    "Define a point in 3D cartesian space"
    def __init__(self, x=rational(0), y=rational(0), z=rational(0), name='A'):
        self.x = toRational(x)
        self.y = toRational(y)
        self.z = toRational(z)
        self.name = name

    def __add__(self,value):
        "Add the corresponding coordinates of two points."
        xnew = self.x+value.x
        ynew = self.y+value.y
        znew = self.z+value.z
        return point(xnew,ynew,znew)

    def __sub__(self,value):
        "Subtract the corresponding coordinates of two points."
        xnew = self.x-value.x
        ynew = self.y-value.y
        znew = self.z-value.z
        return point(xnew,ynew,znew)

    def __mul__(self,value):
        "Scale each coordinate."
        value=toRational(value)
        xnew = self.x*value
        ynew = self.y*value
        znew = self.z*value
        return point(xnew,ynew,znew)

    def __rmul__(self,value):
        "Scale each coordinate from a value to the left."
        value=toRational(value)
        xnew = self.x*value
        ynew = self.y*value
        znew = self.z*value
        return point(xnew,ynew,znew)
        
    def __truediv__(self,value):
        "Divide each coordinate of the point."
        value=toRational(value)
        xnew = self.x/value
        ynew = self.y/value
        znew = self.z/value
        return point(xnew,ynew,znew)
        
    def __eq__(self,value):
        "Are the two points in the same location?"
        if self.x==value.x and self.y==value.y and self.z==value.z:
            return True
        else:
            return False
    
    def __ne__(self,value):
        "Are there two distinct points?"
        if self==value:
            return False
        else:
            return True

    def reduce(self):
        "Simplify the representation of the coordinates."
        xnew = self.x.reduce()
        ynew = self.y.reduce()
        znew = self.z.reduce()
        return point(xnew,ynew,znew)        
    
    def r(self):
        "Calculate the distance a point is from the origin."
        return sqrt(self.x**2 + self.y**2 + self.z**2)

    def latex(self):
        "Print coordinates for the point in latex format."
        return "(%s,%s,%s)" % (self.x.latex(), self.y.latex(), self.z.latex())

    def tikz(self,color='blue'):
        "Draw the projection of the point onto the x,y coordinate plane."
        return "\\fill [color=%s] (%s,%s) circle (1.5pt);" \
               % (color,self.x.printdecimal(),self.y.printdecimal())

class segment:
    "Define a line segment by two points in 3D cartesian space."
    def __init__(self, pts=[point(rational(0),rational(0),rational(0),'A'), point(rational(1),rational(1),rational(0),'B')]):
        self.pts = pts

    def __eq__(self,segment):
        "Test if the two segments have congruent lengths."
        if self.length() == segment.length():
            return True
        else:
            return False
        
    def __ne__(self,segment):
        "Test if two segment are different lengths."
        if self==segment:
            return False
        else:
            return True
        
    def name(self):
        "Name the segment by the two points."
        return self.pts[0].name + self.pts[1].name
        
    def latexname(self):
        "Generate the latex representation for the segment using point names."
        return "\\overline{%s}" % self.name()

    def latexpts(self):
        "Generate the latex printout of the two points."
        return [self.pts[0].latex(),self.pts[1].latex()]

    def midpoint(self):
        "Calculate the midpoint of the segment."
        p=(self.pts[0]+self.pts[1])/2
        return p

    def length(self):
        "Calculate the length of a segment."
        return sqrt((self.pts[0].x-self.pts[1].x)**2+ \
                    (self.pts[0].y-self.pts[1].y)**2+ \
                    (self.pts[0].z-self.pts[1].z)**2)
    
    def tikz(self,color='black'):
        "Draw the projection of the segment onto the x-y coordinate plane."
        return "\\draw [color=%s] (%s,%s)--(%s,%s);" % \
               (color,self.pts[0].x.printdecimal(), self.pts[0].y.printdecimal(), \
                self.pts[1].x.printdecimal(), self.pts[1].y.printdecimal())

class vector:
    def __init__(self,pts=[point(rational(0),rational(0),rational(0)), \
                           point(rational(1),rational(1),rational(0))],name='u'):
        self.pts = pts
        self.name = name

    def __eq__(self,vec):
        if self.mag()==vec.mag() and self.direction()==vec.direction():
            return True
        else:
            return False

    def __ne__(self,vec):
        if self==vec:
            return False
        else:
            return True
    
    def mag(self):
        c=self.pts[1]-self.pts[0]
        return sqrt(c.x**2+c.y**2+c.z**2)

    def direction(self):
        a=self.pts[0]+point(1,0,0)
        d=angle([a,self.pts[0],self.pts[1]])
        return d

    def unit(self):
        return NotImplemented
    
    def bearing(self):
        a=self.pts[0]+point(1,0,0)
        b=angle([a,self.pts[0],self.pts[1]],bearing=True)
        return b
        
    def tikz(self,color='black'):
        return "\\draw [->,color=%s] (%s,%s)--(%s,%s);" % \
               (color,self.pts[0].x.printdecimal(), self.pts[0].y.printdecimal(), \
                self.pts[1].x.printdecimal(), self.pts[1].y.printdecimal())

def dot_product(vec1,vec2):
    return NotImplemented

def cross_product(vec1,vec2):
    return NotImplemented

class ray:
    def __init__(self,pts=[point(rational(0),rational(0),rational(0),'A'), \
                           point(rational(1),rational(1),rational(0),'B')]):
        self.pts = pts

    def name(self):
        return self.pts[0].name + self.pts[1].name

    def opposite(self):
        p = self.pts[0] - (self.pts[1]-self.pts[0])
        return ray([self.pts[0], p])
    
    def latexname(self):
        return "\\overarrow{%s}" % self.name()
    
    def tikz(self,color='black'):
        return "\\draw [->,color=%s] (%s,%s)--(%s,%s);" % \
               (color,self.pts[0].x.printdecimal(), self.pts[0].y.printdecimal(), \
                self.pts[1].x.printdecimal(), self.pts[1].y.printdecimal())

class angle:
    def __init__(self,pts=[point(rational(1),rational(0),rational(0),'A'), \
                           point(rational(0),rational(0),rational(0),'B'), \
                           point(rational(0),rational(1),rational(0),'C')], \
                 bearing=False):
        self.pts = pts
        u=pts[0]-pts[1]
        v=pts[2]-pts[1]
        a1=atan2(u.y,u.x)
        if a1<0:
            a1+=toRational(2*math.pi)
        a2=atan2(v.y,v.x)
        if a2<0:
            a2+=toRational(2*math.pi)
        if a2<a1:
            a2+=toRational(2*math.pi)

        a=a2-a1
        if bearing:
            a=toRational(math.pi/2)-a
        if a<0:
            a+=toRational(2*math.pi)
        self.radians = a

    def __eq__(self,angle):
        if self.radians==angle.radians:
            return True
        else:
            return False

    def __ne__(self,angle):
        if self.radians==angle.radians:
            return False
        else:
            return True

    def degrees(self):
        return toRational(math.degrees(self.radians.value()))

    def quadrant(self):
        if self.radians < math.pi / 2:
            return "I"
        elif self.radians < math.pi:
            return "II"
        elif self.radians < 3.0 * math.pi / 2:
            return "III"
        elif self.radians < 2.0 * math.pi:
            return "IV"
        
class line:
    "Define a line that passes through two points."
    def __init__(self,pts=[point(rational(0),rational(0),rational(0),'A'), \
                           point(rational(1),rational(1),rational(0),'B')]):
        self.pts = pts

    def name(self):
        return 'line ' + self.pts[0].name + self.pts[1].name        

    def intercepts(self):
        "Intercepts assumes line exists in x-y plane."
        m = slope(self.pts)
        b = self.pts[0].y - m*self.pts[0].x
        x = -b/m
        return [point(x,0,0),point(0,b,0)]

    def slope(self):
        s = slope(self.pts)
        return s

    def pointon(self,specify='x',value=rational(0)):
        if specify=='x':
            m=slope(self.pts)
            b = self.pts[0].y - m*self.pts[0].x
            ynew = m*value+b
            p = point(value,ynew,0)
        elif specify=='y':
            m=slope(self.pts)
            b = self.pts[0].y - m*self.pts[0].x
            xnew = (value-b)/m
            p = point(xnew,value,0)
        return p
        
    def slopeintequation(self):
        i = self.intercepts()
        return "y=%sx%s" % (slope(self.pts).latex(), \
                            i[1].y.latex(show_sign=True))

    def ptslopeequation(self,pt):
        if pt.y==0:
            s='y='
        else:
            s='y%s=' % (-pt.y).latex(show_sign=True)
        if pt.x==0:
            s=s+('%sx' % slope(self.pts).latex())
        else:
            s=s+('%s(x%s)' % (slope(self.pts).latex(), \
                              (-pt.x).latex(show_sign=True)))
        return s

    def tikz(self,color='black',extenstion=0):
        s = "\\draw [<->,color=%s] (%s,%s)--(%s,%s);" % \
            (color,self.pts[0].x.printdecimal(), self.pts[0].y.printdecimal(), \
             self.pts[1].x.printdecimal(), self.pts[1].y.printdecimal())
        
        return s

############################################################
#
#  GEOMETRY - 2D
#
############################################################

def whatPolygon(pts=[point(rational(0),rational(0),rational(0),'A'), \
                            point(rational(1),rational(1),rational(0),'B'), \
                            point(rational(2),rational(0),rational(0),'C')]):

    if len(pts)==3:
        return triangle(pts)
    elif len(pts)==4:
        return quadrilateral(pts)
    else:
        return polygon(pts)

class polygon:
    "Define a polygon by passing points in a clockwise order."
    def __init__(self, pts=[point(rational(0),rational(0),rational(0),'A'), \
                            point(rational(1),rational(1),rational(0),'B'), \
                            point(rational(2),rational(0),rational(0),'C')]):
        self.pts = pts

    def __eq__(self,poly):
        # Check for congruent sides and angles.
        return NotImplemented
    
    def n(self):
        return rational(len(self.pts))

    def sides(self):
        sides=[]
        for n in range(0,len(self.pts)):
            nextside=segment([self.pts[(n)%len(self.pts)], \
                              self.pts[(n+1)%len(self.pts)]])
            sides.append(nextside)
        return sides
        
    def angles(self):
        a=[]
        for n in range(0,len(self.pts)):
            nextangle=angle([self.pts[(n-1)%len(self.pts)], \
                             self.pts[(n)%len(self.pts)], \
                             self.pts[(n+1)%len(self.pts)]])
            a.append(nextangle)            
        return a

    def is_equilateral(self):
        for s in self.sides():
            if s.length() != self.sides()[0].length():
                return False
        return True

    def is_equiangular(self):
        for a in self.angles():
            if a.radians != self.angles()[0].radians:
                return False
        return True

    def is_regular(self):
        if self.is_equilateral() and self.is_equiangular():
            return True
        else:
            return False
        
    def diagonals(self):
        d=[]
        for a in range(0,len(self.pts)-2):
            for b in range(a+2,min(a+len(self.pts)-1,len(self.pts))):
                d.append(segment([self.pts[a],self.pts[b]]))
        return d

    def exterioranglesum(self):
        return toRational(2.0*math.pi)

    def interioranglesum(self):
        return (self.n()-2)*math.pi

    def classify(self):
        group = []
        if self.n()==3:
            group.append('triangle')
        elif self.n()==4:
            group.append('quadrilateral')
        elif self.n()==5:
            group.append('pentagon')
        elif self.n()==6:
            group.append('hexagon')
        elif self.n()==7:
            group.append('heptagon')
        elif self.n()==8:
            group.append('octagon')
        elif self.n()==9:
            group.append('nonagon')
        elif self.n()==10:
            group.append('decagon')
        elif self.n()==12:
            group.append('dodecagon')
        else:
            group.append('%s-gon' % self.n().printdecimal())

        a=self.angles()
        found=0
        for n in a:
            if n.degrees() > 180:
                found=1
                # print 'found one', n.degrees().latex()
        if found==1:
            group.append('concave')
        else:
            group.append('convex')
            
        return group
        
    def tikz(self,color='brown',shading=True):
        fill=''
        if shading:
            cycle = ''
            for p in self.pts:
                new = "(%s,%s)--" % (p.x.printdecimal(),p.y.printdecimal())
                cycle = cycle + new
            cycle = cycle + "(%s,%s)" % \
                    (self.pts[0].x.printdecimal(),self.pts[0].y.printdecimal())
            fill = "\\fill[color=%s,fill=%s,fill opacity=0.1] %s -- cycle;" \
                   % (color,color,cycle)

        sides = ''
        for a in range(0,len(self.pts)):
            s = segment([self.pts[a],self.pts[(a+1)%len(self.pts)]])
            sides = sides + s.tikz() + "\n"
        return sides + fill

class triangle(polygon):
    "Define a triangle by three points in 3D cartesian space."
    def __init__(self, pts=[point(rational(0),rational(0),rational(0),'A'), \
                            point(rational(1),rational(1),rational(0),'B'), \
                            point(rational(2),rational(0),rational(0),'C')],
                 normal=[rational(0),rational(0),rational(1)]):
        self.pts = pts

    def name(self):
        return self.pts[0].name + self.pts[1].name + self.pts[2].name

    def medians(self):
        m1 = segment([self.pts[0],self.sides()[1].midpoint()])
        m2 = segment([self.pts[1],self.sides()[2].midpoint()])
        m3 = segment([self.pts[2],self.sides()[0].midpoint()])
        return [m1,m2,m3]

    def anglebisectors(self):
        return NotImplemented

    def perpendicularbisectors(self):
        return NotImplemented

    def altitudes(self):
        return NotImplemented
    
    def midsegments(self):
        s = self.sides()
        m1 = segment([s[2].midpoint(),s[0].midpoint()])
        m2 = segment([s[0].midpoint(),s[1].midpoint()])
        m3 = segment([s[1].midpoint(),s[2].midpoint()])
        return [m1,m2,m3]
        
    def centroid(self):
        # Find point 2/3 of the way from vertex to midpoint.
        [m1,m2,m3] = self.medians()
        x = m1.pts[1].x - m1.pts[0].x
        y = m1.pts[1].y - m1.pts[0].y
        z = m1.pts[1].z - m1.pts[0].z
        xc = (m1.pts[0].x + (x*2/3)).reduce()
        yc = (m1.pts[0].y + (y*2/3)).reduce()
        zc = (m1.pts[0].z + (z*2/3)).reduce()
        return point(xc,yc,zc)

    def circumcenter(self):
        # Find point equidistant to 3 vertices.
        return NotImplementedError

    def orthocenter(self):
        return NotImplemented

    def incenter(self):
        return NotImplemented

    def latex(self):
        return "\\Delta %s" % self.name()

    def area(self):
        'Incomplete:  Need altitude values!'
        return NotImplemented
        return rational(1,2) * toRational(self.sides()[0].length().value()) * \
               toRational(self.altitudes()[0].length().value())

    def classify(self):
        "Classify a triangle according to side lengths and angle measures."
        side = self.sides()
        angle = self.angles()
        classify = []
        # Classify the triangle according to lengths.
        if side[0].length()==side[1].length() and \
           side[1].length()==side[2].length():
            return ['equilateral','equiangular','regular']
        elif side[0].length()==side[1].length() or \
             side[1].length()==side[2].length() or \
             side[2].length()==side[0].length():
            classify.append('isosceles')
        else:
            classify.append('scalene')
        # Classify the triangle according to angles.
        max_angle = 0
        for a in angle:
            if a.radians > max_angle:
                max_angle = a.radians
        if max_angle > math.pi/2:
            classify.append('obtuse')
        elif max_angle < math.pi/2:
            classify.append('acute')
        else:
            classify.append('right')
        return classify

class quadrilateral(polygon):
    def __init__(self, pts=[point(rational(0),rational(0),rational(0)),
                            point(rational(0),rational(1),rational(0)),
                            point(rational(2),rational(1),rational(0)),
                            point(rational(2),rational(0),rational(0))]):
        self.pts = pts

    def names(self):
        options = ['polygon','quadrilateral']

        s=self.sides()
        a=self.angles()
        pairs_parallel=0
        if is_parallel(s[0].pts,s[2].pts):
            pairs_parallel+=1
        if is_parallel(s[1].pts,s[3].pts):
            pairs_parallel+=1
        if pairs_parallel==0:
            # check for kite
            if s[0]==s[1] and s[2]==s[3]:
                options.append('kite')
            if s[1]==s[2] and s[3]==s[0]:
                options.append('kite')
        elif pairs_parallel==1:
            options.append('trapezoid')
            # check for isosceles trapezoid
            if s[0]==s[2] or s[1]==s[3]:
                options.append('isosceles trapezoid')
        elif pairs_parallel==2:
            options.append('parallelogram')
            # check for rhombus, rectangle, square
            if self.is_equilateral():
                options.append('rhombus')
            if self.is_equiangular():
                options.append('rectangle')
            if self.is_equilateral() and self.is_equiangular():
                options.append('square')
        options.reverse()
        return options

    def best_name(self):
        return self.names()[0]

    def area(self):
        return NotImplemented

class circle:
    "Define a circle by a center in 3D cartesian space with a specified radius."
    def __init__(self, center=point(rational(0),rational(0),rational(0),'A'),
                 radius=rational(1),
                 normal=[rational(0),rational(0),rational(1)]):
        self.center = center
        self.radius = toRational(radius)
        self.normal = normal

    def diameter(self):
        return self.radius * 2

    def area(self):
        return (self.radius**2)*math.pi

    def circumference(self):
        return (self.radius*2)*math.pi
    
    def latex(self):
        "Equation in 2D"
        if self.center.x == 0:
            s = 'x^2+'
        else:
            s = '(x%s)^2+' % (-self.center.x).latex(show_sign=True)
        if self.center.y == 0:
            s = s + 'y^2='
        else:
            s = s + '(y%s)^2=' % (-self.center.y).latex(show_sign=True)
        s = s + '%s' % (self.radius**2).latex()
        return s

    def tikz(self,color='black'):
        'Graph a circle.'
        s = "\\draw [color=%s] (%s,%s) circle (%s);\n" \
            % (color,self.center.x.printdecimal(),
               self.center.y.printdecimal(),
               self.radius.printdecimal())
        return s

class ellipse:
    def __init__(self,foci=[point(rational(-1),rational(0),rational(0),'A'),
                            point(rational(1),rational(0),rational(0),'B')]):
        self.foci = foci
        
############################################################
#
#  GEOMETRY - 3D
#
############################################################
    
class polyhedron:
    "Define a polyhedron by its vertices."
    def __init__(self,pts=[point(0,0,0,'A'),point(1,0,0,'A'),point(1,1,0,'A'), \
                           point(0,1,0,'A'),point(0,0,1,'A'),point(1,0,1,'A'), \
                           point(1,1,1,'A'),point(0,1,1,'A')]):
        self.pts = pts

    def tikz(self,zangle=math.pi/4):
        pnew = [0,0,0,0,0,0,0,0]
        for p in range(0,len(self.pts)):
            pnew[p] = point(self.pts[p].x+self.pts[p].z*math.cos(zangle),self.pts[p].y+self.pts[p].z*math.sin(zangle))
        plot=''
        for p in range(0,len(self.pts)):
            for c in range(0,len(self.pts)):
                count = 0
                if self.pts[c].x == self.pts[p].x:
                    count+=1
                if self.pts[c].y == self.pts[p].y:
                    count+=1
                if self.pts[c].z == self.pts[p].z:
                    count+=1
                if count==2:
                    plot = plot + segment([pnew[p],pnew[c]]).tikz() + '\n'
        return plot

############################################################
#
#  ALGEBRA
#
############################################################
    
class arithmeticseries:
    def __init__(self,startvalue=0,difference=1):
        self.startvalue = startvalue
        self.difference = difference

def slope(pts=[point(rational(0),rational(0),rational(0),'A'), \
               point(rational(1),rational(1),rational(0),'B')]):
    value = (pts[1].y-pts[0].y)/ \
            (pts[1].x-pts[0].x)
    return value.reduce()

def is_parallel(pts1=[point(rational(0),rational(0),rational(0),'A'), \
                      point(rational(1),rational(1),rational(0),'B')], \
                pts2=[point(rational(2),rational(0),rational(0),'C'), \
                      point(rational(6),rational(4),rational(0),'D')]):
    "Check for parallel linear equations in 3D space."
    dif1=pts1[0]-pts1[1]
    dif2=pts2[0]-pts2[1]
    scale=[0,0,0]
    if not (dif1.x==0 and dif2.x==0):
        scale[0]=dif1.x/dif2.x
    if not (dif1.y==0 and dif2.y==0):
        scale[1]=dif1.y/dif2.y
    if not (dif1.z==0 and dif2.z==0):
        scale[2]=dif1.z/dif2.z

    check_scale = 0
    for s in scale:
        if s != 0:
            if check_scale == 0:
                check_scale = s
            else:
                if check_scale!=s:
                    return False
    if check_scale==0:
        return False
    else:
        return True
    
def is_perpendicular(pts1=[point(rational(0),rational(0),rational(0),'A'), \
                           point(rational(1),rational(1),rational(0),'B')], \
                     pts2=[point(rational(2),rational(0),rational(0),'C'), \
                           point(rational(3),rational(1),rational(0),'D')]):
    if slope(pts1)==-slope(pts2).reciprocal():
        return True
    else:
        return False

class linear_equation:
    def __init__(self,pts=[point(rational(0),rational(0),rational(0)),
                           point(rational(1),rational(1),rational(0))]):
        if pts[0]==pts[1]:
            print('Error:  Need two distinct points to define a line.')
            raise AttributeError
            
        self.pts = pts

    def latex(self):
        if self.pts[0].x==self.pts[1].x:
            return NotImplemented
        elif self.pts[0].y==self.pts[1].y:
            return NotImplemented
        elif self.pts[0].z==self.pts[1].z:
            return NotImplemented
        else:
            s = 'x = %s %s t\\\\\n' % (self.pts[0].x.latex(),(self.pts[1].x-self.pts[0].x).latex(show_sign=True))
            s = s + 'y = %s %s t\\\\\n' % (self.pts[0].y.latex(),(self.pts[1].y-self.pts[0].y).latex(show_sign=True))
            s = s + 'z = %s %s t\\\\\n' % (self.pts[0].z.latex(),(self.pts[1].z-self.pts[0].z).latex(show_sign=True))
            return s

class linear_system:
    def __init__(self,systems=[linear_equation(),
                               linear_equation()]):
        self.systems=systems

    def intersection(self):
        return NotImplemented

class polynomial:
    "Define a polynomial in one or multiple variables with whole number exponents."
    def __init__(self,coeff=matrix([[1,1]]),var=['x']):
        self.coeff = coeff
        self.var = var

    def latex(self):
        out = ''
        size=self.coeff.shape[1]
        for x in range(0,size):
            n=(size-1)-x
            if n==(size-1):
                coeff="%d"%self.coeff[0,n]
            else:
                coeff="%+d"%self.coeff[0,n]
            if self.coeff[0,n]!=0:
                if n!=0:
                    variable='%s^%d'%(self.var[0],n)
                else:
                    variable=''
                out=out+coeff+variable        
        return out



###################################################################
#
#  DATA, PROBABILITY AND STATISTICS
#
###################################################################

class data_set_num():
    def __init__(self,data=[rational(0),rational(1),rational(2),rational(2)]):
        for n in range(0,len(data)):
            data[n] = toRational(data[n])
        self.data = data

    def printData(self):
        s = ''
        for n in self.data:
            s = s + n.latex() + ', '
        return s[:-2]
    
    def mean(self):
        total = sum(self.data)
        return (total / len(self.data)).reduce()

    def median(self):
        if len(self.data)<=1:
            return self.data[0]
        else:
            sdata = sorted(self.data)
            if len(sdata)%2==0:
                middle = len(sdata)//2-1
                if middle==0:
                    middle=1
                return ((sdata[middle]+sdata[middle+1])/2).reduce()
            else:
                middle = int(len(sdata)/2).value()
                if middle==0:
                    middle=1
                return sdata[middle]

    def sort(self,reverse=False):
        self.data.sort(reverse=reverse)

    def mode(self):
        sdata = sorted(self.data)
        check_mode = sdata[0]
        check_freq = 0
        freq = 0
        for n in sdata:
            if n == check_mode:
                check_freq+=1
            else:
                if check_freq>1 and check_freq>freq:
                    mode = [check_mode] 
                    freq = check_freq
                elif check_freq==freq:
                    mode.append(check_mode)
                check_mode = n
                check_freq=1
        return [mode, freq]

    def range(self):
        return max(self.data)-min(self.data)

    def varianceP(self):
        'Population variance'
        mean = self.mean()
        residuals=rational(0)
        for n in self.data:
            residuals+=(n-mean)**2
        return residuals/len(self.data)

    def varianceS(self):
        'Population variance'
        mean = self.mean()
        residuals=rational(0)
        for n in self.data:
            residuals+=(n-mean)**2
        return residuals/(len(self.data)-1)

    def variance(self):
        'Variance automatically determined sample or population.'
        if len(self.data)>=30:
            return self.varianceP()
        else:
            return self.varianceS()

    def stdevP(self):
        'Population standard deviation'
        variance = self.varianceP()
        return sqrt(variance)

    def stdevS(self):
        'Sample standard deviation'
        variance = self.varianceS()
        return sqrt(variance)

    def stdev(self):
        'Standard deviaiton automatically determined sample or population.'
        if len(self.data)>=30:
            return self.stdevp()
        else:
            return self.stdevs()

    def quartile(self,qrt=1):
        sdata = sorted(self.data)
        if qrt==0:
            return sdata[0]
        elif qrt==4:
            return sdata[-1]
        elif qrt==2:
            return self.median()
        elif qrt==1:
            middle = len(sdata)//2
            if middle==0:
                middle=1
            temp = data_set_num(sdata[0:middle])
            return temp.median()
        elif qrt==3:
            middle = len(sdata)//2
            if middle==0:
                middle=1
            temp = data_set_num(sdata[-middle:])
            return temp.median()

    def decile(self,dec=1):
        return self.quantile(10,dec)

    def percentile(self,pcnt=1):
        return self.quantile(100,pcnt)
    
    def quantile(self,divisions,num):
        if rational(divisions,2) == rational(num,1):
            return self.median()
        elif rational(divisions,4) == rational(num,1):
            return self.quartile(1)
        elif rational(divisions,4)*3 == rational(num,1):
            return self.quartile(3)
        elif divisions==num:
            return max(self.data)
        else:
            pos = len(self.data)*num//divisions
            sdata = sorted(self.data)
            return sdata[pos]

    def boxAndWhisker(self,centerline=1,thickness=0.5):
        q = [min(self.data), self.quartile(1), self.median(), \
             self.quartile(3), max(self.data)]
        #print q[0].latex(), q[1].latex(), q[2].latex(), q[3].latex(), q[4].latex()
        # Left whisker
        lines = [segment([point(q[0],centerline),point(q[1],centerline)])]
        # Box
        lines.append(segment([point(q[1],centerline+thickness),
                              point(q[1],centerline-thickness)]))
        lines.append(segment([point(q[2],centerline+thickness),
                              point(q[2],centerline-thickness)]))
        lines.append(segment([point(q[3],centerline+thickness),
                              point(q[3],centerline-thickness)]))
        lines.append(segment([point(q[1],centerline+thickness),
                              point(q[3],centerline+thickness)]))
        lines.append(segment([point(q[1],centerline-thickness),
                              point(q[3],centerline-thickness)]))
        # Right whisker
        lines.append(segment([point(q[3],centerline),point(q[4],centerline)]))

        s = ''
        for l in lines:
            s = s + l.tikz() + '\n'

        return s
    
class data_set_labels():
    def __init__(self,data=['a','b','c','d']):
        self.data = data

    def sort(self):
        self.data.sort()

    def freqTable(self,barWidth=1):
        sdata = sorted(self.data)
        freq = 0
        check = sdata[0]
        table = []
        for d in sdata:
            if check==d:
                freq+=1
            else:
                table.append([check,freq])
                check = d
                freq = 1
        table.append([check,freq])

        s=''
        for t in range(0,len(table)):
            p=polygon([point(t*barWidth,0),
                       point(t*barWidth,table[t][1]),
                       point((t+1)*barWidth,table[t][1]),
                       point((t+1)*barWidth,0)])
            s = s + p.tikz()
        return s
    
class multi_data_sets_num:
    def __init__(self,datasets=[data_set_num(),data_set_num()]):
        self.datasets = datasets
        
    def linegraph(self,xset=0,yset=1):
        return NotImplemented
    
    def scatterplot(self,xset=0,yset=1):
        return NotImplemented
        
    def correlation(self,xset=0,yset=1):
        return NotImplemented

    def linear_regression(self,independent=0,dependent=1):
        return NotImplemented

    def multi_variable_regression(self,independent=[0,1],dependent=2):
        return NotImplemented

############################################################
#
#   TIKZ/PGF
#
############################################################

class tikz_image:
    def __init__(self,collection=[point(rational(0),rational(0),rational(0))], \
                 scale=[rational(1),rational(1),rational(1)]):
        self.collection = collection
        self.scale = scale

    def code(self):
        s=self.prefix()
        for c in self.collection:
            try:
                s=s+c.tikz()+'\n'
            except AttributeError:
                for n in c:
                    s=s+n.tikz()+'\n'
        s=s+self.postfix()
        return s
        
    def prefix(self):
        # Setup for the image.
        # Define colors and then set the scale of the image.
        s = "\definecolor{qqwuqq}{rgb}{0,0.39,0}\n"
        s = s + "\definecolor{brown}{rgb}{0.6,0.2,0}\n"
        s = s + "\definecolor{blue}{rgb}{0,0,1}\n"
        s = s + "\definecolor{black}{rgb}{0,0,0}\n"
        s = s + "\definecolor{grey}{rgb}{0.25,0.25,0.25}\n"
        s = s + "\definecolor{lightgrey}{rgb}{0.75,0.75,0.75}\n"
        s = s + "\definecolor{lightblue}{rgb}{0.49,0.49,1}\n"
        s = s + "\definecolor{red}{rgb}{1,0,0}\n"
        s = s + "\definecolor{orange}{rgb}{1,0.5,0}\n"
        s = s + "\definecolor{purple}{rgb}{0.5,0,1}\n"
        s = s + "\definecolor{yellow}{rgb}{1,1,0}\n"
        s = s + "\definecolor{green}{rgb}{0,1,0}\n"
        s = s + "\definecolor{lightgreen}{rgb}{0,0.39,0}\n"
        s = s + "\\begin{tikzpicture}[line cap=round,line "
        s = s + "join=round,>=triangle 45,x=%scm,y=%scm]\n" % \
            (self.scale[0].printdecimal(), self.scale[1].printdecimal())
        return s

    def postfix(self):
        # Close out the image.
        s = "\end{tikzpicture}\n"
        return s

    def grid(self):
        return NotImplemented

    def clip(self):
        return NotImplemented

    def axes(self,x=True,y=True):
        return NotImplemented
