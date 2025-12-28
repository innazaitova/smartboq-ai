"""
Cost Estimator - Applies unit rates and calculates project costs
"""

from typing import List, Dict, Any
import json
from datetime import datetime


class CostEstimator:
    """Estimate costs by applying unit rates to quantities"""
    
    def __init__(self):
        self.rates_database = self._initialize_rates_database()
        self.regional_factors = self._initialize_regional_factors()
        self.inflation_factors = self._load_inflation_factors()
    
    def estimate_costs(
        self,
        quantities: List[Dict],
        region: str = "pakistan",
        currency: str = "PKR",
        project_type: str = "residential"
    ) -> List[Dict[str, Any]]:
        """
        Calculate costs for all quantity items
        
        Args:
            quantities: List of quantity items
            region: Geographic region
            currency: Currency code (PKR, USD, GBP, EUR, etc.)
            project_type: Type of project (residential, commercial, industrial)
        
        Returns:
            List of cost items with unit rates and totals
        """
        cost_items = []
        
        for qty_item in quantities:
            material = qty_item.get('material', 'Unknown')
            unit = qty_item.get('unit', 'item')
            quantity = qty_item.get('quantity', 0)
            
            # Get base unit rate
            base_rate = self._get_unit_rate(material, unit, region, currency)
            
            # Apply factors
            regional_factor = self.regional_factors.get(region, {}).get('factor', 1.0)
            project_factor = self._get_project_type_factor(project_type)
            inflation_factor = self.inflation_factors.get(currency, 1.0)
            
            # Calculate final rate
            unit_rate = base_rate * regional_factor * project_factor * inflation_factor
            total_cost = quantity * unit_rate
            
            cost_item = {
                "item_description": qty_item.get('item_description', 'Unknown item'),
                "element_type": qty_item.get('element_type', 'unknown'),
                "material": material,
                "unit": unit,
                "quantity": round(quantity, 3),
                "unit_rate": round(unit_rate, 2),
                "total_cost": round(total_cost, 2),
                "currency": currency,
                "base_rate": round(base_rate, 2),
                "factors": {
                    "regional": regional_factor,
                    "project_type": project_factor,
                    "inflation": inflation_factor
                },
                "element_reference": qty_item.get('element_reference', 'N/A')
            }
            
            cost_items.append(cost_item)
        
        return cost_items
    
    def _initialize_rates_database(self) -> Dict:
        """Initialize unit rates for different materials and regions"""
        return {
            "pakistan": {
                "PKR": {
                    "Concrete": {"m³": 15000, "source": "Market avg 2025"},
                    "Reinforcement Steel": {"kg": 280, "source": "Market avg 2025"},
                    "Formwork": {"m²": 450, "source": "Market avg 2025"},
                    "Bricks": {"nos": 18, "source": "Market avg 2025"},
                    "Mortar": {"m³": 8000, "source": "Market avg 2025"},
                    "Door panel": {"m²": 12000, "source": "Market avg 2025"},
                    "Window frame & glass": {"m²": 8000, "source": "Market avg 2025"},
                    "Paint": {"m²": 120, "source": "Market avg 2025"},
                    "Plaster": {"m²": 180, "source": "Market avg 2025"},
                    "Tiles": {"m²": 1200, "source": "Market avg 2025"}
                }
            },
            "uae": {
                "AED": {
                    "Concrete": {"m³": 850, "source": "Dubai Municipality 2025"},
                    "Reinforcement Steel": {"kg": 6.5, "source": "Dubai Municipality 2025"},
                    "Formwork": {"m²": 45, "source": "Dubai Municipality 2025"},
                    "Bricks": {"nos": 2.2, "source": "Dubai Municipality 2025"},
                    "Mortar": {"m³": 450, "source": "Dubai Municipality 2025"}
                }
            },
            "usa": {
                "USD": {
                    "Concrete": {"m³": 350, "source": "RSMeans 2025"},
                    "Reinforcement Steel": {"kg": 2.8, "source": "RSMeans 2025"},
                    "Formwork": {"m²": 55, "source": "RSMeans 2025"},
                    "Bricks": {"nos": 1.5, "source": "RSMeans 2025"},
                    "Mortar": {"m³": 280, "source": "RSMeans 2025"}
                }
            },
            "uk": {
                "GBP": {
                    "Concrete": {"m³": 180, "source": "Spon's 2025"},
                    "Reinforcement Steel": {"kg": 1.8, "source": "Spon's 2025"},
                    "Formwork": {"m²": 35, "source": "Spon's 2025"},
                    "Bricks": {"nos": 0.85, "source": "Spon's 2025"},
                    "Mortar": {"m³": 150, "source": "Spon's 2025"}
                }
            },
            "india": {
                "INR": {
                    "Concrete": {"m³": 8500, "source": "CPWD 2025"},
                    "Reinforcement Steel": {"kg": 75, "source": "CPWD 2025"},
                    "Formwork": {"m²": 280, "source": "CPWD 2025"},
                    "Bricks": {"nos": 12, "source": "CPWD 2025"},
                    "Mortar": {"m³": 4500, "source": "CPWD 2025"}
                }
            },
            "saudi_arabia": {
                "SAR": {
                    "Concrete": {"m³": 750, "source": "Market avg 2025"},
                    "Reinforcement Steel": {"kg": 5.5, "source": "Market avg 2025"},
                    "Formwork": {"m²": 40, "source": "Market avg 2025"},
                    "Bricks": {"nos": 2.0, "source": "Market avg 2025"},
                    "Mortar": {"m³": 420, "source": "Market avg 2025"}
                }
            }
        }
    
    def _initialize_regional_factors(self) -> Dict:
        """Regional cost adjustment factors"""
        return {
            "pakistan": {"factor": 1.0, "labor_ratio": 0.35},
            "karachi": {"factor": 1.05, "labor_ratio": 0.35},
            "lahore": {"factor": 1.02, "labor_ratio": 0.33},
            "islamabad": {"factor": 1.08, "labor_ratio": 0.37},
            "uae": {"factor": 1.0, "labor_ratio": 0.25},
            "dubai": {"factor": 1.15, "labor_ratio": 0.25},
            "abu_dhabi": {"factor": 1.10, "labor_ratio": 0.23},
            "usa": {"factor": 1.0, "labor_ratio": 0.45},
            "new_york": {"factor": 1.40, "labor_ratio": 0.50},
            "texas": {"factor": 0.85, "labor_ratio": 0.38},
            "california": {"factor": 1.35, "labor_ratio": 0.48},
            "uk": {"factor": 1.0, "labor_ratio": 0.42},
            "london": {"factor": 1.30, "labor_ratio": 0.45},
            "india": {"factor": 1.0, "labor_ratio": 0.40},
            "mumbai": {"factor": 1.25, "labor_ratio": 0.42},
            "delhi": {"factor": 1.20, "labor_ratio": 0.40},
            "saudi_arabia": {"factor": 1.0, "labor_ratio": 0.28},
            "riyadh": {"factor": 1.05, "labor_ratio": 0.28}
        }
    
    def _load_inflation_factors(self) -> Dict:
        """Current inflation adjustment factors (2025)"""
        return {
            "PKR": 1.08,  # 8% inflation in Pakistan
            "USD": 1.03,  # 3% inflation in US
            "GBP": 1.02,  # 2% inflation in UK
            "EUR": 1.02,  # 2% inflation in EU
            "AED": 1.025, # 2.5% inflation in UAE
            "SAR": 1.02,  # 2% inflation in Saudi
            "INR": 1.05   # 5% inflation in India
        }
    
    def _get_unit_rate(self, material: str, unit: str, region: str, currency: str) -> float:
        """Get unit rate for a material in specific region and currency"""
        # Get region rates
        region_rates = self.rates_database.get(region.lower().replace(' ', '_'), {})
        
        # Get currency rates
        currency_rates = region_rates.get(currency.upper(), {})
        
        # Get material rates
        material_rates = currency_rates.get(material, {})
        
        # Get unit rate
        rate = material_rates.get(unit, 0)
        
        # If not found, try to estimate from similar materials
        if rate == 0:
            rate = self._estimate_rate(material, unit, region, currency)
        
        return rate
    
    def _estimate_rate(self, material: str, unit: str, region: str, currency: str) -> float:
        """Estimate rate for unknown materials"""
        # Default rates per unit (in PKR for Pakistan)
        default_rates = {
            "m³": 12000,
            "m²": 800,
            "kg": 200,
            "nos": 50,
            "item": 1000
        }
        
        base_rate = default_rates.get(unit, 1000)
        
        # Convert to target currency if needed
        if currency != "PKR":
            conversion_rates = {
                "USD": 280,  # 1 USD = 280 PKR
                "GBP": 350,  # 1 GBP = 350 PKR
                "EUR": 305,  # 1 EUR = 305 PKR
                "AED": 76,   # 1 AED = 76 PKR
                "SAR": 75,   # 1 SAR = 75 PKR
                "INR": 3.3   # 1 INR = 3.3 PKR
            }
            rate_in_pkr = base_rate
            base_rate = rate_in_pkr / conversion_rates.get(currency, 1)
        
        return base_rate
    
    def _get_project_type_factor(self, project_type: str) -> float:
        """Get cost multiplier based on project type"""
        factors = {
            "residential": 1.0,
            "commercial": 1.15,
            "industrial": 1.25,
            "luxury_residential": 1.4,
            "infrastructure": 1.3,
            "institutional": 1.2
        }
        
        return factors.get(project_type.lower(), 1.0)
    
    def calculate_summary(self, cost_items: List[Dict]) -> Dict[str, Any]:
        """Calculate cost summary and breakdowns"""
        total_cost = sum(item['total_cost'] for item in cost_items)
        
        # Group by element type
        by_element = {}
        for item in cost_items:
            element_type = item['element_type']
            if element_type not in by_element:
                by_element[element_type] = 0
            by_element[element_type] += item['total_cost']
        
        # Group by material
        by_material = {}
        for item in cost_items:
            material = item['material']
            if material not in by_material:
                by_material[material] = 0
            by_material[material] += item['total_cost']
        
        # Calculate percentages
        element_percentages = {
            k: round((v / total_cost * 100), 2) 
            for k, v in by_element.items()
        }
        
        material_percentages = {
            k: round((v / total_cost * 100), 2) 
            for k, v in by_material.items()
        }
        
        return {
            "total_cost": round(total_cost, 2),
            "currency": cost_items[0]['currency'] if cost_items else 'PKR',
            "total_items": len(cost_items),
            "by_element_type": by_element,
            "by_material": by_material,
            "element_percentages": element_percentages,
            "material_percentages": material_percentages,
            "generated_at": datetime.now().isoformat()
        }
    
    def add_contingency(
        self,
        cost_items: List[Dict],
        contingency_percent: float = 10.0
    ) -> List[Dict]:
        """Add contingency to cost estimate"""
        total = sum(item['total_cost'] for item in cost_items)
        contingency_amount = total * (contingency_percent / 100)
        
        contingency_item = {
            "item_description": f"Contingency ({contingency_percent}%)",
            "element_type": "contingency",
            "material": "Allowance",
            "unit": "LS",  # Lump sum
            "quantity": 1,
            "unit_rate": round(contingency_amount, 2),
            "total_cost": round(contingency_amount, 2),
            "currency": cost_items[0]['currency'] if cost_items else 'PKR',
            "element_reference": "Overall"
        }
        
        return cost_items + [contingency_item]
    
    def add_overhead_profit(
        self,
        cost_items: List[Dict],
        overhead_percent: float = 15.0,
        profit_percent: float = 10.0
    ) -> List[Dict]:
        """Add overhead and profit margins"""
        subtotal = sum(item['total_cost'] for item in cost_items)
        
        overhead_amount = subtotal * (overhead_percent / 100)
        profit_amount = subtotal * (profit_percent / 100)
        
        currency = cost_items[0]['currency'] if cost_items else 'PKR'
        
        overhead_item = {
            "item_description": f"Overhead & General Expenses ({overhead_percent}%)",
            "element_type": "overhead",
            "material": "Allowance",
            "unit": "LS",
            "quantity": 1,
            "unit_rate": round(overhead_amount, 2),
            "total_cost": round(overhead_amount, 2),
            "currency": currency,
            "element_reference": "Overall"
        }
        
        profit_item = {
            "item_description": f"Profit Margin ({profit_percent}%)",
            "element_type": "profit",
            "material": "Allowance",
            "unit": "LS",
            "quantity": 1,
            "unit_rate": round(profit_amount, 2),
            "total_cost": round(profit_amount, 2),
            "currency": currency,
            "element_reference": "Overall"
        }
        
        return cost_items + [overhead_item, profit_item]
    
    def convert_currency(
        self,
        amount: float,
        from_currency: str,
        to_currency: str
    ) -> float:
        """Convert amount between currencies"""
        # Exchange rates (relative to PKR)
        rates_to_pkr = {
            "PKR": 1.0,
            "USD": 280.0,
            "GBP": 350.0,
            "EUR": 305.0,
            "AED": 76.0,
            "SAR": 75.0,
            "INR": 3.3
        }
        
        # Convert to PKR first, then to target currency
        amount_in_pkr = amount * rates_to_pkr.get(from_currency, 1.0)
        amount_in_target = amount_in_pkr / rates_to_pkr.get(to_currency, 1.0)
        
        return round(amount_in_target, 2)


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    estimator = CostEstimator()
    
    # Example quantities
    quantities = [
        {
            "item_description": "Concrete for columns",
            "element_type": "column",
            "material": "Concrete",
            "unit": "m³",
            "quantity": 5.4,
            "element_reference": "Columns A1-A4"
        },
        {
            "item_description": "Reinforcement steel for columns",
            "element_type": "column",
            "material": "Reinforcement Steel",
            "unit": "kg",
            "quantity": 635.4,
            "element_reference": "Columns A1-A4"
        }
    ]
    
    # Estimate costs
    cost_items = estimator.estimate_costs(
        quantities,
        region="pakistan",
        currency="PKR",
        project_type="residential"
    )
    
    # Add contingency and O&P
    cost_items = estimator.add_contingency(cost_items, 10.0)
    cost_items = estimator.add_overhead_profit(cost_items, 15.0, 10.0)
    
    # Get summary
    summary = estimator.calculate_summary(cost_items)
    
    print(f"\nTotal Project Cost: {summary['total_cost']:,.2f} {summary['currency']}")
    print(f"\nBreakdown by Element Type:")
    for element, cost in summary['by_element_type'].items():
        print(f"  {element}: {cost:,.2f} ({summary['element_percentages'][element]}%)")
