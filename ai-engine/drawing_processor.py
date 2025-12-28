"""
Drawing Processor - Handles PDF/DWG/Image processing
Lightweight version using pypdf (pure Python, no compilation)
"""

from pypdf import PdfReader
from PIL import Image
import os
from typing import List, Dict, Any, Tuple
import re
import io


class DrawingProcessor:
    """Process construction drawings (PDF, images)"""
    
    def __init__(self):
        self.supported_formats = ['.pdf', '.png', '.jpg', '.jpeg']
        self.temp_dir = "temp_processing"
        os.makedirs(self.temp_dir, exist_ok=True)
    
    def process_file(self, file_path: str) -> Dict[str, Any]:
        """
        Process drawing file and extract information
        
        Args:
            file_path: Path to drawing file
        
        Returns:
            Dictionary with extracted information
        """
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext == '.pdf':
            return self._process_pdf(file_path)
        elif file_ext in ['.png', '.jpg', '.jpeg']:
            return self._process_image(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_ext}. Supported: PDF, PNG, JPG")
    
    def _process_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """Process PDF drawing using pypdf"""
        reader = PdfReader(pdf_path)
        
        result = {
            "file_path": pdf_path,
            "file_type": "pdf",
            "num_pages": len(reader.pages),
            "pages": [],
            "extracted_text": "",
            "scale": None
        }
        
        for page_num, page in enumerate(reader.pages):
            # Extract text
            text = page.extract_text() or ""
            result["extracted_text"] += text + "\n"
            
            # Detect scale from text
            scale = self._detect_scale(text)
            if scale and not result["scale"]:
                result["scale"] = scale
            
            # Detect drawing type
            drawing_type = self._detect_drawing_type(text)
            
            # Get page dimensions
            mediabox = page.mediabox
            width = float(mediabox.width)
            height = float(mediabox.height)
            
            page_info = {
                "page_number": page_num + 1,
                "text": text,
                "scale": scale,
                "drawing_type": drawing_type,
                "dimensions": {
                    "width": width,
                    "height": height
                }
            }
            
            result["pages"].append(page_info)
        
        return result    
    def _process_image(self, image_path: str) -> Dict[str, Any]:
        """Process image file"""
        img = Image.open(image_path)
        
        result = {
            "file_path": image_path,
            "file_type": "image",
            "num_pages": 1,
            "pages": [{
                "page_number": 1,
                "image_path": image_path,
                "dimensions": {
                    "width": img.width,
                    "height": img.height
                }
            }],
            "scale": None
        }
        
        return result
    
    def _process_cad(self, cad_path: str) -> Dict[str, Any]:
        """Process CAD file (DWG/DXF)"""
        try:
            import ezdxf
            
            doc = ezdxf.readfile(cad_path)
            modelspace = doc.modelspace()
            
            # Extract entities
            entities = []
            for entity in modelspace:
                entities.append({
                    "type": entity.dxftype(),
                    "layer": entity.dxf.layer if hasattr(entity.dxf, 'layer') else None
                })
            
            result = {
                "file_path": cad_path,
                "file_type": "cad",
                "num_entities": len(entities),
                "entities": entities[:100],  # Limit to first 100
                "layers": list(doc.layers),
                "scale": None
            }
            
            return result
            
        except Exception as e:
            return result
        
        return result
    
    def _detect_scale(self, text: str) -> str:
        """Detect drawing scale from text"""
        # Common scale patterns
        scale_patterns = [
            r'SCALE[:\s]+1[:\s]*(\d+)',
            r'1[:\s]*(\d+)',
            r'SCALE[:\s]+(\d+)[:\s]*1',
            r'@\s*1[:\s]*(\d+)',
        ]
        
        for pattern in scale_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                scale_value = match.group(1)
                return f"1:{scale_value}"
        
        return None
    
    def _detect_drawing_type(self, text: str) -> str:
        """Detect type of drawing"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['floor plan', 'ground floor', 'plan']):
            return 'plan'
        elif any(word in text_lower for word in ['elevation', 'front view', 'side view']):
            return 'elevation'
        elif any(word in text_lower for word in ['section', 'cross section']):
            return 'section'
        elif any(word in text_lower for word in ['detail', 'connection']):
            return 'detail'
        elif any(word in text_lower for word in ['foundation', 'footing']):
            return 'foundation'
        else:
            return 'unknown'
    
    def extract_dimensions_from_text(self, text: str) -> List[Tuple[float, str]]:
        """Extract dimension annotations from text"""
        # Pattern for dimensions: number followed by unit
        dimension_pattern = r'(\d+(?:\.\d+)?)\s*(mm|cm|m|ft|in|\'|")?'
        
        matches = re.findall(dimension_pattern, text)
        
        dimensions = []
        for value, unit in matches:
            try:
                dim_value = float(value)
                dim_unit = unit or 'unknown'
                dimensions.append((dim_value, dim_unit))
            except ValueError:
                continue
        
        return dimensions
    
    def preprocess_image_for_ai(self, image_path: str, target_size: int = 1568) -> str:
        """
        Preprocess image for AI analysis
        
        Args:
            image_path: Path to image
            target_size: Maximum dimension size
        
        Returns:
            Path to preprocessed image
        """
        img = Image.open(image_path)
        
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize if too large (to save on API costs)
        max_dim = max(img.width, img.height)
        if max_dim > target_size:
            scale = target_size / max_dim
            new_size = (int(img.width * scale), int(img.height * scale))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        # Enhance contrast for better AI recognition
        from PIL import ImageEnhance
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.2)
        
        # Save preprocessed image
        preprocessed_path = image_path.replace('.png', '_preprocessed.png')
        img.save(preprocessed_path, quality=95)
        
        return preprocessed_path
    
    def cleanup_temp_files(self):
        """Clean up temporary files"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
            os.makedirs(self.temp_dir, exist_ok=True)
    
    def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """Get basic file information"""
        file_stats = os.stat(file_path)
        
        return {
            "file_name": os.path.basename(file_path),
            "file_size": file_stats.st_size,
            "file_size_mb": round(file_stats.st_size / (1024 * 1024), 2),
            "file_extension": os.path.splitext(file_path)[1],
            "created_time": file_stats.st_ctime,
            "modified_time": file_stats.st_mtime
        }
    
    def validate_file(self, file_path: str, max_size_mb: int = 50) -> Tuple[bool, str]:
        """
        Validate if file can be processed
        
        Args:
            file_path: Path to file
            max_size_mb: Maximum file size in MB
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check if file exists
        if not os.path.exists(file_path):
            return False, "File does not exist"
        
        # Check file extension
        file_ext = os.path.splitext(file_path)[1].lower()
        if file_ext not in self.supported_formats:
            return False, f"Unsupported file format: {file_ext}"
        
        # Check file size
        file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
        if file_size_mb > max_size_mb:
            return False, f"File too large: {file_size_mb:.1f}MB (max: {max_size_mb}MB)"
        
        return True, "Valid"


# Utility functions
def extract_images_from_pdf(pdf_path: str, output_dir: str = "extracted_images") -> List[str]:
    """Extract all images from PDF pages"""
    processor = DrawingProcessor()
    result = processor.process_file(pdf_path)
    
    image_paths = []
    for page in result.get("pages", []):
        if "image_path" in page:
            image_paths.append(page["image_path"])
    
    return image_paths


def batch_process_drawings(file_paths: List[str]) -> List[Dict[str, Any]]:
    """Process multiple drawings in batch"""
    processor = DrawingProcessor()
    results = []
    
    for file_path in file_paths:
        try:
            result = processor.process_file(file_path)
            results.append(result)
        except Exception as e:
            results.append({
                "file_path": file_path,
                "error": str(e),
                "success": False
            })
    
    return results
