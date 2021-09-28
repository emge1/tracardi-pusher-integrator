import asyncio

from tracardi_pusher_integrator.plugin import PusherIntegratorAction


async def main():
    init = {"instance_id": "3d2e5ae8-bff1-40e9-96c1-beb37384ebbc",
            "secret_key": "D54335B8E565D11DA91E9911AD412A0667DBC3EDBE974266AE926BE50C840D54",
            "interests": None,
            "user_ids": ["hgCkry9t9r0mtHE6aKqUOT6_FNpcl3l1TNSom-og_M4"],
            "web": True,
            "ios": False,
            "android": False,
            "title": "Hello",
            "body": "Hello world",
            "data": {"some": "data"},
            "time_to_live": 111111,
            "icon": None,
            "deep_link": None,
            "hide_notification_if_site_has_focus": False}


    plugin = PusherIntegratorAction(**init)

    payload = {}

    results = await plugin.run(payload)
    print(results)


asyncio.run(main())
