/**
 * Licensed under the MIT License.
 * For more details, see LICENSE file
 */
package com.umnagendra.xmpptest;

import org.jivesoftware.smack.XMPPConnection;
import org.jivesoftware.smack.XMPPException;
import org.jivesoftware.smackx.pubsub.LeafNode;
import org.jivesoftware.smackx.pubsub.Node;
import org.jivesoftware.smackx.pubsub.PubSubManager;

/**
 * XMPP handler class to process XMPP push events
 */
public class XmppSubscriber {

	private final XMPPConnection _connection;
	private final PubSubManager _pubSubManager;
	private final XmppEventListener _eventListener;
	private final Thread _eventListenerThread;

	public XmppSubscriber(XMPPConnection connectTo) {
		this._connection = connectTo;
		final String toAddress = "pubsub." + _connection.getServiceName();
		_pubSubManager = new PubSubManager(connectTo, toAddress);
		_eventListener = new XmppEventListener();
		_eventListenerThread = new Thread(_eventListener);
	}

	public void subscribe(String nodeName) {
		LeafNode node = (LeafNode) getNode(nodeName);
		_eventListenerThread.setName(nodeName + "-Listener");
		_eventListenerThread.start();
		node.addItemEventListener(_eventListener);
		try {
			node.subscribe(_connection.getUser());
			XMPPClient.log("Successfully subscribed to XMPP node [" + nodeName + "]");
			System.out.println("\n\nLISTENING TO XMPP EVENTS ... HIT `CTRL + C` to terminate this program");
		} catch (XMPPException cause) {
			XMPPClient.log("Error subscribing to node [" + nodeName + "], Exception = " + cause.getMessage());
			cause.printStackTrace();
		}
	}

	/**
	 * Reach out the XMPP server to get the node object for subscription
	 * 
	 * @param nodeName
	 *            - public id for a campaign node
	 * @return XMPP node
	 */
	public Node getNode(String nodeName) {
		Node node = null;
		if (isConnectionInvalid()) {
			return node;
		}
		try {
			node = _pubSubManager.getNode(nodeName);
		} catch (XMPPException cause) {
			cause.printStackTrace();
		}
		return node;
	}

	/**
	 * Fail-safe method to guard against invalidated connection handle
	 * 
	 * @return true if connection is valid ; false otherwise
	 */
	private boolean isConnectionInvalid() {
		return (!_connection.isConnected() || !_connection.isAuthenticated());
	}
}
