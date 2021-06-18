<!DOCTYPE html>
<html lang="en">
<head>
  <title>MMS</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
  <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
  <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
  <link rel="stylesheet" href="tabStyles.css">
  <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.25/css/jquery.dataTables.css">
  <script type="text/javascript" charset="utf8" src="https://cdn.datatables.net/1.10.25/js/jquery.dataTables.js"></script>
</head>
<body style ="background-color:#0c030f">
<div class="jumbotron text-center" style="background-color:#0f0b15">
  <h1 style = "color:white">algorithm's open trades</h1>
  <a href="https://github.com/tindll/mms"><img style="position: absolute;top: 7%;right: 5%;float: right" src="github.png" alt="back to github" width="70" height="70"></a>
</div>

<div class="tab" style= "margin-bottom: 1%;">
  <button class="tablinks" onclick="openPosition(event, 'open')" id="defaultOpen" style="color:white">Open positions</button>
  <button class="tablinks" onclick="openPosition(event, 'close')" style="color:white">Closed positions</button>
</div>

<div id="myModal" class="modal">
  <span class="close">&times;</span>
  <img class="modal-content" id="img01">
  <div id="caption"></div>
</div>

<div id="open" class="positionsTab" style ="margin-left: 2%;margin-right: 2%;"  >
  <table id="table_id" class="display" style="color:white">
    <thead style="color:white">
        <tr>
            <th>Trade ID</th>
            <th>Symbol</th>
            <th>Long/Short</th>
            <th>Open price</th>
            <th>Close price</th>
            <th>Leverage</th>
            <th>Date</th>
            <th>Trade reason</th>
        </tr>
    </thead>
    <style> tr{cursor: pointer;margin: 15px 0;}
    </style>
    <tbody style="color:black">
      <?php
        $json = file_get_contents('trades.json');
        $tradesList = json_decode($json, true);
        foreach($tradesList as $key => $arrays){
            foreach($arrays as $array){
              if(in_array("TBD",$array)){
                echo "<tr>";
                foreach($array as $key => $value){
                    echo "<td>". $value . "</td>";
                }
                echo "</tr>";
              }
            }
        }
      ?>
    </tbody>
  </table>
</div>

<div id="close" class="positionsTab" style ="margin-left: 2%;margin-right: 2%;" >
  <table id="table_id1" class="display" style="color:white">
    <thead style="color:white">
        <tr>
            <th>Trade ID</th>
            <th>Symbol</th>
            <th>Long/Short</th>
            <th>Open price</th>
            <th>Close price</th>
            <th>Leverage</th>
            <th>Date</th>
            <th>Trade reason</th>
        </tr>
    </thead>
    <tbody style="color:black">
    <?php
        $json = file_get_contents('trades.json');
        $tradesList = json_decode($json, true);
        foreach($tradesList as $key => $arrays){
            foreach($arrays as $array){
              if(in_array("TBD",$array)==FALSE){
                echo "<tr>";
                foreach($array as $key => $value){
                    echo "<td>". $value . "</td>";
                }
                echo "</tr>";
              }
            }
        }
      ?>
    </tbody>
  </table>
</div>

<script>
  var modal = document.getElementById("myModal");
  var modalImg = document.getElementById("img01");
  var captionText = document.getElementById("caption");
  $(document).ready( function () {
    $('#table_id').DataTable({"order": [[ 0, "desc" ]]});
    $('#table_id1').DataTable({"order": [[ 0, "desc" ]]});
    var table = $('#table_id').DataTable();
    $('#table_id tbody').on('click', 'tr', function () {
        var data = table.row( this ).data();
        modal.style.display = "block";
        modalImg.src = '/charts/chart'+data[0]+'.png';
        captionText.innerHTML = "chart - id:"+data[0]+"<br> (click anywhere to get rid of this chart)"
        let dataID = parseInt(data[0]);
        let tmp  = parseInt(dataID);
        let count = 0;
        modalImg.onerror = function(){
          captionText.innerHTML = "chart - id:"+data[0]+" is unavailable <br> (only 15 most recent charts are stored on the database)<br> (click anywhere to get rid of this message)"
          modalImg.src = '';
        };
        //image.src = 'non-existing.jpg';
        //alert( 'You clicked on '+data[0]+'\'s row' );
    } );
  } );
  function openPosition(event, positionType) {
    var i, positionsTab, tablinks;
    positionsTab = document.getElementsByClassName("positionsTab");

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
  var span = document.getElementsByClassName("close")[0];
  span.onclick = function() { 
    modal.style.display = "none";
  }
  var modal = document.getElementById('myModal');
  modal.addEventListener('click',function(){
  this.style.display="none";
  })
  
  document.getElementById("defaultOpen").click();
  </script>





<footer style ="position: fixed;left: 0;bottom: 0; width: 100%;" class="bg-light text-center text-lg-start">
<div class="text-center p-3" id="footer" style="background-color: rgba(0, 0, 0, 0.2);">
some trades may seem conflicting, but it's most likely because they're on different time frames <br>
click on a position to see the chart, charts are only available on more recent trades because hosting is expensive (in terms of disk space) <br>
</div>
</footer>
</body>
</html>
