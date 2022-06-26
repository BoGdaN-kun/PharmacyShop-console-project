from dataclasses import dataclass


@dataclass
class DrugsNoSales:
    drug_name: str
    number_of_sales: int
