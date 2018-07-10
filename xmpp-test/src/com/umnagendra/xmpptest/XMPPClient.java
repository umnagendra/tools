/**
 * Licensed under the MIT License.
 * For more details, see LICENSE file
 */
package com.umnagendra.xmpptest;

import java.text.SimpleDateFormat;
import java.util.Date;

import org.jivesoftware.smack.ConnectionConfiguration;
import org.jivesoftware.smack.XMPPConnection;

/**
 * Simple client to test XMPP connection and authentication with an XMPP server
 */
public class XMPPClient {

	private static final SimpleDateFormat logDateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss.SSS");

	/**
	 * Log with timestamp to {@link System.out}
	 * 
	 * @param message
	 */
	public static void log(String message) {
		String now = logDateFormat.format(new Date());
		System.out.println(now + " - " + message);
	}

	/**
	 * Show command usage
	 */
	private static void showUsage() {
		System.err.println("USAGE: java -jar xmpp-test.jar "
				+ "<XMPP_HOST> <XMPP_PORT> <XMPP_USERNAME> <XMPP_PASSWORD> <SUBSCRIBE_TO_EVENTS (true | false)> [<XMPP_NODE_NAME>]");
		System.exit(1);
	}

	public static void main(String[] args) {

		if (args.length < 5 || args.length > 6) {
			showUsage();
		}

		String xmppHost = args[0];
		int xmppPort = Integer.valueOf(args[1]);
		String xmppUser = args[2];
		String xmppPassword = args[3];
		boolean subscribe = Boolean.valueOf(args[4]);

		// Create a connection to the server
		ConnectionConfiguration connectionConfiguration = new ConnectionConfiguration(xmppHost, xmppPort);
		final XMPPConnection connection = new XMPPConnection(connectionConfiguration);

		try {
			log("Attempting to connect to XMPP server"
					+ " on host = " + xmppHost + ", port = " + xmppPort + " ...");

			connection.connect();

			if (connection.isConnected()) {
				log("Connection to XMPP server "
						+ "on " + xmppHost + ":" + xmppPort + " was successful.");
			}

			log("Attempting to authenticate on XMPP connection "
					+ "using username = " + xmppUser + ", password = " + xmppPassword);

			connection.login(xmppUser, xmppPassword);

			if (connection.isAuthenticated()) {
				log("Authentication using username = [" + xmppUser + "], "
						+ "password = [" + xmppPassword + "] successful.");
			}

			if (subscribe) {
				if (args.length != 6) {
					showUsage();
				}
				String node = args[5];
				log("Subscribing to XMPP node [" + node + "] over this authenticated connection ...");
				XmppSubscriber xmppSubscriber = new XmppSubscriber(connection);
				xmppSubscriber.subscribe(node);

				// register a shutdown hook
				Runtime.getRuntime().addShutdownHook(new Thread() {
					@Override
					public void run() {
						log("Instruction to ABORT program ...");

						// disconnect XMPP connection
						log("Disconnecting XMPP connection ...");
						connection.disconnect();
					}
				});

				while (true) {
					// do nothing, just be alive
				}
			}
		} catch (Exception e) {
			log("An exception occurred while connecting to XMPP server!");
			e.printStackTrace();
		}
	}
}
