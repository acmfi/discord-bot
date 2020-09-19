
EMOJIS = {
    "short": [":zero:", ":one:", ":two:", ":three:", ":four:", ":five:", ":six:", ":seven:", ":eight:", ":nine:"],
    "unicode": ["{}\N{COMBINING ENCLOSING KEYCAP}".format(num) for num in range(0, 10)]
}


class Emoji:
    def specific(self, short, unicode):
        self.short = short
        self.unicode = unicode
        return self

    def number(self, index):
        self.short = EMOJIS["short"][index]
        self.unicode = EMOJIS["unicode"][index]
        return self

    def __eq__(self, other):
        if isinstance(other, Emoji):
            return self.short == other.short and self.unicode == other.unicode
