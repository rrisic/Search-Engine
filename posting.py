


class Posting:
    def __init__(self, doc_id, word_count, is_special):
        self._doc_id = doc_id
        self._word_count = int(word_count)
        self._is_special = is_special
    def __hash__(self):
        return hash((self._doc_id, self._word_count))
    def __eq__(self, other):
        if isinstance(other, Posting):
            return self._doc_id == other._doc_id and self._word_count == other._word_count
        return False
    def __iter__(self):
        return iter((self._doc_id, self._word_count, self._is_special))