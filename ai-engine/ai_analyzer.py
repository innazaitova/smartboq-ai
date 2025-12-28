"""
AI Analyzer - Uses OpenAI GPT-4 Vision to interpret construction drawings
"""

from openai import OpenAI
import os
import json
from typing import List, Dict, Any
import base64


class AIAnalyzer:
    """Analyzes construction drawings using OpenAI GPT-4 Vision"""
    
    def __init__(self):
        self.client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY")
        )
        self.model = "gpt-4o"
    
    def analyze_drawing(self, image_path: str, drawing_type: str = "plan") -> Dict[str, Any]:
        """
        Analyze a construction drawing and extract elements
        
        Args:
            image_path: Path to the drawing image file
            drawing_type: Type of drawing (plan, elevation, section, detail)
        
        Returns:
            Dictionary containing detected elements and their properties
        """
        try:
            # Read and encode image
            with open(image_path, "rb") as f:
                image_data = base64.standard_b64encode(f.read()).decode("utf-8")
            
            # Determine media type
            if image_path.lower().endswith('.png'):
                media_type = "image/png"
            elif image_path.lower().endswith(('.jpg', '.jpeg')):
                media_type = "image/jpeg"
            else:
                media_type = "image/png"
            
            # Create analysis prompt based on drawing type
            prompt = self._create_analysis_prompt(drawing_type)
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=4096,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:{media_type};base64,{image_data}"
                                }
                            },
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ],
                    }
                ],
            )
            
            # Parse response
            result_text = response.choices[0].message.content
            elements = self._parse_ai_response(result_text)
            
            return {
                "success": True,
                "elements": elements,
                "raw_response": result_text,
                "confidence": self._calculate_confidence(elements)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "elements": []
            }
    
    def _create_analysis_prompt(self, drawing_type: str) -> str:
        """Create appropriate prompt based on drawing type"""
        
        base_prompt = """You are an expert civil engineer analyzing construction drawings. 
Analyze this {drawing_type} and extract ALL structural and architectural elements with precise measurements.

For EACH element you identify, provide:
1. Element type (beam, column, slab, wall, door, window, etc.)
2. Precise dimensions (length, width, height/thickness)
3. Location/position in the drawing
4. Material specifications (if visible)
5. Quantity (number of identical elements)
6. Any relevant notes or specifications

Output your analysis as a JSON array with this structure:
[
  {{
    "element_type": "column",
    "dimensions": {{
      "length": 0.3,
      "width": 0.3,
      "height": 3.0,
      "unit": "meters"
    }},
    "location": "Grid A-1",
    "material": "Reinforced Concrete",
    "quantity": 1,
    "notes": "C1 - Ground floor column",
    "confidence": 0.95
  }}
]

Be extremely thorough. Extract EVERY measurable element. If dimensions are not clearly visible, estimate based on scale and typical construction standards.
"""
        
        specific_instructions = {
            "plan": """
For this floor plan, identify:
- All columns (circular, rectangular, square)
- All beams (primary, secondary, edge beams)
- All walls (load-bearing and partition, with thickness)
- All doors (with sizes: single, double, main, etc.)
- All windows (with sizes)
- Slab areas and thickness
- Room dimensions
- Any structural notes or grid references
""",
            "elevation": """
For this elevation drawing, identify:
- Wall heights and lengths
- Window and door positions and sizes
- Floor levels
- Parapet heights
- Any architectural features
""",
            "section": """
For this section drawing, identify:
- Foundation depth and width
- Floor slab thickness
- Beam depths
- Column heights
- Wall thicknesses
- Roof construction details
""",
            "detail": """
For this detail drawing, identify:
- Connection details
- Reinforcement specifications
- Material specifications
- Dimensions of components
"""
        }
        
        return base_prompt.format(drawing_type=drawing_type) + specific_instructions.get(drawing_type, "")
    
    def _parse_ai_response(self, response_text: str) -> List[Dict[str, Any]]:
        """Parse Claude's JSON response into structured elements"""
        try:
            # Try to find JSON in the response
            start_idx = response_text.find('[')
            end_idx = response_text.rfind(']') + 1
            
            if start_idx != -1 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                elements = json.loads(json_str)
                return elements
            else:
                # If no JSON found, return empty list
                return []
                
        except json.JSONDecodeError:
            # If JSON parsing fails, try to extract information manually
            return self._fallback_parsing(response_text)
    
    def _fallback_parsing(self, text: str) -> List[Dict[str, Any]]:
        """Fallback parsing if JSON extraction fails"""
        # Simple keyword-based extraction (implement more sophisticated parsing as needed)
        elements = []
        
        # This is a simplified example - enhance based on actual response patterns
        keywords = {
            'column': 'column',
            'beam': 'beam',
            'slab': 'slab',
            'wall': 'wall',
            'door': 'door',
            'window': 'window'
        }
        
        for keyword, element_type in keywords.items():
            if keyword in text.lower():
                elements.append({
                    "element_type": element_type,
                    "dimensions": {},
                    "location": "unknown",
                    "material": "unknown",
                    "quantity": 1,
                    "notes": f"Detected {keyword} in text",
                    "confidence": 0.5
                })
        
        return elements
    
    def _calculate_confidence(self, elements: List[Dict]) -> float:
        """Calculate overall confidence score for the analysis"""
        if not elements:
            return 0.0
        
        # Average confidence of all elements
        confidences = [elem.get('confidence', 0.7) for elem in elements]
        return sum(confidences) / len(confidences) if confidences else 0.0
    
    def batch_analyze_drawings(self, drawing_paths: List[str]) -> List[Dict[str, Any]]:
        """
        Analyze multiple drawings in batch
        
        Args:
            drawing_paths: List of paths to drawing files
        
        Returns:
            List of analysis results
        """
        results = []
        
        for path in drawing_paths:
            result = self.analyze_drawing(path)
            results.append({
                "file": path,
                "analysis": result
            })
        
        return results
    
    def verify_dimensions(self, element: Dict[str, Any]) -> bool:
        """
        Verify if extracted dimensions are realistic
        
        Args:
            element: Element dictionary with dimensions
        
        Returns:
            Boolean indicating if dimensions are reasonable
        """
        dimensions = element.get('dimensions', {})
        element_type = element.get('element_type', '').lower()
        
        # Realistic dimension ranges (in meters)
        ranges = {
            'column': {'length': (0.2, 2.0), 'width': (0.2, 2.0), 'height': (2.5, 8.0)},
            'beam': {'length': (1.0, 15.0), 'width': (0.2, 1.0), 'height': (0.3, 2.0)},
            'slab': {'thickness': (0.1, 0.5)},
            'wall': {'thickness': (0.1, 0.5), 'height': (2.5, 8.0)},
            'door': {'width': (0.6, 2.5), 'height': (2.0, 3.5)},
            'window': {'width': (0.6, 3.0), 'height': (0.6, 2.5)}
        }
        
        if element_type not in ranges:
            return True  # Unknown type, assume valid
        
        expected_ranges = ranges[element_type]
        
        for dim, value in dimensions.items():
            if dim in expected_ranges:
                min_val, max_val = expected_ranges[dim]
                if not (min_val <= value <= max_val):
                    return False
        
        return True
    
    def enhance_with_context(self, elements: List[Dict], project_context: Dict) -> List[Dict]:
        """
        Enhance detected elements with project-specific context
        
        Args:
            elements: List of detected elements
            project_context: Dictionary with project information (location, type, codes)
        
        Returns:
            Enhanced elements list
        """
        enhanced_elements = []
        
        for element in elements:
            enhanced = element.copy()
            
            # Add building code requirements
            if project_context.get('building_code'):
                enhanced['applicable_code'] = project_context['building_code']
            
            # Add regional material specifications
            if project_context.get('region'):
                enhanced['region'] = project_context['region']
            
            # Add project-specific notes
            enhanced['project_id'] = project_context.get('project_id')
            
            enhanced_elements.append(enhanced)
        
        return enhanced_elements


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def extract_scale_from_drawing(image_path: str) -> float:
    """
    Extract drawing scale from the drawing
    (This would use OCR to find scale notation like "1:100")
    
    Returns:
        Scale factor (e.g., 100 for 1:100 scale)
    """
    # Placeholder - implement actual scale detection
    return 100.0


