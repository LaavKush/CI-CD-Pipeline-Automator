import typer
from src.llm.log_explainer import explain_log

def explain_error(ctx: typer.Context, pipeline_run_id: int):
    explanation = explain_log(pipeline_run_id)
    typer.echo(f"Error Explanation: {explanation}")
