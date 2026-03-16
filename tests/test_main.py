import pandas as pd

from app.main import execute_operations, main


def test_execute_operations_with_multiple_rows(capsys):
    """Test execute_operations with multiple operations to cover all lines."""
    df = pd.DataFrame(
        {
            "operation": ["add", "sub", "square", "add", "square"],
            "a": [3, 6, 8, 10, 4],
            "b": [5, 3, None, 2, None],
        }
    )

    # Appel de la fonction
    execute_operations(df)

    # Capture l'affichage
    captured = capsys.readouterr()

    # Vérifie que chaque opération est exécutée avec float
    assert "add(3, 5.0) = 8.0" in captured.out
    assert "sub(6, 3.0) = 3.0" in captured.out
    assert "square(8, nan) = 64" in captured.out
    assert "add(10, 2.0) = 12.0" in captured.out
    assert "square(4, nan) = 16" in captured.out


def test_main_function_creates_csv(tmp_path, monkeypatch, capsys):
    """Test the full main function with CSV reading/writing."""
    # Préparer un chemin temporaire pour le CSV
    csv_file = tmp_path / "moncsv.csv"

    # Données d’exemple
    data = pd.DataFrame(
        {
            "operation": ["add", "sub", "square"],
            "a": [1, 5, 3],
            "b": [2, 2, None],
        }
    )
    data.to_csv(csv_file, index=False)

    # Remplacer temporairement le chemin CSV dans main
    monkeypatch.setattr("app.main.CSV_FILE_PATH", csv_file)

    # Exécuter main()
    main()

    # Vérifier que les résultats sont affichés
    captured = capsys.readouterr()
    assert "add(1, 2.0) = 3.0" in captured.out
    assert "sub(5, 2.0) = 3.0" in captured.out
    assert "square(3, nan) = 9" in captured.out
