<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
<meta content="text/html; charset=utf-8" http-equiv="Content-Type" />
<title>IP Lookup Service</title>
<link href="style.css" rel="stylesheet" type="text/css">
</head>

<body>
<div id="header">
<nav id="top-nav">
<a href="index.html" id="site-title">OTX-V</a>
<a href="maltime.html">Malware Timeline</a>
<a href="iplookup.html">IP Lookup</a>
<a href="portchecker.html">Port Checker</a>
<a href="stylo.html">STYLO</a>
<a href="http://localhost:5601/app/kibana">Kibana</a>
<a href="glossary.html">Glossary</a>
</nav>
</div>

<div id="main-body">
<p>Enter an IPv4 or IPv6 address to look up:</p>
<form action="ip.php" method="post">
<input type="text" name="ip">
<input type="submit" value="submit" >
</form>
</div>
    <?php
    set_time_limit(100);
    global $ip, $socket, $bytes, $address, $port, $ipinfo, $array, $bip;
    $ip = $_POST["ip"];
    $bip = base64_encode($ip);
    $method = 'iplookup';
    $bmethod = base64_encode($method);
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
    socket_write($socket, $bip, strlen($bip));
    sleep(2);
    global $buf, $boolean;
    $buf = socket_read($socket, 1024);
    $ipinfo = array(base64_decode($buf));
    ?>
<table style="border:solid 10px black;margin=7px;">
<tr>
<th>IP Address</th>
<th>Associated Address</th>
<th>Latitude</th>
<th>Longitude</th>
</tr>
<tr>
<td><?php echo $ip ?></td>
<td><?php /*add this here*/ ?></td>
<td><?php /*DEBUG: FIGURE OUT HOW TO RETURN THESE!*/ echo $ipinfo['lat'] ?></td>
<td><?php /*DEBUG: FIGURE OUT HOW TO RETURN THESE!*/ echo $ipinfo['lng'] ?></td>
</tr>
</table>
    <?php
    socket_close($socket);
    ?>
</body>

</html>