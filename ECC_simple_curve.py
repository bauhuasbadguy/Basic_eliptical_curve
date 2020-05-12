#Simple ECC
#This program does a ECC multiplication on the
#curve [y^2 = x^3 + ax + b] mod p

#we need some advanced maths functions
import math

#Sources:-
#http://www.crypto-textbook.com/
#http://arstechnica.com/security/2013/10/a-relatively-easy-to-understand-primer-on-elliptic-curve-cryptography/
#(This ones really good actually)
#https://en.wikipedia.org/wiki/Elliptic_curve_cryptography
#https://www.math.brown.edu/~jhs/Presentations/WyomingEllipticCurve.pdf


#Define some maths functions
#Find the greatest common demominatior of a and b
#using the euclidian algorithm
def gcd(a, b):

    while a != b:

        if a > b:
            a = a - b

        else:
            b = b - a
            
    return a

#Find the inverse mod of a number in the prime field p
#using the extended euclidain algorithm
def extended_euclid(a, p):

    #Find if the input is positive or negative
    if a < 0:
        sign = -1
    else:
        sign = 1
        
    a *= sign

    c = gcd(a, p)
    
    #gcd must be one or else the inverse does not exist

    u = a
    v = p

    u1 = 1
    u3 = a
    v1 = 0
    v3 = v

    it = 1

    #if a and p are not coprime the result is zero
    if c != 1:
        print('Input numbers are not coprime')
        v3 = 0
        inv = 0


    while v3 != 0:

        q = math.floor(u3 / v3)

        t3 = u3 % v3

        t1 = u1 + (q * v1)

        [u1, v1, u3, v3] = [v1, t1, v3, t3]

        it = -it


    if (u3 != 1):
        inv = 0

    if (it < 0):
        inv = v - u1

    else:
        inv = u1

    #make the result the same +/- as when we
    #started
    inv *= sign
    
    return inv

#P is the start point
#p is the prime field
#what is a?
#Am I working on the curve y^2 = x^3 + ax + b?
#this explains where the 3 came from as the s values are the differentials of
#each side. What is the point of the b? Does the b vanish?
def Point_Double(P, a, p):
    
    #Find the gradient of the line in x at point P
    s1 = (3 * pow(P.x,2) + a) % p
    
    #Get the inverse of the gradient of the line in y at point P
    s2 = extended_euclid((2 * P.y),p)

    #find the gradient of the line
    m = (s1 * s2) % p

    #find the x value we go through
    x3 = (pow(m,2) - P.x - P.x) % p

    #what is this y3 value?
    y3 = ((m * (P.x - x3)) - P.y) % p

    #print y3
    #is this the final point, what did we just do?
    R = Point(x3, y3)

    return R

#scalar addition function
def Point_Addition(P, Q, a, p):

    #calculate dy of the line L in the prime field p
    s1 = (Q.y - P.y) % p

    #calculate dx of the line L in the prime field y and then do 1/dx
    #so we can find the gradient of the line to draw it 
    s2 = extended_euclid((Q.x - P.x), p)

    #m is the gradient of the line through P and Q
    m = (s1 * s2) % p

    #find the x point we end up at
    #This is subing in the value of m we found into y=mx+c
    x3 = (pow(m,2) - P.x - Q.x) % p
    #print x3

    #find the y point we end up at
    #how is this working exactly?
    y3 = ((m * (P.x - x3)) - P.y) % p

    #print y3

    R = Point(x3, y3)

    return R

#Scalar multiplication program. P is the starting point
#d is the amount to multiply by, a and p are defined by the
#curve.
#Is this using russian multiplication?
def Scalar_multiplication(P, d, a, p):

    sumation = 1
    D = bin(d)[2:]
    R = P
    for i, I in enumerate(D[1:]):

        #Do a point double as we have gone <<        
        R = Point_Double(R, a, p)
        sumation *= 2
        
        #do an addition since we have a 1 at the end
        #of our new most significant binary value
        if I == '1':

            sumation += 1
            R = Point_Addition(R, P, a, p)

    return [sumation, R]
    


#create a new class for the public key, the points on the curve\\
class Point:
    def __init__(self, x_val, y_val):
         self.x = int(x_val)
         self.y = int(y_val)



#now start actually doing things.
#Here we give an example of point multiplication
P = Point(5,1)
#we will experement with the curve y^2 = x^3 + 2*x + b
a = 2
b = 0
p = 17


d = 17

[r, R] = Scalar_multiplication(P, d, a, p)


#here we have an example of key exchange
#the public keys are the points and the curve
#each person multiplies by their private keys,
#the results are exchanged and then you multiply
#the other persons result by your key and you
#both get the same answer that you can both agree
#on and therefore use as your keys for another encryption
#algorithm such as AES or twofish

#Alices key
dA = 10

#Bobs key
dB = 14

#Alice moves from the start point to her public point
[r, PA] = Scalar_multiplication(P, dA, a, p)
#Bob moves from the start point to his public point
[r, PB] = Scalar_multiplication(P, dB, a, p)

#Bob moves to his point
[r, Pf1] = Scalar_multiplication(PA, dB, a, p)
#Alice moves from Bob's point to the end point
[r, Pf2] = Scalar_multiplication(PB, dA, a, p)


print('---------Q1--------')
print('(' + repr(Pf1.x) + ', ' + repr(Pf1.y) + ')')
print('-------------------')


print('---------Q2--------')
print('(' + repr(Pf2.x) + ', ' + repr(Pf2.y) + ')')
print('-------------------')

