/**
 * Licensed under the MIT License.
 * For more details, see LICENSE file
 */
package com.umnagendra.xmpptest;

import java.util.List;

import org.jivesoftware.smackx.pubsub.ItemPublishEvent;
import org.jivesoftware.smackx.pubsub.PayloadItem;
import org.jivesoftware.smackx.pubsub.SimplePayload;
import org.jivesoftware.smackx.pubsub.listener.ItemEventListener;

/**
 * Listener for XMPP events
 */
@SuppressWarnings("rawtypes")
public class XmppEventListener implements ItemEventListener, Runnable {

	@Override
	public void run() {
		final String threadName = Thread.currentThread().getName();
		XMPPClient.log("Starting XMPP EventListener... Thread Name = " + threadName);
		while (true) {
			if (Thread.interrupted()) {
				break;
			}
		}
		XMPPClient.log("Exiting XMPP EventListener thread [" + threadName + "]");
	}

	/**
	 * Callback method to handle XMPP push events for subscribed node
	 * 
	 * @param event
	 *            - event published from XMPP server
	 */
	@SuppressWarnings("unchecked")
	@Override
	public void handlePublishedItems(ItemPublishEvent event) {
		final List<PayloadItem<SimplePayload>> eventList = event.getItems();
		for (PayloadItem<SimplePayload> item : eventList) {
			final String payloadXml = item.getPayload().toXML();
			System.out.print("\n\n");
			XMPPClient.log("XMPP EVENT RECEIVED: " + payloadXml);
		}
	}
}
