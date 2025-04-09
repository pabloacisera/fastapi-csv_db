from fastapi import APIRouter, HTTPException, Body
from typing import Dict, List, Any
from controllers.products_controller import ProductsController

router = APIRouter()
controller = ProductsController()

@router.get('/')
async def get_all_products():
    try:
        # Mantén el await aquí porque el método del controlador es async
        data = await controller.get_all_products()
        return data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/{id_producto}')
async def get_product_by_id(id_producto: int):
    try:
        # Mantén el await aquí porque el método del controlador es async
        product = await controller.get_product_by_id(id_producto)
        return product
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/', status_code=201)
async def create_product(product_data: Dict[str, Any] = Body(...)):
    """
        Crea un nuevo producto con los campos:
        nombre, descripcion, precio, categoria, stock, marca
    """
    try:
        result = await controller.create_product(product_data)
        return result
    except HTTPException:
        raise
    except Exception as e:
        HTTPException(status_code=500, detail=str(e))

@router.put('/{id_producto}')
async def update_product(
        id_producto: int,
        update_data: Dict[str, Any] = Body(...)
):
    """Actualiza un producto existente"""
    try:
        result = await controller.update_product(id_producto, update_data)
        return result
    except HTTPException as e:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.delete('/{id_producto}')
async def remove_product(id_producto: int):
    """
    :param id_producto:
    :return:
    """
    try:
        result = await controller.delete_product(id_producto)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.get('/search/{query}')
async def search_product(query: str):
    """

    :param query:
    :return:
    """
    try:
        result = await controller.search_products(query)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
