from typing import Dict, List, Any
from datetime import datetime
import difflib

class ChangeTracker:
    """Tracks and manages changes made during document merging"""
    
    def __init__(self):
        self.changes = []
    
    def track_change(self, field: str, old_value: str, new_value: str, description: str) -> Dict[str, Any]:
        """Track a single change"""
        change = {
            'id': len(self.changes) + 1,
            'field': field,
            'old_value': old_value,
            'new_value': new_value,
            'description': description,
            'timestamp': datetime.now().isoformat(),
            'change_type': self._determine_change_type(old_value, new_value)
        }
        
        self.changes.append(change)
        return change
    
    def _determine_change_type(self, old_value: str, new_value: str) -> str:
        """Determine the type of change"""
        if not old_value and new_value:
            return 'addition'
        elif old_value and not new_value:
            return 'deletion'
        elif old_value != new_value:
            return 'modification'
        else:
            return 'no_change'
    
    def get_text_diff(self, old_text: str, new_text: str) -> List[str]:
        """Generate a detailed diff between two text strings"""
        differ = difflib.unified_diff(
            old_text.splitlines(keepends=True),
            new_text.splitlines(keepends=True),
            fromfile='original',
            tofile='modified',
            lineterm=''
        )
        return list(differ)
    
    def generate_summary(self, changes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate a comprehensive summary of all changes"""
        if not changes:
            return {
                'total_changes': 0,
                'change_types': {},
                'fields_modified': [],
                'summary': 'No changes were made to the document.'
            }
        
        # Count change types
        change_types = {
            'additions': 0,
            'modifications': 0,
            'deletions': 0
        }
        
        fields_modified = set()
        
        for change in changes:
            change_type = change['change_type']
            if change_type == 'addition':
                change_types['additions'] += 1
            elif change_type == 'modification':
                change_types['modifications'] += 1
            elif change_type == 'deletion':
                change_types['deletions'] += 1
            
            fields_modified.add(change['field'])
        
        # Generate summary text
        summary_parts = []
        if change_types['additions'] > 0:
            summary_parts.append(f"{change_types['additions']} addition(s)")
        if change_types['modifications'] > 0:
            summary_parts.append(f"{change_types['modifications']} modification(s)")
        if change_types['deletions'] > 0:
            summary_parts.append(f"{change_types['deletions']} deletion(s)")
        
        summary_text = f"Document successfully merged with {', '.join(summary_parts)}."
        
        return {
            'total_changes': len(changes),
            'change_types': change_types,
            'fields_modified': list(fields_modified),
            'summary': summary_text,
            'timestamp': datetime.now().isoformat()
        }
    
    def format_change_for_display(self, change: Dict[str, Any]) -> Dict[str, Any]:
        """Format a change for display in the UI"""
        return {
            'id': change['id'],
            'field': self._format_field_name(change['field']),
            'description': change['description'],
            'change_type': change['change_type'],
            'old_value': self._truncate_text(change['old_value'], 200),
            'new_value': self._truncate_text(change['new_value'], 200),
            'timestamp': change['timestamp']
        }
    
    def _format_field_name(self, field: str) -> str:
        """Format field names for display"""
        field_names = {
            'vessel_name': 'Vessel Name',
            'charter_date': 'Charter Date',
            'owner_details': 'Owner Details',
            'charterer_details': 'Charterer Details',
            'charter_period': 'Charter Period',
            'delivery_port': 'Delivery Port',
            'laycan': 'Laycan Period',
            'trading_exclusions': 'Trading Exclusions',
            'dry_docking': 'Dry-Docking Clause'
        }
        return field_names.get(field, field.replace('_', ' ').title())
    
    def _truncate_text(self, text: str, max_length: int) -> str:
        """Truncate text for display"""
        if not text:
            return ''
        if len(text) <= max_length:
            return text
        return text[:max_length] + '...'
    
    def export_changes_to_dict(self) -> List[Dict[str, Any]]:
        """Export all changes as a list of dictionaries"""
        return [self.format_change_for_display(change) for change in self.changes]
