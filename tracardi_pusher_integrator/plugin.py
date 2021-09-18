from aiohttp import ClientConnectorError
from pusher_push_notifications import PushNotifications
from tracardi_plugin_sdk.domain.register import Plugin, Spec, MetaData
from tracardi_plugin_sdk.domain.result import Result
from tracardi_plugin_sdk.action_runner import ActionRunner

from tracardi_pusher_integrator.model.configuration import PusherIntegratorConfiguration, PusherClient


class PusherIntegratorAction(ActionRunner):
    def __init__(self, **kwargs):
        self.config = PusherIntegratorConfiguration(**kwargs)
        self.client = PusherClient(**kwargs)

    async def run(self, payload):
        try:
            beams_client = PushNotifications(instance_id=self.client.instance_id,
                                             secret_key=self.client.secret_key)

            if 1 <= len(self.config.interests) <= 100:
                raise ValueError("List of interests must be in range from 1 to 100")

            response = beams_client.publish_to_interests(
                interests=[self.config.interests],
                publish_body = {
                    'apns': {
                        'aps': {
                            'alert': {
                                'title': self.config.title,
                                'body': self.config.body,
                            },
                        },
                        'data': self.config.data,
                    },
                    'fcm': {
                        'notification': {
                            'title': self.config.title,
                            'body': self.config.body,
                        },
                        'data': self.config.data,
                    },
                    'web': {
                        'time_to_live': self.config.time_to_live,
                        'notification': {
                            'title': self.config.title,
                            'body': self.config.body,
                            'icon': self.config.icon,
                            'deep_link': self.config.deep_link,
                            'hide_notification_if_site_has_focus': self.config.hide_notification_if_site_has_focus,
                        },
                        'data': self.config.data,
                    }
                )

            return Result(port="response", value=response), Result(port="error", value=None)


        except ClientConnectorError as e:
        return Result(port="response", value=None), Result(port="error", value=str(e))


def register() -> Plugin:
    return Plugin(
        start=False,
        spec=Spec(
            module='tracardi_pusher_integrator.plugin',
            className='PusherIntegratorAction',
            inputs=['payload'],
            outputs=["response", "error"],
            init={"instance_id": None,
                  "secret_key": None,
                  "user_ids": [None],
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

            version="0.1.2",
            author="Marcin Gaca",
            license="MIT",
            manual="pusher_integrator_action",
        ),
        metadata=MetaData(
            name='Pusher Beams',
            desc='Sends notification via Pusher Beams.',
            type='flowNode',
            width=200,
            height=100,
            icon='pusher-beams',
            group=["Connectors"]
        )
    )
