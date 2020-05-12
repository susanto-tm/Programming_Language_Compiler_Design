from Lexer import Lexer
from Parser import Parser
from argparse import ArgumentParser

DEBUG_MODE = False

ap = ArgumentParser()
ap.add_argument('--file', help='Enter file name under extension ".ma".')
ap.add_argument("--lexer", action='store_true', help='View lexer output.')
ap.add_argument("--run", action='store_true', help='Runs the file.')
args = vars(ap.parse_args())


def run():
    if args['file'] is not None:
        f = open(args['file'], 'r')
        text = f.read()
        f.close()
    else:
        f = open('test.ma', 'r')
        text = f.read()
        f.close()

    lexer = Lexer()
    lexer.build()

    if args['lexer']:
        lexer.test(text)

    if args['run']:
        parser = Parser().build()
        ast = parser.parse(text, debug=DEBUG_MODE)
        ast.eval()


if __name__ == '__main__':
    run()

