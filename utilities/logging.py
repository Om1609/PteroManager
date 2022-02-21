from rich import print


def log(level, text):
    if level == 0:
        print(f"[bold red]FATAL:[/bold red] {text}")
    elif level == 1:
        print(f"[pink]Error:[/pink] {text}")
    elif level == 2:
        print(f"[yellow]Warning:[/yellow] {text}")
    elif level == 3:
        print(f"[blue]INFO:[/blue] {text}")
    elif level == 4:
        print(f"[green]Success:[/green] {text}")
