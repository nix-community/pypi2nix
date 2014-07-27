import click


@click.command()
@click.argument('input', type=click.File('rb'))
def inout(input):
