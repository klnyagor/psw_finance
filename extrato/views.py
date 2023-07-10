from django.shortcuts import render, redirect
from perfil.models import Conta, Categoria
from .models import Valores
from django.contrib import messages
from django.contrib.messages import constants
from datetime import datetime, timedelta
from django.template.loader import render_to_string
import os
from django.conf import settings
from weasyprint import HTML
from io import BytesIO
from django.http import FileResponse
# Create your views here.

def novo_valor(request):
    if request.method == "GET":
        contas = Conta.objects.all()
        categorias = Categoria.objects.all()
        
        return render(request, 'novo_valor.html', {'contas': contas, 'categorias': categorias})
    elif request.method == "POST":
        valor = request.POST.get('valor')
        categoria = request.POST.get('categoria')
        descricao = request.POST.get('descricao')
        data = request.POST.get('data')
        conta = request.POST.get('conta')
        tipo = request.POST.get('tipo')
        
        valores = Valores(
            valor=valor,
            categoria_id=categoria,
            descricao=descricao,
            data=data,
            conta_id=conta,
            tipo=tipo,

        )

        valores.save()

        conta = Conta.objects.get(id=conta)

        if tipo == 'E':
            conta.valor += int(valor)
            msg = "Entrada cadastrada com sucesso"
        else:
            conta.valor -= int(valor)
            msg = "Saida cadastrada com sucesso"

        conta.save()

        messages.add_message(request, constants.SUCCESS, msg)
        return redirect('/extrato/novo_valor')
 
def view_extrato(request):
    contas = Conta.objects.all()
    categorias = Categoria.objects.all()
    valores = Valores.objects.all()

    conta_get = request.GET.get('conta')
    categoria_get = request.GET.get('categoria')
    periodo_get = request.GET.get('periodo')

    #Filtrar por periodo
    if(periodo_get == "1"):
        valores = valores.filter(data__month=datetime.now().month)
    elif(periodo_get == "2"):
        #data__range = [inicio, fim]
        valores = valores.filter(data__range=[datetime.today()-timedelta(days=7), datetime.today()])
    elif(periodo_get == "3"):
        valores = valores.filter(data=datetime.today())

    if conta_get:
        valores = valores.filter(conta__id=conta_get)
    if categoria_get:
        valores = valores.filter(categoria__id=categoria_get)
 
    return render(request, 'view_extrato.html', {'valores': valores, 'contas': contas, 'categorias': categorias})

def exportar_pdf(request):
    valores = Valores.objects.filter(data__month=datetime.now().month)
    contas = Conta.objects.all()
    categorias = Categoria.objects.all()
    
    path_template = os.path.join(settings.BASE_DIR, 'templates/partials/extrato.html')
    path_output = BytesIO()

    template_render = render_to_string(path_template, {'valores': valores, 'contas': contas, 'categorias': categorias})
    HTML(string=template_render).write_pdf(path_output)

    path_output.seek(0)

    return FileResponse(path_output, filename="extrato.pdf")