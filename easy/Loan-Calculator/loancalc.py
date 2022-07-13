import math
import argparse


parser = argparse.ArgumentParser()  # create new instance for argument parser
parser.add_argument("--type", choices=["annuity", "diff"])
parser.add_argument("--payment")
parser.add_argument("--principal")
parser.add_argument("--periods")
parser.add_argument("--interest")
args = parser.parse_args()

param = []
loan_type = args.type
M = args.payment
P = args.principal
n = args.periods
loan_interest = args.interest

while loan_type and loan_interest is not None:
    loan_interest = float(loan_interest)
    param.append(loan_interest)
    param.append(loan_type)
    i = loan_interest / (12 * 100)  # interest rate

    if loan_type == "annuity" and M is None:
        P, n = float(P), int(n)
        param.append(P)
        param.append(n)

        A = (P * i * math.pow(1 + i, n)) / (math.pow(1 + i, n) - 1)
        A = math.ceil(A)
        OverPayment = round(abs(P - n * A))

        print(f"Your annuity payment = {A}!")
        print(f"Overpayment = {OverPayment}")

    elif loan_type == "annuity" and P is None:
        M, n = float(M), int(n)
        param.append(M)
        param.append(n)

        A = M
        P = A / ((i * math.pow(1+i, n)) / (math.pow(1+i, n) - 1))
        OverPayment = round(abs(P - n * A))

        print(f"Your loan principal = {P}!")
        print(f"Overpayment = {OverPayment}")

    elif loan_type == "annuity" and n is None:
        M, P = float(M), float(P)
        param.append(M)
        param.append(P)

        A = M
        temp = math.log((A / (A - i * P)), 1 + i)
        n = math.ceil(temp)
        OverPayment = round(abs(P - n * A))

        if n > 12:
            n2Y = math.floor(n / 12)
            rest_n2Y = n % 12
            if not rest_n2Y == 0:
                print(f"It will take {n2Y} years and {rest_n2Y} months to repay this loan!")
            else:
                print(f"It will take {n2Y} years to repay this loan!")
        elif n == 12:
            print(f"It will take 1 year to repay this loan!")
        else:
            print(f"It will take {n} months to repay this loan!")

        print(f"Overpayment = {OverPayment}")

    elif loan_type == "diff" and M is None:
        P, n = float(P), int(n)
        param.append(P)
        param.append(n)
        A = 0.0

        for month in range(n):
            M = (P / n) + i * (P - (P * month) / n)
            M = math.ceil(M)
            print(f"Month {month+1}: payment is {M}")
            A += M
            OverPayment = round(abs(P - A))

        print(f"Overpayment = {OverPayment}")

    break

if len(param) < 4:
    print("Incorrect parameters.")
