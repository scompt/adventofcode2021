from typing import Any, TextIO, List, Dict

def read_lines(textio: TextIO, spec: Dict[str, type]) -> List[Dict[str, Any]]:
    output = []
    lines = textio.readlines()
    for line in lines:
        blah = dict()
        pieces = line.strip().split(' ')
        for index, (piece_name, piece_type) in enumerate(spec.items()):
            blah[piece_name] = piece_type(pieces[index])
        output.append(blah)
    return output

def lookahead(iterable):
    """Pass through all values from the given iterable, augmented by the
    information if there are more values to come after the current one
    (True), or if it is the last value (False).

    https://stackoverflow.com/a/1630350/111777
    """
    # Get an iterator and pull the first value.
    it = iter(iterable)
    last = next(it)
    # Run the iterator to exhaustion (starting from the second value).
    for val in it:
        # Report the *previous* value (more to come).
        yield last, True
        last = val
    # Report the last value.
    yield last, False
