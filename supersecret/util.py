
class AttrDict(dict):
    """
    A dictionary that allows you to access keys as attributes.
    """
    def __getattr__(self, attr):
        return self[attr]

    def __setattr__(self, attr, value):
        self[attr] = value

    def __delattr__(self, attr):
        del self[attr]

    def __repr__(self):
        return f'<AttrDict {super().__repr__()}>'
