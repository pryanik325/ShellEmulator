import shlex
from typing import List, Optional, Tuple


def parse_command(
    line: str,
) -> Tuple[Optional[str], List[str]]:
    tokens = list(shlex.split(line))

    command = tokens[0]
    args = tokens[1:]
    return command, args