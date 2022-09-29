import prophecies
import prophecies.parser
import prophecies.compiler


__version__ = "0.1.0"

#COMPILER = prophecies.compiler.Compiler()
#PARSER = prophecies.parser.Parser()
STORE = prophecies.compiler.store.Store()
def init_engine():
    global STORE
    #STORE.set_tokens(prophecies.parser.tokens.TOKENS)
    STORE.set_compiler(prophecies.compiler.compiler.Compiler())

def destroy_engine():
    import curses
    curses.endwin()

