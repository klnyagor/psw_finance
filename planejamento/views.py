from django.shortcuts import render
from perfil.models import Categoria, Conta
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from perfil.utils import calcula_total

# Create your views here.

def definir_planejamento(request):
    categorias = Categoria.objects.all()
    return render(request, 'definir_planejamento.html', {'categorias': categorias})

@csrf_exempt
def update_valor_categoria(request, id):
    novo_valor = json.load(request)['novo_valor']
    categoria = Categoria.objects.get(id=id)
    categoria.valor_planejamento = novo_valor
    categoria.save()

    return JsonResponse({'status': 'Sucesso'})

def ver_planejamento(request):
    categorias = Categoria.objects.all()
    gastos_totais = 0
    for categoria in categorias:
        gastos_totais += categoria.total_gasto()
    
    total_planejamento = calcula_total(categorias, 'valor_planejamento')

    percentual_gasto_total = int((gastos_totais * 100) / total_planejamento)


    return render(request, 'ver_planejamento.html', {'categorias': categorias, 'gastos_totais': gastos_totais, 'total_planejamento': total_planejamento, 'percentual_gasto_total': percentual_gasto_total })

