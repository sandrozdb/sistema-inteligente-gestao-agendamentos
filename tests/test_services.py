import sys
import unittest
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from services import (  # noqa: E402
    horarios_conflitam,
    texto_obrigatorio,
    validar_email,
    validar_data_hora,
    validar_preco,
    validar_status,
)


class RegrasDeNegocioTest(unittest.TestCase):
    def test_texto_obrigatorio(self):
        self.assertEqual(texto_obrigatorio("  Sandro ", "Nome"), "Sandro")
        with self.assertRaises(ValueError):
            texto_obrigatorio(" ", "Nome")

    def test_email(self):
        self.assertEqual(validar_email("sandro@example.com"), "sandro@example.com")
        with self.assertRaises(ValueError):
            validar_email("email-invalido")

    def test_preco(self):
        self.assertEqual(str(validar_preco("35,50")), "35.50")
        with self.assertRaises(ValueError):
            validar_preco("0")

    def test_status(self):
        self.assertEqual(validar_status("AGENDADO"), "agendado")
        with self.assertRaises(ValueError):
            validar_status("pendente")

    def test_conflito_de_horario(self):
        base = datetime(2026, 8, 20, 10, 0)
        self.assertTrue(horarios_conflitam(base, 60, base.replace(minute=30), 30))
        self.assertFalse(horarios_conflitam(base, 30, base.replace(minute=30), 30))

    def test_data_hora(self):
        self.assertEqual(validar_data_hora("20/08/2026 14:30"), datetime(2026, 8, 20, 14, 30))
        with self.assertRaises(ValueError):
            validar_data_hora("2026-08-20")


if __name__ == "__main__":
    unittest.main()
