from math import *
sum = 0.0;
ratio = 0.0;
n = 0;
while 1:
	input = raw_input("Enter a number n:\n");
	n = float(input);
	if n == -1:
		break;
	for x in range(2, n):
		for y in range(2, x / 2 + 1):
			if x % y == 0:
				break;
		else:
			sum = sum + log(x);
	else:
		ratio = sum / n;
		print "sum = " + str(sum);
		print "n = " + str(n)
		print "ratio = " + str(ratio);
		
			