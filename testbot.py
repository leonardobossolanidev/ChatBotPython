import unittest
from io import StringIO
import sys

# Importando funções e variáveis do bot
from bot_frutas import registrar_compra, calcular_total, bot_fala, carrinho

class TestBotFrutas(unittest.TestCase):

    def setUp(self):
        """Executa antes de cada teste."""
        carrinho.clear()  # Limpa o carrinho para não haver interferência entre testes

    def test_registrar_compra_e_total(self):
        """Testa se o registro da compra e o total funcionam corretamente."""
        registrar_compra("maçã", 2)  # 2 x 3.50 = 7.00
        registrar_compra("banana", 1)  # 1 x 2.00 = 2.00
        total = calcular_total()
        self.assertEqual(total, 9.00)

    def test_bot_fala_output(self):
        """Testa se a resposta do bot é exibida corretamente."""
        captured_output = StringIO()
        sys.stdout = captured_output
        bot_fala("Teste de resposta")
        sys.stdout = sys.__stdout__
        self.assertIn("🤖 Bot: Teste de resposta", captured_output.getvalue())

    def test_total_sem_compras(self):
        """Testa se o total é zero quando não há compras."""
        self.assertEqual(calcular_total(), 0)

if __name__ == "__main__":
    unittest.main()
