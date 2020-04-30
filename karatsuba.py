import math, string

def parse_int(s):
    return int(s) if len(s) > 0 else 0

def kar_multiply(num1, num2):
    len1 = len(num1)
    len2 = len(num2)
    n = max(len1, len2)

    if (n <= 1):
        return parse_int(num1) * parse_int(num2)

    if (n > len1):
        num1 = "".join(["0"] * (n - len1)) + num1 

    if (n > len2):
        num2 = "".join(["0"] * (n - len2)) + num2

    m = math.ceil(n/2) 

    #print(n/2)

    a = num1[:m] #math.floor(num1 / half_order)
    b = num1[m:] #math.floor(num1 % half_order)

    c = num2[:m] #math.floor(num2 / half_order)
    d = num2[m:] #math.floor(num2 % half_order)

    print("n = " + str(n) + "; m = " + str(m) + ";a = " + str(a) + "; b = " + str(b) + ";c = " + str(c) + "; d = " + str(d))

    a_c = kar_multiply(a, c)
    b_d = kar_multiply(b, d)

    ab_cd = kar_multiply(str(parse_int(a) + parse_int(b)), str(parse_int(c) + parse_int(d)))



    diff = ab_cd - b_d - a_c

    first = a_c * (10**(m*2))

    second = diff * (10**m)

    return parse_int(str(first + second + b_d)) #int((a_c * pow(10, m * 2)) + b_d + diff * half_order)

#print(kar_multiply("1234", "5678"))



def kar_multiply_old(num1, num2):
    if (num1 < 10 and num2 < 10):
        return num1 * num2

    n = max(len(str(int(num1))), len(str(int(num2))))
    m = math.ceil(n/2) 

    half_order = pow(10, m)

    a = math.floor(num1 / half_order)
    b = math.floor(num1 % half_order)

    c = math.floor(num2 / half_order)
    d = math.floor(num2 % half_order)

    #print("n = " + str(n) + "; m = " + str(m) + ";a = " + str(a) + "; b = " + str(b) + ";c = " + str(c) + "; d = " + str(d))

    a_c = kar_multiply_old(a, c)
    b_d = kar_multiply_old(b, d)

    ab_cd = kar_multiply_old(a + b, c + d)

    diff = ab_cd - b_d - a_c
    res = int((a_c * pow(10, m * 2)) + diff * half_order + b_d)

    return res


# print(3141592653589793238462643383279502884197169399375105820974944592 * 2718281828459045235360287471352662497757247093699959574966967627)
# print(kar_multiply_old(3141592653589793238462643383279502884197169399375105820974944592, 2718281828459045235360287471352662497757247093699959574966967627))
x = 3141592653589793238462643383279502884197169399375105820974944592
y = 2718281828459045235360287471352662497757247093699959574966967627

result = kar_multiply_old(x, y)
print(result)
print(x * y)
print(result == x * y)

