"""
Write the function eval_str so that eval_str('1 + 3 / 2 - 6 * 2') returns -9.5. Basically just evaluate the
string and return the float value. Multiplication and division group closer than add/sub. You can use
operatior.mul and its friends.
"""

import operator as op


def eval_str(exp_str):
    """
    Evaluate expression string.
    """
    # Assume characters are delimated by space
    # ....Otherwise break via regex??
    expression = exp_str.split(" ")

    # Init evaluation stack.
    stack = []

    # Iterate over remaining characters
    for i, e in enumerate(expression):
        # Values are even
        if i % 2 == 0:
            stack.append(e)
        # Operators are odd.
        else:
            # We can "close parentheses and evaluate when we hit a +/-
            if e in "+-":
                stack = _reduce_stack(stack)
            # Apply operator to reduced stack.
            stack.append(e)

    # Reduce any final form and return value.
    return _reduce_stack(stack)[0]


def _reduce_stack(stack):
    """
    Evaluate stack from right to left.

    # If necessary, use recursion to reduce right side and then eval.
    """
    if len(stack) == 1:
        return stack
    elif len(stack) == 3:
        return [_eval(*stack)]
    else:
        stack = stack[:-3] + _reduce_stack(stack[-3:])
        return _reduce_stack(stack)


def _eval(a, o, b):
    o = _get_operator_from_chr(o)
    return o(float(a), float(b))


def _get_operator_from_chr(c):
    if c == "+":
        return op.add
    elif c == "-":
        return op.sub
    elif c == "*":
        return op.mul
    elif c == "/":
        return op.truediv
    else:
        raise ValueError(f"Invalid operator character: {c}")


def test_eval_str_example():
    assert eval_str("1 + 3 / 2 - 6 * 2") == -9.5


def test_eval_str_plus():
    assert eval_str("1 + 2 + 3") == 6


def test_eval_str_mult():
    assert eval_str("1 * 2 * 3") == 6


def test_eval_str_neg():
    assert eval_str("-1 - 2") == -3
