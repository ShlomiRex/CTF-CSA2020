import time
def resolve_undecided_mappings(resolved_char , undecided_mapping):
    """
    Loop pairwise mappings that one of the chars is resolved_char
    Lets say:
        undecided_mappings =  [['i', 'b'], ['i', 'r']]
    Then we get:
        char 'g' is in secret word and char 'r' is not in secret word
    So we say 'g' is resolved and also 'r' is resolved (100% we know)
    That means that char 'i' is also not in secret word, because it has pairwise: ['i', 'r']
    Because we resolved 'i' we call the function again
    and it should return also ['i', 'b'] because it has 'i' in it
    So in total it should returns: 'r', 'i', 'b'
    """
    def check_all_pairs(char):
        other_chars = set()
        to_remove = []
        for x in undecided_mapping:
            if char == x[0]:
                other_chars.add(x[1])
                to_remove.append(x)
            elif char == x[1]:
                other_chars.add(x[0])
                to_remove.append(x)
        for x in to_remove:
            undecided_mapping.remove(x)
        return other_chars

    res = set(resolved_char)
    while True:
        changed = False
        for x in list(res):
            ret = check_all_pairs(x)
            if len(ret) > 0:
                res = res | ret
                changed = True
        if changed == False:
            break

    return res


mapping = [['i', 'b'], ['i', 'r'], ['a', 'r'], ['b', 'c'], ['c', 'g'], ['g', 'b'], ['g', 'x'], ['x', 'g'], ['j', 'y'], ['y', 'j'], ['k', 'x']]
print(resolve_undecided_mappings('r', mapping))
