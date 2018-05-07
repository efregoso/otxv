<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
<meta content="text/html; charset=utf-8" http-equiv="Content-Type" />
<title>Stylometric Results</title>
</head>

<body>
    <?php
    set_time_limit(100);
    global $key, $socket, $bytes, $address, $port;
    $ip = $_POST["ip"];
    $bytes = base64_encode($ip);
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
    global $buf, $boolean;
    socket_recv($socket, $buf, 100, MSG_WAITALL);
    $checkresult = base64_decode($buf);
    ?>
<p><?php echo $checkresult; ?></p>
    <?php
    socket_close($socket);
    ?>
</body>

</html>