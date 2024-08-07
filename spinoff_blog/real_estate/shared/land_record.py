from typing import List, Dict, Any
from dataclasses import dataclass
from datetime import datetime
from spinoff_blog.shared.helpers import format_currency


@dataclass
class Geometry:
    type: str
    coordinates: List[List[List[List[float]]]]


@dataclass
class SaleRecord:
    amount: float
    date: str
    house_number: str = ""
    road: str = ""
    land_area: float = 0.0


@dataclass
class Zoning:
    r_code: str
    scheme_name: str
    scheme_number: str
    geometry: Dict[str, Any]


class LandRecord:
    def __init__(self, data: Dict[str, Any]):
        self.geometry = Geometry(**data["geometry"])
        self.other_land_sale_records = [
            SaleRecord(**record) for record in data["other_land_sale_records"]
        ]
        self.land_sale_records = [
            SaleRecord(**record) for record in data["land_sale_records"]
        ]
        self.house_number = data["house_number"]
        self.road = data["road"]
        self.city = data["city"]
        self.state = data["state"]
        self.land_area = data["land_area"]
        self.land_type = data["land_type"]
        self.zoning = [Zoning(**zone) for zone in data["zoning"]]

    def formatted_address(self) -> str:
        return f"{self.house_number} {self.road}".title()

    def cost_per_m2(self) -> float:
        if not self.land_sale_records:
            return 0.0

        most_recent_sale = max(
            self.land_sale_records, key=lambda x: datetime.strptime(x.date, "%Y-%m-%d")
        )
        return most_recent_sale.amount / self.land_area if self.land_area else 0.0

    def formatted_cost_per_m2(self) -> str:
        return format_currency(self.cost_per_m2())


# Example usage:
# Assuming you have your JSON data as a dictionary named 'json_data'
# land_record = LandRecord(json_data)
# print(f"Cost per m2: ${land_record.cost_per_m2():.2f}")
