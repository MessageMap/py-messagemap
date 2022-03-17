# py-messagemap
https://MessageMap.IO/ Python Interface

This is the Main Python Module for Sending Messages to MessageMap

Documentation for Usage:

    Class Attributes
    ----------
    address : str 
        Short name of MessageMap address "http://address.msgmap.io"
    application_id : str
        Application Id from UI
    application_apikey : str
        Application APIKey from address ApiKey

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
