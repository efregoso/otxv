<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
<meta content="text/html; charset=utf-8" http-equiv="Content-Type" />
<title>Stylometric Results</title>
<link href="style.css" rel="stylesheet" type="text/css">
</head>

<body>
<div id="header">
<nav style="vertical-align:middle" id="top-nav">
<a href="index.html" id="site-title">OTX-V</a>
<a href="iplookup.html">IP Lookup</a>
<a href="portchecker.html">Port Checker</a>
<a href="stylo.html">STYLO</a>
<a href="http://localhost:5601/app/kibana">Kibana</a>
<a href="glossary.html">Glossary</a>
</nav>
</div>

<div id="main-body">
<h1>STYLO: Stylometric Text Analysis Tool</h1>
<p>Enter a control text block:</p>
<textarea rows="10" style="width:100%" form="styloform" name="ctrl"></textarea>
<p>Enter up to three comparison text blocks:</p>
<textarea rows="10" style="width:100%" form="styloform" name="comp1"></textarea>
<br/>
<textarea rows="10" style="width:100%" form="styloform" name="comp2"></textarea>
<br/>
<textarea rows="10" style="width:100%" form="styloform" name="comp3"></textarea>
<br/>
<p>Type of analysis to perform?</p>
<form id="styloform" method="post" action="stylo.php">
<input type="radio" value="stylokey" name="analysis">Keyword<br/>
<input type="radio" value="stylounigram" name="analysis">Unigram<br/>
<input type="radio" value="stylobigram" name="analysis">Bigram<br/>
<input type="submit" value="Submit">
</form>
</div>
    <?php
    set_time_limit(100);
    global $ctrl, $comp1, $comp2, $comp3, $socket, $bytes, $address, $port, $method;
    $ctrl = $_POST["ctrl"];
    $comp1 = $_POST["comp1"];
    $comp2 = $_POST["comp2"];
    $comp3 = $_POST["comp3"];
    $method = $_POST["analysis"];
    $bctrl = base64_encode($ctrl);
    $bcomp1 = base64_encode($comp1);
    $bcomp2 = base64_encode($comp2);
    $bcomp3 = base64_encode($comp3);
    $bmethod = base64_encode($method);
    $null = "---";
    $bnull = base64_encode($null);
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
    if ($ctrl != "") {
        socket_write($socket, $bctrl, strlen($bctrl));
    }
    else {
        socket_write($socket, $bnull, strlen($bnull));
    }
    sleep(2);
    if ($comp1 != "") {
        socket_write($socket, $bcomp1, strlen($bcomp1));
    }
    else {
        socket_write($socket, $bnull, strlen($bnull));
    }
    sleep(2);
    if ($comp2 != "") {
        socket_write($socket, $bcomp2, strlen($bcomp2));
    }
    else {
        socket_write($socket, $bnull, strlen($bnull));
    }
    sleep(2);
    if ($comp3 != "") {
        socket_write($socket, $bcomp3, strlen($bcomp3));
    }
    else {
        socket_write($socket, $bnull, strlen($bnull));
    }
    sleep(2);
    global $buf, $boolean;
    $buf = socket_read($socket, 2000);
    $checkresult = base64_decode($buf);
    $resultarray = preg_split('/~/', $checkresult);
    ?>
<table id="stylo-info">
<tr>
<th>Control Hash Table</th>
<td><?php echo $resultarray[0] ?></td>
</tr>
<tr>
<th>Comparison Sample 1 Hash Table</th>
<td><?php echo $resultarray[1] ?></td>
</tr>
<tr>
<th>Comparison Sample 2 Hash Table</th>
<td><?php echo $resultarray[2] ?></td>
</tr>
<tr>
<th>Comparison Sample 3 Hash Table</th>
<td><?php echo $resultarray[3] ?></td>
</tr>
<tr>
<th>Sample 1 Similarity Score</th>
<td><?php echo $resultarray[4] ?></td>
</tr>
<tr>
<th>Sample 2 Similarity Score</th>
<td><?php echo $resultarray[5] ?></td>
</tr>
<tr>
<th>Sample 3 Similarity Score</th>
<td><?php echo $resultarray[6] ?></td>
</tr>
</table>
    <?php
    socket_close($socket);
    ?>
</body>

</html>