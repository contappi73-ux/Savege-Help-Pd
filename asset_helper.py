
import os
import sys

def get_bundled_asset(filename: str) -> str:
    """
    Retorna o caminho para um asset bundled (dentro do EXE).
    Verifica m�ltiplas localiza��es.
    """
    
    if getattr(sys, 'frozen', False):
        
        base_path = sys._MEIPASS
        candidates = [
            os.path.join(base_path, filename),
            os.path.join(base_path, ".", filename),
        ]
    else:
        
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        candidates = [
            os.path.join(base_path, filename),
            os.path.join(base_path, "ui", filename),
            filename,
        ]
    
    
    for candidate in candidates:
        if os.path.exists(candidate):
            return candidate
    
    
    return candidates[0] if candidates else filename
