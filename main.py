import argparse

from pathlib import Path
from converter.converter import Converter
from converter.spell import LssSpell, TTGSpell

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Создание карточек заклинаний для DnD')
    parser.add_argument('--spell_path', dest='spell_path', type=str, required=True,
                        help='Путь к файлу, где содержатся названия заклинаний или ссылки на них')
    
    parser.add_argument('--output_file', dest='output_file', type=str, required=True,
                        help='Файл с карточками заклинаний')
    
    parser.add_argument('--parser', dest='parser', choices=('lss', 'ttg_api'), default='ttg_api', type=str,
                        help='Какой парсер использовать')
    
    parser.add_argument('--cache_path', dest='cache_path', default='.cache', type=str,
                        help='Путь к кэшу')

    args = parser.parse_args()
    if args.parser == 'lss':
        parser_class = LssSpell
    elif args.parser == 'ttg_api':
        parser_class = TTGSpell

    converter = Converter(Path(args.spell_path), parser_class, Path(args.cache_path))
    converter.create_presentation(Path(args.output_file))