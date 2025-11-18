import typer
from src.llm.fix_suggester import apply_fix

def apply_fix(ctx: typer.Context, pipeline_run_id: int):
    fix = apply_fix(pipeline_run_id)
    typer.echo(f"Fix applied: {fix}")
