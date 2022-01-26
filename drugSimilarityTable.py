class SimilarityTable:
    drugsSimilarities = {}

    def __init__(self, drug_id):
        self.drug_id = drug_id

    def addItem(self, item_id, item_value):
        if len(self.drugsSimilarities) < 10:
            self.drugsSimilarities.update({item_id: item_value})
            self.orderDictionarity()

    def orderDictionarity(self):
        sortedSimilarities = sorted(self.drugsSimilarities.items(), key=lambda x:x[1], reverse=True)
        newDrugsSimilarities = {}
        for value in sortedSimilarities:
            newDrugsSimilarities[value[0]] = value[1]
        self.drugsSimilarities = newDrugsSimilarities

    def printDictionarity(self):
        for key, value in self.drugsSimilarities:
            print(key, value)
