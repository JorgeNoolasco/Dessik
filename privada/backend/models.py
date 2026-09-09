"""Sem ORM: as tabelas estão em database/schema.sql e usamos dicionários."""

def serialize_product(product):
    # Decimal vira texto no JSON para preservar os centavos.
    product["preco"] = str(product["preco"])
    return product
