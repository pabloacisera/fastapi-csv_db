from tabulate import tabulate

def print_routes(app):
    
    routes = []

    for route in app.routes:
        if hasattr(route, 'methods') and hasattr(route, 'path'):
            methods = ', '.join(route.methods)
            path = route.path
            routes.append([ methods, path ])


    table = tabulate(routes, headers=['Método', 'Ruta'], tablefmt='grid')
    return table 
