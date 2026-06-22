from fastapi import APIRouter, HTTPException
from app.schemas.schemas import Create
from app.models.models import Pedido
from app.database import collection
from app.rabbitmq.rabbitmq import enviar_mensagem
from app.kafka.kafka import publicar_evento

router = APIRouter()

@router.post("/pedidos")
def cadastrar_pedido(pedido: Create,):

    novo_pedido = Pedido(
        user=pedido.user,
        produto=pedido.produto,
        quantidade=pedido.quantidade
    )

    collection.insert_one(novo_pedido.model_dump())

    mensagem = {
        "id": novo_pedido["id"],
        "evento": "PEDIDO_CRIADO"
    }

    enviar_mensagem(mensagem)
    publicar_evento(mensagem)

    return novo_pedido

@router.get("/pedidos")
def listar_pedidos():

    pedidos = list(
        collection.find({}, {"_id": 0})
    )

    return pedidos

@router.put("/pedidos/{pedido_id}")
def atualizar_pedido(pedido_id: str, pedido: Create):

    dados_atualizados = {
        "user": pedido.user,
        "produto": pedido.produto,
        "quantidade": pedido.quantidade
    }

    resultado = collection.update_one(
        {"id": pedido_id},
        {"$set": dados_atualizados}
    )

    if resultado.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Pedido não encontrado"
        )

    mensagem = {
        "id": pedido_id,
        "evento": "PEDIDO_ATUALIZADO"
    }

    enviar_mensagem(mensagem)
    publicar_evento(mensagem)

    pedido_atualizado = collection.find_one(
        {"id": pedido_id},
        {"_id": 0}
    )

    return pedido_atualizado

@router.delete("/pedidos/{pedido_id}")
def deletar_pedido(pedido_id: str):

    resultado = collection.delete_one(
        {"id": pedido_id}
    )

    if resultado.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Pedido não encontrado"
        )

    mensagem = {
        "id": pedido_id,
        "evento": "PEDIDO_DELETADO"
    }

    enviar_mensagem(mensagem)
    publicar_evento(mensagem)

    return {
        "mensagem": "Pedido removido com sucesso"
    }