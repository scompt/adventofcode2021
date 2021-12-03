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