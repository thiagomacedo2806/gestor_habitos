import os
import django
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "manage")
django.setup()

from django.test import TestCase, Client
from habitos import Habito

class HabitosTestCase(TestCase):
    """
    Conjunto de testes automatizados para verificar as operações do Gestor de Hábitos.
    """
    def setUp(self) -> None: 
        self.client = Client()

    def test_fluxo_gerenciamento_habitos(self) -> None:
        payload = {
            "nome": "Beber 3L de água",
            "frequencia_semanal": 7,
            "concluido_hoje": True
        }
        response_criar = self.client.post(
            "/criar/",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(response_criar.status_code, 201)
        self.assertIn("id", response_criar.json())

        response_listar = self.client.get("/")
        self.assertEqual(response_listar.status_code, 200)
        habitos = response_listar.json()
        self.assertEqual(len(habitos), 1)
        self.assertEqual(habitos[0]["nome"], "Beber 3L de água")
        self.assertEqual(habitos[0]["frequencia_semanal"], 7)

        response_invalido_nome = self.client.post(
            "/criar/",
            data=json.dumps({"frequencia_semanal": 5}),
            content_type="application/json"
        )
        self.assertEqual(response_invalido_nome.status_code, 400)

        response_invalido_frequencia = self.client.post(
            "/criar/",
            data=json.dumps({"nome": "Malhar", "frequencia_semanal": 10}),
            content_type="application/json"
        )
        self.assertEqual(response_invalido_frequencia.status_code, 400)