def convert_dimensions(dimensions: Dict, from_unit: str, to_unit: str) -> Dict:
    """Convert dimensions between units"""
    conversion_factors = {
        ('meters', 'feet'): 3.28084,
        ('feet', 'meters'): 0.3048,
        ('meters', 'inches'): 39.3701,
        ('inches', 'meters'): 0.0254,
        ('mm', 'meters'): 0.001,
        ('meters', 'mm'): 1000
    }
    
    factor = conversion_factors.get((from_unit, to_unit), 1.0)
    
    converted = {}
    for key, value in dimensions.items():
        if isinstance(value, (int, float)):
            converted[key] = value * factor
        else:
            converted[key] = value
    
    converted['unit'] = to_unit
    return converted


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    # Example usage
    analyzer = AIAnalyzer()
    
    # Analyze a single drawing
    result = analyzer.analyze_drawing(
        image_path="sample_drawing.pdf",
        drawing_type="plan"
    )
    
    print(f"Analysis Success: {result['success']}")
    print(f"Elements Detected: {len(result['elements'])}")
    print(f"Overall Confidence: {result['confidence']:.2f}")
    
    # Print first few elements
    for element in result['elements'][:3]:
        print(f"\nElement: {element['element_type']}")
        print(f"Dimensions: {element['dimensions']}")
        print(f"Location: {element['location']}")
