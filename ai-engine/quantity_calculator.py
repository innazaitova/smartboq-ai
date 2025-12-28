"""
Quantity Calculator - Calculates material quantities from detected elements
"""

from typing import Dict, List, Any
import math


class QuantityCalculator:
    """Calculate construction quantities from detected elements"""
    
    def __init__(self):
        self.formulas = self._load_formulas()
        self.material_properties = self._load_material_properties()
    
    def calculate_quantities(self, elements: List[Dict[str, Any]], building_code: str = "IBC") -> List[Dict[str, Any]]:
        """
        Calculate quantities for all elements
        
        Args:
            elements: List of detected elements with dimensions
            building_code: Building code to apply (IBC, Eurocode, IS, etc.)
        
        Returns:
            List of quantity items with calculations
        """
        quantities = []
        
        for element in elements:
            element_type = element.get('element_type', '').lower()
            
            # Calculate based on element type
            if element_type == 'column':
                qty = self._calculate_column_quantities(element, building_code)
            elif element_type == 'beam':
                qty = self._calculate_beam_quantities(element, building_code)
            elif element_type == 'slab':
                qty = self._calculate_slab_quantities(element, building_code)
            elif element_type == 'wall':
                qty = self._calculate_wall_quantities(element, building_code)
            elif element_type == 'door':
                qty = self._calculate_door_quantities(element)
            elif element_type == 'window':
                qty = self._calculate_window_quantities(element)
            else:
                qty = self._calculate_generic_quantities(element)
            
            quantities.extend(qty)
        
        return quantities
    
    # ========================================================================
    # COLUMN CALCULATIONS
    # ========================================================================
    
    def _calculate_column_quantities(self, element: Dict, code: str) -> List[Dict]:
        """Calculate concrete, reinforcement, and formwork for columns"""
        dims = element.get('dimensions', {})
        length = dims.get('length', 0)
        width = dims.get('width', 0)
        height = dims.get('height', 0)
        quantity = element.get('quantity', 1)
        
        quantities = []
        
        # 1. Concrete Volume
        concrete_volume = length * width * height * quantity
        quantities.append({
            "item_description": f"Concrete for {element.get('notes', 'Column')}",
            "element_type": "column",
            "material": "Concrete",
            "unit": "m³",
            "quantity": round(concrete_volume, 3),
            "formula": "length × width × height × qty",
            "element_reference": element.get('location', 'N/A')
        })
        
        # 2. Reinforcement Steel
        # Estimate based on column cross-section (typical 1-2% of concrete volume)
        rebar_percentage = self._get_rebar_percentage('column', code)
        concrete_density = 2400  # kg/m³
        steel_density = 7850  # kg/m³
        
        rebar_volume = concrete_volume * (rebar_percentage / 100)
        rebar_weight = rebar_volume * steel_density
        
        quantities.append({
            "item_description": f"Reinforcement steel for {element.get('notes', 'Column')}",
            "element_type": "column",
            "material": "Reinforcement Steel",
            "unit": "kg",
            "quantity": round(rebar_weight, 2),
            "formula": f"concrete_volume × {rebar_percentage}% × steel_density",
            "element_reference": element.get('location', 'N/A')
        })
        
        # 3. Formwork
        perimeter = 2 * (length + width)
        formwork_area = perimeter * height * quantity
        
        quantities.append({
            "item_description": f"Formwork for {element.get('notes', 'Column')}",
            "element_type": "column",
            "material": "Formwork",
            "unit": "m²",
            "quantity": round(formwork_area, 2),
            "formula": "2 × (length + width) × height × qty",
            "element_reference": element.get('location', 'N/A')
        })
        
        return quantities
    
    # ========================================================================
    # BEAM CALCULATIONS
    # ========================================================================
    
    def _calculate_beam_quantities(self, element: Dict, code: str) -> List[Dict]:
        """Calculate concrete, reinforcement, and formwork for beams"""
        dims = element.get('dimensions', {})
        length = dims.get('length', 0)
        width = dims.get('width', 0)
        depth = dims.get('depth', dims.get('height', 0))
        quantity = element.get('quantity', 1)
        
        quantities = []
        
        # 1. Concrete Volume
        concrete_volume = length * width * depth * quantity
        quantities.append({
            "item_description": f"Concrete for {element.get('notes', 'Beam')}",
            "element_type": "beam",
            "material": "Concrete",
            "unit": "m³",
            "quantity": round(concrete_volume, 3),
            "formula": "length × width × depth × qty",
            "element_reference": element.get('location', 'N/A')
        })
        
        # 2. Reinforcement Steel (beams typically 1.5-2.5%)
        rebar_percentage = self._get_rebar_percentage('beam', code)
        steel_density = 7850
        
        rebar_volume = concrete_volume * (rebar_percentage / 100)
        rebar_weight = rebar_volume * steel_density
        
        quantities.append({
            "item_description": f"Reinforcement steel for {element.get('notes', 'Beam')}",
            "element_type": "beam",
            "material": "Reinforcement Steel",
            "unit": "kg",
            "quantity": round(rebar_weight, 2),
            "formula": f"concrete_volume × {rebar_percentage}% × steel_density",
            "element_reference": element.get('location', 'N/A')
        })
        
        # 3. Formwork (bottom + two sides)
        formwork_area = (length * width + 2 * length * depth) * quantity
        
        quantities.append({
            "item_description": f"Formwork for {element.get('notes', 'Beam')}",
            "element_type": "beam",
            "material": "Formwork",
            "unit": "m²",
            "quantity": round(formwork_area, 2),
            "formula": "(length × width + 2 × length × depth) × qty",
            "element_reference": element.get('location', 'N/A')
        })
        
        return quantities
    
    # ========================================================================
    # SLAB CALCULATIONS
    # ========================================================================
    
    def _calculate_slab_quantities(self, element: Dict, code: str) -> List[Dict]:
        """Calculate concrete, reinforcement, and formwork for slabs"""
        dims = element.get('dimensions', {})
        length = dims.get('length', 0)
        width = dims.get('width', 0)
        thickness = dims.get('thickness', dims.get('depth', 0.15))  # Default 150mm
        quantity = element.get('quantity', 1)
        
        quantities = []
        
        # 1. Concrete Volume
        concrete_volume = length * width * thickness * quantity
        quantities.append({
            "item_description": f"Concrete for {element.get('notes', 'Slab')}",
            "element_type": "slab",
            "material": "Concrete",
            "unit": "m³",
            "quantity": round(concrete_volume, 3),
            "formula": "length × width × thickness × qty",
            "element_reference": element.get('location', 'N/A')
        })
        
        # 2. Reinforcement Steel (slabs typically 0.8-1.5%)
        rebar_percentage = self._get_rebar_percentage('slab', code)
        steel_density = 7850
        
        rebar_volume = concrete_volume * (rebar_percentage / 100)
        rebar_weight = rebar_volume * steel_density
        
        quantities.append({
            "item_description": f"Reinforcement steel for {element.get('notes', 'Slab')}",
            "element_type": "slab",
            "material": "Reinforcement Steel",
            "unit": "kg",
            "quantity": round(rebar_weight, 2),
            "formula": f"concrete_volume × {rebar_percentage}% × steel_density",
            "element_reference": element.get('location', 'N/A')
        })
        
        # 3. Formwork (bottom surface)
        formwork_area = length * width * quantity
        
        quantities.append({
            "item_description": f"Formwork for {element.get('notes', 'Slab')}",
            "element_type": "slab",
            "material": "Formwork",
            "unit": "m²",
            "quantity": round(formwork_area, 2),
            "formula": "length × width × qty",
            "element_reference": element.get('location', 'N/A')
        })
        
        return quantities
    
    # ========================================================================
    # WALL CALCULATIONS
    # ========================================================================
    
    def _calculate_wall_quantities(self, element: Dict, code: str) -> List[Dict]:
        """Calculate masonry/concrete for walls"""
        dims = element.get('dimensions', {})
        length = dims.get('length', 0)
        height = dims.get('height', 0)
        thickness = dims.get('thickness', 0.23)  # Default 9" wall
        quantity = element.get('quantity', 1)
        
        material = element.get('material', 'Brick Masonry')
        
        quantities = []
        
        # Wall volume
        wall_volume = length * height * thickness * quantity
        
        if 'concrete' in material.lower():
            # Concrete wall
            quantities.append({
                "item_description": f"Concrete for {element.get('notes', 'Wall')}",
                "element_type": "wall",
                "material": "Concrete",
                "unit": "m³",
                "quantity": round(wall_volume, 3),
                "formula": "length × height × thickness × qty",
                "element_reference": element.get('location', 'N/A')
            })
        else:
            # Masonry wall
            wall_area = length * height * quantity
            
            # Bricks (assuming standard brick size 230x110x75mm)
            bricks_per_sqm = self._get_bricks_per_sqm(thickness)
            total_bricks = wall_area * bricks_per_sqm
            
            quantities.append({
                "item_description": f"Bricks for {element.get('notes', 'Wall')}",
                "element_type": "wall",
                "material": "Bricks",
                "unit": "nos",
                "quantity": round(total_bricks, 0),
                "formula": f"area × {bricks_per_sqm} bricks/m²",
                "element_reference": element.get('location', 'N/A')
            })
            
            # Mortar (typically 30% of wall volume for brick masonry)
            mortar_volume = wall_volume * 0.30
            
            quantities.append({
                "item_description": f"Mortar for {element.get('notes', 'Wall')}",
                "element_type": "wall",
                "material": "Mortar",
                "unit": "m³",
                "quantity": round(mortar_volume, 3),
                "formula": "wall_volume × 0.30",
                "element_reference": element.get('location', 'N/A')
            })
        
        return quantities
    
    # ========================================================================
    # DOOR & WINDOW CALCULATIONS
    # ========================================================================
    
    def _calculate_door_quantities(self, element: Dict) -> List[Dict]:
        """Calculate door quantities"""
        dims = element.get('dimensions', {})
        width = dims.get('width', 0)
        height = dims.get('height', 0)
        quantity = element.get('quantity', 1)
        
        area = width * height * quantity
        
        return [{
            "item_description": f"Door - {element.get('notes', 'Standard door')}",
            "element_type": "door",
            "material": "Door panel",
            "unit": "m²",
            "quantity": round(area, 2),
            "formula": "width × height × qty",
            "element_reference": element.get('location', 'N/A')
        }]
    
    def _calculate_window_quantities(self, element: Dict) -> List[Dict]:
        """Calculate window quantities"""
        dims = element.get('dimensions', {})
        width = dims.get('width', 0)
        height = dims.get('height', 0)
        quantity = element.get('quantity', 1)
        
        area = width * height * quantity
        
        return [{
            "item_description": f"Window - {element.get('notes', 'Standard window')}",
            "element_type": "window",
            "material": "Window frame & glass",
            "unit": "m²",
            "quantity": round(area, 2),
            "formula": "width × height × qty",
            "element_reference": element.get('location', 'N/A')
        }]
    
    def _calculate_generic_quantities(self, element: Dict) -> List[Dict]:
        """Generic calculation for unknown elements"""
        return [{
            "item_description": f"{element.get('element_type', 'Unknown')} - {element.get('notes', 'Item')}",
            "element_type": element.get('element_type', 'unknown'),
            "material": element.get('material', 'Unknown'),
            "unit": "item",
            "quantity": element.get('quantity', 1),
            "formula": "Count",
            "element_reference": element.get('location', 'N/A')
        }]
    
    # ========================================================================
    # HELPER METHODS
    # ========================================================================
    
    def _load_formulas(self) -> Dict:
        """Load all calculation formulas"""
        return {
            "concrete_volume": lambda l, w, h: l * w * h,
            "rebar_weight": lambda dia, length: (dia**2 / 162) * length,
            "formwork_area": lambda l, w, h: 2 * (l + w) * h,
            "brick_count": lambda area, thickness: area * self._get_bricks_per_sqm(thickness)
        }
    
    def _load_material_properties(self) -> Dict:
        """Load material density and properties"""
        return {
            "concrete": {"density": 2400, "unit": "kg/m³"},
            "steel": {"density": 7850, "unit": "kg/m³"},
            "brick": {"density": 1920, "unit": "kg/m³"},
            "mortar": {"density": 2080, "unit": "kg/m³"}
        }
    
    def _get_rebar_percentage(self, element_type: str, code: str) -> float:
        """Get typical reinforcement percentage based on element and code"""
        percentages = {
            "IBC": {"column": 1.5, "beam": 2.0, "slab": 1.0},
            "Eurocode": {"column": 1.2, "beam": 1.8, "slab": 0.8},
            "IS": {"column": 1.5, "beam": 2.0, "slab": 1.2}
        }
        
        return percentages.get(code, percentages["IBC"]).get(element_type, 1.5)
    
    def _get_bricks_per_sqm(self, wall_thickness: float) -> int:
        """Calculate number of bricks per square meter based on wall thickness"""
        # Standard brick: 230mm × 110mm × 75mm
        # With 10mm mortar joint
        
        if wall_thickness <= 0.12:  # Half brick (110mm)
            return 55
        elif wall_thickness <= 0.24:  # Full brick (230mm)
            return 110
        else:  # Double brick or more
            return 165
    
    def aggregate_quantities(self, quantities: List[Dict]) -> List[Dict]:
        """Aggregate similar items"""
        aggregated = {}
        
        for item in quantities:
            key = (item['material'], item['unit'])
            
            if key in aggregated:
                aggregated[key]['quantity'] += item['quantity']
                aggregated[key]['references'].append(item['element_reference'])
            else:
                aggregated[key] = item.copy()
                aggregated[key]['references'] = [item['element_reference']]
        
        return list(aggregated.values())


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    calculator = QuantityCalculator()
    
    # Example elements from AI analysis
    elements = [
        {
            "element_type": "column",
            "dimensions": {"length": 0.3, "width": 0.3, "height": 3.0},
            "location": "A-1",
            "material": "Reinforced Concrete",
            "quantity": 4,
            "notes": "Ground floor columns"
        },
        {
            "element_type": "beam",
            "dimensions": {"length": 6.0, "width": 0.23, "depth": 0.45},
            "location": "B1",
            "material": "Reinforced Concrete",
            "quantity": 2,
            "notes": "Primary beam"
        }
    ]
    
    # Calculate quantities
    quantities = calculator.calculate_quantities(elements, building_code="IBC")
    
    print(f"\nTotal quantity items: {len(quantities)}")
    for qty in quantities:
        print(f"\n{qty['item_description']}")
        print(f"  Quantity: {qty['quantity']} {qty['unit']}")
        print(f"  Formula: {qty['formula']}")
