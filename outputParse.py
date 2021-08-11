def parse():
	AtotalBalances = ["0"] * 7
	AtotalK = ["0"] * 7

	BtotalBalances = ["0"] * 7
	BtotalK = ["0"] * 7

	iterations = 100

	inputSizes = [10,100,1000,10000,100000,1000000,10000000]

	BallData = []
	AallData = []

	f = open("outputT.txt", "r")

	for i in range(2):
		lines = f.readline()
		print(lines)

parse()