rule figure:
    """
    Generates a figure given a figure script and optional dependencies.
    This is the workhorse of ``showyourwork``, which generates all the
    figures in the article. Users can subclass this rule or override it
    entirely to customize the build process.

    """
    message:
        "Generating figure `{output}`..."
    input:
        figure_script,
        figure_script_dependencies,
        "environment.yml",
    output:
        report("{figure}", category="Figure")
    wildcard_constraints:
        figure="src/figures/(.*?)\.{}".format("|".join(config["figexts"])),
    params:
        script_name=script_name,
        FIGURES=relpaths.figures,
        TEMP=relpaths.temp
    conda:
        posix(abspaths.user / "environment.yml")
    script:
        "../scripts/figure.py"
