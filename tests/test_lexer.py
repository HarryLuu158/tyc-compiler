"""
Lexer test cases for TyC compiler
100 test cases using the existing Tokenizer class in tests/utils.py
"""

import pytest
from tests.utils import Tokenizer
from lexererr import *

class TestLexer:

    def check(self, input_str):
        """Helper to return the token string from the utils Tokenizer"""
        return Tokenizer(input_str).get_tokens_as_string()

    # --- KEYWORDS (16 Tests) ---
    # format is always: TOKEN_NAME,text,EOF
    def test_kwd_break(self): assert self.check("break") == "BREAK,break,EOF"
    def test_kwd_case(self): assert self.check("case") == "CASE,case,EOF"
    def test_kwd_continue(self): assert self.check("continue") == "CONTINUE,continue,EOF"
    def test_kwd_default(self): assert self.check("default") == "DEFAULT,default,EOF"
    def test_kwd_else(self): assert self.check("else") == "ELSE,else,EOF"
    def test_kwd_for(self): assert self.check("for") == "FOR,for,EOF"
    def test_kwd_if(self): assert self.check("if") == "IF,if,EOF"
    def test_kwd_return(self): assert self.check("return") == "RETURN,return,EOF"
    def test_kwd_switch(self): assert self.check("switch") == "SWITCH,switch,EOF"
    def test_kwd_while(self): assert self.check("while") == "WHILE,while,EOF"
    def test_kwd_int(self): assert self.check("int") == "INT,int,EOF"
    def test_kwd_float(self): assert self.check("float") == "FLOAT,float,EOF"
    def test_kwd_string(self): assert self.check("string") == "STRING,string,EOF"
    def test_kwd_void(self): assert self.check("void") == "VOID,void,EOF"
    def test_kwd_struct(self): assert self.check("struct") == "STRUCT,struct,EOF"
    def test_kwd_auto(self): assert self.check("auto") == "AUTO,auto,EOF"

    # --- IDENTIFIERS (10 Tests) ---
    def test_id_basic(self): assert self.check("x") == "ID,x,EOF"
    def test_id_multi(self): assert self.check("count") == "ID,count,EOF"
    def test_id_underscore(self): assert self.check("_temp") == "ID,_temp,EOF"
    def test_id_camel(self): assert self.check("myVar") == "ID,myVar,EOF"
    def test_id_snake(self): assert self.check("my_var") == "ID,my_var,EOF"
    def test_id_digits(self): assert self.check("var123") == "ID,var123,EOF"
    def test_id_mixed(self): assert self.check("Type_2_Name") == "ID,Type_2_Name,EOF"
    def test_id_keyword_prefix(self): assert self.check("integer") == "ID,integer,EOF"
    def test_id_keyword_suffix(self): assert self.check("myint") == "ID,myint,EOF"
    def test_id_caps(self): assert self.check("MAX_VAL") == "ID,MAX_VAL,EOF"

    # --- INT LITERALS (10 Tests) ---
    def test_int_zero(self): assert self.check("0") == "INT_LIT,0,EOF"
    def test_int_pos(self): assert self.check("123") == "INT_LIT,123,EOF"
    def test_int_large(self): assert self.check("999999999") == "INT_LIT,999999999,EOF"
    # Note: Tokenizer output puts commas between token parts
    def test_int_list(self): assert self.check("1 2 3") == "INT_LIT,1,INT_LIT,2,INT_LIT,3,EOF"
    def test_int_leading_zero_split(self): 
        # 012 -> 0 then 12
        assert self.check("012") == "INT_LIT,0,INT_LIT,12,EOF"
    def test_int_simple_expr(self): assert self.check("1+1") == "INT_LIT,1,ADD,+,INT_LIT,1,EOF"
    def test_int_hex_like_id(self): assert self.check("0x123") == "INT_LIT,0,ID,x123,EOF" # 0 is int, x123 is ID
    def test_int_neg(self): assert self.check("-5") == "SUB,-,INT_LIT,5,EOF"
    def test_int_neg_space(self): assert self.check("- 5") == "SUB,-,INT_LIT,5,EOF"
    def test_int_with_dot(self): assert self.check("1.2") != "INT_LIT,1,INT_LIT,2,EOF" # Should be float

    # --- FLOAT LITERALS (15 Tests) ---
    def test_float_std(self): assert self.check("3.14") == "FLOAT_LIT,3.14,EOF"
    def test_float_start_dot(self): assert self.check(".5") == "FLOAT_LIT,.5,EOF"
    def test_float_end_dot(self): assert self.check("10.") == "FLOAT_LIT,10.,EOF"
    def test_float_sci(self): assert self.check("1e5") == "FLOAT_LIT,1e5,EOF"
    def test_float_sci_pos(self): assert self.check("1E+5") == "FLOAT_LIT,1E+5,EOF"
    def test_float_sci_neg(self): assert self.check("1.2e-3") == "FLOAT_LIT,1.2e-3,EOF"
    def test_float_complex(self): assert self.check(".5E2") == "FLOAT_LIT,.5E2,EOF"
    def test_float_zeros(self): assert self.check("0.0") == "FLOAT_LIT,0.0,EOF"
    def test_float_many_digits(self): assert self.check("123.456") == "FLOAT_LIT,123.456,EOF"
    def test_float_sci_capital(self): assert self.check("1E5") == "FLOAT_LIT,1E5,EOF"
    def test_float_neg(self): assert self.check("-1.5") == "SUB,-,FLOAT_LIT,1.5,EOF"
    def test_float_dot_only_fail(self): 
        # dot by itself is the DOT operator
        assert self.check(".") == "DOT,.,EOF"
    def test_float_bad_sci(self): assert self.check("1e") == "INT_LIT,1,ID,e,EOF"
    def test_float_leading_zeros(self): assert self.check("00.5") == "FLOAT_LIT,00.5,EOF"
    def test_float_sci_no_dot(self): assert self.check("5e10") == "FLOAT_LIT,5e10,EOF"

    # --- STRING LITERALS (10 Tests) ---
    # Note: Grammar modification self.text[1:-1] strips quotes in the result
    def test_str_empty(self): assert self.check('""') == "STRING_LIT,,EOF"
    def test_str_basic(self): assert self.check('"hello"') == "STRING_LIT,hello,EOF"
    def test_str_spaces(self): assert self.check('"hello world"') == "STRING_LIT,hello world,EOF"
    # Escapes are preserved in text but stripping quotes might affect how they look
    def test_str_escape_n(self): assert self.check(r'"\n"') == r"STRING_LIT,\n,EOF"
    def test_str_escape_t(self): assert self.check(r'"\t"') == r"STRING_LIT,\t,EOF"
    def test_str_escape_quote(self): assert self.check(r'"\""') == r"STRING_LIT,\",EOF"
    def test_str_escape_slash(self): assert self.check(r'"\\"') == r"STRING_LIT,\\,EOF"
    def test_str_keywords_inside(self): assert self.check('"int float"') == "STRING_LIT,int float,EOF"
    def test_str_symbols_inside(self): assert self.check('"{};"') == "STRING_LIT,{};,EOF"
    def test_str_numbers_inside(self): assert self.check('"123"') == "STRING_LIT,123,EOF"

    # --- OPERATORS & SEPARATORS (25 Tests) ---
    def test_op_add(self): assert self.check("+") == "ADD,+,EOF"
    def test_op_sub(self): assert self.check("-") == "SUB,-,EOF"
    def test_op_mul(self): assert self.check("*") == "MUL,*,EOF"
    def test_op_div(self): assert self.check("/") == "DIV,/,EOF"
    def test_op_mod(self): assert self.check("%") == "MOD,%,EOF"
    def test_op_eq(self): assert self.check("==") == "EQUAL,==,EOF"
    def test_op_neq(self): assert self.check("!=") == "NOTEQUAL,!=,EOF"
    def test_op_lt(self): assert self.check("<") == "LT,<,EOF"
    def test_op_gt(self): assert self.check(">") == "GT,>,EOF"
    def test_op_le(self): assert self.check("<=") == "LE,<=,EOF"
    def test_op_ge(self): assert self.check(">=") == "GE,>=,EOF"
    def test_op_and(self): assert self.check("&&") == "AND,&&,EOF"
    def test_op_or(self): assert self.check("||") == "OR,||,EOF"
    def test_op_not(self): assert self.check("!") == "NOT,!,EOF"
    def test_op_inc(self): assert self.check("++") == "INC,++,EOF"
    def test_op_dec(self): assert self.check("--") == "DEC,--,EOF"
    def test_op_assign(self): assert self.check("=") == "ASSIGN,=,EOF"
    def test_op_dot(self): assert self.check(".") == "DOT,.,EOF"
    def test_sep_lparen(self): assert self.check("(") == "LPAREN,(,EOF"
    def test_sep_rparen(self): assert self.check(")") == "RPAREN,),EOF"
    def test_sep_lbrace(self): assert self.check("{") == "LBRACE,{,EOF"
    def test_sep_rbrace(self): assert self.check("}") == "RBRACE,},EOF"
    def test_sep_semi(self): assert self.check(";") == "SEMI,;,EOF"
    def test_sep_comma(self): assert self.check(",") == "COMMA,,,EOF"

    # --- COMMENTS & WHITESPACE (5 Tests) ---
    def test_comment_line(self): assert self.check("// abc") == "EOF"
    def test_comment_block(self): assert self.check("/* abc */") == "EOF"
    def test_ws_space(self): assert self.check("  ") == "EOF"
    def test_ws_tab(self): assert self.check("\t") == "EOF"
    def test_ws_mixed(self): assert self.check(" \t \n ") == "EOF"

    # --- ERROR HANDLING (9 Tests) ---
    def test_err_unclose_str(self): 
        with pytest.raises(UncloseString): self.check('"abc')
    def test_err_bad_escape(self): 
        with pytest.raises(IllegalEscape): self.check('"\\k"')
    def test_err_char_at(self): 
        with pytest.raises(ErrorToken): self.check("@")
    def test_err_char_hash(self): 
        with pytest.raises(ErrorToken): self.check("#")
    def test_err_char_dollar(self): 
        with pytest.raises(ErrorToken): self.check("$")
    def test_err_char_tilde(self): 
        with pytest.raises(ErrorToken): self.check("~")
    def test_err_char_question(self): 
        # ? is not an operator in grammar
        with pytest.raises(ErrorToken): self.check("?")
    def test_err_unclose_str_newline(self):
        with pytest.raises(UncloseString): self.check('"\n"')
    def test_err_unclose_str_empty(self):
        with pytest.raises(UncloseString): self.check('"')