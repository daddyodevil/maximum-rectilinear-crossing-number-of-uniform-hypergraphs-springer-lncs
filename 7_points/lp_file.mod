var x1;
var x2;
maximize obj: x1 + x2;
s.t. c1: 69 * x1 + 59* x2 = 1;
s.t. c2: 13 * x1 + 125* x2 >= 1;
s.t. c3: 63 * x1 + 195* x2 >= 1;
s.t. c4: 143 * x1 + 217* x2 >= 1;
s.t. c5: 243 * x1 + 153* x2 >= 1;
s.t. c6: 229 * x1 + 80* x2 >= 1;
s.t. c7: 160 * x1 + 40* x2 >= 1;
solve;
end;