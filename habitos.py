from django.db import models
from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
import json

class Habito(models.Model):
    """
    Modelo simplificado que representa um hábito diário a ser monitorado.
    """
    nome = models.CharField(max_length=150)
    frequencia_semanal = models.IntegerField(default=7)
    concluido_hoje = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "habitos"

    def __str__(self) -> str:
        return self.nome

def listar_habitos(request: HttpRequest) -> JsonResponse:
    """
    Retorna todos os hábitos cadastrados no banco de dados.
    """
    habitos = list(Habito.objects.values("id", "nome", "frequencia_semanal", "concluido_hoje"))
    return JsonResponse(habitos, safe=False, json_dumps_params={"ensure_ascii": False})

@csrf_exempt
def criar_habito(request: HttpRequest) -> JsonResponse:
    """
    Cria um novo hábito através de uma requisição POST com dados JSON.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            if not data.get("nome"):
                return JsonResponse({"erro": "O nome é obrigatório"}, status=400)
            
            try:
                frequencia = int(data.get("frequencia_semanal", 7))
                if frequencia < 1 or frequencia > 7:
                    return JsonResponse({"erro": "A frequência semanal deve ser entre 1 e 7"}, status=400)
            except (ValueError, TypeError):
                return JsonResponse({"erro": "Frequência semanal inválida"}, status=400)

            habito = Habito.objects.create(
                nome=data.get("nome"),
                frequencia_semanal=frequencia,
                concluido_hoje=bool(data.get("concluido_hoje", False))
            )
            return JsonResponse({"id": habito.id, "status": "criado"}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"erro": "JSON inválido"}, status=400)
        except Exception as e:
            return JsonResponse({"erro": str(e)}, status=500)
            
    return JsonResponse({"erro": "Método não permitido"}, status=405)