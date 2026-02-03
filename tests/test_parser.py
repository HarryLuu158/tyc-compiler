"""
Parser test cases for TyC compiler
100 test cases using the instance-based Parser class from tests/utils.py
"""

import pytest
from tests.utils import Parser

class TestParser:

    def check(self, input_str):
        """Helper to instantiate Parser and call .parse()"""
        return Parser(input_str).parse()

    # --- 1. PROGRAM STRUCTURE (10 Tests) ---
    def test_prog_empty(self): assert self.check("") == "success"
    def test_prog_one_func(self): assert self.check("void main() {}") == "success"
    def test_prog_two_func(self): assert self.check("void f1(){} void f2(){}") == "success"
    def test_prog_struct_func(self): assert self.check("struct S {}; void f(){}") == "success"
    def test_prog_func_struct(self): assert self.check("void f(){} struct S {};") == "success"
    def test_prog_mixed(self): assert self.check("struct A{}; void f1(){} struct B{}; void f2(){}") == "success"
    def test_prog_comments(self): assert self.check("// cmt\nvoid main() {}") == "success"
    def test_prog_spaces(self): assert self.check("   void    main  (  )   {  }   ") == "success"
    def test_prog_newline(self): assert self.check("\nvoid main()\n{\n}\n") == "success"
    def test_prog_comment_block(self): assert self.check("/* */ void main(){}") == "success"

    # --- 2. STRUCTS (10 Tests) ---
    def test_struct_empty(self): assert self.check("struct A {};") == "success"
    def test_struct_one_mem(self): assert self.check("struct A { int x; };") == "success"
    def test_struct_two_mem(self): assert self.check("struct A { int x; float y; };") == "success"
    def test_struct_type_struct(self): assert self.check("struct A { B b; };") == "success"
    def test_struct_string(self): assert self.check("struct A { string s; };") == "success"
    def test_struct_id_type(self): assert self.check("struct A { MyType m; };") == "success"
    def test_struct_many_mems(self): assert self.check("struct A { int a; int b; int c; };") == "success"
    # Negative struct tests
    def test_struct_nested_fail(self): assert self.check("struct A { struct B {}; };") != "success"
    def test_struct_no_semi_fail(self): assert self.check("struct A {}") != "success"
    def test_struct_init_empty(self): assert self.check("void f() { A a = {}; }") == "success"

    # --- 3. FUNCTIONS (15 Tests) ---
    def test_func_void(self): assert self.check("void f(){}") == "success"
    def test_func_int(self): assert self.check("int f(){ return 1; }") == "success"
    def test_func_arg1(self): assert self.check("void f(int x){}") == "success"
    def test_func_arg2(self): assert self.check("void f(int x, float y){}") == "success"
    def test_func_arg3(self): assert self.check("void f(A a, B b, C c){}") == "success"
    def test_func_no_type(self): assert self.check("f(){}") == "success"
    def test_func_no_ret(self): assert self.check("int f(){}") == "success"
    def test_func_ret_stmt(self): assert self.check("void f(){ return; }") == "success"
    def test_func_ret_expr(self): assert self.check("int f(){ return 1+2; }") == "success"
    def test_func_nested_call(self): assert self.check("void f(){ g(); }") == "success"
    def test_func_call_args(self): assert self.check("void f(){ g(1,2); }") == "success"
    def test_func_call_empty(self): assert self.check("void f(){ g(); }") == "success"
    def test_func_call_complex(self): assert self.check("void f(){ g(a+b, c*d); }") == "success"
    def test_func_arg_struct(self): assert self.check("void f(Point p){}") == "success"
    def test_func_block_stmts(self): assert self.check("void f(){ int x; x=1; }") == "success"

    # --- 4. VARIABLES (15 Tests) ---
    def test_var_decl_int(self): assert self.check("void f(){ int x; }") == "success"
    def test_var_decl_float(self): assert self.check("void f(){ float x; }") == "success"
    def test_var_decl_string(self): assert self.check("void f(){ string s; }") == "success"
    def test_var_decl_struct(self): assert self.check("void f(){ Point p; }") == "success"
    def test_var_init_lit(self): assert self.check("void f(){ int x = 1; }") == "success"
    def test_var_init_expr(self): assert self.check("void f(){ int x = 1+2; }") == "success"
    def test_var_auto_lit(self): assert self.check("void f(){ auto x = 1; }") == "success"
    def test_var_auto_expr(self): assert self.check("void f(){ auto x = y*z; }") == "success"
    def test_var_auto_no_init(self): assert self.check("void f(){ auto x; }") == "success"
    def test_var_struct_init(self): assert self.check("void f(){ Point p = {1,2}; }") == "success"
    def test_var_struct_empty(self): assert self.check("void f(){ Point p = {}; }") == "success"
    def test_var_assign(self): assert self.check("void f(){ x = 1; }") == "success"
    def test_var_assign_chain(self): assert self.check("void f(){ x = y = 1; }") == "success"
    def test_var_decl_block(self): assert self.check("void f(){ { int x; } }") == "success"
    def test_var_decl_fail_semi(self): assert self.check("void f(){ int x }") != "success"

    # --- 5. EXPRESSIONS (20 Tests) ---
    def test_expr_add(self): assert self.check("void f(){ x = a + b; }") == "success"
    def test_expr_mul(self): assert self.check("void f(){ x = a * b; }") == "success"
    def test_expr_prec(self): assert self.check("void f(){ x = a + b * c; }") == "success"
    def test_expr_paren(self): assert self.check("void f(){ x = (a + b) * c; }") == "success"
    def test_expr_unary(self): assert self.check("void f(){ x = -a; }") == "success"
    def test_expr_not(self): assert self.check("void f(){ x = !a; }") == "success"
    def test_expr_member(self): assert self.check("void f(){ x = p.x; }") == "success"
    def test_expr_member_chain(self): assert self.check("void f(){ x = a.b.c; }") == "success"
    def test_expr_inc(self): assert self.check("void f(){ x++; }") == "success"
    def test_expr_dec(self): assert self.check("void f(){ --x; }") == "success"
    def test_expr_inc_member(self): assert self.check("void f(){ p.x++; }") == "success"
    def test_expr_logic_and(self): assert self.check("void f(){ x = a && b; }") == "success"
    def test_expr_logic_or(self): assert self.check("void f(){ x = a || b; }") == "success"
    def test_expr_rel_lt(self): assert self.check("void f(){ x = a < b; }") == "success"
    def test_expr_rel_eq(self): assert self.check("void f(){ x = a == b; }") == "success"
    def test_expr_lit_str(self): assert self.check('void f(){ s = "hi"; }') == "success"
    def test_expr_lit_float(self): assert self.check("void f(){ f = 1.2; }") == "success"
    def test_expr_nested_init(self): assert self.check("void f(){ f({1,2}); }") == "success"
    def test_expr_init_nested(self): assert self.check("void f(){ p = {{1}, 2}; }") == "success"
    def test_expr_func_call(self): assert self.check("void f(){ x = call(); }") == "success"

    # --- 6. CONTROL FLOW (20 Tests) ---
    def test_stmt_if(self): assert self.check("void f(){ if(x) y; }") == "success"
    def test_stmt_if_block(self): assert self.check("void f(){ if(x) { y; } }") == "success"
    def test_stmt_if_else(self): assert self.check("void f(){ if(x) y; else z; }") == "success"
    def test_stmt_while(self): assert self.check("void f(){ while(x) y; }") == "success"
    
    # FIXED: Replaced ';' bodies with '{}' since grammar forbids empty statements
    def test_stmt_for_full(self): assert self.check("void f(){ for(i=0;i<10;i++) {} }") == "success"
    def test_stmt_for_decl(self): assert self.check("void f(){ for(int i=0;i<10;i++) {} }") == "success"
    def test_stmt_for_empty(self): assert self.check("void f(){ for(;;) {} }") == "success"
    def test_stmt_for_missing(self): assert self.check("void f(){ for(;i<10;) {} }") == "success"
    
    def test_stmt_switch(self): assert self.check("void f(){ switch(x){} }") == "success"
    def test_stmt_switch_case(self): assert self.check("void f(){ switch(x){ case 1: break; } }") == "success"
    def test_stmt_switch_default(self): assert self.check("void f(){ switch(x){ default: break; } }") == "success"
    def test_stmt_switch_multi(self): assert self.check("void f(){ switch(x){ case 1: case 2: break; } }") == "success"
    def test_stmt_break(self): assert self.check("void f(){ while(1) break; }") == "success"
    def test_stmt_continue(self): assert self.check("void f(){ while(1) continue; }") == "success"
    def test_stmt_return(self): assert self.check("void f(){ return; }") == "success"
    def test_stmt_return_val(self): assert self.check("void f(){ return 1; }") == "success"
    def test_stmt_block_nested(self): assert self.check("void f(){ { { } } }") == "success"
    def test_stmt_expr(self): assert self.check("void f(){ 1+2; }") == "success"
    def test_stmt_empty_fail(self): assert self.check("void f(){ ; }") != "success"
    def test_stmt_loop_nest(self): assert self.check("void f(){ while(1) { if(x) break; } }") == "success"

    # --- 7. NEGATIVE CASES (10 Tests) ---
    def test_neg_no_semi(self): assert self.check("void f(){ x = 1 }") != "success"
    def test_neg_bad_if(self): assert self.check("void f(){ if x ) ; }") != "success"
    def test_neg_bad_while(self): assert self.check("void f(){ while(x ; }") != "success"
    def test_neg_bad_for(self): assert self.check("void f(){ for(x;y) ; }") != "success"
    def test_neg_bad_struct(self): assert self.check("struct { int x; };") != "success"
    def test_neg_bad_func(self): assert self.check("void f(int x,) {}") != "success"
    def test_neg_global_stmt(self): assert self.check("x = 1;") != "success"
    def test_neg_nested_func(self): assert self.check("void f(){ void g(){} }") != "success"
    def test_neg_switch_no_brace(self): assert self.check("void f(){ switch(x) case 1:; }") != "success"
    def test_neg_case_outside(self): assert self.check("void f(){ case 1: ; }") != "success"