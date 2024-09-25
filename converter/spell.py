import json
from dataclasses import dataclass
from enum import StrEnum
from typing import Any

@dataclass
class Activation:
    type: str 
    cost: int
    condition: str


@dataclass
class Duration:
    value: int | None
    units: str


@dataclass
class SaveThrow:
    ability: str
    dc: int | None
    scaling: str


@dataclass
class Components:
    vocal: bool
    somatic: bool
    material: bool
    ritual: bool
    concentration: bool
    value: str


@dataclass
class Materials:
    value: str
    consumed: bool
    cost: int
    supply: int


class Spell:
    def __init__(self, spell_json: str | dict[str, Any]):
        self._load(spell_json)

    def _load(self, spell_json: str | dict[str, Any]):
        if isinstance(spell_json, str):
            spell_json = json.loads(spell_json)
        
        self.name = spell_json['name']
        self.classes = spell_json['classes']
        system = spell_json['system']
        self.description = self._convert_description(system['description']['value'])
        self.source = system['source']
        self.activation = Activation(**system['activation'])
        self.duration = Duration(**system['duration'])
        self.range = system['range']['value']
        self.action_type = system['actionType']
        self.attack_bonus = system['attackBonus']
        self.save_throw = SaveThrow(**system['save'])
        self.level = system['level']
        self.school = system['school']
        self.components = Components(**system['components'])
        self.materials = Materials(**system['materials'])

    
    def _convert_description(self, description: str):
        return description