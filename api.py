from aiohttp import web
from aiohttp.web_server import BaseRequest
from models import VM, Users


api_routes = web.RouteTableDef()


@api_routes.get('/api/my_vms')
async def my_vms(request: BaseRequest):
    owner: str or None = request.query.get('owner')
    if not owner:
        return web.json_response({'error': 'please provide owner'})

    user: Users = await Users.get_by_name(owner)
    if not user:
        return web.json_response({'error': 'invalid username'})

    vms: list = await VM.get_by_owner(user.id)
    if not vms:
        return web.json_response({'result': []})

    return web.json_response({'result': sorted([await x.to_dict() for x in vms], key=lambda x: x['name'])})


@api_routes.post('/api/new_vm')
async def new_vm(request: BaseRequest):
    json_req: dict or None = await request.json()
    if not json_req:
        return web.json_response({'error': 'please provide request in json'})

    if not all(x in ['name', 'description', 'cpu', 'ram', 'hdd', 'owner'] for x in json_req.keys()):
        return web.json_response({'error': 'incorrect request'})

    owner: Users = await Users.get_by_name(json_req['owner'])
    if not owner:
        return web.json_response({'error': 'please provide correct owner name'})

    await VM.new(name=json_req['name'], description=json_req['description'], cpu=json_req['cpu'],
                 ram=json_req['ram'],  hdd=json_req['hdd'], owner=owner.id)

    return web.json_response({'result': 'success'})


@api_routes.post('/api/change_vm')
async def new_vm(request: BaseRequest):
    json_req: dict or None = await request.json()
    if not json_req:
        return web.json_response({'error': 'please provide request in json'})

    if not all(x in ['description', 'cpu', 'ram', 'hdd', 'name'] for x in json_req.keys()):
        return web.json_response({'error': 'incorrect request'})

    vm: VM = await VM.get_by_name(json_req['name'])
    if not vm:
        return web.json_response({'error': 'please provide correct vm name'})

    await vm.update_values(**json_req)

    return web.json_response({'result': 'success'})


@api_routes.post('/api/delete_vm')
async def new_vm(request: BaseRequest):
    json_req: dict or None = await request.json()
    if not json_req:
        return web.json_response({'error': 'please provide request in json'})

    if not json_req.get('name'):
        return web.json_response({'error': 'incorrect request'})

    vm: VM = await VM.get_by_name(json_req['name'])
    if not vm:
        return web.json_response({'error': 'please provide correct vm name'})

    await vm.delete_vm()

    return web.json_response({'result': 'success'})
