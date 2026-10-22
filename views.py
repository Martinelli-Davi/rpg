from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from django.db.models import Q
from .models import Campanha, Personagem
from django.shortcuts import render, redirect, get_object_or_404


# Create your views here.
@login_required(login_url='entrar')


def dashboard(request):
    # Busca campanhas onde o usuário é o mestre OU onde ele está na lista de jogadores
    campanhas = Campanha.objects.filter(
        Q(mestre=request.user) | Q(jogadores=request.user)
    ).distinct()
    
    return render(request, 'dashboard.html', {'campanhas': campanhas})


def entrar(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    return render(request, 'entrar.html')

def detalhes_campanha(request, id):
    # 1. Busca a campanha
    campanha = get_object_or_404(Campanha, id=id)
    
    # 2. Busca todas as fichas vinculadas a essa campanha
    todas_fichas = Personagem.objects.filter(campanha=campanha)
    
    # 3. Separa as fichas por tipo
    fichas_jogadores = todas_fichas.filter(eh_npc=False, eh_criatura=False)
    fichas_npcs = todas_fichas.filter(eh_npc=True, eh_criatura=False)
    fichas_criaturas = todas_fichas.filter(eh_criatura=True)
    
    context = {
        'campanha': campanha,
        'fichas_jogadores': fichas_jogadores,
        'fichas_npcs': fichas_npcs,
        'fichas_criaturas': fichas_criaturas,
    }
    
    return render(request, 'detalhes_campanha.html', context)

def criar_campanha(request):
    if request.method == "POST":
        # 1. Cria o objeto mas não salva no banco ainda (commit=False)
        nova_campanha = Campanha(
            nome=request.POST.get('nome'),
            sistema=request.POST.get('sistema'),
            descricao=request.POST.get('descricao'),
            mestre=request.user # O mestre é quem está logado
        )
        nova_campanha.save() # Agora salva para gerar um ID

        # 2. Adiciona os jogadores (M2M precisa ser depois do save)
        jogadores_ids = request.POST.getlist('jogadores')
        nova_campanha.jogadores.set(jogadores_ids)
        
        return redirect('dashboard')

    # Para carregar a lista de amigos no formulário
    usuarios = User.objects.all()
    return render(request, 'criar_campanha.html', {'todos_os_usuarios': usuarios})


# DELETAR CAMPANHA
def deletar_campanha(request, id):
    campanha = get_object_or_404(Campanha, id=id)
    
    # Segurança: Só o mestre da campanha pode deletar
    if campanha.mestre == request.user:
        campanha.delete()
    
    return redirect('dashboard')

# EDITAR CAMPANHA
@login_required(login_url='entrar')
def editar_campanha(request, id):
    campanha = get_object_or_404(Campanha, id=id)
    
    # Segurança: Só o mestre pode editar
    if campanha.mestre != request.user:
        return redirect('dashboard')

    if request.method == "POST":
        campanha.nome = request.POST.get('nome')
        campanha.sistema = request.POST.get('sistema')
        campanha.descricao = request.POST.get('descricao')
        
        # Atualiza jogadores
        jogadores_ids = request.POST.getlist('jogadores')
        campanha.jogadores.set(jogadores_ids)
        
        campanha.save()
        return redirect('dashboard')

    # Para carregar os dados atuais no formulário
    usuarios = User.objects.all()
    context = {
        'campanha': campanha,
        'todos_os_usuarios': usuarios,
    }
    return render(request, 'editar_campanha.html', context)

@login_required(login_url='entrar')
def criar_ficha(request, id):
    # 1. Busca a campanha onde a ficha será criada
    campanha = get_object_or_404(Campanha, id=id)
    
    # 2. Captura o tipo da URL (?tipo=npc, ?tipo=criatura ou ?tipo=player)
    tipo = request.GET.get('tipo', 'player')
    
    # 3. Define as flags de controle para o HTML e para o Banco
    # Isso evita que o sistema se confunda entre os tipos
    es_npc = (tipo == 'npc')
    es_criatura = (tipo == 'criatura')
    es_player = (not es_npc and not es_criatura)

    if request.method == "POST":
        # 4. Criando o objeto no banco com os dados básicos
        nova_ficha = Personagem(
            campanha=campanha,
            eh_npc=es_npc,
            eh_criatura=es_criatura,
            nome=request.POST.get('nome'),
            raca=request.POST.get('raca'),
            nivel=int(request.POST.get('nivel', 1)),
            
            # Atributos Base
            attr_parautilitario=int(request.POST.get('attr_parautilitario', 1)),
            attr_intelecto=int(request.POST.get('attr_intelecto', 1)),
            attr_psique=int(request.POST.get('attr_psique', 1)),
            attr_fisico=int(request.POST.get('attr_fisico', 1)),
            attr_motoras=int(request.POST.get('attr_motoras', 1)),

            # Perícias - Intelecto
            skill_logica=int(request.POST.get('skill_logica', 0)),
            skill_atualidades=int(request.POST.get('skill_atualidades', 0)),
            skill_diplomacia=int(request.POST.get('skill_diplomacia', 0)),
            skill_drama=int(request.POST.get('skill_drama', 0)),
            skill_conceitualizacao=int(request.POST.get('skill_conceitualizacao', 0)),
            skill_calculo_visual=int(request.POST.get('skill_calculo_visual', 0)),

            # Perícias - Psique
            skill_vontade=int(request.POST.get('skill_vontade', 0)),
            skill_pressentimento=int(request.POST.get('skill_pressentimento', 0)),
            skill_empatia=int(request.POST.get('skill_empatia', 0)),
            skill_autoridade=int(request.POST.get('skill_autoridade', 0)),
            skill_colmeia=int(request.POST.get('skill_colmeia', 0)),
            skill_sugestao=int(request.POST.get('skill_sugestao', 0)),

            # Perícias - Físico
            skill_resistencia=int(request.POST.get('skill_resistencia', 0)),
            skill_limite_dor=int(request.POST.get('skill_limite_dor', 0)),
            skill_luta=int(request.POST.get('skill_luta', 0)),
            skill_eletroquimica=int(request.POST.get('skill_eletroquimica', 0)),
            skill_arrepio=int(request.POST.get('skill_arrepio', 0)),
            skill_memoria_muscular=int(request.POST.get('skill_memoria_muscular', 0)),

            # Perícias - Motoras
            skill_coord_motora=int(request.POST.get('skill_coord_motora', 0)),
            skill_percepcao=int(request.POST.get('skill_percepcao', 0)),
            skill_veloc_reacao=int(request.POST.get('skill_veloc_reacao', 0)),
            skill_destreza=int(request.POST.get('skill_destreza', 0)),
            skill_manufatura=int(request.POST.get('skill_manufatura', 0)),
            skill_compostura=int(request.POST.get('skill_compostura', 0)),

            # Perícias - Parautilitário
            skill_arquetipo=int(request.POST.get('skill_arquetipo', 0)),
            skill_geometria_alma=int(request.POST.get('skill_geometria_alma', 0)),
            skill_sacrificio_astral=int(request.POST.get('skill_sacrificio_astral', 0)),
            skill_timor_mortis=int(request.POST.get('skill_timor_mortis', 0)),
            skill_ritos=int(request.POST.get('skill_ritos', 0)),
            skill_alma=int(request.POST.get('skill_alma', 0)),
        )

        # Se for uma criatura, capturamos os valores de status manuais
        if es_criatura:
            nova_ficha.estabilidade_atual = int(request.POST.get('estabilidade_atual', 10))
            nova_ficha.essencia_atual = int(request.POST.get('essencia_atual', 0))
            nova_ficha.cansaco_atual = int(request.POST.get('cansaco_atual', 10))

        # Se for um Player, vinculamos ao usuário selecionado
        if es_player:
            id_usuario = request.POST.get('usuario')
            if id_usuario:
                nova_ficha.usuario = User.objects.get(id=id_usuario)

        nova_ficha.save()
        return redirect('detalhes_campanha', id=campanha.id)

    # 5. GET: Preparando os dados para exibir o formulário vazio
    # Filtramos os usuários que podem ser vinculados (jogadores da campanha)
    jogadores_vinculados = campanha.jogadores.all()
    
    context = {
        'campanha': campanha,
        'jogadores': jogadores_vinculados,
        'es_npc': es_npc,
        'es_criatura': es_criatura,
        'es_player': es_player, # Flag extra para garantir o título no HTML
    }
    
    return render(request, 'criar_ficha.html', context)

@login_required(login_url='entrar')
def ver_ficha(request, id):
    ficha = get_object_or_404(Personagem, id=id)
    return render(request, 'ver_ficha.html', {'ficha': ficha})

@login_required(login_url='entrar')
def editar_ficha(request, id):
    # 1. Busca a ficha que será editada
    ficha = get_object_or_404(Personagem, id=id)
    
    # 2. SEGURANÇA: Só o mestre da campanha ou o dono da ficha podem editar
    if request.user != ficha.campanha.mestre and request.user != ficha.usuario:
        return redirect('dashboard')

    if request.method == "POST":
        # 3. Atualiza os dados básicos
        ficha.nome = request.POST.get('nome')
        ficha.raca = request.POST.get('raca')
        ficha.nivel = int(request.POST.get('nivel', 1))

        # 4. Atualiza os Atributos
        ficha.attr_parautilitario = int(request.POST.get('attr_parautilitario', 1))
        ficha.attr_intelecto = int(request.POST.get('attr_intelecto', 1))
        ficha.attr_psique = int(request.POST.get('attr_psique', 1))
        ficha.attr_fisico = int(request.POST.get('attr_fisico', 1))
        ficha.attr_motoras = int(request.POST.get('attr_motoras', 1))

        # 5. Atualiza as Perícias (Intelecto)
        ficha.skill_logica = int(request.POST.get('skill_logica', 0))
        ficha.skill_atualidades = int(request.POST.get('skill_atualidades', 0))
        ficha.skill_diplomacia = int(request.POST.get('skill_diplomacia', 0))
        ficha.skill_drama = int(request.POST.get('skill_drama', 0))
        ficha.skill_conceitualizacao = int(request.POST.get('skill_conceitualizacao', 0))
        ficha.skill_calculo_visual = int(request.POST.get('skill_calculo_visual', 0))

        # 6. Atualiza as Perícias (Psique)
        ficha.skill_vontade = int(request.POST.get('skill_vontade', 0))
        ficha.skill_pressentimento = int(request.POST.get('skill_pressentimento', 0))
        ficha.skill_empatia = int(request.POST.get('skill_empatia', 0))
        ficha.skill_autoridade = int(request.POST.get('skill_autoridade', 0))
        ficha.skill_colmeia = int(request.POST.get('skill_colmeia', 0))
        ficha.skill_sugestao = int(request.POST.get('skill_sugestao', 0))

        # 7. Atualiza as Perícias (Físico)
        ficha.skill_resistencia = int(request.POST.get('skill_resistencia', 0))
        ficha.skill_limite_dor = int(request.POST.get('skill_limite_dor', 0))
        ficha.skill_luta = int(request.POST.get('skill_luta', 0))
        ficha.skill_eletroquimica = int(request.POST.get('skill_eletroquimica', 0))
        ficha.skill_arrepio = int(request.POST.get('skill_arrepio', 0))
        ficha.skill_memoria_muscular = int(request.POST.get('skill_memoria_muscular', 0))

        # 8. Atualiza as Perícias (Motoras)
        ficha.skill_coord_motora = int(request.POST.get('skill_coord_motora', 0))
        ficha.skill_percepcao = int(request.POST.get('skill_percepcao', 0))
        ficha.skill_veloc_reacao = int(request.POST.get('skill_veloc_reacao', 0))
        ficha.skill_destreza = int(request.POST.get('skill_destreza', 0))
        ficha.skill_manufatura = int(request.POST.get('skill_manufatura', 0))
        ficha.skill_compostura = int(request.POST.get('skill_compostura', 0))

        # 9. Atualiza as Perícias (Parautilitário)
        ficha.skill_arquetipo = int(request.POST.get('skill_arquetipo', 0))
        ficha.skill_geometria_alma = int(request.POST.get('skill_geometria_alma', 0))
        ficha.skill_sacrificio_astral = int(request.POST.get('skill_sacrificio_astral', 0))
        ficha.skill_timor_mortis = int(request.POST.get('skill_timor_mortis', 0))
        ficha.skill_ritos = int(request.POST.get('skill_ritos', 0))
        ficha.skill_alma = int(request.POST.get('skill_alma', 0))

        # 10. Atualiza o vínculo com o usuário (apenas se for Player)
        if not ficha.eh_npc:
            usuario_id = request.POST.get('usuario')
            if usuario_id:
                ficha.usuario = User.objects.get(id=usuario_id)
            else:
                ficha.usuario = None

        # 11. Salva as alterações no banco
        ficha.save()
        
        # Volta para os detalhes da campanha
        return redirect('detalhes_campanha', id=ficha.campanha.id)

    # Caso seja GET (carregar a página), pegamos os jogadores da campanha para o select
    jogadores = ficha.campanha.jogadores.all()
    
    return render(request, 'editar_ficha.html', {
        'ficha': ficha,
        'jogadores': jogadores
    })

@login_required(login_url='entrar')
def deletar_ficha(request, id):
    # 1. Busca a ficha
    ficha = get_object_or_404(Personagem, id=id)
    
    # Guarda o ID da campanha para saber para onde voltar depois de deletar
    campanha_id = ficha.campanha.id

    # 2. SEGURANÇA: Só o mestre da campanha ou o dono da ficha podem deletar
    if request.user == ficha.campanha.mestre or request.user == ficha.usuario:
        ficha.delete()
        messages.success(request, "Ficha excluída com sucesso!")
    else:
        messages.error(request, "Você não tem permissão para excluir esta ficha.")

    # 3. Volta para os detalhes da campanha
    return redirect('detalhes_campanha', id=campanha_id)

def sair(request):
    logout(request)
    return redirect('entrar')