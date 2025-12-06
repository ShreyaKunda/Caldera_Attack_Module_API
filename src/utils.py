from rich.console import Console

console = Console()

def log_info(msg):
    console.print(f"[bold cyan][INFO][/bold cyan] {msg}")

def log_success(msg):
    console.print(f"[bold green][SUCCESS][/bold green] {msg}")

def log_error(msg):
    console.print(f"[bold red][ERROR][/bold red] {msg}")
