import re
args_pattern = re.compile(
    r"""
    ^
    (
        (--(?P<HELP>help).*)|
        ((?P<STATS>stats)\s)?
        ((?:-n|--name)\s(?P<STAT_NAME>.*?))|
        ((?P<DOWNLOAD>download)\s)?
        ((?:-n|--name)\s(?P<DOWNLOAD_NAME>.*?)\s)?
        ((?:-r|--range)\s(?P<RANGE>.*?))
    )
    $
""",
    re.VERBOSE,
)
class CLI:
    @staticmethod
    def parse(arg_line: str):
        args: dict[str, str] = {}
        if match_object := args_pattern.match(arg_line):
            args = {k: v for k, v in match_object.groupdict().items()
                    if v is not None}
        return args