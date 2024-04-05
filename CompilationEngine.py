"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import JackTokenizer

CLASS = "<class>\n"
CLASS_CLOSE = "</class>\n"
TERM = "<term>\n"
TERM_CLOSE = "</term>\n"
CLASSVARDEC = "<classVarDec>\n"
CLASSVARDEC_CLOSE = "</classVarDec>\n"
SUBRODEC = "<subroutineDec>\n"
SUBRODEC_CLOSE = "</subroutineDec>\n"
SUBROBOD = "<subroutineBody>\n"
SUBROBOD_CLOSE = "</subroutineBody>\n"
PARAML = "<parameterList>\n"
PARAML_CLOSE = "</parameterList>\n"
VARDEC = "<varDec>\n"
VARDEC_CLOSE = "</varDec>\n"
STATEMENTS = "<statements>\n"
STATEMENTS_CLOSE = "</statements>\n"
DO = "<doStatement>\n"
DO_CLOSE = "</doStatement>\n"
LET = "<letStatement>\n"
LET_CLOSE = "</letStatement>\n"
WHILE = "<whileStatement>\n"
WHILE_CLOSE = "</whileStatement>\n"
RETURN = "<returnStatement>\n"
RETURN_CLOSE = "</returnStatement>\n"
IF = "<ifStatement>\n"
IF_CLOSE = "</ifStatement>\n"
EXPR = "<expression>\n"
EXPR_CLOSE = "</expression>\n"
EXPRLIST = "<expressionList>\n"
EXPRLIST_CLOSE = "</expressionList>\n"

symbol_map = {
            "<": "&lt;",
            ">": "&gt;",
            "&": "&amp;",
            '"': "&quot;"
        }

