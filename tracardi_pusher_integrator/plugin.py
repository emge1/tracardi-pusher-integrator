from tracardi_plugin_sdk.action_runner import ActionRunner
from tracardi_plugin_sdk.domain.register import Plugin, Spec, MetaData
from tracardi_plugin_sdk.domain.result import Result

from aiohttp import ClientConnectorError
from tracardi_pusher_integrator.model.configuration import PusherAuthentication, PusherConfiguration, \
    PusherPlatform
from pusher_push_notifications import PushNotifications


class PusherIntegratorAction(ActionRunner):

    def __init__(self, **kwargs):
        self.config = PusherConfiguration(**kwargs)
        self.auth = PusherAuthentication(**kwargs)
        self.platform = PusherPlatform(**kwargs)

    async def run(self, payload):
        try:
            beams_client = PushNotifications(instance_id=self.auth.instance_id,
                                             secret_key=self.auth.secret_key)

            if self.config.interests is not None and self.config.user_ids is not None:
                raise ValueError("You can send only to interests or to individual users at the same time")

            publish_body = {}

            dot = DotAccessor(self.profile, self.session, payload, self.event, self.flow)
            title = dot[self.config.title]
            body = dot[self.config.body]

            notification = {'title': title,
                            'body': body}

            if self.platform.android is True:
                fcm = {'notification': notification}
                if self.config.data is not None:
                    fcm.update({'data': self.config.data})
                publish_body.update({'fcm': notification})

            if self.platform.ios is True:
                alert = {'title': self.config.title,
                         'body': self.config.body}
                apns = {}
                apns.update({'alert': alert})
                if self.config.data is not None:
                    apns.update({'data': self.config.data})
                publish_body.update({'apns': alert})

            if self.platform.web is not None:
                if self.config.icon is not None:
                    notification.update({'icon': self.config.icon})
                    print(notification)
                if self.config.deep_link is not None:
                    notification.update({'deep_link': self.config.deep_link})
                if self.config.hide_notification_if_site_has_focus is True:
                    notification.update({'hide_notification_if_site_has_focus':
                                             self.config.hide_notification_if_site_has_focus})
                print(notification)
                web = {}
                if self.config.time_to_live is not None:
                    web.update({'time_to_live': self.config.time_to_live,
                                'notification': notification})

                if self.config.data is not None:
                    web.update({'data': self.config.data})

                if self.platform.web is True:
                    publish_body.update({'web': web})

            if self.config.interests is not None:
                response = beams_client.publish_to_interests(
                    interests=[x for x in self.config.interests],
                    publish_body=publish_body)

            elif self.config.user_ids is not None:
                response = beams_client.publish_to_users(
                    user_ids=[x for x in self.config.user_ids],
                    publish_body=publish_body)

            else:
                raise ValueError("You should choose if you wanto to send notifications to users or to interests")

            return Result(port="response", value=response), Result(port="error", value=None)

        except ClientConnectorError as e:
            return Result(port="response", value=None), Result(port="error", value=str(e))


def register() -> Plugin:
    return Plugin(
        start=False,
        spec=Spec(
            module='tracardi_pusher_integrator.plugin',
            className='PusherIntegratorAction',
            inputs=["payload"],
            outputs=['response', 'error'],
            version='0.1',
            license="MIT",
            author="Marcin Gaca",
            init={"instance_id": None,
                  "secret_key": None,
                  "interests": None,
                  "user_ids": None,
                  "web": False,
                  "ios": False,
                  "android": False,
                  "title": None,
                  "body": None,
                  "data": None,
                  "time_to_live": None,
                  "icon": None,
                  "deep_link": None,
                  "hide_notification_if_site_has_focus": False},
        ),
        metadata=MetaData(
            name='tracardi-pusher-integrator',
            desc='This plugin sends notifications via Pusher Beams.',
            type='flowNode',
            width=200,
            height=100,
            icon='icon',
            group=["General"]
        )
    )
