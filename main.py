import typer
from pathlib import Path
from parser import fetch_tenders, save

app = typer.Typer(help="Mini-parser for B2B-Center tenders")

@app.command()
def run(
    max_rows: int = typer.Option(100, help="Сколько тендеров собрать"),
    output: Path = typer.Option("tenders.csv", help="Файл для сохранения"),
    fmt: str = typer.Option("csv", help="csv или sqlite")
):
    df = fetch_tenders(max_rows)
    save(df, output, fmt)
    typer.echo(f"Сохранено {len(df)} записей в {output}")

if __name__ == "__main__":
    app()