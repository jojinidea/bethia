def updatePredecessors(self, predecessor):
        if self.fPredecessor != None:
            if predecessor > self.fPredecessor and (predecessor < self._id or self.fPredecessor > self._id):
                self.sPredecessor = self.fPredecessor
                self.fPredecessor = predecessor
            elif predecessor < self.fPredecessor and predecessor < self._id and self.fPredecessor > self._id:
                self.sPredecessor = self.fPredecessor
                self.fPredecessor = predecessor
            else:
                self.sPredecessor = predecessor
        else: 
            self.fPredecessor = predecessor
        print("{} {} {}".format(self.sPredecessor, self.fPredecessor, self._id)