class Meta:
    def __init__(self, meta=None):
        self._meta = {} if meta is None else meta

    def get_meta(self, key):
        return self._meta.get(key)

    def add_meta(self, key, value):
        self._meta.setdefault(key, value)

    def serialize(self):
        return self._meta

    @classmethod
    def from_dict(cls, meta):
        return cls(meta)
