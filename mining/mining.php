<?php
$command="python3 mining.py";
exec($command,$outputs);

$text = "
<thead>
  <tr>
    <th>順位</th>
    <th>単語</th>
    <th>出現回数</th>
  </tr>
</thead>
<tbody>
";

foreach($outputs as $output){
    $text .= $output;
}

$text .= "</tbody>";



  $list = array("text" => $text);
  header("Content-type: application/json; charset=UTF-8");
  echo json_encode($list,JSON_UNESCAPED_UNICODE);
  exit;

?> 