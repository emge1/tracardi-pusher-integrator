# Tracardi plugin

This code can be run within Tracardi workflow.

# Pusher integrator action

The purpose of this plugin is to push notifications via Pusher Beams.

# Configuration

This node requires configuration. 

To authenticate, you need to write your unique identifier for your Push 
notifications instance and your secret key your server. These two ones 
can be found in the dashboard under “Keys”.

You can push notifications to interests OR to users by their ids. You can't 
send notifications to these two gropus at the same time. The list
of interests/users must be in range from 1 to 100.

You can push notifications to iOS users (APNs format), Android users (FCM format)
or web application users (Web format). You need to write True in adequate fields.

You can set the title, text (body) and (optionally) data of notification. If you 
want to use Web format, you can also set optionally:
* time to live - the number of seconds the web push gateway should store the 
  notification for whilst the user is offline. Max: 2419200. Default: 4 weeks
  
* icon 

* deep link - if provided, this URL will be opened in a new tab when the notification 
  is clicked
  
* parameter hide_notification_if_site_has_focus - if set to True, the notification will 
  not be shown if your site has focus. Default: False.

Example #1 - sending to interests:

```json
            init={"instance_id": "your_instance_id",
                  "secret_key": "your_secret_key",
                  "interests": ["hello"],
                  "user_ids": None,
                  "web": True,
                  "ios": False,
                  "android": False,
                  "title": "Hello",
                  "body": "Hello world!",
                  "data": {"some": "data"},
                  "time_to_live": None,
                  "icon": None,
                  "deep_link": "https://example.com/messages?message_id=1111",
                  "hide_notification_if_site_has_focus": False},
```

Example #2 - sending to users:

```json
            init={"instance_id": "your_instance_id",
                  "secret_key": "your_secret_key",
                  "interests": None,
                  "user_ids": ["user1", "user2"],
                  "web": True,
                  "ios": True,
                  "android": True,
                  "title": "Hello",
                  "body": "Hello world!",
                  "data": {"some": "data"},
                  "time_to_live": 100000,
                  "icon": "https://example.com/img/icon.jpg",
                  "deep_link": None,
                  "hide_notification_if_site_has_focus": False},
```

# Input payload

This node does not process input payload.

# Output

This node does not return output to client.
