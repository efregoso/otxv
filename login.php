<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
<meta content="text/html; charset=utf-8" http-equiv="Content-Type" />
<title>Login to OTX-V</title>
</head>

<body>
    <?php
    set_time_limit(100);
    global $key, $socket, $bytes, $address, $port;
    $key = $_POST["apikey"];
    $bytes = base64_encode($key);
    $address = 'localhost';
    $port = 10000;
    $socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
    if ($socket === false){
        echo "socket_create() failed: reason: " . socket_strerror(socket_last_error()) . "\n";
    }
    $result = socket_connect($socket, $address, $port);
    if ($result === false) {
        echo "socket_connect() failed.\nReason: ($result) " . socket_strerror(socket_last_error($socket)) . "\n";
    };
    socket_write($socket, $bytes, strlen($bytes));
    ?>
Sending key to server...
    <?php
    global $buf, $boolean;
    socket_recv($socket, $buf, 8, MSG_WAITALL);
    $boolean = base64_decode($buf);
    if ($boolean == "True") {
        header("Location: http://localhost:5601/app/kibana");
        exit;
    }
    else {
        header("Location: http://localhost:8000/loginerror.html");
        exit;
    }
    socket_close($socket);
    ?>
</body>

</html>