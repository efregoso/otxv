<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
<meta content="text/html; charset=utf-8" http-equiv="Content-Type" />
<title>Port Checking Service</title>
<link href="style.css" rel="stylesheet" type="text/css">
</head>

<body>
<!-- A navigation bar and a central view that loads.-->
<div id="header">
<nav id="top-nav">
<a href="index.html" id="site-title">OTX-V</a>
<a href="iplookup.html">IP Lookup</a>
<a href="portchecker.html">Port Checker</a>
<a href="stylo.html">STYLO</a>
<a href="http://localhost:5601/app/kibana">Kibana</a>
<a href="glossary.html">Glossary</a>
</nav>
</div>

<div id="main-body">
<h1>Port Checker</h1>
<p>Enter a domain to port-check:</p>
<form method="post" action="portchecker.php">
<input type="text" name="domain">
<p>Enter a number of times to ping:</p>
<input type="text" name="count">
<input type="submit" value="submit">
</form>
</div>

    <?php
    set_time_limit(100);
    global $socket, $address, $port, $count, $checkarray;
    $method = 'portcheck';
    $domain = $_POST["domain"];
    $count = $_POST["count"];
    $bmethod = base64_encode($method);
    $bdomain = base64_encode($domain);
    $bcount = base64_encode($count);
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
    socket_write($socket, $bmethod, strlen($bmethod));
    sleep(2);
    socket_write($socket, $bdomain, strlen($bdomain));
    sleep(2);
    socket_write($socket, $bcount, strlen($bcount));
    sleep(2);
    global $buf, $boolean;
    $buf = socket_read($socket, 500);
    $checkresult = base64_decode($buf);
    $checkarray = preg_split('/ ... /', $checkresult);
    ?>
<table>
    <?php
    global $i;
    for ($i = 0; $i+1 < $count; $i++) {
    ?>
        <tr>
        <th><?php echo $checkarray[$i]; ?></th>
        <td><?php echo $checkarray[$i+1]; ?></td>
        </tr>
    <?php
    }
    socket_close($socket);
    ?>
</table>
</body>

</html>