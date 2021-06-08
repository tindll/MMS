<!DOCTYPE html>
<html lang="en">
<head>
  <title>MMS</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
  <link rel="stylesheet" href="tabStyles.css">
</head>
<body style ="background-color:#0c030f">
<div class="jumbotron text-center" style="background-color:#0f0b15">
  <h1 style = "color:white">algorithm's open trades</h1>
  <a href="https://github.com/tindll/mms"><img style="position: absolute;top: 7%;right: 5%;float: right" src="github.png" alt="back to github" width="70" height="70"></a>
</div>

<div class="tab">
  <button class="tablinks" onclick="openPosition(event, 'open')" id="defaultOpen" style="color:white">Open positions</button>
  <button class="tablinks" onclick="openPosition(event, 'close')" style="color:white">Closed positions</button>
</div>

<div id="open" class="positionsTab" style="color:white">

</div>

<div id="close" class="positionsTab" style="color:white">

</div>

<script>
  document.getElementById("defaultOpen").click();
  function openPosition(event, positionType) {
    var i, positionsTab, tablinks;
    positionsTab = document.getElementsByClassName("positionsTab");

    //if(positionType=='open'){
    //  document.getElementById('footer').innerHTML = "Above is a list of all open positions taken by the algorithm."
    //} 
    //else if(positionType =='close'){document.getElementById('footer').innerHTML = "Above is a list of all closed positions that the algorithm has taken recently."
    //}
    for (i = 0; i < positionsTab.length; i++) {
      positionsTab[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(positionType).style.display = "block";
    event.currentTarget.className += " active";
  }
  </script>

<?php
        $json = file_get_contents('trades.json');
        $tradesList = json_decode($json, true);
        foreach($tradesList as $key => $arrays){
            echo $key . "<br />";
            foreach($arrays as $array){
                foreach($array as $key => $value){
                    echo $key . " => " . $value . "<br />";
                }
                echo "<br />";
            }
            echo "<br />";
        }
?>






<footer style ="position: fixed;left: 0;bottom: 0; width: 100%;" class="bg-light text-center text-lg-start">
<div class="text-center p-3" id="footer" style="background-color: rgba(0, 0, 0, 0.2);">
this page is just placeholder for now, everything is subject to change to make it look a lot nicer
</div>
</footer>
</body>
</html>
