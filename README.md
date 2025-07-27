# Python-Tor-Chat
Simple Python server-client script for chatting through tor network

How to run:

1) On server default port is 80 ref server.py

       port = 80 #you can change it as per your needs

2) To setup server, Download tor browser and configure your Tor Onion Service:

   edit torrc file

          HiddenServiceDir /var/lib/tor/my_website/
          HiddenServicePort 80 127.0.0.1:80

   for more information about tor onion service vist : https://community.torproject.org/onion-services/setup/

   After editing torrc file start tor browser and connect.

3) To set up client, change the server onion address in client.py

   look for line

          host = 'tpsyqgfdio25qxfakdksdyioq6u6bghipd3pcpboibwiowcvs3yv4gad.onion'  # Server's IP address

   and after changing, start the tor browser and connect.

4) After set up on both client and server side run: server.py on server and client.py on client and start chatting
5) Chat between server and client is encrypted. In server.py and client.py you can add new key.

   Look for line:

          fernet = Fernet('KHBYrz6d77qr2D8sb4wiPF09qOFhuQVP7vht28I-ZRk=')

   The same secret key should be used in both client.py and server.py.

6) additional requirement

          pip3 install PySocks

          pip3 install cryptography

          pip3 install threaded
