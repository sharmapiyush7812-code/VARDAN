import json
import uuid
from pathlib import Path
from django.conf import settings
from datetime import datetime
import threading

# Thread lock for safe concurrent JSON access
_file_locks = {}

class JsonStorage:
    """Safe JSON file storage abstraction layer for MVP data persistence."""
    
    @staticmethod
    def _get_lock(filename):
        """Get or create a lock for a specific file."""
        if filename not in _file_locks:
            _file_locks[filename] = threading.Lock()
        return _file_locks[filename]
    
    @staticmethod
    def _get_file_path(filename):
        """Get the full path to a data file."""
        data_dir = settings.DATA_DIR
        data_dir.mkdir(exist_ok=True)
        return data_dir / f'{filename}.json'
    
    @staticmethod
    def read(filename):
        """Read and parse a JSON file."""
        filepath = JsonStorage._get_file_path(filename)
        lock = JsonStorage._get_lock(filename)
        
        with lock:
            try:
                if not filepath.exists():
                    return []
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error reading {filename}: {e}")
                return []
    
    @staticmethod
    def write(filename, data):
        """Write data to a JSON file safely."""
        filepath = JsonStorage._get_file_path(filename)
        lock = JsonStorage._get_lock(filename)
        
        with lock:
            try:
                # Write to temporary file first
                temp_path = filepath.with_suffix('.tmp')
                with open(temp_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                # Atomic rename
                temp_path.replace(filepath)
                return True
            except IOError as e:
                print(f"Error writing {filename}: {e}")
                return False
    
    @staticmethod
    def find_by_id(filename, object_id):
        """Find an object by ID in a JSON file."""
        data = JsonStorage.read(filename)
        if isinstance(data, dict):
            return data.get(object_id)
        elif isinstance(data, list):
            return next((obj for obj in data if obj.get('id') == object_id), None)
        return None
    
    @staticmethod
    def append(filename, obj):
        """Append an object to a JSON array file."""
        data = JsonStorage.read(filename)
        if not isinstance(data, list):
            data = []
        data.append(obj)
        return JsonStorage.write(filename, data)
    
    @staticmethod
    def update(filename, object_id, updates):
        """Update an object in a JSON file."""
        data = JsonStorage.read(filename)
        
        if isinstance(data, dict):
            if object_id in data:
                data[object_id].update(updates)
                return JsonStorage.write(filename, data), data[object_id]
        elif isinstance(data, list):
            for obj in data:
                if obj.get('id') == object_id:
                    obj.update(updates)
                    JsonStorage.write(filename, data)
                    return True, obj
        return False, None
    
    @staticmethod
    def delete(filename, object_id):
        """Delete an object from a JSON file."""
        data = JsonStorage.read(filename)
        
        if isinstance(data, dict):
            if object_id in data:
                del data[object_id]
                return JsonStorage.write(filename, data)
        elif isinstance(data, list):
            initial_len = len(data)
            data = [obj for obj in data if obj.get('id') != object_id]
            if len(data) < initial_len:
                return JsonStorage.write(filename, data)
        return False
    
    @staticmethod
    def filter(filename, predicate):
        """Filter objects in a JSON file by a predicate function."""
        data = JsonStorage.read(filename)
        if isinstance(data, list):
            return [obj for obj in data if predicate(obj)]
        elif isinstance(data, dict):
            return [obj for key, obj in data.items() if predicate(obj)]
        return []


class StorageService:
    """High-level service for managing all app data."""
    
    @staticmethod
    def generate_id(prefix):
        """Generate a unique ID with a prefix."""
        return f"{prefix}-{str(uuid.uuid4())[:8]}"
    
    @staticmethod
    def get_timestamp():
        """Get current ISO timestamp."""
        return datetime.utcnow().isoformat() + 'Z'
