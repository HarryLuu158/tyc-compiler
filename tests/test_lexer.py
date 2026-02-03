"""
Lexer test cases for TyC compiler (Advanced/Complex)
100 test cases covering edge cases, boundary conditions, and tricky combinations.
"""

import pytest
from tests.utils import Tokenizer
from lexererr import *

class TestLexer:

    def check(self, input_str):
        """
        Helper to bridge the gap between tests and utils.py.
        Instantiates Tokenizer and calls get_tokens_as_string().
        """
        return Tokenizer(input_str).get_tokens_as_string()

    # --- 1. KEYWORDS & BOUNDARIES (16 Tests) ---
    def test_kwd_break_boundary(self): assert self.check("break breaking break_") == "BREAK,break,ID,breaking,ID,break_,EOF"
    def test_kwd_case_case(self): assert self.check("case casey Case") == "CASE,case,ID,casey,ID,Case,EOF"
    def test_kwd_continue_mixed(self): assert self.check("continue continue;CONTINUE") == "CONTINUE,continue,CONTINUE,continue,SEMI,;,ID,CONTINUE,EOF"
    def test_kwd_default_col(self): assert self.check("default:default") == "DEFAULT,default,COLON,:,DEFAULT,default,EOF"
    def test_kwd_else_if(self): assert self.check("else if elseif") == "ELSE,else,IF,if,ID,elseif,EOF"
    def test_kwd_for_loop(self): assert self.check("for(;;)for_") == "FOR,for,LPAREN,(,SEMI,;,SEMI,;,RPAREN,),ID,for_,EOF"
    def test_kwd_if_iff(self): assert self.check("if(iff)") == "IF,if,LPAREN,(,ID,iff,RPAREN,),EOF"
    def test_kwd_return_val(self): assert self.check("return_val return 0") == "ID,return_val,RETURN,return,INT_LIT,0,EOF"
    def test_kwd_switch_switch(self): assert self.check("switch(switch1)") == "SWITCH,switch,LPAREN,(,ID,switch1,RPAREN,),EOF"
    def test_kwd_while_wile(self): assert self.check("while(wile)whiles") == "WHILE,while,LPAREN,(,ID,wile,RPAREN,),ID,whiles,EOF"
    def test_kwd_types_concat(self): assert self.check("int float string void") == "INT,int,FLOAT,float,STRING,string,VOID,void,EOF"
    def test_kwd_struct_def(self): assert self.check("struct structure") == "STRUCT,struct,ID,structure,EOF"
    def test_kwd_auto_autom(self): assert self.check("auto automatic") == "AUTO,auto,ID,automatic,EOF"
    def test_kwd_case_insensitive(self): assert self.check("Int Float") == "ID,Int,ID,Float,EOF"
    def test_kwd_near_op(self): assert self.check("if(true)") == "IF,if,LPAREN,(,ID,true,RPAREN,),EOF"
    def test_kwd_newline_sep(self): assert self.check("int\nx") == "INT,int,ID,x,EOF"

    # --- 2. IDENTIFIERS & NAMING (10 Tests) ---
    def test_id_underscore_start(self): assert self.check("_ _x __init") == "ID,_,ID,_x,ID,__init,EOF"
    def test_id_with_digits(self): assert self.check("var1 var_2 v3r") == "ID,var1,ID,var_2,ID,v3r,EOF"
    def test_id_mixed_caps(self): assert self.check("myVar MyVar MYVAR") == "ID,myVar,ID,MyVar,ID,MYVAR,EOF"
    def test_id_long(self): assert self.check("this_is_a_very_long_variable_name_12345") == "ID,this_is_a_very_long_variable_name_12345,EOF"
    def test_id_touching_ints(self): assert self.check("x1 1x") == "ID,x1,INT_LIT,1,ID,x,EOF"
    def test_id_touching_floats(self): assert self.check("f1.2") == "ID,f1,FLOAT_LIT,.2,EOF"
    def test_id_keywords_inside(self): assert self.check("printInt readFloat") == "ID,printInt,ID,readFloat,EOF"
    def test_id_single_char(self): assert self.check("a b c") == "ID,a,ID,b,ID,c,EOF"
    def test_id_operator_lookalike(self): assert self.check("or and not") == "ID,or,ID,and,ID,not,EOF"
    def test_id_consecutive(self): assert self.check("x y z") == "ID,x,ID,y,ID,z,EOF"

    # --- 3. INT LITERALS & BOUNDARIES (10 Tests) ---
    def test_int_sequence(self): assert self.check("0 1 10 100") == "INT_LIT,0,INT_LIT,1,INT_LIT,10,INT_LIT,100,EOF"
    def test_int_leading_zeros(self): assert self.check("00 01 007") == "INT_LIT,0,INT_LIT,0,INT_LIT,0,INT_LIT,1,INT_LIT,0,INT_LIT,0,INT_LIT,7,EOF"
    def test_int_max_boundary(self): assert self.check("2147483647") == "INT_LIT,2147483647,EOF"
    def test_int_touching_ops(self): assert self.check("1+2-3") == "INT_LIT,1,ADD,+,INT_LIT,2,SUB,-,INT_LIT,3,EOF"
    def test_int_touching_dot(self): assert self.check("1. 2.") == "FLOAT_LIT,1.,FLOAT_LIT,2.,EOF"
    def test_int_hex_fail(self): assert self.check("0x1A") == "INT_LIT,0,ID,x1A,EOF"
    def test_int_massive(self): assert self.check("12345678901234567890") == "INT_LIT,12345678901234567890,EOF"
    def test_int_neg_is_op(self): assert self.check("-1") == "SUB,-,INT_LIT,1,EOF"
    def test_int_sep_by_comment(self): assert self.check("1/**/2") == "INT_LIT,1,INT_LIT,2,EOF"
    def test_int_block_scope(self): assert self.check("{1}") == "LBRACE,{,INT_LIT,1,RBRACE,},EOF"

    # --- 4. FLOAT LITERALS & SCIENTIFIC NOTATION (15 Tests) ---
    def test_float_std_variants(self): assert self.check("1.2 .2 3.") == "FLOAT_LIT,1.2,FLOAT_LIT,.2,FLOAT_LIT,3.,EOF"
    def test_float_sci_basic(self): assert self.check("1e10 1.e2 .5e-2") == "FLOAT_LIT,1e10,FLOAT_LIT,1.e2,FLOAT_LIT,.5e-2,EOF"
    def test_float_sci_plus(self): assert self.check("1E+5 3.14e+0") == "FLOAT_LIT,1E+5,FLOAT_LIT,3.14e+0,EOF"
    def test_float_sci_complex(self): assert self.check("10.5e-10") == "FLOAT_LIT,10.5e-10,EOF"
    def test_float_adjacent_dots(self): assert self.check("1..2") == "FLOAT_LIT,1.,FLOAT_LIT,.2,EOF"
    def test_float_bad_sci(self): assert self.check("1e") == "INT_LIT,1,ID,e,EOF"
    def test_float_bad_sci_op(self): assert self.check("1e+ 2") == "INT_LIT,1,ID,e,ADD,+,INT_LIT,2,EOF"
    def test_float_starting_zeros(self): assert self.check("0.0 00.5 0e0") == "FLOAT_LIT,0.0,FLOAT_LIT,00.5,FLOAT_LIT,0e0,EOF"
    def test_float_vs_method(self): assert self.check("obj.method") == "ID,obj,DOT,.,ID,method,EOF"
    def test_float_vs_range(self): assert self.check("1..3") == "FLOAT_LIT,1.,FLOAT_LIT,.3,EOF"
    def test_float_many_dots(self): assert self.check("...") == "DOT,.,DOT,.,DOT,.,EOF"
    def test_float_sci_capital(self): assert self.check("1.2E-3") == "FLOAT_LIT,1.2E-3,EOF"
    def test_float_no_int_part(self): assert self.check(".123") == "FLOAT_LIT,.123,EOF"
    def test_float_ending_dot_op(self): assert self.check("3. + 4.") == "FLOAT_LIT,3.,ADD,+,FLOAT_LIT,4.,EOF"
    def test_float_consecutive(self): assert self.check("1.2 3.4") == "FLOAT_LIT,1.2,FLOAT_LIT,3.4,EOF"

    # --- 5. STRINGS & ESCAPES (10 Tests) ---
    def test_str_complex_escapes(self): assert self.check(r'"\n\t\"\\"') == r"STRING_LIT,\n\t\"\\,EOF"
    def test_str_with_keywords(self): assert self.check('"if else while"') == "STRING_LIT,if else while,EOF"
    def test_str_with_ops(self): assert self.check('"++ -- =="') == "STRING_LIT,++ -- ==,EOF"
    def test_str_with_comments(self): assert self.check('"// not comment"') == "STRING_LIT,// not comment,EOF"
    def test_str_empty(self): assert self.check('""') == "STRING_LIT,,EOF"
    def test_str_single_quote_inside(self): assert self.check('"\'"') == "STRING_LIT,',EOF"
    def test_str_spaces(self): assert self.check('"   "') == "STRING_LIT,   ,EOF"
    def test_str_multiline_fail(self): 
        with pytest.raises(UncloseString): self.check('"line1\nline2"')
    def test_str_concat_op(self): assert self.check('"a" + "b"') == "STRING_LIT,a,ADD,+,STRING_LIT,b,EOF"
    def test_str_nested_appearance(self): assert self.check(r'"nested \"quote\""') == r"STRING_LIT,nested \"quote\",EOF"

    # --- 6. OPERATOR COMBINATIONS (25 Tests) ---
    def test_op_triple_add(self): assert self.check("+++") == "INC,++,ADD,+,EOF"
    def test_op_triple_sub(self): assert self.check("---") == "DEC,--,SUB,-,EOF"
    def test_op_eq_assign(self): assert self.check("===") == "EQUAL,==,ASSIGN,=,EOF"
    def test_op_arrow_mimic(self): assert self.check("->") == "SUB,-,GT,>,EOF"
    def test_op_lte_assign(self): assert self.check("<==") == "LE,<=,ASSIGN,=,EOF"
    def test_op_gte_assign(self): assert self.check(">==") == "GE,>=,ASSIGN,=,EOF"
    def test_op_not_neq(self): assert self.check("!!=") == "NOT,!,NOTEQUAL,!=,EOF"
    def test_op_and_logic(self): assert self.check("&& !") == "AND,&&,NOT,!,EOF"
    def test_op_div_mul(self): assert self.check("/*") == "DIV,/,MUL,*,EOF"
    def test_op_div_div(self): assert self.check("//") == "EOF"
    def test_op_valid_combo(self): assert self.check("*=") == "MUL,*,ASSIGN,=,EOF"
    def test_op_paren_mix(self): assert self.check("(){}") == "LPAREN,(,RPAREN,),LBRACE,{,RBRACE,},EOF"
    def test_op_brace_semi(self): assert self.check("};") == "RBRACE,},SEMI,;,EOF"
    def test_op_comma_dot(self): assert self.check(",.") == "COMMA,,,DOT,.,EOF"
    def test_op_nested_parens(self): assert self.check("((a))") == "LPAREN,(,LPAREN,(,ID,a,RPAREN,),RPAREN,),EOF"
    def test_op_arith_prec(self): assert self.check("a*b+c") == "ID,a,MUL,*,ID,b,ADD,+,ID,c,EOF"
    def test_op_logic_prec(self): assert self.check("a&&b||c") == "ID,a,AND,&&,ID,b,OR,||,ID,c,EOF"
    def test_op_inc_dec_space(self): assert self.check("++ --") == "INC,++,DEC,--,EOF"
    def test_op_unary_neg(self): assert self.check("x = -1") == "ID,x,ASSIGN,=,SUB,-,INT_LIT,1,EOF"
    def test_op_unary_not(self): assert self.check("!x") == "NOT,!,ID,x,EOF"
    def test_op_relational(self): assert self.check("< > <= >=") == "LT,<,GT,>,LE,<=,GE,>=,EOF"
    def test_op_mod_div(self): assert self.check("% /") == "MOD,%,DIV,/,EOF"
    def test_op_comment_trick_1(self): assert self.check("/ *") == "DIV,/,MUL,*,EOF"
    def test_op_comment_trick_2(self): assert self.check("/*/") == "DIV,/,MUL,*,DIV,/,EOF"
    def test_op_div_star_space(self): assert self.check("/ * * /") == "DIV,/,MUL,*,MUL,*,DIV,/,EOF"

    # --- 7. COMMENTS & WHITESPACE (5 Tests) ---
    def test_ws_complex(self): assert self.check(" \t\r\n ") == "EOF"
    def test_comment_nested_fake(self): assert self.check("/* /* */") == "EOF"
    def test_comment_star_inside(self): assert self.check("/* * */") == "EOF"
    def test_comment_slashes_inside(self): assert self.check("// ///") == "EOF"
    def test_comment_ends_with_eof(self): assert self.check("// eof") == "EOF"

    # --- 8. ERROR HANDLING & EDGE CASES (9 Tests) ---
    def test_err_unclose_quote_eol(self): 
        with pytest.raises(UncloseString): self.check('"unfinished\n"')
    def test_err_unclose_quote_eof(self): 
        with pytest.raises(UncloseString): self.check('"unfinished')
    def test_err_bad_escape_char(self): 
        with pytest.raises(IllegalEscape): self.check(r'"\q"')
    def test_err_bad_escape_end(self): 
        with pytest.raises(UncloseString): self.check('"\\')
    def test_err_bad_char_at(self): 
        with pytest.raises(ErrorToken): self.check("@var")
    def test_err_bad_char_hash(self): 
        with pytest.raises(ErrorToken): self.check("#define")
    def test_err_bad_char_tilde(self): 
        with pytest.raises(ErrorToken): self.check("~destructor")
    def test_err_bad_char_question(self): 
        with pytest.raises(ErrorToken): self.check("x ? y : z")
    def test_err_bad_char_backtick(self): 
        with pytest.raises(ErrorToken): self.check("`")