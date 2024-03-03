import asyncio
from websockets.server import serve
from websockets import broadcast
import json

users = {}

async def msg(ws):
	async for msg in ws:
		data = json.loads(msg, strict=False)
		user = data['username']
		target = data['target']
		if user not in users:
			print(f'ADDED USER: {user}')
			users[user] = ws

			if target in users:
				print('Broadcasting')
				await asyncio.gather(
					ws.send('{"iscaller": true}'),
					users[target].send('{"iscaller": false}'),
				)

		if 'disconnect' in data:
			print(f'DISCONNECTED: {user}')
			users.pop(user)
			return

		if target in users and 'hello' not in data:
			await users[target].send(msg)


async def main():
	async with serve(msg, 'localhost', 8765):
		await asyncio.Future()

asyncio.run(main())