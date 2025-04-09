from utils.csv_to_dict import csv_to_dict, get_record_by_id, add_record, delete_record, search_by_name, update_record
from fastapi import HTTPException
from typing import Dict, List, Any


class ProductsController:
    async def get_all_products(self):
        try:
            csv = csv_to_dict('products')  # Quita el await

            products = []
            num_products = len(csv.get('id_producto', []))

            for i in range(num_products):
                product = {
                    'id': csv['id_producto'][i],
                    'name': csv['nombre'][i],
                    'description': csv['descripcion'][i],
                    'price': csv['precio'][i],
                    'category': csv['categoria'][i],
                    'stock': csv['stock'][i],
                    'brand': csv['marca'][i],
                    'created_at': csv['fecha_creacion'][i]
                }
                products.append(product)
            return {
                'status': 'success',
                'count': len(products),
                'data': products
            }
        except FileNotFoundError as e:
            raise HTTPException(status_code=404, detail=f"Archivo no encontrado: {e}")
        except KeyError as e:
            raise HTTPException(status_code=400, detail=f"Columna faltante en CSV: {e}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

    async def get_product_by_id(self, id_producto):
        try:
            # Obtener datos primero para diagnóstico
            data = csv_to_dict('products')
            print("IDs reales en CSV:", data['id_producto'])

            # Buscar el registro
            record = get_record_by_id('products', id_producto, 'id_producto')

            if not record:
                raise HTTPException(
                    status_code=404,
                    detail={
                        'message': f'Producto con ID {id_producto} no encontrado',
                        'available_ids': data['id_producto'],
                        'diagnostic': {
                            'search_type': type(id_producto).__name__,
                            'stored_ids_sample': data['id_producto'][:5],
                            'searched_value': str(id_producto)
                        }
                    }
                )

            return {'status': 'success', 'data': record}

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def create_product(self, product_data: Dict[str, Any]):
        try:
            required_fields = ['nombre', 'descripcion', 'precio', 'categoria', 'stock', 'marca']

            if not all(field in product_data for field in required_fields):
                missing = [field for field in required_fields if field not in product_data]
                raise HTTPException(
                    status_code=400,
                    detail=f"fields required emptys: {', '.join(missing)}"
                )

            if 'fecha_creacion' not in product_data:
                from datetime import datetime
                product_data['fecha_creacion'] = datetime.now().strftime('%Y-%m-%d')

            created_product = add_record('products', product_data)

            return {
                'status':'success',
                'message':'Product created successfully',
                'data': created_product
            }
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f'Error to create product: {str(e)}')

    async def delete_product(self, id_producto: int):
        try:
            success = delete_record('products', id_producto)

            if not success:
                raise HTTPException(
                    status_code=500,
                    detail='Error unknown'
                )
            return {
                'status': 'success',
                'message': f'Product by id: {id_producto} deleted'
            }
        except ValueError as e:
            raise HTTPException(
                status_code=404,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f'Error to eliminate product: {str(e)}'
            )

    async def search_products(self, query: str):
        try:
            results = search_by_name('products', query)

            return {
                'status': 'success',
                'count': len(results),
                'data': results
            }
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en búsqueda: {str(e)}")

    async def update_product(self, id_producto: int, update_data: Dict[str, Any]):
        try:
            # No permitir actualización del ID
            if 'id_producto' in update_data:
                raise HTTPException(
                    status_code=400,
                    detail="No se puede modificar el ID del producto"
                )

            # Actualizar el producto
            updated_product = update_record('products', id_producto, update_data)

            return {
                'status': 'success',
                'message': 'Producto actualizado exitosamente',
                'data': updated_product
            }
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al actualizar producto: {str(e)}")