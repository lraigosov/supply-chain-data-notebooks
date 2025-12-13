#!/usr/bin/env python
"""
CLI principal unificado para todas las utilidades de notebooks.

Uso:
    python -m scripts <comando> [opciones]

Comandos disponibles:
    catalog            - Navegar y ejecutar notebooks del catálogo
    validate           - Validar estructura y metadatos de notebooks
    export-html        - Exportar catálogo a HTML
    update-navigation  - Actualizar navegación de notebooks
    smoke-test         - Ejecutar tests rápidos de notebooks
    validate-reqs      - Validar requirements.lock

Ejemplos:
    python -m scripts catalog list
    python -m scripts validate
    python -m scripts export-html
    python -m scripts update-navigation
    python -m scripts smoke-test
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Add scripts to path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def main():
    """Entry point for unified CLI."""
    parser = argparse.ArgumentParser(
        description="Utilidades para gestión de notebooks del proyecto",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Comando a ejecutar")
    
    # Catalog commands
    catalog_parser = subparsers.add_parser(
        "catalog",
        help="Gestionar catálogo de notebooks"
    )
    catalog_parser.add_argument("action", nargs="?", help="Acción: list, show, run, search")
    catalog_parser.add_argument("--specialty", help="Filtrar por especialidad")
    catalog_parser.add_argument("--level", help="Filtrar por nivel")
    catalog_parser.add_argument("--tags", help="Filtrar por tags (separados por coma)")
    catalog_parser.add_argument("args", nargs="*", help="Argumentos adicionales")
    
    # Validate commands
    validate_parser = subparsers.add_parser(
        "validate",
        help="Validar notebooks"
    )
    validate_parser.add_argument(
        "--type",
        choices=["metadata", "structure", "all"],
        default="all",
        help="Tipo de validación"
    )
    
    # Export HTML command
    export_parser = subparsers.add_parser(
        "export-html",
        help="Exportar catálogo a HTML"
    )
    export_parser.add_argument(
        "--output",
        help="Ruta de salida para el HTML"
    )
    
    # Update navigation command
    nav_parser = subparsers.add_parser(
        "update-navigation",
        help="Actualizar navegación de notebooks"
    )
    
    # Smoke test command
    smoke_parser = subparsers.add_parser(
        "smoke-test",
        help="Ejecutar tests rápidos de notebooks"
    )
    smoke_parser.add_argument(
        "--ids",
        help="IDs de notebooks a testear (separados por coma)"
    )
    smoke_parser.add_argument(
        "--timeout",
        type=int,
        default=300,
        help="Timeout en segundos"
    )
    
    # Validate requirements command
    reqs_parser = subparsers.add_parser(
        "validate-reqs",
        help="Validar requirements.lock"
    )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0
    
    # Dispatch to appropriate module
    if args.command == "catalog":
        from scripts.catalog import main as catalog_main
        # Reconstruct argv for catalog module
        sys.argv = ["catalog"] + ([args.action] if args.action else []) + args.args
        if args.specialty:
            sys.argv.extend(["--specialty", args.specialty])
        if args.level:
            sys.argv.extend(["--level", args.level])
        if args.tags:
            sys.argv.extend(["--tags", args.tags])
        return catalog_main()
    
    elif args.command == "validate":
        if args.type in ["metadata", "all"]:
            from scripts.validate_notebook_metadata import main as validate_meta
            print("🔍 Validando metadatos...")
            sys.argv = ["validate_notebook_metadata"]
            validate_meta()
        
        if args.type in ["structure", "all"]:
            from scripts.validate_notebook_structure import main as validate_struct
            print("\n🔍 Validando estructura...")
            sys.argv = ["validate_notebook_structure"]
            validate_struct()
        
        return 0
    
    elif args.command == "export-html":
        from scripts.export_catalog_html import main as export_main
        sys.argv = ["export_catalog_html"]
        if args.output:
            sys.argv.extend(["--output", args.output])
        return export_main()
    
    elif args.command == "update-navigation":
        from scripts.update_navigation import main as nav_main
        return nav_main()
    
    elif args.command == "smoke-test":
        from scripts.smoke_test_notebooks import main as smoke_main
        sys.argv = ["smoke_test_notebooks"]
        if args.ids:
            sys.argv.extend(["--ids", args.ids])
        if args.timeout:
            sys.argv.extend(["--timeout", str(args.timeout)])
        return smoke_main()
    
    elif args.command == "validate-reqs":
        from scripts.validate_requirements import main as reqs_main
        return reqs_main()
    
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
