<?php

$remoteHost = '192.168.45.14';
$remoteUsername = 'root';
$remotePassword = 'RiskAster@DataCenter2012.SBT.japan';
$confFile = '/etc/asterisk/sip.d/sipallowip.conf';
$iptablesCommand = 'iptables -I SBT-ASTERISK-RULES 5 -s <ip_address> -j ACCEPT';
$sipReloadCommand = '/usr/sbin/asterisk -rx "sip reload"';

// Database configuration
$servername = "localhost";
$username = "python";
$password = "sbtph@2018";
$dbname = "utils";

// Establish database connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check if the connection was successful
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
else {
   echo "Connected";
}



if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $ipAddress = $_POST['ip_address'];

    // Check if the IP address already exists in the database
    $stmt = $conn->prepare("SELECT ip_address FROM ip_addresses WHERE ip_address = ?");
    $stmt->bind_param("s", $ipAddress);
    $stmt->execute();
    $stmt->store_result();

    if ($stmt->num_rows === 0) {
        // IP address does not exist in the database, insert it
        $stmt = $conn->prepare("INSERT INTO ip_addresses (ip_address) VALUES (?)");
        $stmt->bind_param("s", $ipAddress);
        $stmt->execute();

        echo "Entered IP Address: " . $ipAddress;

          // Append the new IP address to sipallowip.conf file on the remote machine
          $appendCommand = 'echo "permit=' . $ipAddress . '" >> ' . $confFile;
          $sshConn = ssh2_connect($remoteHost);
          if (ssh2_auth_password($sshConn, $remoteUsername, $remotePassword)) {
             echo "SSH Connected";
              ssh2_exec($sshConn, $appendCommand);
  
              // Execute iptables command remotely
              ssh2_exec($sshConn, $iptablesCommand);
  
              // Execute Asterisk SIP reload command remotely
              ssh2_exec($sshConn, $sipReloadCommand);
  
              echo "IP address added to sipallowip.conf and iptables command executed successfully.";
          } else {
              echo "SSH authentication failed.";
          }

    } else {
        echo "IP Address already exists: " . $ipAddress;
    }

    // Close the statement
    $stmt->close();
}

// Close the database connection
$conn->close();
?>


<!DOCTYPE html>
<html>
<head>
    <title>IP Address Input</title>
    <style>
        body {
            font-family: Arial, sans-serif;
        }

        form {
            margin: 20px;
        }

        label {
            font-weight: bold;
        }

        input[type="text"] {
            padding: 10px;
            width: 300px;
        }

        button {
            padding: 10px 20px;
            background-color: #4CAF50;
            color: white;
            border: none;
            cursor: pointer;
        }

        button:hover {
            background-color: #45a049;
        }

        .message {
            margin: 20px;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <form method="POST" action="">
        <label for="ip_address">IP Address:</label>
        <input type="text" name="ip_address" id="ip_address" required>
        <button type="submit">Submit</button>
    </
