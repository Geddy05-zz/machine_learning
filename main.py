from naiveBayes import NaiveBayes
naiveBayes = NaiveBayes("grasshopper.csv", 3)
naiveBayes.print_enable = True
naiveBayes.train()


print(naiveBayes.predict([5.1, 'young', 7.0]))
