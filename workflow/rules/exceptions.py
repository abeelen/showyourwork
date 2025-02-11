"""
Defines a custom exception for worfklow errors that
tries to print informative error messages at the very
end of the build log.

"""
import os
from pathlib import Path


TEMPLATE = """
{hline}

\033[1;30m{title}\033[0m

{hline}

\033[1;30mError:\033[0m {brief}
\033[1;30mRule:\033[0m {rule_name}
\033[1;30mScript:\033[0m {script}

\033[1;30mContext:\033[0m {context}

\033[1;30mDetailed error message:\033[0m 

{message}
{hline}
"""


class ShowyourworkException(Exception):
    """
    Custom exception that stores error messages
    in a temporary file to be displayed at the
    end of the build process.

    """

    def __init__(
        self,
        message,
        exception_file=None,
        script=None,
        rule_name=None,
        context=None,
        delayed=True,
        brief="An error occurred while executing your workflow.",
        *args,
        **kwargs,
    ):

        # We only need to provide `exception_file` if we're not
        # inside the main Snakemake workflow run
        if exception_file is None:
            try:
                exception_file = files.exception
            except:
                exception_file = Path(".showyourwork/exception.log")

        # Format the info
        if script is None:
            script = "N/A"
        else:
            script = f"`showyourwork/workflow/scripts/{script}`"
        if rule_name is None:
            rule_name = "N/A"
        else:
            rule_name = f"{rule_name} in `showyourwork/workflow/rules/{rule_name}.smk`"
        if context is None:
            context = "N/A"
        width = os.get_terminal_size().columns
        hline = "*" * width
        title = "SHOWYOURWORK ERROR"
        pad = " " * max(0, (width - len(title)) // 2 - 2)
        title = f"{pad}{title}{pad}"

        if delayed:

            # Store the message in a temp file (read in the `onerror:` section
            # of the `Snakefile`, to be printed at the end of the log).
            with open(exception_file, "w") as f:
                print(
                    TEMPLATE.format(
                        hline=hline,
                        title=title,
                        script=script,
                        rule_name=rule_name,
                        brief=brief,
                        context=context,
                        message=message,
                    ),
                    file=f,
                )

        else:

            # Print it to the terminal right away
            print(
                TEMPLATE.format(
                    hline=hline,
                    title=title,
                    script=script,
                    rule_name=rule_name,
                    brief=brief,
                    context=context,
                    message=message,
                )
            )

        # Raise the exception as usual
        super().__init__("\n\n" + message, *args, **kwargs)

    @staticmethod
    def print(exception_file=None):

        # We only need to provide `exception_file` if we're not
        # inside the main Snakemake workflow run
        if exception_file is None:
            try:
                exception_file = files.exception
            except:
                exception_file = Path(".showyourwork/exception.log")

        # Print any existing exceptions
        if exception_file.exists():
            with open(exception_file, "r") as f:
                message = f.read()
            print(message)