primeCount = 0;
n = 2;
while 1:
	for x in range(2, n / 2 + 1):
		if n % x == 0:
			break;
	else:
		primeCount = primeCount + 1;
		if primeCount == 1000:
			print "The 1000th prime number is " + str(n);
			break;
	n = n + 1;
			