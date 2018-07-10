# xmpp-test
Simple client to test XMPP connection + auth with any XMPP server, and to subscribe and listen to XMPP events on a node

DOWNLOAD
--------
Latest executable JAR available [here](xmpp-test/bin/xmpp-test.jar)

REQUIREMENTS
------------
- JRE 1.7+
- Direct access to an XMPP server (no capability to configure / use proxies)

USAGE
-----

```shell
java -jar xmpp-test.jar <XMPP_HOST> <XMPP_PORT> <XMPP_USERNAME> <XMPP_PASSWORD> <SUBSCRIBE_TO_EVENTS (true | false)> [<XMPP_NODE_NAME>]
```
where
```
XMPP_HOST            = Hostname / IP address of the XMPP server
XMPP_PORT            = Port on the XMPP server to connect to
XMPP_USERNAME        = Valid username to authenticate with the XMPP server
XMPP_PASSWORD        = Password to authenticate username
SUBSCRIBE_TO_EVENTS  = Boolean flag (true | false) indicating whether to subscribe to XMPP events
XMPP_NODE_NAME       = Canonical name of XMPP node to subscribe to for events (Optional, if SUBSCRIBE_TO_EVENTS is true)
```

