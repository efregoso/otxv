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
<a href="iplookup.html">IP Lookup</a>
<a href="portchecker.html">Port Checker</a>
<a href="stylo.html">STYLO</a>
<a href="http://localhost:5601/app/kibana">Kibana</a>
<a href="glossary.html">Glossary</a>
</nav>
</div>

<div id="main-body">
<h1>IP Address DNS Lookup</h1>
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
    global $buf, $boolean, $ipinfo, $iparray;
    $buf = socket_read($socket, 1024);
    $ipinfo = (string)base64_decode($buf);
    $iparray = preg_split('/~/', $ipinfo);
    ?>
<table id="ip-info">
<tr>
<th>IP Address</th>
<td><?php echo $ip ?></td>
</tr>
<tr>
<th>ASN Description</th>
<td><?php echo $iparray[0] ?></td>
</tr>
<tr>
<th>IP Version</th>
<td><?php echo $iparray[1] ?></td>
</tr>
<tr>
<th>Owner Name</th>
<td><?php echo $iparray[2] ?></td>
</tr>
<tr>
<th>Owner Location</th>
<td><?php echo $iparray[3] ?></td>
</tr>
<tr>
<th>Contact Name</th>
<td><?php echo $iparray[4] ?></td>
</tr>
<tr>
<th>Contact Location</th>
<td><?php echo $iparray[5] ?></td>
</tr>
<tr>
<th>Contact Email</th>
<td><?php echo $iparray[6] ?></td>
</tr>
<tr>
<th>Contact Phone</th>
<td><?php echo $iparray[7] ?></td>
</tr>
</table>
    <?php
    socket_close($socket);
    ?>
</body>

</html>