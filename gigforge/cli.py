import click
from gigforge import utils

@click.group()
def cli():
    pass

@cli.command()
@click.option('--title', required=True)
@click.option('--hours', type=float, default=0.0)
@click.option('--rate', type=float, default=0.0)
@click.option('--fixed', type=float, default=None)
@click.option('--margin', type=float, default=0.2)
def gig(title, hours, rate, fixed, margin):
    price = utils.calc_price(hours=hours, rate=rate, fixed=fixed, margin=margin)
    outline = f"{title}\n\nPrice: ${price}\n\nBrief: I will deliver a high-quality {title}."
    click.echo(outline)

@cli.command()
@click.option('--client', required=True)
@click.option('--project', required=True)
@click.option('--author', default="Freelancer")
@click.option('--hours', type=float, default=0.0)
@click.option('--rate', type=float, default=0.0)
@click.option('--fixed', type=float, default=None)
@click.option('--out', default=None)
def proposal(client, project, author, hours, rate, fixed, out):
    price = utils.calc_price(hours=hours, rate=rate, fixed=fixed)
    ctx = utils.build_proposal_context({
        "client": client, "project": project, "author": author, "price": price
    })
    text = utils.render_template("proposal.md.j2", ctx)
    if out:
        with open(out,"w") as f: f.write(text); click.echo(f"Wrote proposal to {out}")
    else:
        click.echo(text)

@cli.command()
@click.option('--client', required=True)
@click.option('--project', default="Project")
@click.option('--items', multiple=True, help='List items as Description:Amount')
@click.option('--out', default="invoice.pdf")
def invoice(client, project, items, out):
    parsed=[]
    for it in items:
        if ":" in it:
            d,a = it.split(":",1); parsed.append((d.strip(), float(a)))
    pdf = utils.generate_invoice_pdf_bytes(parsed, client, project)
    with open(out, "wb") as f: f.write(pdf)
    click.echo(f"Wrote invoice to {out}")

@cli.command()
@click.option('--title', required=True)
@click.option('--subtitle', default="")
@click.option('--out', default="promo.png")
def promo(title, subtitle, out):
    data = utils.generate_promo_image(title, subtitle)
    with open(out,"wb") as f: f.write(data)
    click.echo(f"Wrote promo image to {out}")

if __name__=="__main__":
    cli()
if __name__ == "__main__":
    print("NightAnvil CLI ready")
