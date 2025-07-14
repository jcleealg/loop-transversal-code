import ast
import sys
import shlex

import typer

from greedy_syndrome_mapper import GreedySyndromeMapper

app = typer.Typer()

def load_patterns(error_patterns: str = None, file: str = None, standard_basis: int = None):
    if error_patterns:
        # Directly parse string to list[list[int]]
        return ast.literal_eval(error_patterns)
    elif file:
        with open(file, 'r') as f:
            lines = f.readlines()
            return [ast.literal_eval(line.strip()) for line in lines if line.strip()]
    elif standard_basis is not None:
        # Generate standard_basis
        n = standard_basis
        return [[int(i == j) for i in range(n)] for j in range(n)]
    else:
        raise typer.BadParameter("Please provide --error-patterns, --file, or --standard-basis.")


@app.command()
def full_syndrome_mapping(error_patterns: str = typer.Option(None), file: str = typer.Option(None), standard_basis: int = typer.Option(None)):
    """
    Print full syndrome mapping for error patterns (from error_patterns, file, or standard_basis).
    """
    loaded_error_patterns = load_patterns(error_patterns, file, standard_basis)
    mapper = GreedySyndromeMapper(loaded_error_patterns)
    print("Full syndrome mapping (vector -> syndrome):")
    for vector, syndrome in sorted(mapper.syndrome_map.items()):
        print(f"  {vector} -> {syndrome}")

@app.command()
def basis_mapping(error_patterns: str = typer.Option(None), file: str = typer.Option(None), standard_basis: int = typer.Option(None)):
    """
    Print basis mapping for error patterns (from error_patterns, file, or standard_basis).
    """
    loaded_error_patterns = load_patterns(error_patterns, file, standard_basis)
    mapper = GreedySyndromeMapper(loaded_error_patterns)
    print("Basis mapping in original format:")
    basis_map = mapper.get_basis_map_list()
    for basis_v, syndrome_v in basis_map:
        print(f"  {basis_v} -> {syndrome_v}")

@app.command()
def parity_check_matrix(error_patterns: str = typer.Option(None), file: str = typer.Option(None), standard_basis: int = typer.Option(None)):
    """
    Print parity check matrix for error patterns (from error_patterns, file, or standard_basis).
    """
    loaded_error_patterns = load_patterns(error_patterns, file, standard_basis)
    mapper = GreedySyndromeMapper(loaded_error_patterns)
    print("Parity check matrix:")
    matrix = mapper.get_parity_check_matrix()
    print(matrix)


# Create a command that combines all three functionalities
@app.command()
def all_mapping(error_patterns: str = typer.Option(None), file: str = typer.Option(None), standard_basis: int = typer.Option(None)):
    """
    Print all mappings: full syndrome mapping, basis mapping, and parity check matrix.
    """
    loaded_error_patterns = load_patterns(error_patterns, file, standard_basis)
    mapper = GreedySyndromeMapper(loaded_error_patterns)
    print("Full syndrome mapping (vector -> syndrome):")
    for vector, syndrome in sorted(mapper.syndrome_map.items()):
        print(f"  {vector} -> {syndrome}")
    print("\nBasis mapping in original format:")
    basis_map = mapper.get_basis_map_list()
    for basis_v, syndrome_v in basis_map:
        print(f"  {basis_v} -> {syndrome_v}")
    print("\nParity check matrix:")
    matrix = mapper.get_parity_check_matrix()
    print(matrix)



if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("No command-line arguments detected.")
        cmd = input("Please enter CLI command and options (e.g. all-mapping --error-patterns [[0,0,0,0,0,1],[0,0,0,0,1,0],[0,0,0,0,1,1],[0,0,0,1,0,0],[0,0,0,1,1,0],[0,0,1,0,0,0],[0,0,1,1,0,0],[0,1,0,0,0,0],[0,1,1,0,0,0],[1,0,0,0,0,0],[1,1,0,0,0,0]]):\n")
        sys.argv += shlex.split(cmd)
    try:
        app()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        input("Press Enter to exit...")
