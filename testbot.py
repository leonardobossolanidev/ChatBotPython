import unittest
from io import StringIO
import sys
import time

# Supondo que você tenha o script principal salvo como `bot_frutas.py`
from bot_frutas import (
    registrar_compra,
    calcular_total,
    carrinho,
    bot_fala,
    estoque,
    exibir_resumo,
)

class TestBotFrutas(unittest.TestCase):

    def setUp(self):
        """Executado antes de cada teste para garantir estado limpo."""
        carrinho.clear()

    def test_registrar_compra_adiciona_itens(self):
        registrar_compra("maçã", 2)  # 2 x 3.50 = 7.00
        self.assertEqual(len(carrinho), 1)
        self.assertEqual(carrinho[0]['fruta'], "maçã")
        self.assertEqual(carrinho[0]['quantidade'], 2)
        self.assertEqual(carrinho[0]['preco'], estoque["maçã"])

    def test_calcular_total_funciona(self):
        registrar_compra("maçã", 2)    # 7.00
        registrar_compra("banana", 1)  # 2.00
        total = calcular_total()
        self.assertAlmostEqual(total, 9.00, places=2)

    def test_total_sem_compras(self):
        self.assertEqual(calcular_total(), 0)

    def test_bot_fala_saida_terminal(self):
        captured_output = StringIO()
        sys.stdout = captured_output
        bot_fala("Mensagem de teste")
        sys.stdout = sys.__stdout__
        self.assertIn("🤖 Bot: Mensagem de teste", captured_output.getvalue())

    def test_exibir_resumo_saida(self):
        registrar_compra("banana", 1)
        captured_output = StringIO()
        sys.stdout = captured_output
        exibir_resumo()
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("banana", output)
        self.assertIn("Total a pagar", output)

    def test_compra_com_fruta_inexistente(self):
        fruta_falsa = "kiwi"
        self.assertNotIn(fruta_falsa, estoque)

    def test_compra_com_quantidade_zero(self):
        registrar_compra("maçã", 0)
        self.assertEqual(calcular_total(), 0)

    def test_compra_com_quantidade_negativa(self):
        registrar_compra("maçã", -1)
        self.assertEqual(calcular_total(), -3.50)  # tecnicamente, o script original não bloqueia isso ainda

if __name__ == "__main__":
    unittest.main()
