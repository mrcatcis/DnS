import abc
import json
from dataclasses import dataclass
from enum import StrEnum
from typing import Any
import re


@dataclass
class Components:
    vocal: bool
    somatic: bool
    material: str | None
    ritual: bool
    concentration: bool


class BaseSpell(abc.ABC):
    name: str
    classes: tuple[str]
    description: str
    source: str
    activation: str
    duration: str
    range: str
    level: int
    school: str
    components: Components

    def __init__(self, spell_json: str | dict[str, Any], *args, **kwargs):
        self._load(spell_json)

    @abc.abstractmethod
    def _load(self, spell_json: str | dict[str, Any]):
        pass

    
class LssSpell(BaseSpell):
    def _load(self, spell_json: str | dict[str, Any]):
        if isinstance(spell_json, str):
            spell_json = json.loads(spell_json)
        
        self.name = spell_json['name']
        self.classes = tuple(spell_json['classes'])
        system = spell_json['system']
        self.description = self._convert_description(system['description']['value'])

        self.source = system['source']
        self.activation = f"{system['activation']['cost']} {system['activation']['type']}"
        duration = system['duration']
        if duration['units'] == 'inst':
            self.duration = 'Мгновенная'
        else:
            self.duration = f"{duration['value']} {duration['units']}"
            
        self.range = f"{system['range']['value']} {system['range']['value']}"
        self.level = system['level']
        self.school = system['school']
        components = system['components']
        self.components = Components(
            vocal=components['vocal'],
            somatic=components['somatic'],
            ritual=components['ritual'],
            concentration=components['concentration'],
            material=system['components']['value']
        )

    
    def _convert_description(self, description: str):
        return description
    

class TTGSpell(BaseSpell):
    def _load(self, spell_json: str | dict[str, Any]):
        if isinstance(spell_json, str):
            spell_json = json.loads(spell_json)
        
        self.name = spell_json['name']['rus']
        self.classes = tuple(class_['name'] for class_ in spell_json['classes'])
        self.description = self._convert_description(spell_json['description'] + spell_json.get('upper', ''))

        self.source = spell_json['source']['shortName']
        self.activation = spell_json['time']
        self.duration = spell_json['duration']
            
        self.range = spell_json['range']
        self.level = spell_json['level']
        self.school = spell_json['school']
        self.components = Components(
            vocal=spell_json['components'].get('v', False),
            somatic=spell_json['components'].get('s', False),
            ritual=spell_json.get('ritual', False),
            concentration=spell_json.get('concentration', False),
            material=spell_json['components'].get('m', None)
        )

    
    def _convert_description(self, description: str):
        description = description.replace('<p>', '')
        description = description.replace('</p>', '\v')        
        description = description.replace('<blockquote>', '')
        description = description.replace('</blockquote>', '\v')        
        description = description.replace('<ul>', '')
        description = description.replace('</ul>', '\v')        
        description = description.replace('&nbsp;', '')        
        description = description.replace('&laquo;', '"')        
        description = description.replace('&raquo;', '"')        

        description = re.sub(
            r'<detail-tooltip type=".+?"><a href=".+?">(.+?)</a></detail-tooltip>',
            r'\1',
            description,
        )

        description = re.sub(
            r'<a href=".+?">(.+?)</a>',
            r'\1',
            description,
        )

        description = re.sub(
            r'<li>(.+?)</li>',
            '· \\1\v',
            description,
        )
        

        description = re.sub(
            r'<span class=\"saving_throw\">([а-яА-ЯёЁ\s]+)</span>',
            '\n#!save_throw\\1\n',
            description,
        )

        description = re.sub(
            r'<span class=\"disadvantage\">([а-яА-ЯёЁ\s]+)</span>',
            '\n#dd0000\\1\n',
            description,
        )

        description = re.sub(
            r'<span class=\"advantage\">([а-яА-ЯёЁ\s]+)</span>',
            '\n#00dd00\\1\n',
            description,
        )

        description = re.sub(
            r'<dice-roller formula=".+?"( label=".+?")?>(.+?)</dice-roller>',
            r'\2',
            description,
        )

        description = re.sub(
            r'<span .+?=".+?">(.+?)</span>',
            '\n\\1\n',
            description,
        )
        
        description = re.sub(
            r'(\d*к\d+)+',
            '\n#3333ff\\1\n',
            description,
        )

        description = re.sub(
            r'<strong>(.+?)</strong>',
            '\n#!bold\\1\n',
            description,
        )

        description = re.sub(
            r'<em>(.+?)</em>',
            '\n#!italic\\1\n',
            description,
        )


        return description


