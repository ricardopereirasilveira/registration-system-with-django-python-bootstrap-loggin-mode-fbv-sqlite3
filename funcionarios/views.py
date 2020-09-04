from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Funcionario
from .formulario import FormularioFuncionario

from loggin import log
from datetime import datetime
from . import funcs


infoLOG = log.LogginMIX()

# TODO: Inserir a página bootstrap personalizada
@login_required
def adicionarFuncionario(request):
    user = request.user.username
    form = FormularioFuncionario(request.POST or None)
    infoLOG.imprimirINFO(datetime.now(), user, 'visitou a sessao de adicionar Funcinário')
    if form.is_valid():
        try:
            form.save()
            infoLOG.imprimirINFO(datetime.now(), user,
                f'adicionou um usuario chamado: {form.cleaned_data["primeiroNome"]} {form.cleaned_data["ultimoNome"]}')
            return redirect('listFunc')
        except Exception as e:
            infoLOG.imprimirERROR(f'{datetime.now()}', user, f'falhou um usuario chamado: {form.cleaned_data["primeiroNome"]} {form.cleaned_data["ultimoNome"]}\n {e}')
    return render(request, 'adicionarfuncionario.html', {'form': form})


# TODO: Inserir a busca por clientes por campo nome & sobrenome
@login_required
def listarFuncionario(request):
    saudacao = funcs.saudacao()
    user = request.user.username
    try:
        infoLOG.imprimirINFO(f'{datetime.now()}', user,
                             f'visitou a sessao de ListarFuncionario')
        func = Funcionario.objects.all()
        return render(request, 'listarfuncionario.html', {'func': func, 'saudacao': saudacao})
    except Exception as e:
        infoLOG.imprimirERROR(f'{datetime.now()}',
                              user,
                              'a Sessao de listarFuncionarios falhou ao carregar o banco de dados!')
        return render(request, 'listarfuncionario.html', {'func': func, 'saudacao': saudacao})


# TODO: Inserir a página bootstrap personalizada.
@login_required
def editarFuncionario(request, id):
    user = request.user.username
    func = get_object_or_404(Funcionario, pk=id)
    form = FormularioFuncionario(request.POST or None, request.FILES or None, instance=func)
    infoLOG.imprimirINFO(f'{datetime.now()}', user,
                         f'Entrou na tela de edição do {func}')
    if form.is_valid():
        try:
            form.save()
            infoLOG.imprimirINFO(f'{datetime.now()}',
                                 user,
                                 f'O usuário {form.cleaned_data["primeiroNome"]} foi alterado!')
            return redirect('listFunc')
        except Exception as e:
            pass
    return render(request, 'adicionarfuncionario.html', {'form': form})


# TODO: Inserir a página bootstrap personalizada
@login_required
def deletarFuncionario(request, id):
    user = request.user.username
    func = get_object_or_404(Funcionario, pk=id)
    infoLOG.imprimirINFO(f'{datetime.now()}', user,
            f'Entrou na tela de confirmação para deletar o {func}')
    if request.method == 'POST':
        try:
            infoLOG.imprimirINFO(f'{datetime.now()}', user,
                                 f'O usuário {func} foi DELETADO.'
                                 )
            func.delete()
            return redirect('listFunc')
        except Exception as e:
            pass
    return render(request, 'deletarfuncionario.html', {'func': func})

