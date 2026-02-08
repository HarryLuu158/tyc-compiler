"""
Parser test cases for TyC compiler (100% Complex/Advanced/Stress)
100 test cases covering:
- Full Algorithmic Implementations (Sorting, Math, Recursion)
- Deeply Nested Control Flow ("Spaghetti Code" simulations)
- Complex Expressions (Massive equations, Logic bombs)
- Advanced Struct Usage (Recursive types, deep chains)
- Syntax Stress & Edge Cases
"""

import pytest
from tests.utils import Parser

class TestParser:

    def check(self, input_str):
        """Helper to instantiate Parser and call .parse()"""
        return Parser(input_str).parse()

    # ==============================================================================
    # GROUP 1: COMPLEX ALGORITHMS & FULL PROGRAMS (20 Tests)
    # ==============================================================================

    def test_algo_quicksort_partition(self):
        code = """
        int partition(int low, int high) {
            int pivot = get(high); 
            int i = (low - 1);
            for (int j = low; j <= high - 1; j++) {
                if (get(j) < pivot) {
                    i++;
                    swap(i, j);
                }
            }
            swap(i + 1, high);
            return (i + 1);
        }
        """
        assert self.check(code) == "success"

    def test_algo_binary_search_iterative(self):
        code = """
        int binarySearch(int l, int r, int x) {
            while (l <= r) {
                int m = l + (r - l) / 2;
                if (get(m) == x) return m;
                if (get(m) < x) l = m + 1;
                else r = m - 1;
            }
            return -1;
        }
        """
        assert self.check(code) == "success"

    def test_algo_matrix_multiplication_simulated(self):
        code = """
        void multiply(int r1, int c1, int r2, int c2) {
            for (int i = 0; i < r1; ++i) {
                for (int j = 0; j < c2; ++j) {
                    for (int k = 0; k < c1; ++k) {
                        int val = get(i, j) + get(i, k) * get(k, j);
                        set(i, j, val);
                    }
                }
            }
        }
        """
        assert self.check(code) == "success"

    def test_algo_merge_sort_logic(self):
        code = """
        void merge(int l, int m, int r) {
            int n1 = m - l + 1;
            int n2 = r - m;
            while (i < n1 && j < n2) {
                if (getL(i) <= getR(j)) { setArr(k, getL(i)); i++; }
                else { setArr(k, getR(j)); j++; }
                k++;
            }
        }
        """
        assert self.check(code) == "success"

    def test_algo_dijkstra_init(self):
        code = """
        void dijkstra(int src) {
            for (int i = 0; i < V; i++) {
                dist.set(i, INT_MAX);
                sptSet.set(i, false);
            }
            dist.set(src, 0);
            for (int count = 0; count < V - 1; count++) {
                int u = minDistance(dist, sptSet);
                sptSet.set(u, true);
            }
        }
        """
        assert self.check(code) == "success"

    def test_algo_dfs_recursive(self):
        code = """
        void DFSUtil(int v, bool visited) {
            visited.set(v, true);
            print(v);
            for (int i = adj.begin(v); i != adj.end(v); ++i) {
                if (!visited.get(i)) DFSUtil(i, visited);
            }
        }
        """
        assert self.check(code) == "success"

    def test_algo_fibonacci_memoization(self):
        code = """
        int fib(int n) {
            if (memo.get(n) != -1) return memo.get(n);
            if (n <= 1) return n;
            int res = fib(n-1) + fib(n-2);
            memo.set(n, res);
            return res;
        }
        """
        assert self.check(code) == "success"

    def test_algo_knapsack_dp(self):
        code = """
        int knapSack(int W, int n) {
            if (n == 0 || W == 0) return 0;
            if (wt.get(n-1) > W) return knapSack(W, n-1);
            else return max( val.get(n-1) + knapSack(W-wt.get(n-1), n-1), knapSack(W, n-1) );
        }
        """
        assert self.check(code) == "success"

    def test_algo_lcs_recursive(self):
        code = """
        int lcs( int m, int n ) {
            if (m == 0 || n == 0) return 0;
            if (X.get(m-1) == Y.get(n-1)) return 1 + lcs(m-1, n-1);
            else return max(lcs(m, n-1), lcs(m-1, n));
        }
        """
        assert self.check(code) == "success"

    def test_algo_tower_of_hanoi(self):
        code = """
        void towerOfHanoi(int n, char from_rod, char to_rod, char aux_rod) {
            if (n == 1) {
                printMove(from_rod, to_rod);
                return;
            }
            towerOfHanoi(n - 1, from_rod, aux_rod, to_rod);
            printMove(from_rod, to_rod);
            towerOfHanoi(n - 1, aux_rod, to_rod, from_rod);
        }
        """
        assert self.check(code) == "success"

    def test_algo_floyd_warshall(self):
        code = """
        void floydWarshall() {
            for (k = 0; k < V; k++) {
                for (i = 0; i < V; i++) {
                    for (j = 0; j < V; j++) {
                        if (dist.get(i,k) + dist.get(k,j) < dist.get(i,j))
                            dist.set(i, j, dist.get(i,k) + dist.get(k,j));
                    }
                }
            }
        }
        """
        assert self.check(code) == "success"

    def test_algo_kmp_search(self):
        code = """
        void KMPSearch(string pat, string txt) {
            int M = pat.length();
            int N = txt.length();
            int i = 0; int j = 0;
            while ((N - i) >= (M - j)) {
                if (pat.charAt(j) == txt.charAt(i)) { j++; i++; }
                if (j == M) {
                    print(i - j);
                    j = lps.get(j - 1);
                } else if (i < N && pat.charAt(j) != txt.charAt(i)) {
                    if (j != 0) j = lps.get(j - 1);
                    else i = i + 1;
                }
            }
        }
        """
        assert self.check(code) == "success"

    def test_algo_convex_hull_check(self):
        code = """
        int orientation(Point p, Point q, Point r) {
            int val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y);
            if (val == 0) return 0;
            if (val > 0) return 1; else return 2;
        }
        """
        assert self.check(code) == "success"

    def test_algo_newton_sqrt(self):
        code = """
        float sqrt(float n) {
            float x = n;
            float root;
            while (1) {
                root = 0.5 * (x + (n / x));
                if (abs(root - x) < 0.0001) break;
                x = root;
            }
            return root;
        }
        """
        assert self.check(code) == "success"

    def test_algo_sieve_of_eratosthenes(self):
        code = """
        void sieve(int n) {
            for (int p = 2; p * p <= n; p++) {
                if (prime.get(p) == true) {
                    for (int i = p * p; i <= n; i = i + p)
                        prime.set(i, false);
                }
            }
        }
        """
        assert self.check(code) == "success"

    def test_algo_bst_insert(self):
        code = """
        Node insert(Node node, int key) {
            if (node == null) return newNode(key);
            if (key < node.key) node.left = insert(node.left, key);
            else if (key > node.key) node.right = insert(node.right, key);
            return node;
        }
        """
        assert self.check(code) == "success"

    def test_algo_avl_rotate_right(self):
        code = """
        Node rightRotate(Node y) {
            Node x = y.left;
            Node T2 = x.right;
            x.right = y;
            y.left = T2;
            y.height = max(height(y.left), height(y.right)) + 1;
            x.height = max(height(x.left), height(x.right)) + 1;
            return x;
        }
        """
        assert self.check(code) == "success"

    def test_algo_graph_bfs(self):
        code = """
        void BFS(int s) {
            visited.set(s, true);
            queue.push(s);
            while(!queue.empty()) {
                s = queue.front();
                queue.pop();
                for(int i = 0; i < adj.size(s); ++i) {
                    int n = adj.get(s, i);
                    if(!visited.get(n)) {
                        visited.set(n, true);
                        queue.push(n);
                    }
                }
            }
        }
        """
        assert self.check(code) == "success"

    def test_algo_linked_list_reverse(self):
        code = """
        void reverse() {
            Node current = head;
            Node prev = null;
            Node next = null;
            while (current != null) {
                next = current.next;
                current.next = prev;
                prev = current;
                current = next;
            }
            head = prev;
        }
        """
        assert self.check(code) == "success"

    def test_algo_stack_using_queues(self):
        code = """
        void push(int x) {
            q2.push(x);
            while (!q1.empty()) {
                q2.push(q1.front());
                q1.pop();
            }
            Queue q = q1;
            q1 = q2;
            q2 = q;
        }
        """
        assert self.check(code) == "success"

    # ==============================================================================
    # GROUP 2: DEEP NESTING & CONTROL FLOW COMPLEXITY (20 Tests)
    # ==============================================================================

    def test_nest_ladder_hell(self):
        code = """
        void f() {
            for(int i=0; i<N; i++) {
                while(check(i)) {
                    if(i%2==0) { 
                        switch(i) {
                            case 0: break; 
                            default: continue; 
                        }
                    } else {
                        return;
                    }
                }
            }
        }
        """
        assert self.check(code) == "success"

    def test_nest_switch_ception(self):
        code = """
        void f() {
            while(1) {
                if(valid) {
                    switch(type) {
                        case 1: 
                            switch(subtype) {
                                case A: processA(); break;
                                case B: processB(); break;
                            }
                            break;
                    }
                }
            }
        }
        """
        assert self.check(code) == "success"

    def test_nest_variable_shadowing_deep(self):
        code = """
        void f() {
            int x = 1;
            {
                int x = 2;
                {
                    string x = "shadow";
                    if(true) {
                        float x = 3.14;
                    }
                }
            }
            x = 5;
        }
        """
        assert self.check(code) == "success"

    def test_nest_spaghetti_jumps(self):
        code = """
        int f() {
            for(;;) {
                if(cond1) continue;
                if(cond2) {
                    while(1) {
                        if(cond3) break;
                        return 1;
                    }
                }
                break;
            }
            return 0;
        }
        """
        assert self.check(code) == "success"

    def test_nest_dangling_else_chain(self):
        code = """
        void f() {
            if(a) 
                if(b) 
                    if(c) x=1;
                    else x=2;
                else 
                    if(d) x=3;
            else x=4;
        }
        """
        assert self.check(code) == "success"

    def test_nest_mixed_blocks_params(self):
        code = """
        void f(int x) {
            {
                int y = x;
                {
                    int x = y; 
                }
            }
        }
        """
        assert self.check(code) == "success"

    def test_nest_recursion_in_loop(self):
        code = """
        void f(int n) {
            while(n > 0) {
                f(n-1);
                n--;
            }
        }
        """
        assert self.check(code) == "success"

    def test_nest_infinite_for_complex_init(self):
        code = "void f() { for(int i=0; i<100; i++) { if(check(i)) break; } }"
        assert self.check(code) == "success"

    def test_nest_empty_bodies_chain(self):
        code = "void f() { while(1){} for(;;){} if(1){} else{} }"
        assert self.check(code) == "success"

    def test_nest_complex_condition(self):
        code = "void f() { if( (a || b) && (c || (d && e)) ) { x=1; } }"
        assert self.check(code) == "success"

    def test_nest_return_in_switch(self):
        code = "int f() { switch(x) { case 1: return 1; case 2: { return 2; } default: return 0; } }"
        assert self.check(code) == "success"

    def test_nest_break_in_if_in_loop(self):
        code = "void f() { while(1) { if(done) { break; } else { continue; } } }"
        assert self.check(code) == "success"

    def test_nest_deep_struct_init(self):
        code = "void f() { A a = { {1,2}, {3, {4,5}} }; }"
        assert self.check(code) == "success"

    def test_nest_func_ptr_sim_call(self):
        code = "void f() { handlers.get(event)(arg1, arg2); }"
        assert self.check(code) == "success"

    def test_nest_ternary_sim_nested(self):
        code = "void f() { if(c1) { if(c2) x=1; else x=2; } else x=3; }"
        assert self.check(code) == "success"

    def test_nest_multi_level_access(self):
        code = "void f() { x = root.child.sibling.child.val; }"
        assert self.check(code) == "success"

    def test_nest_crazy_parens(self):
        code = "void f() { x = (( (a) + (b) ) * (c)); }"
        assert self.check(code) == "success"

    def test_nest_switch_empty_case(self):
        code = "void f() { switch(x) { case 1: case 2: case 3: doSomething(); break; } }"
        assert self.check(code) == "success"

    def test_nest_func_arg_is_func_call(self):
        code = "void f() { g( a(), b( c() ) ); }"
        assert self.check(code) == "success"

    def test_nest_block_scope_lifetime(self):
        code = "void f() { { int x=1; } { int x=2; } }"
        assert self.check(code) == "success"

    # ==============================================================================
    # GROUP 3: COMPLEX EXPRESSIONS (20 Tests)
    # ==============================================================================

    def test_expr_math_monster(self):
        code = "void f() { x = a * b + c / d - e % f + (g * h) - (i / j) + k * (l - m); }"
        assert self.check(code) == "success"

    def test_expr_logic_bomb(self):
        code = "void f() { bool b = (x > 0 && y < 10) || (z == 5 && !flag) || (a != b && c >= d); }"
        assert self.check(code) == "success"

    def test_expr_function_call_chain_deep(self):
        code = "void f() { x = obj.getManager().getTeam().getLeader().getName(); }"
        assert self.check(code) == "success"

    def test_expr_assignment_chaining(self):
        code = "void f() { a = b = c = d = e = 0; }"
        assert self.check(code) == "success"

    def test_expr_mixed_unary_binary(self):
        code = "void f() { x = -a * !b + ++c - d--; }"
        assert self.check(code) == "success"

    def test_expr_struct_literal_complex(self):
        code = "void f() { Point p = { 1 + 2, (x * y) / z }; }"
        assert self.check(code) == "success"

    def test_expr_func_args_math(self):
        code = "void f() { Math.max( (a+b)*c, pow(x, 2) + pow(y, 2) ); }"
        assert self.check(code) == "success"

    def test_expr_associativity_check(self):
        code = "void f() { x = a / b / c * d % e; }"
        assert self.check(code) == "success"

    def test_expr_inc_dec_mess(self):
        code = "void f() { int x = ++i + i++ + --j + j--; }"
        assert self.check(code) == "success"

    def test_expr_logic_short_circuit_sim(self):
        code = "void f() { if( ptr != null && ptr.val > 0 ) {} }"
        assert self.check(code) == "success"

    def test_expr_bitwise_sim_logic(self):
        code = "void f() { x = a && b || c && d || e; }"
        assert self.check(code) == "success"

    def test_expr_parens_excessive(self):
        code = "void f() { x = ( ( ( (a) ) ) ); }"
        assert self.check(code) == "success"

    def test_expr_float_scientific_math(self):
        code = "void f() { val = 1.23e-4 * 4.56E+2 + .001; }"
        assert self.check(code) == "success"

    def test_expr_string_concat_sim(self):
        code = "void f() { s = \"Hello\" + \" \" + \"World\"; }"
        assert self.check(code) == "success"

    def test_expr_member_array_access_sim(self):
        code = "void f() { val = arr.get(i).field; }"
        assert self.check(code) == "success"

    def test_expr_call_in_condition(self):
        code = "void f() { if( isValid(x) && hasPermission(user) ) {} }"
        assert self.check(code) == "success"

    def test_expr_deep_nested_init(self):
        code = "void f() { Matrix m = { {1,0}, {0,1} }; }"
        assert self.check(code) == "success"

    def test_expr_comment_interleaved(self):
        code = "void f() { x = 1 /* one */ + 2 /* two */ ; }"
        assert self.check(code) == "success"

    def test_expr_cast_sim(self):
        # Using toFloat because 'float' is a keyword and parser would fail otherwise
        assert self.check("void f(){ x = toFloat(toInt(y)); }") == "success"

    def test_expr_compare_calls(self):
        code = "void f() { if( getX() == getY() ) {} }"
        assert self.check(code) == "success"

    # ==============================================================================
    # GROUP 4: ADVANCED STRUCT & TYPE USAGE (20 Tests)
    # ==============================================================================

    def test_struct_complex_mutual_recursion(self):
        # Mutual recursion: Node -> Edge -> Node
        # Parser should accept 'Edge' as a type even if defined later (syntactically)
        code = """
        struct Node { 
            int id; 
            float value; 
            Edge outgoing; 
            Edge incoming; 
        }; 
        struct Edge { 
            Node src; 
            Node dest; 
            float weight; 
            int flags;
        };
        """
        assert self.check(code) == "success"

    def test_struct_deep_nested_hierarchy(self):
        # 4-level deep structure hierarchy
        code = """
        struct Geo { float lat; float lon; };
        struct City { string name; Geo location; int population; };
        struct Address { int streetNum; string streetName; City city; };
        struct User { int id; string username; Address billingAddr; Address shippingAddr; };
        """
        assert self.check(code) == "success"

    def test_struct_deep_access_logic(self):
        # Accessing deeply nested members in complex expressions
        code = """
        void process(User u) {
            if (u.billingAddr.city.location.lat > 0.0 && u.shippingAddr.city.population > 1000000) {
                print(u.billingAddr.streetName);
            }
            float dist = sqrt( pow(u.billingAddr.city.location.lat, 2) + pow(u.billingAddr.city.location.lon, 2) );
        }
        """
        assert self.check(code) == "success"

    def test_struct_factory_pattern(self):
        # Function returning a complex struct initialized with params
        code = """
        struct Rect { float x; float y; float w; float h; };
        Rect createRect(float cx, float cy, float size) {
            float half = size / 2.0;
            Rect r = { cx - half, cy - half, size, size };
            return r;
        }
        """
        assert self.check(code) == "success"

    def test_struct_param_manipulation(self):
        # Passing structs, modifying local copies, and accessing members
        code = """
        void updatePhysics(Body b, float dt) {
            b.pos.x = b.pos.x + b.vel.x * dt;
            b.pos.y = b.pos.y + b.vel.y * dt;
            b.vel.x = b.vel.x * 0.99; // Friction
            b.acc.x = 0.0;
        }
        """
        assert self.check(code) == "success"

    def test_struct_nested_init_heavy(self):
        # 3-level nested initialization expression
        code = """
        void init() {
            // Polygon -> Vertices -> Coordinates
            Triangle t = { 
                {0.0, 0.0, 1.0}, 
                {10.0, 0.0, 1.0}, 
                {5.0, 10.0, 1.0} 
            };
            Mesh m = { t, {1.0, 0.0, 0.0} }; // Triangle + Color
        }
        """
        assert self.check(code) == "success"

    def test_struct_method_chaining_sim(self):
        # Simulating method chaining: obj.getComponent().update().value
        code = """
        void f() { 
            float val = entity.getTransform().getPosition().x; 
            game.getPlayer(1).inventory.getItem(0).use();
        }
        """
        assert self.check(code) == "success"

    def test_struct_array_sim_access(self):
        # Accessing "arrays" via function calls inside structs
        code = """
        void f() {
            int val = matrix.getRow(i).getCol(j).val;
            list.get(0).next.get(1).prev.val = 100;
        }
        """
        assert self.check(code) == "success"

    def test_struct_mixed_type_fields(self):
        # Struct with all supported types including other structs
        code = """
        struct Record {
            int id;
            float score;
            string label;
            Record next;
            Record prev;
            Metadata meta;
        };
        """
        assert self.check(code) == "success"

    def test_struct_decl_inside_block_fail(self):
        # Struct definitions are only allowed at global scope (Syntax Error check)
        code = """
        void f() {
            if (true) {
                struct Local { int x; }; // Should fail
            }
        }
        """
        assert self.check(code) != "success"

    def test_struct_empty_definitions(self):
        # Empty structs are valid syntactically
        code = """
        struct Signal {}; 
        struct Mutex {};
        void wait(Mutex m, Signal s) {}
        """
        assert self.check(code) == "success"

    def test_struct_variable_shadowing_types(self):
        # Stress test: Variable name same as Struct type name
        code = """
        struct Vector { int x; };
        void f() {
            Vector Vector; // Variable 'Vector' of type 'Vector'
            Vector.x = 1;
            int x = Vector.x;
        }
        """
        assert self.check(code) == "success"

    def test_struct_case_sensitivity_strict(self):
        # 'Point' and 'POINT' are different types
        code = """
        struct Point { int x; };
        struct POINT { float x; };
        void f() {
            Point p1;
            POINT p2;
            p1.x = 1;
            p2.x = 1.5;
        }
        """
        assert self.check(code) == "success"

    def test_struct_keyword_as_field_name_fail(self):
        # Using a keyword as a field name
        code = "struct A { int while; float if; };"
        assert self.check(code) != "success"

    def test_struct_field_missing_semicolon_fail(self):
        # Missing semicolon inside struct definition
        code = """
        struct A { 
            int x
            int y; 
        };
        """
        assert self.check(code) != "success"

    def test_struct_malformed_declaration_fail(self):
        # Missing name or braces
        code = "struct { int x; };" # Anonymous struct not allowed
        assert self.check(code) != "success"

    def test_struct_init_expr_with_vars(self):
        # Initializing struct with variables and math expressions
        code = """
        void setup(int w, int h) {
            int area = w * h;
            Box b = { 0, 0, w, h, area + 10 };
            Config c = { b, "main_window" };
        }
        """
        assert self.check(code) == "success"

    def test_struct_assignment_copy(self):
        # Assigning structs to one another
        code = """
        void swap(Point a, Point b) {
            Point temp = a;
            a = b;
            b = temp;
            temp.x = 0; // Should affect only temp
        }
        """
        assert self.check(code) == "success"

    def test_struct_member_as_function_arg(self):
        # Passing member fields directly to functions
        code = """
        void draw() {
            line(p1.x, p1.y, p2.x, p2.y);
            color(style.fg.r, style.fg.g, style.fg.b);
        }
        """
        assert self.check(code) == "success"

    def test_struct_nested_if_access(self):
        # Complex access inside nested if statement
        code = """
        void f() {
            if (node.next != null) {
                if (node.next.val > 0) {
                    node.next.next.val = node.val * 2;
                }
            }
        }
        """
        assert self.check(code) == "success"

    # ==============================================================================
    # GROUP 5: SYNTAX STRESS & ERROR RECOVERY (20 Tests)
    # ==============================================================================

    def test_stress_whitespace_hell(self):
        code = "\n  void  \t  f  (  \n  int  \t  x  )  \n  {  \n  x  =  1  ;  \n  }  "
        assert self.check(code) == "success"

    def test_stress_comment_labyrinth(self):
        code = "/*h*/void/*e*/f/*l*/(/*l*/){/*o*/x/*w*/=/*o*/1/*r*/;/*l*/}//d"
        assert self.check(code) == "success"

    def test_stress_max_nesting_braces(self):
        code = "void f() { {{{{{{{{{{{{{{{{{}}}}}}}}}}}}}}}}} }"
        assert self.check(code) == "success"

    def test_stress_long_statement(self):
        code = "void f() { x = 1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1; }"
        assert self.check(code) == "success"

    def test_stress_many_globals(self):
        code = "int a; int b; int c; int d; void f(){}"
        assert self.check(code) == "success"

    def test_err_missing_func_name(self):
        code = "void (){}"
        assert self.check(code) != "success"

    def test_err_missing_paren_if(self):
        code = "void f() { if x==1 {} }"
        assert self.check(code) != "success"

    def test_err_missing_semi_stmt(self):
        code = "void f() { x=1 y=2; }"
        assert self.check(code) != "success"

    def test_err_struct_syntax_bad_parens(self):
        code = "struct A ( int x; );"
        assert self.check(code) != "success"

    def test_err_func_in_struct(self):
        code = "struct A { void f() {} };"
        assert self.check(code) != "success"

    def test_err_stmt_global_scope(self):
        code = "x = 1; void f(){}"
        assert self.check(code) != "success"

    def test_err_trailing_comma_struct(self):
        code = "struct A { int x,; };"
        assert self.check(code) != "success"

    def test_err_double_type_decl(self):
        code = "void f() { int int x; }"
        assert self.check(code) != "success"

    def test_err_keyword_as_func_name(self):
        code = "void while() {}"
        assert self.check(code) != "success"

    def test_err_unclosed_comment_eof(self):
        code = "/* "
        assert self.check(code) != "success"

    def test_err_bad_escape_in_string(self):
        code = "void f() { s = \"\\q\"; }"
        assert self.check(code) != "success"

    def test_err_float_malformed(self):
        code = "void f() { f = 1.2.3; }"
        assert self.check(code) != "success"

    def test_err_operator_clash(self):
        code = "void f() { x = 1 + * 2; }"
        assert self.check(code) != "success"

    def test_err_empty_struct_decl_malformed(self):
        code = "struct {};"
        assert self.check(code) != "success"

    def test_err_var_decl_assign_operator(self):
        code = "void f() { int x += 1; }" 
        assert self.check(code) != "success"