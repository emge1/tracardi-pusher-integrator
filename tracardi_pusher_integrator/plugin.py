from tracardi_plugin_sdk.action_runner import ActionRunner
from tracardi_plugin_sdk.domain.register import Plugin, Spec, MetaData
from tracardi_plugin_sdk.domain.result import Result

from aiohttp import ClientConnectorError
from tracardi_pusher_integrator.model.configuration import PusherClient, PusherConfiguration, \
    PusherPlatform
from pusher_push_notifications import PushNotifications


class PusherIntegratorAction(ActionRunner):

    def __init__(self, **kwargs):
        self.config = PusherConfiguration(**kwargs)
        self.client = PusherClient(**kwargs)
        self.platform = PusherPlatform(**kwargs)

    async def run(self, payload):
        try:
            beams_client = PushNotifications(instance_id=self.client.instance_id,
                                             secret_key=self.client.secret_key)

            ''' trzeba wypełnić przynajmniej pole subskrybentów lub użytkowników, adresatów
             powiadomienia, jak nie, to bład'''
            if self.config.interests is not None and self.config.user_ids is not None:
                raise ValueError("You can send only to interests or to individual users at the same time")

            '''gole publish body na początku. ogólnie program ma sprawdzać, czy przy jakimś polu
            jest coś napisanego w init. zależnie od spełnienia napisanych warunków, program
            dołacza to do publish body'''
            publish_body = {}

            '''notification - przyda się do androida i webu'''
            notification = {'title': self.config.title,
                            'body': self.config.body}

            '''android - jak użytkownik dał android jako True, to dołączenie do publish body
            jak jeszcze wypełnił data, to dołączenie danych do tego powiadomienia'''
            if self.platform.android is True:
                fcm = {}
                fcm.update({'notification': notification})
                if self.config.data is not None:
                    fcm.update({'data': self.config.data})
                publish_body.update({'fcm': notification})


            '''apple - zdefiniowanie alertu, potem jak użytkownik zaznaczył pole ios w init,
            to dołącza do publish body. jak jeszcze jest wypełnione pole data, to do alertu
            są dołączane też dane'''


            if self.platform.ios is True:
                alert = {'title': self.config.title,
                         'body': self.config.body}
                apns = {}
                apns.update({'alert': alert})
                if self.config.data is not None:
                    apns.update({'data': self.config.data})
                publish_body.update({'apns': alert})


            '''web - tutaj więcej, bo więcej parametrów'''
            if self.platform.web is not None:   #jest sporo do sprawdzenia, więc aby oszczędzić czas
                # uznałem, że tak będzie oszczędniej
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

            print(publish_body)


            ''' dwie wersje - albo wysłanie do subskrybentów, albo do 
            konkretnych użytkowników. w obu przypadkach ta sama funkcja, tylko jeden 
            parametr inny'''
            if self.config.interests is not None:
                response = beams_client.publish_to_interests(
                    interests=[x for x in self.config.interests],
                    publish_body=publish_body)

            if self.config.user_ids is not None:
                response = beams_client.publish_to_users(
                    user_ids=[x for x in self.config.user_ids],
                    publish_body=publish_body)

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