class CompilationEngine:
    """Gets input from a Jackinput_file and emits its parsed structure into an
    output stream.
    """

    def __init__(self, input_stream: "JackTokenizer", output_file) -> None:
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        :param input_stream: The input stream.
        :param output_file: The output stream.
        """
        # Your code goes here!
        self.output_file = output_file
        self.input_file = input_stream

    def compile_class(self) -> None:
        """Compiles a complete class."""
        # Your code goes here!
        self.output_file.write(CLASS)
        self.keyword_output()
        self.identifier_output()
        self.symbol_output()
        while self.input_file.keyword() in ["static", "field"] and \
                self.input_file.token_type() == "KEYWORD":
            self.compile_class_var_dec()
        while self.input_file.keyword() in ["function", "method", "constructor"] and \
                self.input_file.token_type() == "KEYWORD":
            self.compile_subroutine()
        self.symbol_output()
        self.output_file.write(CLASS_CLOSE)

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        # Your code goes here!
        self.output_file.write(CLASSVARDEC)
        self.keyword_output()
        if self.input_file.token_type() == "IDENTIFIER":
            self.identifier_output()
        elif self.input_file.token_type() == "KEYWORD":
            self.keyword_output()
        self.identifier_output()
        while self.input_file.symbol() == ',':
            self.symbol_output()
            self.identifier_output()
        self.symbol_output()
        self.output_file.write(CLASSVARDEC_CLOSE)

    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """
        # Your code goes here!
        self.output_file.write(SUBRODEC)
        self.keyword_output()
        if self.input_file.token_type() == "IDENTIFIER":
            self.identifier_output()
        elif self.input_file.token_type() == "KEYWORD":
            self.keyword_output()
        self.identifier_output()
        self.symbol_output()
        self.compile_parameter_list()
        self.symbol_output()
        self.output_file.write(SUBROBOD)
        self.symbol_output()
        while self.input_file.keyword() == "var":
            self.compile_var_dec()
        self.compile_statements()
        self.symbol_output()
        self.output_file.write(SUBROBOD_CLOSE)
        self.output_file.write(SUBRODEC_CLOSE)

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the
        enclosing "()".
        """
        # Your code goes here!
        self.output_file.write(PARAML)
        while self.input_file.token_type() != "SYMBOL":
            if self.input_file.token_type() == "IDENTIFIER":
                self.identifier_output()
            elif self.input_file.token_type() == "KEYWORD":
                self.keyword_output()
            self.identifier_output()
            if self.input_file.symbol() == ',':
                self.symbol_output()
        self.output_file.write(PARAML_CLOSE)

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        # Your code goes here!
        self.output_file.write(VARDEC)
        self.keyword_output()
        if self.input_file.token_type() == "KEYWORD":
            self.keyword_output()
        elif self.input_file.token_type() == "IDENTIFIER":
            self.identifier_output()
        self.identifier_output()
        while self.input_file.symbol() == ',':
            self.symbol_output()
            self.identifier_output()
        self.symbol_output()
        self.output_file.write(VARDEC_CLOSE)

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing
        "{}".
        """
        # Your code goes here!
        self.output_file.write(STATEMENTS)
        while self.input_file.token_type() == "KEYWORD":
            keyword = self.input_file.keyword()
            if keyword == "if":
                self.compile_if()
            if keyword == "while":
                self.compile_while()
            if keyword == "return":
                self.compile_return()
            if keyword == "do":
                self.compile_do()
            if keyword == "let":
                self.compile_let()
        self.output_file.write(STATEMENTS_CLOSE)

    def compile_do(self) -> None:

        """Compiles a do statement."""
        # Your code goes here!
        self.output_file.write(DO)
        self.keyword_output()
        self.compile_term()
        self.symbol_output()
        self.output_file.write(DO_CLOSE)

    def compile_let(self) -> None:
        """Compiles a let statement."""
        # Your code goes here!

        self.output_file.write(LET)
        self.keyword_output()
        self.identifier_output()
        if self.input_file.symbol() == "[":
            self.symbol_output()
            self.compile_expression()
            self.symbol_output()
        self.symbol_output()
        self.compile_expression()
        self.symbol_output()
        self.output_file.write(LET_CLOSE)

    def compile_while(self) -> None:
        """Compiles a while statement."""
        # Your code goes here!
        self.output_file.write(WHILE)
        self.keyword_output()
        self.symbol_output()
        self.compile_expression()
        self.symbol_output()
        self.symbol_output()
        self.compile_statements()
        self.symbol_output()
        self.output_file.write(WHILE_CLOSE)

    def compile_return(self) -> None:
        """Compiles a return statement."""
        # Your code goes here!
        input_file = self.input_file
        self.output_file.write(RETURN)
        self.keyword_output()
        if input_file.token_type() != "SYMBOL" and input_file.symbol() != ";":
            self.compile_expression()
        self.symbol_output()
        self.output_file.write(RETURN_CLOSE)

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        # Your code goes here!
        input_file = self.input_file
        self.output_file.write(IF)
        self.keyword_output()
        self.symbol_output()
        self.compile_expression()
        self.symbol_output()
        self.symbol_output()
        self.compile_statements()
        self.symbol_output()
        if input_file.keyword() == "else":
            self.keyword_output()
            self.symbol_output()
            self.compile_statements()
            self.symbol_output()
        self.output_file.write(IF_CLOSE)

    def compile_expression(self) -> None:
        """expression: term (op term)*"""
        """Compiles an expression."""
        # Your code goes here!
        self.output_file.write(EXPR)
        self.output_file.write(TERM)
        self.compile_term()
        self.output_file.write(TERM_CLOSE)
        while self.input_file.symbol() in ['+', '-', '*', '/', '&', '|', '<', '>', '=']:
            self.symbol_output()
            self.output_file.write(TERM)
            self.compile_term()
            self.output_file.write(TERM_CLOSE)
        self.output_file.write(EXPR_CLOSE)

    def compile_term(self) -> None:
        """Compiles a term.
        This routine is faced with a slight difficulty when
        trying to decide between some of the alternative parsing rules.
        Specifically, if the current token is an identifier, the routing must
        distinguish between a variable, an array entry, and a subroutine call.
        A single look-ahead token, which may be one of "[", "(", or "." suffices
        to distinguish between the three possibilities. Any other token is not
        part of this term and should not be advanced over.
        """
        # Your code goes here!
        if self.input_file.token_type() == "INT_CONST":
            if self.input_file.token_type() == "INT_CONST":
                self.output_file.write(f"<integerConstant> {str(self.input_file.int_val())} </integerConstant>\n")
            if self.input_file.has_more_tokens():
                self.input_file.advance()
        elif self.input_file.token_type() == "STRING_CONST":
            if self.input_file.token_type() == "STRING_CONST":
                self.output_file.write(f"<stringConstant> {self.input_file.string_val()} </stringConstant>\n")
            if self.input_file.has_more_tokens():
                self.input_file.advance()
        elif self.input_file.token_type() == "KEYWORD":
            self.keyword_output()
        elif self.input_file.token_type() == "IDENTIFIER":
            self.term_identifier()
        elif self.input_file.token_type() == "SYMBOL":
            self.term_symbol()

    def term_symbol(self):
        if self.input_file.symbol() == "(":
            self.symbol_output()
            self.compile_expression()
            self.symbol_output()
        elif self.input_file.symbol() in ['-', '~', '^', '#']:
            self.symbol_output()
            self.output_file.write(TERM)
            self.compile_term()
            self.output_file.write(TERM_CLOSE)

    def term_identifier(self):
        ident = self.input_file.current_token
        self.input_file.advance()
        if self.input_file.symbol() == "[":
            self.output_file.write("<identifier> " + ident + " </identifier>\n")
            self.symbol_output()
            self.compile_expression()
            self.symbol_output()
        elif self.input_file.symbol() == "(":
            self.output_file.write("<identifier> " + ident + " </identifier>\n")
            self.symbol_output()
            self.compile_expression_list()
            self.symbol_output()
        elif self.input_file.symbol() == ".":
            self.output_file.write("<identifier> " + ident + " </identifier>\n")
            self.symbol_output()
            self.identifier_output()
            self.symbol_output()
            self.compile_expression_list()
            self.symbol_output()
        else:
            self.output_file.write("<identifier> " + ident + " </identifier>\n")

    def compile_expression_list(self) -> None:
        """ expressionList: (expression (',' expression)* )?"""
        """Compiles a (possibly empty) comma-separated list of expressions."""
        # # Your code goes here!
        self.output_file.write(EXPRLIST)
        while self.input_file.has_more_tokens():
            if self.input_file.symbol() == ')':
                break
            self.compile_expression()
            if self.input_file.symbol() == ',':
                self.symbol_output()
            else:
                break
        self.output_file.write(EXPRLIST_CLOSE)

    def keyword_output(self):
        if self.input_file.token_type() == "KEYWORD":
            self.output_file.write(f"<keyword> {self.input_file.keyword()} </keyword>\n")
        if self.input_file.has_more_tokens():
            self.input_file.advance()

    def identifier_output(self):
        if self.input_file.token_type() == "IDENTIFIER":
            self.output_file.write(f"<identifier> {self.input_file.identifier()} </identifier>\n")
        if self.input_file.has_more_tokens():
            self.input_file.advance()

    def symbol_output(self):

        current_token = self.input_file.current_token
        if current_token in symbol_map:
            current_token = symbol_map[current_token]
        if self.input_file.token_type() == "SYMBOL":
            self.output_file.write(f"<symbol> {current_token} </symbol>\n")
        if self.input_file.has_more_tokens():
            self.input_file.advance()
