class Store(dict):
    def set_compiler(self, compiler):
        self["__compiler"] = compiler

    def set_tokens(self, tokens):
        self["__tokens"] = AstTokens(tokens)

    @property
    def compiler(self):
        return self["__compiler"]

    @property
    def tokens(self):
        return self["__tokens"]

    def add_token(self, key, token):
        self.tokens[key] = token
