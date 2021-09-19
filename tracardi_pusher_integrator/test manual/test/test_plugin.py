import asyncio

from tracardi_pusher_integrator.plugin import PusherIntegratorAction


async def main():
    init = {"instance_id": None,
            "secret_key": None,
            "interests": None,
            "user_ids": None,
            "publish_body": {
                'apns': {
                    'aps': {
                        'alert': {
                            'title': None,
                            'body': None,
                        },
                        'data': {},
                    },
                },
                'fcm': {
                    'notification': {
                        'title': None,
                        'body': None,
                    },
                    'data': {},
                },
                'web': {
                    'time_to_live': None,
                    'notification': {
                        'title': None,
                        'body': None,
                        'icon': None,
                        'deep_link': None,
                        'hide_notification_if_site_has_focus': False,
                    },
                    'data': {},
                },
            },
            },

    plugin = PusherIntegratorAction(**init)

    payload = {}

    results = await plugin.run(payload)
    print(results)


asyncio.run(main())
