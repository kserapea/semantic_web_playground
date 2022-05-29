import csv


class SimpleGraph:
    def __init__(self):
        """
        The name of the index indicates the ordering of the terms in the index
        the pos index stores the predicate, then the object, and then the subject, in that order
        """
        self._spo = {}
        self._pos = {}
        self._osp = {}

    """
    the pos index could be instantiated with a new triple like so:
        self._pos = {predicate:{object:set([subject])}}
    query for all triples with a specific predicate and object could be answered like so:
        for subject in self._pos[predicate][object]: yield (subject, predicate, object)
    """

    def add(self, sub_pred_obj):
        """ Adds a triple to the graph"""
        (sub, pred, obj) = sub_pred_obj
        self._addToIndex(self._spo, sub, pred, obj)
        self._addToIndex(self._pos, pred, obj, sub)
        self._addToIndex(self._osp, obj, sub, pred)

    def _addToIndex(self, index, a, b, c):
        """adds the terms to the index
            creating a dictionary and set if the terms are not already in the index:"""
        if a not in index:
            index[a] = {b: {c}}
        else:
            if b not in index[a]:
                index[a][b] = {c}
            else:
                index[a][b].add(c)

    def remove(self, sub_pred_obj):
        """finds all triples that match a pattern, permutes them, and removes them from each index"""
        (sub, pred, obj) = sub_pred_obj
        triples = list(self.triples((sub, pred, obj)))
        for (delSub, delPred, delObj) in triples:
            self._removeFromIndex(self._spo, delSub, delPred, delObj)
            self._removeFromIndex(self._pos, delPred, delObj, delSub)
            self._removeFromIndex(self._osp, delObj, delSub, delPred)

    def _removeFromIndex(self, index, a, b, c):
        """walks down the index, cleaning up empty intermediate dictionaries
            and sets while removing the terms of the triple"""
        try:
            bs = index[a]
            cset = bs[b]
            cset.remove(c)
            if len(cset) == 0: del bs[b]
            if len(bs) == 0: del index[a]
        # KeyErrors occur if a term was missing, which means that it wasn't a
        # valid delete:
        except KeyError:
            pass

    """methods for loading and saving the triples in the graph to comma-separated files"""

    def load(self, filename):
        f = open(filename, "rb")
        reader = csv.reader(f)
        for sub, pred, obj in reader:
            sub = sub.decode("UTF-8")
            pred = pred.decode("UTF-8")
            obj = obj.decode("UTF-8")
            self.add((sub, pred, obj))
        f.close()

    def save(self, filename):
        f = open(filename, "wb")
        writer = csv.writer(f)
        for sub, pred, obj in self.triples((None, None, None)):
            writer.writerow([sub.encode("UTF-8"), pred.encode("UTF-8"), obj.encode("UTF-8")])
        f.close()

    def triples(self, sub_pred_obj):
        # check which terms are present in order to use the correct index:
        (sub, pred, obj) = sub_pred_obj
        try:
            if sub is not None:
                if pred is not None:
                    # sub pred obj
                    if obj is not None:
                        if obj in self._spo[sub][pred]:
                            yield sub, pred, obj
                    # sub pred None
                    else:
                        for retObj in self._spo[sub][pred]:
                            yield sub, pred, retObj
                else:
                    # sub None obj
                    if obj is not None:
                        for retPred in self._osp[obj][sub]:
                            yield sub, retPred, obj
                    # sub None None
                    else:
                        for retPred, objSet in self._spo[sub].items():
                            for retObj in objSet:
                                yield sub, retPred, retObj
            else:
                if pred is not None:
                    # None pred obj
                    if obj is not None:
                        for retSub in self._pos[pred][obj]:
                            yield retSub, pred, obj
                    # None pred None
                    else:
                        for retObj, subSet in self._pos[pred].items():
                            for retSub in subSet:
                                yield retSub, pred, retObj
                else:
                    # None None obj
                    if obj is not None:
                        for retSub, predSet in self._osp[obj].items():
                            for retPred in predSet:
                                yield retSub, retPred, obj
                    # None None None
                    else:
                        for retSub, predSet in self._spo.items():
                            for retPred, objSet in predSet.items():
                                for retObj in objSet:
                                    yield retSub, retPred, retObj
        # KeyErrors occur if a query term wasn't in the index,
        # so we yield nothing:
        except KeyError:
            pass

    def value(self, sub=None, pred=None, obj=None):
        for retSub, retPred, retObj in self.triples((sub, pred, obj)):
            if sub is None:
                return retSub
            if pred is None:
                return retPred
            if obj is None:
                return retObj
            break
        return None
