from naiveBayes import NaiveBayes
naiveBayes = NaiveBayes("grasshopper.csv", 2)
naiveBayes.calculations()


print(naiveBayes.predict([5.1, 7.0]))
