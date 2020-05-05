from aiohttp import web
from aiohttp.web_response import Response
# import aiohttp_cors
from api import api_routes


app = web.Application()

# cors = aiohttp_cors.setup(app, defaults={
#     "*": aiohttp_cors.ResourceOptions(
#             allow_credentials=True,
#             expose_headers="*",
#             allow_headers="*",
#         )
# })

frontend_routes = web.RouteTableDef()


@frontend_routes.get('/')
@frontend_routes.get('/{path:.*}')
async def test(request):
    with open('dist/index.html') as file:
        return Response(text=file.read(), content_type='text/html')


app.router.add_static('/_nuxt', path='dist/_nuxt')
app.add_routes(api_routes)
app.add_routes(frontend_routes)

# for route in list(app.router.routes()):
#     cors.add(route)

web.run_app(app)
