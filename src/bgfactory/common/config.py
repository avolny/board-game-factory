from dataclasses import dataclass

@dataclass
class BGFConfig:
    tolerance: float = 0.1
    
bgfconfig = BGFConfig()