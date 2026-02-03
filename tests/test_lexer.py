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

    # --- 1. PROGRAM STRUCTURE (10 Tests) ---
    def test_prog_empty(self): assert self.check("") == "success"
    def test_prog_single_func(self): assert self.check("void main() {}") == "success"
    def test_prog_multiple_funcs(self): assert self.check("int a() {} float b() {} void c() {}") == "success"
    def test_prog_struct_decl(self): assert self.check("struct Point { int x; int y; };") == "success"
    def test_prog_mixed_decls(self): assert self.check("struct S {}; void f() {} int g() { return 1; }") == "success"
    def test_prog_global_comments(self): assert self.check("/* Header */ void main() { // Body \n }") == "success"
    def test_prog_whitespace_crazy(self): assert self.check("\n\n   void   \t  f  (   )  \n { \n }  ") == "success"
    def test_prog_param_types(self): assert self.check("void f(int i, float f, string s, MyStruct m) {}") == "success"
    def test_prog_no_param(self): assert self.check("void f() {}") == "success"
    def test_prog_func_return_type_array(self): assert self.check("int[] f() {}") != "success" # Arrays not in grammar yet

    # --- 2. STRUCT DECLARATIONS (10 Tests) ---
    def test_struct_basic(self): assert self.check("struct A { int x; };") == "success"
    def test_struct_multi_field(self): assert self.check("struct Person { string name; int age; float height; };") == "success"
    def test_struct_nested_type(self): assert self.check("struct Line { Point p1; Point p2; };") == "success"
    def test_struct_empty_body(self): assert self.check("struct Empty {};") == "success"
    def test_struct_array_field_fail(self): assert self.check("struct A { int x[]; };") != "success" # No arrays
    def test_struct_init_in_field_fail(self): assert self.check("struct A { int x = 1; };") != "success" # No default init in struct
    def test_struct_missing_semi(self): assert self.check("struct A { int x }") != "success"
    def test_struct_missing_end_semi(self): assert self.check("struct A { int x; }") != "success" # Needs ; after }
    def test_struct_keyword_name_fail(self): assert self.check("struct if { int x; };") != "success"
    def test_struct_duplicate_member_valid_parse(self): 
        assert self.check("struct A { int x; int x; };") == "success"

    # --- 3. VARIABLE DECLARATIONS & ASSIGNMENTS (10 Tests) ---
    def test_var_basic_types(self): assert self.check("void f() { int i; float f; string s; }") == "success"
    def test_var_init_literal(self): assert self.check("void f() { int x = 10; float y = 3.14; }") == "success"
    def test_var_init_complex(self): assert self.check("void f() { int x = (1 + 2) * 3; }") == "success"
    def test_var_auto_infer(self): assert self.check("void f() { auto x = 100; }") == "success"
    def test_var_auto_expr(self): assert self.check("void f() { auto y = x + 1; }") == "success"
    def test_var_struct_inst(self): assert self.check("void f() { Point p; }") == "success"
    def test_var_struct_init(self): assert self.check("void f() { Point p = {1, 2}; }") == "success"
    def test_var_assign_stmt(self): assert self.check("void f() { x = 1; }") == "success"
    def test_var_decl_missing_semi(self): assert self.check("void f() { int x }") != "success"
    def test_var_auto_no_init_valid(self): 
        assert self.check("void f() { auto x; }") == "success"

    # --- 4. FUNCTION DECLARATIONS & CALLS (10 Tests) ---
    def test_func_ret_void(self): assert self.check("void f() { return; }") == "success"
    def test_func_ret_val(self): assert self.check("int f() { return 1; }") == "success"
    def test_func_args_mixed(self): assert self.check("void f(int a, float b) {}") == "success"
    def test_func_args_struct(self): assert self.check("void f(Point p) {}") == "success"
    def test_func_call_stmt(self): assert self.check("void f() { g(); }") == "success"
    def test_func_call_args(self): assert self.check("void f() { g(1, a, \"s\"); }") == "success"
    def test_func_call_expr_arg(self): assert self.check("void f() { g(a + b); }") == "success"
    def test_func_nested_def_fail(self): assert self.check("void f() { void g() {} }") != "success"
    def test_func_missing_body(self): assert self.check("void f();") != "success"
    def test_func_param_no_type(self): assert self.check("void f(x) {}") != "success"

    # --- 5. EXPRESSIONS (15 Tests) ---
    def test_expr_math_prec(self): assert self.check("void f() { x = 1 + 2 * 3; }") == "success" # 1+(2*3)
    def test_expr_paren_override(self): assert self.check("void f() { x = (1 + 2) * 3; }") == "success"
    def test_expr_assoc_right(self): assert self.check("void f() { x = a = b = 0; }") == "success"
    def test_expr_relational(self): assert self.check("void f() { b = x < 10 && y > 5; }") == "success"
    def test_expr_equality(self): assert self.check("void f() { b = x == 10 || x != 5; }") == "success"
    def test_expr_unary_not(self): assert self.check("void f() { b = !true; }") == "success"
    def test_expr_unary_neg(self): assert self.check("void f() { x = -y; }") == "success"
    def test_expr_member_access(self): assert self.check("void f() { x = p.x; }") == "success"
    def test_expr_member_assign(self): assert self.check("void f() { p.x = 10; }") == "success"
    def test_expr_inc_dec_prefix(self): assert self.check("void f() { ++x; --y; }") == "success"
    def test_expr_inc_dec_postfix(self): assert self.check("void f() { x++; y--; }") == "success"
    def test_expr_struct_init_nest(self): assert self.check("void f() { Rect r = {{0,0}, {10,10}}; }") == "success"
    def test_expr_invalid_op_seq(self): assert self.check("void f() { x = 1 + * 2; }") != "success"
    def test_expr_missing_operand(self): assert self.check("void f() { x = 1 + ; }") != "success"
    def test_expr_unbalanced_paren(self): assert self.check("void f() { x = (1 + 2; }") != "success"

    # --- 6. CONTROL FLOW: IF STATEMENTS (10 Tests) ---
    def test_if_simple(self): assert self.check("void f() { if (x) return; }") == "success"
    def test_if_block(self): assert self.check("void f() { if (x) { x=1; } }") == "success"
    def test_if_else(self): assert self.check("void f() { if (x) y=1; else y=2; }") == "success"
    def test_if_else_chain(self): assert self.check("void f() { if(a) {} else if(b) {} else {} }") == "success"
    def test_if_nested(self): assert self.check("void f() { if(a) { if(b) c=1; } }") == "success"
    def test_if_dangling_else(self): assert self.check("void f() { if(a) if(b) c=1; else c=2; }") == "success"
    def test_if_cond_assign(self): assert self.check("void f() { if (x = 1) {} }") == "success" # Valid C-style syntax
    def test_if_empty_stmt_fail(self): assert self.check("void f() { if (x) ; }") != "success" # Grammar forbids empty ';'
    def test_if_missing_paren(self): assert self.check("void f() { if x {} }") != "success"
    def test_if_no_body(self): assert self.check("void f() { if (x) }") != "success"

    # --- 7. CONTROL FLOW: LOOPS (10 Tests) ---
    def test_while_basic(self): assert self.check("void f() { while (x > 0) x--; }") == "success"
    def test_while_block(self): assert self.check("void f() { while (true) { break; } }") == "success"
    def test_for_basic(self): assert self.check("void f() { for (i=0; i<10; i++) {} }") == "success"
    def test_for_decl(self): assert self.check("void f() { for (int i=0; i<10; i++) {} }") == "success"
    def test_for_infinite(self): assert self.check("void f() { for (;;) {} }") == "success"
    def test_for_missing_parts(self): assert self.check("void f() { for (; x<10; ) {} }") == "success"
    def test_for_nested(self): assert self.check("void f() { for(;;) { while(1) {} } }") == "success"
    def test_for_break_continue(self): assert self.check("void f() { while(1) { break; continue; } }") == "success"
    def test_while_missing_cond(self): assert self.check("void f() { while() {} }") != "success"
    def test_for_bad_syntax(self): assert self.check("void f() { for(i=0 i<10 i++) {} }") != "success"

    # --- 8. CONTROL FLOW: SWITCH (10 Tests) ---
    def test_switch_basic(self): assert self.check("void f() { switch(x) { case 1: break; } }") == "success"
    def test_switch_default(self): assert self.check("void f() { switch(x) { default: break; } }") == "success"
    def test_switch_mixed(self): assert self.check("void f() { switch(x) { case 1: y=1; break; default: y=0; } }") == "success"
    def test_switch_fallthrough(self): assert self.check("void f() { switch(x) { case 1: case 2: y=1; } }") == "success"
    def test_switch_nested(self): assert self.check("void f() { switch(x) { case 1: switch(y){} } }") == "success"
    def test_switch_empty(self): assert self.check("void f() { switch(x) {} }") == "success"
    def test_switch_no_brace(self): assert self.check("void f() { switch(x) case 1: break; }") != "success"
    def test_break_outside_loop(self): assert self.check("void f() { break; }") == "success" 
    def test_return_void_val(self): assert self.check("void f() { return 1+2; }") == "success"
    def test_continue_basic(self): assert self.check("void f() { continue; }") == "success"

    # --- 9. NESTING & COMPLEXITY (10 Tests) ---
    def test_nest_deep_blocks(self): assert self.check("void f() { { { { int x; } } } }") == "success"
    def test_nest_mixed_loops(self): 
        assert self.check("void f() { for(;;) { if(x) { while(y) { break; } } } }") == "success"
    def test_nest_expr_crazy(self): 
        assert self.check("void f() { x = ((a+b)*(c-d))/(e%f) + g[h]; }") != "success" 
    def test_nest_expr_valid_crazy(self):
        assert self.check("void f() { x = (a + (b * (c - d.e))); }") == "success"
    def test_nest_struct_decl_local(self): 
        assert self.check("void f() { struct Local {}; }") != "success"

    # --- 10. ERROR HANDLING (15 Tests) ---
    def test_err_bad_char(self): assert self.check("void f() { int x = @; }") != "success"
    def test_err_missing_brace(self): assert self.check("void f() { if(x) { x=1; }") != "success"
    def test_err_double_semi(self): assert self.check("void f() { x=1;; }") != "success" 
    def test_err_reserved_word_var(self): assert self.check("void f() { int while = 1; }") != "success"
    def test_err_reserved_word_func(self): assert self.check("void if() {}") != "success"
    def test_err_bad_assign(self): assert self.check("void f() { 1 = x; }") != "success" 
    def test_err_assign_in_decl(self): assert self.check("void f() { int x = = 1; }") != "success"
    def test_err_unclosed_string(self): assert self.check("void f() { s = \"hello; }") != "success"
    def test_err_incomplete_expr(self): assert self.check("void f() { x = 1 + ; }") != "success"
    def test_err_stmt_outside_func(self): assert self.check("x = 1; void f(){}") != "success"