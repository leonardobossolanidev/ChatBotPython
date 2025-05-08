import unittest
from bot_frutas import calcular_preco, bot_responde  # Importa as funções do bot

class TestBot(unittest.TestCase):

    def test_calculo_preco(self):
        """Testa o cálculo do preço da fruta."""
        preco = calcular_preco("maçã", 2)
        self.assertEqual(preco, 7.00)

    def test_bot_resposta(self):
        """Testa a resposta do bot em relação à entrada."""
        captured_output = StringIO()
        sys.stdout = captured_output
        bot_responde("Olá, cliente!")
        sys.stdout = sys.__stdout__
        self.assertIn("Bot: Olá, cliente!", captured_output.getvalue())

    def test_calculo_preco_invalido(self):
        """Testa se a função de cálculo lida com entradas inválidas."""
        preco = calcular_preco("melancia", 2)
        self.assertIsNone(preco)

if __name__ == "__main__":
    unittest.main()
