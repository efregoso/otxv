<html>
<body>
    <?php
    $key = $_GET["apikey"];
    $address = '172.20.2.205';
    $port = 10001;
    $socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP)
    if ($socket === false){
        echo "socket_create() failed: reason: " . socket_strerror(socket_last_error()) . "\n";
    }
    $result = socket_connect($socket, $address, $port);
    if ($result === false) {
        echo "socket_connect() failed.\nReason: ($result) " . socket_strerror(socket_last_error($socket)) . "\n";
    };
    socket_write($socket, $key, strlen($key));
    socket_close($socket);
    ?>

Sending <?php $key2 = $_GET["apikey"];echo $key2; ?> to server.
</body>
</html>