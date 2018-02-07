# regex_magic
will contain features of: negating regex, intersection between couple of regex expressions, and maybe more.

The usage will be: take your regex and negate (or other feature) it with this tool, that will not be the most efficient way to do it,
but you will get a "compiled" regex that you can work with.

# How negate works for regex
let a of Sigma.
And lets define the operator '-' for regex as the group of options (lhs) without rhs.

neg(a) = Sigma - a

neg(a|b) = Sigma - a - b

neg(ab) = ((a)neg(b) | (neg(a)b)

neg(a*) = (Sigma - a)+ #because epsilon is also in kleene clouse)


neg(a+) = (epsilon | (Sigma - a))

neg(x1x2..xn) = x1x2..neg(xn) | x1xn..neg(xn-1).. | neg(x1)x2.. | ..

// You can think about it as a production of 0|1's where 0 is neg and 1 is true, BUT without the whole expression will be 1's (because then it will be true)
