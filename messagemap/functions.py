# -*- coding: utf-8 -*-
"""
Start of MessageMap Class Documentation for
Making API Calls to a MessageMap Environment
"""
import http.client
import json

class MessageMap:
    """
    A class to Interact with MessageMap Environments

    ...

    Attributes
    ----------
    environment : str
        Short name of MessageMap environment "{env}.msgmap.io"
    application_id : str
        Application Id from UI
    application_apikey : str
        Application APIKey from Environment ApiKey

    Methods
    -------
    auth()
        Returns API Token Keys
    publish(topic, payload, version=False)
        Returns Result of Pushing messages to Topic
    publish(topic, payload, version=False)
        Returns the of subscribing applications queues message was pushed too
    pull(limit=False)
        Returns messages in the Queue for Application
    """

    def __init__(self, environment, application_id, application_apikey):
        """
        Constructs setting MessageMap Object

        Parameters
        ----------
            env : str
                Short name of MessageMap environment "{env}.msgmap.io"
            appid : str
                Application Id from UI
            apikey : str
                Application APIKey from Environment ApiKey
        """
        self.env = environment
        self.appid = application_id
        self.apikey = application_apikey
        self.access_token = False
        self.headers = { 'Content-Type': 'application/json' }

    @classmethod
    def update_access_token(cls, token):
        '''
        Internal method to Update Attribute Access Token
        :param token:
            token (uuid): access_token value
        :return:
            Update object with access_token
        '''
        cls.access_token = token

    def auth(self):
        '''
        Returns Access Token and Refresh Token with Application Scopes

                Returns:
                    apitokens (json): Returns the application tokens
        '''
        conn = http.client.HTTPSConnection("%s.msgmap.io" % self.env)
        uri = "/api/auth/token?client_id=%s&grant_type=authorization_code&code=%s"\
              % (self.appid, self.apikey)
        conn.request("POST", uri, "", self.headers)
        res = conn.getresponse()
        data = res.read().decode("utf-8")
        conn.close()
        if res.status != 200:
            result = "Unable to Find Authentication Key"
            if 'error' in json.loads(data):
                result = json.loads(data)['error']
            return result
        self.update_access_token(json.loads(data)['access_token'])
        return json.loads(data)

    def publish(self, topic, payload, version=False):
        '''
        Push Messages into MessageMap Environment

                Parameters:
                        topic         (str):  Topic for Queue to push messages too
                        payload       (json): JSON Message to Push to Queue
                        version       (str):  Optional - Version Number for JSON Schema validation

                Returns:
                        publish_status (json): Subscribers queues message status
        '''
        if not self.access_token:
            self.access_token = self.auth()['access_token']

        self.headers['Authorization'] = "%s" % self.access_token
        conn = http.client.HTTPSConnection("%s.msgmap.io" % self.env)
        uri = "/messages/%s" % topic
        if version:
            uri = "/messages/%s/%s" % (version, topic)
        conn.request("POST", uri, json.dumps(payload), self.headers)
        res = conn.getresponse()
        data = res.read()
        conn.close()
        if res.status == 401:
            self.auth()
            self.publish(topic, payload, version)
        return json.loads(data)

    def pull(self, limit=False):
        '''
        Pull Messages from MessageMap Environment

                Parameters:
                        limit   (int):  Optional - Limit Number of messages to return

                Returns:
                        MessagesInQueue (json): Messages In Queue
        '''
        if not self.access_token:
            self.access_token = self.auth()['access_token']
        self.headers ['Authorization'] = "%s" % self.access_token
        conn = http.client.HTTPSConnection("%s.msgmap.io" % self.env)
        uri = "/messages"
        if limit and isinstance(limit, int):
            uri = "/messages?limit=%s" % limit
        conn.request("GET", uri, "", self.headers)
        res = conn.getresponse()
        data = res.read().decode("utf-8")
        conn.close()
        if res.status == 401:
            self.auth()
            self.pull(limit)
        return data
