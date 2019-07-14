class Sources:
    def __init__(self):
        self.sources = dict()

    def add(self, name, source):
        self.sources[name] = source

    def __contains__(self, item):
        return item in self.sources

    def __getitem__(self, item_name):
        return self.sources[item_name]

    def update(self, other_sources):
        self.sources = dict(self.sources, **other_sources.sources)

    def items(self):
        return tuple(self.sources.items())

    def __len__(self):
        return len(self.sources)
