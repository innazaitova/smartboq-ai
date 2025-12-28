"""
BOQ Generator - Creates Excel and PDF Bill of Quantities
"""

from typing import List, Dict, Any
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
from datetime import datetime
import os


class BOQGenerator:
    """Generate professional Bill of Quantities documents"""
    
    def __init__(self):
        self.company_name = "QuantiBot AI"
        self.company_logo = None  # Path to logo image
    
    def generate_excel(
        self,
        project: Dict[str, Any],
        quantities: List[Dict[str, Any]],
        cost_items: List[Dict[str, Any]],
        region: str,
        currency: str,
        output_dir: str = "outputs"
    ) -> str:
        """
        Generate Excel BOQ
        
        Args:
            project: Project information
            quantities: List of quantity items
            cost_items: List of cost items
            region: Region for rates
            currency: Currency code
            output_dir: Output directory
        
        Returns:
            Path to generated Excel file
        """
        # Create workbook
        wb = openpyxl.Workbook()
        
        # Remove default sheet
        wb.remove(wb.active)
        
        # Create sheets
        self._create_summary_sheet(wb, project, cost_items, currency)
        self._create_detailed_boq_sheet(wb, cost_items, currency)
        self._create_quantities_sheet(wb, quantities)
        self._create_assumptions_sheet(wb, project, region)
        
        # Save file
        os.makedirs(f"{output_dir}/{project['id']}", exist_ok=True)
        filename = f"{output_dir}/{project['id']}/boq.xlsx"
        wb.save(filename)
        
        return filename
    
    def _create_summary_sheet(self, wb, project, cost_items, currency):
        """Create summary sheet"""
        ws = wb.create_sheet("Summary", 0)
        
        # Title
        ws['A1'] = "BILL OF QUANTITIES - SUMMARY"
        ws['A1'].font = Font(size=16, bold=True)
        ws['A1'].alignment = Alignment(horizontal='center')
        ws.merge_cells('A1:F1')
        
        # Project information
        row = 3
        info_fields = [
            ("Project Name:", project.get('project_name', 'N/A')),
            ("Location:", project.get('location', 'N/A')),
            ("Project Type:", project.get('project_type', 'N/A')),
            ("Area (sq ft):", project.get('area_sqft', 'N/A')),
            ("Date:", datetime.now().strftime('%Y-%m-%d')),
            ("Currency:", currency)
        ]
        
        for label, value in info_fields:
            ws[f'A{row}'] = label
            ws[f'A{row}'].font = Font(bold=True)
            ws[f'B{row}'] = value
            row += 1
        
        # Cost breakdown by element type
        row += 2
        ws[f'A{row}'] = "COST BREAKDOWN BY ELEMENT"
        ws[f'A{row}'].font = Font(size=12, bold=True)
        row += 1
        
        # Headers
        headers = ['Element Type', 'Total Cost', 'Percentage']
        for col, header in enumerate(headers, start=1):
            cell = ws.cell(row=row, column=col)
            cell.value = header
            cell.font = Font(bold=True)
            cell.fill = PatternFill(start_color='CCE5FF', end_color='CCE5FF', fill_type='solid')
        row += 1
        
        # Group by element type
        element_totals = {}
        for item in cost_items:
            element_type = item.get('element_type', 'Other')
            element_totals[element_type] = element_totals.get(element_type, 0) + item.get('total_cost', 0)
        
        total_cost = sum(element_totals.values())
        
        for element, cost in sorted(element_totals.items(), key=lambda x: x[1], reverse=True):
            percentage = (cost / total_cost * 100) if total_cost > 0 else 0
            ws[f'A{row}'] = element.replace('_', ' ').title()
            ws[f'B{row}'] = cost
            ws[f'B{row}'].number_format = '#,##0.00'
            ws[f'C{row}'] = f"{percentage:.1f}%"
            row += 1
        
        # Total
        ws[f'A{row}'] = "TOTAL PROJECT COST"
        ws[f'A{row}'].font = Font(bold=True, size=12)
        ws[f'B{row}'] = total_cost
        ws[f'B{row}'].font = Font(bold=True, size=12)
        ws[f'B{row}'].number_format = '#,##0.00'
        
        # Column widths
        ws.column_dimensions['A'].width = 25
        ws.column_dimensions['B'].width = 20
        ws.column_dimensions['C'].width = 15
    
    def _create_detailed_boq_sheet(self, wb, cost_items, currency):
        """Create detailed BOQ sheet"""
        ws = wb.create_sheet("Detailed BOQ")
        
        # Title
        ws['A1'] = "DETAILED BILL OF QUANTITIES"
        ws['A1'].font = Font(size=14, bold=True)
        ws['A1'].alignment = Alignment(horizontal='center')
        ws.merge_cells('A1:G1')
        
        # Headers
        row = 3
        headers = ['Item No.', 'Description', 'Unit', 'Quantity', 'Unit Rate', 'Total Cost', 'Reference']
        
        for col, header in enumerate(headers, start=1):
            cell = ws.cell(row=row, column=col)
            cell.value = header
            cell.font = Font(bold=True)
            cell.fill = PatternFill(start_color='4472C4', end_color='4472C4', fill_type='solid')
            cell.font = Font(bold=True, color='FFFFFF')
            cell.alignment = Alignment(horizontal='center')
        
        # Add border
        thin_border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )
        
        # Data rows
        row += 1
        item_no = 1
        
        # Group by element type
        grouped_items = {}
        for item in cost_items:
            element_type = item.get('element_type', 'Other')
            if element_type not in grouped_items:
                grouped_items[element_type] = []
            grouped_items[element_type].append(item)
        
        subtotal = 0
        
        for element_type, items in sorted(grouped_items.items()):
            # Element type header
            ws[f'A{row}'] = element_type.replace('_', ' ').upper()
            ws[f'A{row}'].font = Font(bold=True)
            ws[f'A{row}'].fill = PatternFill(start_color='E7E6E6', end_color='E7E6E6', fill_type='solid')
            ws.merge_cells(f'A{row}:G{row}')
            row += 1
            
            # Items
            for item in items:
                ws[f'A{row}'] = item_no
                ws[f'B{row}'] = item.get('item_description', 'N/A')
                ws[f'C{row}'] = item.get('unit', '')
                ws[f'D{row}'] = item.get('quantity', 0)
                ws[f'D{row}'].number_format = '#,##0.000'
                ws[f'E{row}'] = item.get('unit_rate', 0)
                ws[f'E{row}'].number_format = '#,##0.00'
                ws[f'F{row}'] = item.get('total_cost', 0)
                ws[f'F{row}'].number_format = '#,##0.00'
                ws[f'G{row}'] = item.get('element_reference', '')
                
                # Apply borders
                for col in range(1, 8):
                    ws.cell(row=row, column=col).border = thin_border
                
                subtotal += item.get('total_cost', 0)
                item_no += 1
                row += 1
            
            # Subtotal
            ws[f'E{row}'] = "Subtotal:"
            ws[f'E{row}'].font = Font(bold=True)
            ws[f'F{row}'] = subtotal
            ws[f'F{row}'].font = Font(bold=True)
            ws[f'F{row}'].number_format = '#,##0.00'
            row += 2
        
        # Grand total
        ws[f'E{row}'] = "GRAND TOTAL:"
        ws[f'E{row}'].font = Font(bold=True, size=12)
        ws[f'F{row}'] = subtotal
        ws[f'F{row}'].font = Font(bold=True, size=12)
        ws[f'F{row}'].number_format = '#,##0.00'
        ws[f'F{row}'].fill = PatternFill(start_color='FFFF00', end_color='FFFF00', fill_type='solid')
        
        # Column widths
        ws.column_dimensions['A'].width = 10
        ws.column_dimensions['B'].width = 50
        ws.column_dimensions['C'].width = 10
        ws.column_dimensions['D'].width = 15
        ws.column_dimensions['E'].width = 15
        ws.column_dimensions['F'].width = 15
        ws.column_dimensions['G'].width = 20
    
    def _create_quantities_sheet(self, wb, quantities):
        """Create quantities sheet (without costs)"""
        ws = wb.create_sheet("Quantities Only")
        
        # Title
        ws['A1'] = "QUANTITY TAKEOFF"
        ws['A1'].font = Font(size=14, bold=True)
        
        # Headers
        row = 3
        headers = ['Item No.', 'Description', 'Unit', 'Quantity', 'Formula', 'Reference']
        
        for col, header in enumerate(headers, start=1):
            cell = ws.cell(row=row, column=col)
            cell.value = header
            cell.font = Font(bold=True)
            cell.fill = PatternFill(start_color='92D050', end_color='92D050', fill_type='solid')
        
        # Data
        row += 1
        for idx, qty in enumerate(quantities, start=1):
            ws[f'A{row}'] = idx
            ws[f'B{row}'] = qty.get('item_description', '')
            ws[f'C{row}'] = qty.get('unit', '')
            ws[f'D{row}'] = qty.get('quantity', 0)
            ws[f'D{row}'].number_format = '#,##0.000'
            ws[f'E{row}'] = qty.get('formula', '')
            ws[f'F{row}'] = qty.get('element_reference', '')
            row += 1
        
        # Column widths
        ws.column_dimensions['B'].width = 50
        ws.column_dimensions['E'].width = 30
    
    def _create_assumptions_sheet(self, wb, project, region):
        """Create assumptions and notes sheet"""
        ws = wb.create_sheet("Assumptions & Notes")
        
        ws['A1'] = "ASSUMPTIONS & NOTES"
        ws['A1'].font = Font(size=14, bold=True)
        
        row = 3
        assumptions = [
            "1. GENERAL ASSUMPTIONS",
            "",
            "• All quantities are calculated from drawings provided",
            "• Unit rates are based on current market rates",
            f"• Region: {region}",
            "• Rates include material and labor",
            "• GST/VAT not included unless specified",
            "• Transportation costs included in unit rates",
            "",
            "2. EXCLUSIONS",
            "",
            "• Site preparation and mobilization",
            "• Temporary works and scaffolding",
            "• Professional fees",
            "• Testing and commissioning",
            "• Permits and approvals",
            "",
            "3. VALIDITY",
            "",
            "• This estimate is valid for 30 days from date of issue",
            "• Material prices subject to change",
            "• Quantities are approximate and subject to site verification",
            "",
            "4. NOTES",
            "",
            "• Generated by QuantiBot AI",
            f"• Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "• For any queries, contact: support@quantibot.ai",
        ]
        
        for text in assumptions:
            ws[f'A{row}'] = text
            if text.startswith(('1.', '2.', '3.', '4.')):
                ws[f'A{row}'].font = Font(bold=True, size=11)
            row += 1
        
        ws.column_dimensions['A'].width = 80
    
    def generate_pdf(self, excel_file: str) -> str:
        """
        Convert Excel to PDF
        (Requires additional library like openpyxl or reportlab)
        
        Args:
            excel_file: Path to Excel file
        
        Returns:
            Path to PDF file
        """
        # Placeholder - implement PDF generation
        # Options:
        # 1. Use reportlab to create PDF from scratch
        # 2. Use openpyxl to convert Excel to PDF
        # 3. Use external service like CloudConvert
        
        pdf_file = excel_file.replace('.xlsx', '.pdf')
        
        # TODO: Implement PDF generation
        
        return pdf_file


# Utility function
def create_boq(project, quantities, cost_items, region="pakistan", currency="PKR"):
    """Convenience function to generate BOQ"""
    generator = BOQGenerator()
    excel_file = generator.generate_excel(project, quantities, cost_items, region, currency)
    return excel_file
