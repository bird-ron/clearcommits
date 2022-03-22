from argparse import ArgumentParser, Namespace
from subprocess import call, getoutput
from sys import argv
from typing import Final

DEFAULT_MESSAGE: Final[str] = "REDACTED"
DEFAULT_REMOTE: Final[str] = "origin"
DEFAULT_TEMP: Final[str] = "temp"
PAUSE_SHORT: Final[str] = "-p"
PAUSE_LONG: Final[str] = "--pause"


def get_args() -> tuple[str, str, bool, str, str]:
    """
    Tries to parse the arguments given to the program.
    If parsing is successful, the parsed values are returned.
        Note that pause is not returned since we still need to check for this flag if parsing fails.
        The optional flags have default values.
    Otherwise, the argument parser will display a usage message and try to exit.
    :return: A five-tuple containing the values (branch, message, quiet, remote, temp).
    """
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument("branch", help="branch to purge")
    parser.add_argument("-m", "--message", help=f"commit message (defaults to \"{DEFAULT_MESSAGE}\")")
    parser.add_argument(PAUSE_SHORT, PAUSE_LONG, help="pause before exiting", action="store_true")
    parser.add_argument("-q", "--quiet", help="produce no console output", action="store_true")
    parser.add_argument("-r", "--remote", help=f"name of remote repository (defaults to \"{DEFAULT_REMOTE}\")")
    parser.add_argument("-t", "--temp", help=f"temporary name of orphan branch (defaults to \"{DEFAULT_TEMP}\")")
    args: Namespace = parser.parse_args()
    branch: str = args.branch
    message: str = args.message if args.message else DEFAULT_MESSAGE
    quiet: bool = args.quiet if args.quiet else False
    remote: str = args.remote if args.remote else DEFAULT_REMOTE
    temp: str = args.temp if args.temp else DEFAULT_TEMP
    return branch, message, quiet, remote, temp


def system(com: str) -> int:
    """
    Same functionality as os.system, but using the subprocess library.
    :param com: Command to execute in the shell.
    :return: Return code.
    """
    return call(com, shell=True)


def purge_commits(branch: str, message: str, quiet: bool, remote: str, temp: str) -> None:
    """
    Uses git commands to purge local and remote commit history.
    :param branch: The branch to purge the history from.
    :param message: The message used to commit the orphan branch.
    :param quiet: Produces no console output if this is true.
    :param remote: The name of the remote repo.
    :param temp: The temporary name used to initialize the orphan branch.
    """
    coms: list[str] = [
                       f"git checkout --orphan {temp}",  # create orphan branch (no ancestors)
                       f"git commit -m \"{message}\"",  # commit existing files so our branch isn't empty
                       f"git branch -D {branch}",  # delete the branch we're purging
                       f"git branch -m {branch}",  # steal the name of the branch we're purging
                       f"git push -f {remote} {branch}"  # update remote
                      ]
    if quiet:
        for idx, com in enumerate(coms):
            coms[idx] = com + " -q"
    for com in coms:
        system(com)


def main() -> None:
    """
    Checks for errors, then purges commit history.
    """
    try:
        branch: str
        message: str
        quiet: bool
        remote: str
        temp: str
        branch, message, quiet, remote, temp = get_args()

        commit_comparison: str = getoutput(f"git rev-list --left-right --count {remote}/{branch}...{branch}")
        behind: int
        ahead: int
        try:
            behind, ahead = (int(no) for no in commit_comparison.split("\t"))
            if not behind and not ahead:
                purge_commits(branch, message, quiet, remote, temp)
            else:
                print(f"fatal: local branch {branch} behind by {behind} commits, ahead by {ahead} commits")
                print("branches must be synchronized before purging commit history")
        except ValueError:
            print("fatal: branch not found")
    except SystemExit:  # don't let argument parser exit because we might need to pause
        pass
    if PAUSE_SHORT in argv or PAUSE_LONG in argv:
        input("paused -- press enter to exit\n")


if __name__ == "__main__":
    main()
